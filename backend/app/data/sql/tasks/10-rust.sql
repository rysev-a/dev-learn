-- Упражнения книги 10 «rust — Изучаем Rust». Файл строит export_tasks.py — руками не правьте.

INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-hello', 0, 'rust', 'Привет, мир!', 'Напишите программу, которая печатает одну строку: Привет, мир!

Ожидаемый вывод:
Привет, мир!', 'fn main() {
    // ваш код
}
', 'Внутри fn main() вызовите println!("…"); не забудьте точку с запятой в конце.', '{"driver": "", "expected": ["Привет, мир!"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-two-lines', 1, 'rust', 'Две строки', 'Напечатайте две строки: сначала «Меня зовут Rust», затем «Мне уже больше десяти лет».

Ожидаемый вывод:
Меня зовут Rust
Мне уже больше десяти лет', 'fn main() {
    // ваш код
}
', 'Каждый вызов println! печатает строку и переводит её. Два вызова — две строки.', '{"driver": "", "expected": ["Меня зовут Rust", "Мне уже больше десяти лет"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-print-one-line', 2, 'rust', 'print! без перевода строки', 'С помощью трёх вызовов print! (а не println!) напечатайте на одной строке: Раз, два, три! — и затем один вызов println!(), который только переведёт строку.

Ожидаемый вывод:
Раз, два, три!', 'fn main() {
    // ваш код
}
', 'print!("…") не добавляет перевод строки; пустой println!() переводит строку.', '{"driver": "", "expected": ["Раз, два, три!"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-placeholders', 3, 'rust', 'Подстановка значений', 'Напечатайте равенство 2 + 3 = 5, передав числа 2, 3 и 5 как аргументы println! (в строке используйте три пары {}).

Ожидаемый вывод:
2 + 3 = 5', 'fn main() {
    // ваш код
}
', 'println!("{} + {} = {}", 2, 3, 5); — значения подставляются слева направо.', '{"driver": "", "expected": ["2 + 3 = 5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-expression-arg', 4, 'rust', 'Выражение прямо в аргументе', 'Напечатайте строку «Сумма: 12», но число 12 пусть вычисляет программа: передайте в println! выражение 5 + 7.

Ожидаемый вывод:
Сумма: 12', 'fn main() {
    // ваш код
}
', 'Аргументом println! может быть любое выражение: println!("Сумма: {}", 5 + 7);', '{"driver": "", "expected": ["Сумма: 12"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-named-args', 5, 'rust', 'Имена внутри скобок', 'Объявите две переменные: let name = "Аня"; let age = 30; и напечатайте «Аня, 30 лет», подставив их прямо в строку: {name} и {age} (без аргументов после строки).

Ожидаемый вывод:
Аня, 30 лет', 'fn main() {
    // ваш код
}
', 'Если в скобках написать имя переменной, println! возьмёт её значение: {name}.', '{"driver": "", "expected": ["Аня, 30 лет"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-escape-braces', 6, 'rust', 'Настоящие фигурные скобки', 'Напечатайте строку {ok} вместе со скобками, а на следующей строке — {} (пустые скобки).

Ожидаемый вывод:
{ok}
{}', 'fn main() {
    // ваш код
}
', 'Чтобы напечатать одну фигурную скобку, пишут две подряд: {{ и }}.', '{"driver": "", "expected": ["{ok}", "{}"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-quotes', 7, 'rust', 'Кавычки и обратная косая черта', 'Напечатайте две строки. Первая: Он сказал: "привет" (с двойными кавычками внутри). Вторая: C:\temp\new (с обратными косыми чертами).

Ожидаемый вывод:
Он сказал: "привет"
C:\temp\new', 'fn main() {
    // ваш код
}
', 'Внутри строки кавычка пишется как \", а обратная косая черта — как \\.', '{"driver": "", "expected": ["Он сказал: \"привет\"", "C:\\temp\\new"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-tabs', 8, 'rust', 'Табуляция', 'Напечатайте таблицу из двух строк, где колонки разделены символом табуляции \t: «Имя<tab>Возраст» и «Аня<tab>30».

Ожидаемый вывод:
Имя	Возраст
Аня	30', 'fn main() {
    // ваш код
}
', '\t внутри строки — один символ табуляции.', '{"driver": "", "expected": ["Имя\tВозраст", "Аня\t30"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-card', 9, 'rust', 'Визитка', 'Напечатайте визитку из четырёх строк (вывод показан ниже; обратите внимание на рамку из символов + - |).

Ожидаемый вывод:
+----------------+
| Аня Петрова    |
| Rust-новичок   |
+----------------+', 'fn main() {
    // ваш код
}
', 'Каждая строка визитки — отдельный println!; пробелы внутри кавычек важны.', '{"driver": "", "expected": ["+----------------+", "| Аня Петрова    |", "| Rust-новичок   |", "+----------------+"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-cat', 10, 'rust', 'Кот из символов', 'Нарисуйте кота четырьмя строками (точный вид — в ожидаемом выводе ниже).

Ожидаемый вывод:
 /\_/\
( o.o )
 > ^ <
мяу!', 'fn main() {
    // ваш код
}
', 'Косая черта «\» в строке пишется как \\ — иначе она начинает управляющую последовательность.', '{"driver": "", "expected": [" /\\_/\\", "( o.o )", " > ^ <", "мяу!"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-receipt', 11, 'rust', 'Чек с вычислениями', 'Напечатайте чек: «Хлеб: 40», «Молоко: 95», «Сыр: 310» и итоговую строку «Итого: 445». Итог не вводите вручную — вычислите его выражением 40 + 95 + 310 прямо в println!.

Ожидаемый вывод:
Хлеб: 40
Молоко: 95
Сыр: 310
Итого: 445', 'fn main() {
    // ваш код
}
', 'println!("Итого: {}", 40 + 95 + 310);', '{"driver": "", "expected": ["Хлеб: 40", "Молоко: 95", "Сыр: 310", "Итого: 445"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-mult-table', 12, 'rust', 'Таблица умножения 3×3', 'Напечатайте таблицу умножения 3×3: три строки, в каждой три числа через пробел (произведения i·j). Вычисляйте произведения в аргументах println!, а не вписывайте готовые числа.

Ожидаемый вывод:
1 2 3
2 4 6
3 6 9', 'fn main() {
    // ваш код
}
', 'println!("{} {} {}", 1 * 1, 1 * 2, 1 * 3); — и так три строки.', '{"driver": "", "expected": ["1 2 3", "2 4 6", "3 6 9"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-number-bases', 13, 'rust', 'Системы счисления', 'Напечатайте число 42 четырьмя способами в одной строке через пробел: десятичное ({}), двоичное ({:b}), шестнадцатеричное ({:x}) и восьмеричное ({:o}).

Ожидаемый вывод:
42 101010 2a 52', 'fn main() {
    // ваш код
}
', 'После двоеточия в скобках указывается формат: b — двоичный, x — шестнадцатеричный, o — восьмеричный.', '{"driver": "", "expected": ["42 101010 2a 52"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-width', 14, 'rust', 'Выравнивание по ширине', 'Напечатайте число 42 тремя способами, каждый в квадратных скобках на своей строке: по правому краю в пяти позициях [   42], по левому краю [42   ] и с нулями [00042]. Используйте {:>5}, {:<5} и {:05}.

Ожидаемый вывод:
[   42]
[42   ]
[00042]', 'fn main() {
    // ваш код
}
', '>5 — по правому краю, <5 — по левому, 05 — дополнить нулями до пяти позиций.', '{"driver": "", "expected": ["[   42]", "[42   ]", "[00042]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-precision', 15, 'rust', 'Сколько знаков после запятой', 'Напечатайте число 3.14159 с двумя знаками после запятой (3.14), а число 2.0 / 3.0 — с тремя (0.667), каждое на своей строке. Формат: {:.2} и {:.3}.

Ожидаемый вывод:
3.14
0.667', 'fn main() {
    // ваш код
}
', '{:.2} — два знака после запятой; округление выполняется автоматически.', '{"driver": "", "expected": ["3.14", "0.667"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-debug', 16, 'rust', 'Отладочный вывод {:?}', 'Напечатайте в одной строке через пробел с помощью {:?}: строку "текст", число 5, символ ''a'' и кортеж (1, 2.5, true). Формат {:?} показывает значения так, как они выглядят в коде (со строкой в кавычках).

Ожидаемый вывод:
"текст" 5 ''a'' (1, 2.5, true)', 'fn main() {
    // ваш код
}
', '{:?} работает почти для любых значений — удобно при отладке.', '{"driver": "", "expected": ["\"текст\" 5 ''a'' (1, 2.5, true)"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-raw-string', 17, 'rust', 'Сырая строка', 'Напечатайте путь C:\Users\anna\docs одной сырой строкой r"…" (в такой строке обратные косые черты не нужно удваивать).

Ожидаемый вывод:
C:\Users\anna\docs', 'fn main() {
    // ваш код
}
', 'r"…" — сырая строка: внутри нет управляющих последовательностей. Её можно передать как аргумент {}.', '{"driver": "", "expected": ["C:\\Users\\anna\\docs"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-unicode', 18, 'rust', 'Русский и Unicode', 'Напечатайте две строки: «Раст любит Unicode» и «Краб 🦀 говорит привет».

Ожидаемый вывод:
Раст любит Unicode
Краб 🦀 говорит привет', 'fn main() {
    // ваш код
}
', 'Строки в расте — UTF-8, поэтому русские буквы и эмодзи можно писать прямо в кавычках.', '{"driver": "", "expected": ["Раст любит Unicode", "Краб 🦀 говорит привет"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-multiline-literal', 19, 'rust', 'Строка из нескольких строк', 'Одним вызовом println! напечатайте три строки: «Первая», «Вторая», «Третья». Для этого вставьте в строку два символа перевода строки \n (или напишите строку прямо на нескольких строках кода).

Ожидаемый вывод:
Первая
Вторая
Третья', 'fn main() {
    // ваш код
}
', '\n внутри строки — перевод строки; println! добавит ещё один в самом конце.', '{"driver": "", "expected": ["Первая", "Вторая", "Третья"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-arith-ops', 20, 'rust', 'Пять арифметических действий', 'Напечатайте пять строк с действиями над целыми 7 и 3: «7 + 3 = 10», «7 - 3 = 4», «7 * 3 = 21», «7 / 3 = 2» (целочисленное деление) и «7 % 3 = 1» (остаток). Результаты вычисляйте в программе.

Ожидаемый вывод:
7 + 3 = 10
7 - 3 = 4
7 * 3 = 21
7 / 3 = 2
7 % 3 = 1', 'fn main() {
    // ваш код
}
', 'Целые числа делятся нацело: 7 / 3 даёт 2, а остаток — 7 % 3.', '{"driver": "", "expected": ["7 + 3 = 10", "7 - 3 = 4", "7 * 3 = 21", "7 / 3 = 2", "7 % 3 = 1"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-float-ops', 21, 'rust', 'Дробные числа', 'Напечатайте три строки: 7.0 / 3.0 с тремя знаками после запятой, 2.5 * 4.0 с одним и 10.0 - 0.1 с двумя знаками (только результаты, по одному числу на строку).

Ожидаемый вывод:
2.333
10.0
9.90', 'fn main() {
    // ваш код
}
', 'Дробные литералы пишутся с точкой: 7.0, а не 7.', '{"driver": "", "expected": ["2.333", "10.0", "9.90"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-seconds', 22, 'rust', 'Секунд в сутках', 'Напечатайте строку «В сутках 86400 секунд», вычислив число выражением 24 * 60 * 60 внутри println!.

Ожидаемый вывод:
В сутках 86400 секунд', 'fn main() {
    // ваш код
}
', 'println!("В сутках {} секунд", 24 * 60 * 60);', '{"driver": "", "expected": ["В сутках 86400 секунд"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-circle', 23, 'rust', 'Площадь круга', 'Площадь круга радиуса 5 равна 3.14159 · 5 · 5. Напечатайте «Площадь: 78.54» (два знака после запятой), вычислив число в программе.

Ожидаемый вывод:
Площадь: 78.54', 'fn main() {
    // ваш код
}
', 'Дробные числа в выражении — через точку: 3.14159 * 5.0 * 5.0; формат {:.2}.', '{"driver": "", "expected": ["Площадь: 78.54"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-celsius', 24, 'rust', 'Градусы Цельсия и Фаренгейта', 'Напечатайте «100°C = 212°F», вычислив 212 по формуле 100.0 * 9.0 / 5.0 + 32.0 (выведите число без знаков после запятой: формат {:.0}).

Ожидаемый вывод:
100°C = 212°F', 'fn main() {
    // ваш код
}
', '{:.0} округляет до целого; не забудьте, что дробные литералы пишутся с точкой.', '{"driver": "", "expected": ["100°C = 212°F"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-booleans', 25, 'rust', 'Истина и ложь', 'Напечатайте в одной строке через пробел результаты сравнений 5 > 3, 2 + 2 == 5 и 4 <= 4 (получится: true false true).

Ожидаемый вывод:
true false true', 'fn main() {
    // ваш код
}
', 'Сравнение — это выражение типа bool; println! печатает его как true или false.', '{"driver": "", "expected": ["true false true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-char-number', 26, 'rust', 'Символ и его номер', 'Напечатайте символ ''R'' и его числовой код в Unicode через as: «R 82». Для этого выражение ''R'' as u32.

Ожидаемый вывод:
R 82', 'fn main() {
    // ваш код
}
', 'as u32 превращает символ char в число — его код.', '{"driver": "", "expected": ["R 82"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-progress-bar', 27, 'rust', 'Полоса прогресса', 'Напечатайте полосу прогресса из десяти символов: пять решёток и пять дефисов в квадратных скобках, затем пробел и 50%.

Ожидаемый вывод:
[#####-----] 50%', 'fn main() {
    // ваш код
}
', 'Знак процента в println! печатается как есть: символа % в формате не требуется экранировать.', '{"driver": "", "expected": ["[#####-----] 50%"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-schedule', 28, 'rust', 'Расписание дня', 'Напечатайте расписание из пяти строк в формате «время<tab>занятие»: 08:00 зарядка, 09:00 работа, 13:00 обед, 18:00 прогулка, 22:00 сон.

Ожидаемый вывод:
08:00	зарядка
09:00	работа
13:00	обед
18:00	прогулка
22:00	сон', 'fn main() {
    // ваш код
}
', 'Время и занятие разделяйте символом \t.', '{"driver": "", "expected": ["08:00\tзарядка", "09:00\tработа", "13:00\tобед", "18:00\tпрогулка", "22:00\tсон"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 1, 'r1-comments', 29, 'rust', 'Комментарии не печатаются', 'Программа должна напечатать ровно две строки: «Видно» и «Тоже видно». Между двумя println! добавьте два комментария: строчный (// …) с любым текстом и блочный (/* … */), внутри которого лежит фрагмент println!("не должно быть видно"); — он не должен выполняться.

Ожидаемый вывод:
Видно
Тоже видно', 'fn main() {
    // ваш код
}
', 'Всё внутри // до конца строки и внутри /* … */ — комментарий, компилятор его пропускает.', '{"driver": "", "expected": ["Видно", "Тоже видно"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-first-variable', 0, 'rust', 'Первая переменная', 'Объявите две переменные: name со значением "Аня" и age со значением 30. Напечатайте их через пробел: «Аня 30».

Ожидаемый вывод:
Аня 30', 'fn main() {
    // ваш код
}
', 'let name = "Аня"; let age = 30; затем println!("{} {}", name, age);', '{"driver": "", "expected": ["Аня 30"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-sum-diff', 1, 'rust', 'Сумма и разность', 'Объявите a = 17 и b = 5. Напечатайте две строки: «Сумма: …» и «Разность: …», подставив значения вычислений.

Ожидаемый вывод:
Сумма: 22
Разность: 12', 'fn main() {
    // ваш код
}
', 'Выражения a + b и a - b можно подставить прямо в println!.', '{"driver": "", "expected": ["Сумма: 22", "Разность: 12"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-mut-counter', 2, 'rust', 'Счётчик с mut', 'Объявите изменяемый счётчик count = 0. Трижды увеличьте его на 1 (count = count + 1), и после каждого шага печатайте его значение: 1, 2, 3 — по одному на строке.

Ожидаемый вывод:
1
2
3', 'fn main() {
    // ваш код
}
', 'let mut count = 0; затем три раза: count = count + 1; и println!.', '{"driver": "", "expected": ["1", "2", "3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-compound-ops', 3, 'rust', 'Составные присваивания', 'Начните с n = 10 (mut). Последовательно выполните n += 5, n -= 3, n *= 2, n /= 4, n %= 4 и после каждой операции печатайте n: пять строк.

Ожидаемый вывод:
15
12
24
6
2', 'fn main() {
    // ваш код
}
', 'После каждой операции — println!("{}", n); результаты: 15, 12, 24, 6, 2.', '{"driver": "", "expected": ["15", "12", "24", "6", "2"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-fix-immutable', 4, 'rust', 'Исправьте: нельзя присвоить дважды', 'Программа не собирается: переменная неизменяема, а ей присваивают второй раз. Исправьте объявление так, чтобы программа напечатала 5 и затем 10.

Ожидаемый вывод:
5
10', 'fn main() {
    let x = 5;
    println!("{}", x);
    x = 10;
    println!("{}", x);
}
', 'Добавьте слово mut: let mut x = 5;', '{"driver": "", "expected": ["5", "10"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-fix-total', 5, 'rust', 'Исправьте: накопитель без mut', 'Программа должна напечатать итог 12, но total объявлен неизменяемым. Исправьте.

Ожидаемый вывод:
12', 'fn main() {
    let total = 0;
    total += 5;
    total += 7;
    println!("{}", total);
}
', 'Накопитель всегда изменяемый: let mut total = 0;', '{"driver": "", "expected": ["12"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-shadow-steps', 6, 'rust', 'Затенение по шагам', 'Объявите x = 5, затем затените: x = x + 1, затем x = x * 2. После каждого объявления печатайте x: 5, 6, 12.

Ожидаемый вывод:
5
6
12', 'fn main() {
    // ваш код
}
', 'Каждый раз пишите новое let x = …; это не изменение, а новая переменная.', '{"driver": "", "expected": ["5", "6", "12"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-shadow-type', 7, 'rust', 'Затенение с новым типом', 'Объявите data = "12345" (строка). Затените её длиной строки data.len(). Напечатайте «Длина: 5».

Ожидаемый вывод:
Длина: 5', 'fn main() {
    // ваш код
}
', 'let data = data.len(); — переменная теперь число, а не строка.', '{"driver": "", "expected": ["Длина: 5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-fix-type-change', 8, 'rust', 'Исправьте: нельзя сменить тип через mut', 'Программа хочет превратить строку в её длину под тем же именем, но через присваивание это невозможно (mismatched types). Исправьте затенением. Результат: «Длина: 6».

Ожидаемый вывод:
Длина: 6', 'fn main() {
    let mut s = "привет";
    s = s.len();
    println!("Длина: {}", s);
}
', 'Вместо s = … напишите новое let s = …; обратите внимание: s.len() — длина в байтах (12), а нужно число символов: s.chars().count().', '{"driver": "", "expected": ["Длина: 6"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-const-seconds', 9, 'rust', 'Константы времени', 'Объявите константы SECONDS_PER_MINUTE: u32 = 60 и MINUTES_PER_HOUR: u32 = 60. Вычислите и напечатайте, сколько секунд в 3 часах: «10800».

Ожидаемый вывод:
10800', 'fn main() {
    // ваш код
}
', 'Константы объявляют вне fn main — над ней; тип обязателен: const NAME: u32 = 60;', '{"driver": "", "expected": ["10800"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-const-pi', 10, 'rust', 'Длина окружности', 'Объявите константу PI: f64 = 3.14159. Радиус r = 10.0. Напечатайте длину окружности 2·PI·r с двумя знаками: «62.83».

Ожидаемый вывод:
62.83', 'fn main() {
    // ваш код
}
', 'println!("{:.2}", 2.0 * PI * r);', '{"driver": "", "expected": ["62.83"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-scope-blocks', 11, 'rust', 'Блоки и затенение', 'Объявите x = 1. Во вложенном блоке { … } затените x значением 100 и напечатайте его (100). После блока снова напечатайте x (1).

Ожидаемый вывод:
100
1', 'fn main() {
    // ваш код
}
', 'Внутренний x живёт до закрывающей скобки блока; после блока видна старая переменная.', '{"driver": "", "expected": ["100", "1"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-block-expression', 12, 'rust', 'Блок как выражение', 'Блок { … } тоже выражение: значением становится его последняя строка без точки с запятой. Объявите y = { let x = 3; x * x + 1 }; и напечатайте y (10).

Ожидаемый вывод:
10', 'fn main() {
    // ваш код
}
', 'Последнее выражение в блоке — без точки с запятой: оно становится значением блока.', '{"driver": "", "expected": ["10"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-explicit-types', 13, 'rust', 'Явные типы', 'Объявите три переменные с явными типами: a: i64 = 3_000_000_000, b: u8 = 255, c: f32 = 1.5. Напечатайте их по одной на строке.

Ожидаемый вывод:
3000000000
255
1.5', 'fn main() {
    // ваш код
}
', 'Тип пишут после двоеточия; подчёркивания внутри числа — просто для читаемости.', '{"driver": "", "expected": ["3000000000", "255", "1.5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-literal-forms', 14, 'rust', 'Формы записи чисел', 'Напечатайте в одну строку через пробел значения литералов: 1_000_000, 0xff, 0b1010, 0o17 (десятичные значения будут: 1000000 255 10 15).

Ожидаемый вывод:
1000000 255 10 15', 'fn main() {
    // ваш код
}
', '0x — шестнадцатеричный, 0b — двоичный, 0o — восьмеричный литерал.', '{"driver": "", "expected": ["1000000 255 10 15"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-swap-temp', 15, 'rust', 'Обмен через третью переменную', 'a = 3, b = 8 (mut). Поменяйте значения через временную переменную tmp. Напечатайте «a=8 b=3» после обмена.

Ожидаемый вывод:
a=8 b=3', 'fn main() {
    // ваш код
}
', 'tmp = a; a = b; b = tmp; — порядок важен.', '{"driver": "", "expected": ["a=8 b=3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-swap-tuple', 16, 'rust', 'Обмен через кортеж', 'То же, что в прошлой задаче, но без временной переменной: (a, b) = (b, a);. a = 3, b = 8; напечатайте «a=8 b=3».

Ожидаемый вывод:
a=8 b=3', 'fn main() {
    // ваш код
}
', 'Справа сначала собирается кортеж (b, a), потом он раскладывается в a и b.', '{"driver": "", "expected": ["a=8 b=3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-destructure', 17, 'rust', 'Разбор кортежа', 'Разберите кортеж (1, 2.5, "три") в переменные x, y, z одним let. Напечатайте «1 2.5 три».

Ожидаемый вывод:
1 2.5 три', 'fn main() {
    // ваш код
}
', 'let (x, y, z) = (…); — три переменные сразу.', '{"driver": "", "expected": ["1 2.5 три"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-deferred-init', 18, 'rust', 'Присвоить позже', 'Объявите let grade; без значения. Если score (= 85) не меньше 60, присвойте «сдано», иначе «не сдано». Напечатайте «Оценка: сдано».

Ожидаемый вывод:
Оценка: сдано', 'fn main() {
    // ваш код
}
', 'if условие { … } else { … } — условие в расте без скобок; в каждой ветке grade присваивается ровно один раз.', '{"driver": "", "expected": ["Оценка: сдано"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-rectangle', 19, 'rust', 'Прямоугольник', 'width = 12, height = 5. Напечатайте две строки: «Площадь: 60» и «Периметр: 34».

Ожидаемый вывод:
Площадь: 60
Периметр: 34', 'fn main() {
    // ваш код
}
', 'Площадь — width * height, периметр — 2 * (width + height).', '{"driver": "", "expected": ["Площадь: 60", "Периметр: 34"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-bank-balance', 20, 'rust', 'Баланс счёта', 'balance = 1000 (mut). Зачислите 250, спишите 400, зачислите 75. После каждой операции печатайте баланс: 1250, 850, 925.

Ожидаемый вывод:
1250
850
925', 'fn main() {
    // ваш код
}
', 'balance += 250; balance -= 400; balance += 75; и println! после каждой строки.', '{"driver": "", "expected": ["1250", "850", "925"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-celsius-shadow', 21, 'rust', 'Цельсий → Фаренгейт затенением', 'temp = 36.6 (градусы Цельсия). Затените её значением в Фаренгейтах (× 9 / 5 + 32) и напечатайте с одним знаком: «97.9».

Ожидаемый вывод:
97.9', 'fn main() {
    // ваш код
}
', 'Дробные числа пишите с точкой: 9.0, 5.0, 32.0.', '{"driver": "", "expected": ["97.9"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-average', 22, 'rust', 'Среднее трёх чисел', 'a = 4, b = 7, c = 10 (целые). Напечатайте среднее арифметическое с тремя знаками после запятой: «7.000». Превратите сумму в дробное число с помощью as f64.

Ожидаемый вывод:
7.000', 'fn main() {
    // ваш код
}
', 'Целое в дробное переводится явно: sum as f64.', '{"driver": "", "expected": ["7.000"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-shadow-in-block', 23, 'rust', 'Результат блока и затенение', 'Объявите n = 10. Затените в блоке n = n * 2 + 1 и верните значение из блока в переменную r. Напечатайте «r=21 n=10».

Ожидаемый вывод:
r=21 n=10', 'fn main() {
    // ваш код
}
', 'Блок вернёт последнее выражение (n без точки с запятой); внешняя n не изменится.', '{"driver": "", "expected": ["r=21 n=10"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-countdown', 24, 'rust', 'Обратный отсчёт вручную', 'n = 3 (mut). Напечатайте n, уменьшите на 1 (n -= 1), снова напечатайте — так для 3, 2, 1, затем напечатайте «Старт!».

Ожидаемый вывод:
3
2
1
Старт!', 'fn main() {
    // ваш код
}
', 'Три пары «печать, уменьшение» (последнее уменьшение можно не писать) и финальная строка.', '{"driver": "", "expected": ["3", "2", "1", "Старт!"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-string-mut', 25, 'rust', 'Изменяемая строка', 'Создайте изменяемую строку let mut s = String::from("Привет"); допишите к ней методом push_str текст ", мир!" и напечатайте: «Привет, мир!».

Ожидаемый вывод:
Привет, мир!', 'fn main() {
    // ваш код
}
', 'String::from("…") создаёт владеющую строку, а s.push_str("…") дописывает в конец; для этого нужен mut.', '{"driver": "", "expected": ["Привет, мир!"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-bmi', 26, 'rust', 'Индекс массы тела', 'weight = 70.0 (кг), height = 1.75 (м). ИМТ = weight / (height * height). Напечатайте «ИМТ: 22.9».

Ожидаемый вывод:
ИМТ: 22.9', 'fn main() {
    // ваш код
}
', 'Все числа дробные — с точкой; формат {:.1}.', '{"driver": "", "expected": ["ИМТ: 22.9"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-fix-annotation', 27, 'rust', 'Исправьте: тип не подходит значению', 'Программа не собирается: число 5.5 нельзя записать в переменную с типом i32. Исправьте тип так, чтобы вывод был «5.5».

Ожидаемый вывод:
5.5', 'fn main() {
    let n: i32 = 5.5;
    println!("{}", n);
}
', 'Дробным числам подходит f64 (или f32).', '{"driver": "", "expected": ["5.5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-fix-uninit', 28, 'rust', 'Исправьте: переменная без значения', 'Программа читает переменную, которой могло не быть присвоено значение. Исправьте так, чтобы напечатать «большое», когда n = 150, и «маленькое» иначе.

Ожидаемый вывод:
большое', 'fn main() {
    let n = 150;
    let label;
    if n > 100 {
        label = "большое";
    }
    println!("{}", label);
}
', 'Добавьте ветку else: тогда во всех путях значение будет присвоено.', '{"driver": "", "expected": ["большое"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 2, 'r2-final-program', 29, 'rust', 'Итоговая программа: зарплата', 'Salary = 120000. Налог 13% — вычтите (используйте целочисленную арифметику: salary * 13 / 100). Затем затените salary суммой после налога и напечатайте три строки: «Налог: 15600», «На руки: 104400» и «В месяц на аренду: 31320» (30% от оставшегося, снова salary * 30 / 100).

Ожидаемый вывод:
Налог: 15600
На руки: 104400
В месяц на аренду: 31320', 'fn main() {
    // ваш код
}
', 'tax = salary * 13 / 100; затем let salary = salary - tax; rent = salary * 30 / 100.', '{"driver": "", "expected": ["Налог: 15600", "На руки: 104400", "В месяц на аренду: 31320"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-i32-default', 0, 'rust', 'Целое по умолчанию', 'Объявите n = 2147483647 (это i32::MAX) и напечатайте n. Затем напечатайте значение константы i32::MIN. Две строки.

Ожидаемый вывод:
2147483647
-2147483648', 'fn main() {
    // ваш код
}
', 'i32::MIN — константа типа; печатается как обычное число.', '{"driver": "", "expected": ["2147483647", "-2147483648"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-u8-range', 1, 'rust', 'Границы u8 и i8', 'Напечатайте через пробел u8::MIN, u8::MAX, i8::MIN, i8::MAX: «0 255 -128 127».

Ожидаемый вывод:
0 255 -128 127', 'fn main() {
    // ваш код
}
', 'println!("{} {} {} {}", u8::MIN, …);', '{"driver": "", "expected": ["0 255 -128 127"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-i64-big', 2, 'rust', 'Большое число', 'Объявите big: i64 = 5_000_000_000 и напечатайте big * 2 («10000000000»). С типом i32 такое число не поместилось бы.

Ожидаемый вывод:
10000000000', 'fn main() {
    // ваш код
}
', 'Явный тип i64 после двоеточия.', '{"driver": "", "expected": ["10000000000"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-size-of', 3, 'rust', 'Размеры типов', 'Напечатайте размеры в байтах типов u8, i32, f64, char, bool — по одному на строке: 1, 4, 8, 4, 1. Функция: std::mem::size_of::<T>().

Ожидаемый вывод:
1
4
8
4
1', 'fn main() {
    // ваш код
}
', 'Тип указывают в угловых скобках: size_of::<u8>().', '{"driver": "", "expected": ["1", "4", "8", "4", "1"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-int-division', 4, 'rust', 'Целое деление и остаток', 'Напечатайте три строки: 17 / 5, 17 % 5 и 17.0 / 5.0. Ожидается «3», «2» и «3.4».

Ожидаемый вывод:
3
2
3.4', 'fn main() {
    // ваш код
}
', 'Целые числа дают целый результат, дробные — дробный.', '{"driver": "", "expected": ["3", "2", "3.4"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-neg-rem', 5, 'rust', 'Остаток с отрицательным', 'Напечатайте -7 / 2, -7 % 2 и (-7_i32).rem_euclid(2) — по строке: «-3», «-1», «1». Остаток в Rust берёт знак делимого, rem_euclid — всегда неотрицательный.

Ожидаемый вывод:
-3
-1
1', 'fn main() {
    // ваш код
}
', 'В питоне -7 // 2 = -4, а в расте целое деление отсекает к нулю.', '{"driver": "", "expected": ["-3", "-1", "1"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-pow', 6, 'rust', 'Степени', 'Напечатайте 2^10 (методом pow для целого) и 1.5^3 (методом powi для дробного): «1024» и «3.375».

Ожидаемый вывод:
1024
3.375', 'fn main() {
    // ваш код
}
', '2_i32.pow(10); 1.5_f64.powi(3)', '{"driver": "", "expected": ["1024", "3.375"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-checked', 7, 'rust', 'checked_add', 'Напечатайте результат 250_u8.checked_add(5) и 250_u8.checked_add(10) — по строке. Метод возвращает Option: «Some(255)» и «None». Для вывода Option используйте {:?}.

Ожидаемый вывод:
Some(255)
None', 'fn main() {
    // ваш код
}
', 'println!("{:?}", …) — отладочный вывод.', '{"driver": "", "expected": ["Some(255)", "None"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-wrapping', 8, 'rust', 'Оборот по кругу', 'Напечатайте 250_u8.wrapping_add(10) («4»), 250_u8.saturating_add(10) («255») и 5_u8.wrapping_sub(10) («251») — три строки.

Ожидаемый вывод:
4
255
251', 'fn main() {
    // ваш код
}
', 'wrapping — по кругу, saturating — упирается в границу.', '{"driver": "", "expected": ["4", "255", "251"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-overflowing', 9, 'rust', 'overflowing_add', 'Напечатайте 200_u8.overflowing_add(100) и 20_u8.overflowing_add(100) — результат пара: «(44, true)» и «(120, false)». Для пары используйте {:?}.

Ожидаемый вывод:
(44, true)
(120, false)', 'fn main() {
    // ваш код
}
', 'Пара (результат, было_ли_переполнение).', '{"driver": "", "expected": ["(44, true)", "(120, false)"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-fix-overflow', 10, 'rust', 'Исправьте: константа не влезает', 'Программа не собирается: число 300 не помещается в u8. Замените тип на подходящий (u16), чтобы напечатать «300».

Ожидаемый вывод:
300', 'fn main() {
    let x: u8 = 300;
    println!("{}", x);
}
', 'u8 вмещает до 255; u16 — до 65535.', '{"driver": "", "expected": ["300"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-hex-bin', 11, 'rust', 'Системы счисления', 'Напечатайте число 255 как «ff» (формат {:x}), как «11111111» (формат {:b}) и как «377» (формат {:o}) — три строки.

Ожидаемый вывод:
ff
11111111
377', 'fn main() {
    // ваш код
}
', '{:x} — шестнадцатеричная, {:b} — двоичная, {:o} — восьмеричная запись.', '{"driver": "", "expected": ["ff", "11111111", "377"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-f64-ops', 12, 'rust', 'Дробная арифметика', 'Напечатайте две строки: 10.0 / 4.0 и 10.0 % 4.0 — «2.5» и «2».

Ожидаемый вывод:
2.5
2', 'fn main() {
    // ваш код
}
', 'Остаток определён и для дробных чисел.', '{"driver": "", "expected": ["2.5", "2"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-float-compare', 13, 'rust', 'Неточность дробных', 'Напечатайте 0.1 + 0.2 (будет «0.30000000000000004»), затем результат сравнения 0.1 + 0.2 == 0.3 («false»), затем сравнение с допуском: ((0.1 + 0.2) - 0.3).abs() < 1e-9 («true»).

Ожидаемый вывод:
0.30000000000000004
false
true', 'fn main() {
    // ваш код
}
', 'Дробные числа сравнивают через допуск, а не через ==.', '{"driver": "", "expected": ["0.30000000000000004", "false", "true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-round-family', 14, 'rust', 'Округление', 'x = 2.5. Напечатайте x.floor(), x.ceil(), x.round(), x.trunc() — по строке: «2», «3», «3», «2» (дробные результаты, печатаются без .0 при выводе через {}).

Ожидаемый вывод:
2
3
3
2', 'fn main() {
    // ваш код
}
', 'floor — вниз, ceil — вверх, round — к ближайшему (0.5 — от нуля), trunc — отбросить дробь.', '{"driver": "", "expected": ["2", "3", "3", "2"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-sqrt-hypot', 15, 'rust', 'Гипотенуза', 'Катеты 3.0 и 4.0. Напечатайте длину гипотенузы через sqrt: «5».

Ожидаемый вывод:
5', 'fn main() {
    // ваш код
}
', '(a * a + b * b).sqrt() — метод sqrt у дробного числа.', '{"driver": "", "expected": ["5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-nan-inf', 16, 'rust', 'inf и NaN', 'Напечатайте 1.0 / 0.0, -1.0 / 0.0 и 0.0 / 0.0 (три строки: «inf», «-inf», «NaN»), а затем (0.0_f64 / 0.0).is_nan() («true»).

Ожидаемый вывод:
inf
-inf
NaN
true', 'fn main() {
    // ваш код
}
', 'Тип f64 указан, чтобы компилятор понял метод is_nan.', '{"driver": "", "expected": ["inf", "-inf", "NaN", "true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-as-cast', 17, 'rust', 'Приведения as', 'Напечатайте по строке: 3.99_f64 as i32 («3»), 300_i32 as u8 («44»), -1_i32 as u32 («4294967295»), 65_u8 as char («A»).

Ожидаемый вывод:
3
44
4294967295
A', 'fn main() {
    // ваш код
}
', 'as отрезает биты и дробную часть.', '{"driver": "", "expected": ["3", "44", "4294967295", "A"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-fix-mix', 18, 'rust', 'Исправьте: смешанные типы', 'Нельзя сложить i32 и f64 без преобразования. Исправьте программу так, чтобы вывод был «7.5».

Ожидаемый вывод:
7.5', 'fn main() {
    let a: i32 = 3;
    let b: f64 = 4.5;
    println!("{}", a + b);
}
', 'a as f64 + b', '{"driver": "", "expected": ["7.5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-from', 19, 'rust', 'From без потерь', 'Объявите a: u8 = 200 и b: i64 = 5_000_000_000. Напечатайте сумму i64::from(a) + b: «5000000200».

Ожидаемый вывод:
5000000200', 'fn main() {
    // ваш код
}
', 'i64::from(a) безопасно расширяет u8 до i64.', '{"driver": "", "expected": ["5000000200"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-try-from', 20, 'rust', 'try_from', 'Напечатайте u8::try_from(200_i32).is_ok() и u8::try_from(300_i32).is_ok() — «true» и «false».

Ожидаемый вывод:
true
false', 'fn main() {
    // ваш код
}
', 'try_from возвращает Result; .is_ok() — «получилось ли».', '{"driver": "", "expected": ["true", "false"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-parse', 21, 'rust', 'Разбор числа из текста', 'Разберите строки «41» и «3.5» в i32 и f64 методом parse с unwrap. Напечатайте сумму n + 1 и произведение x * 2.0: «42» и «7».

Ожидаемый вывод:
42
7', 'fn main() {
    // ваш код
}
', 'let n: i32 = "41".parse().unwrap(); — тип берётся из аннотации.', '{"driver": "", "expected": ["42", "7"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-parse-fail', 22, 'rust', 'parse с ошибкой', 'Для строк «12», «abc» и «-5» напечатайте, получилось ли превратить в i32: «true», «false», «true» (метод parse::<i32>().is_ok()).

Ожидаемый вывод:
true
false
true', 'fn main() {
    // ваш код
}
', 'Тип можно указать через turbofish: parse::<i32>().', '{"driver": "", "expected": ["true", "false", "true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-bool-ops', 23, 'rust', 'Логика', 'Пусть a = true, b = false. Напечатайте a && b, a || b, !a, a && !b — по строке: «false», «true», «false», «true».

Ожидаемый вывод:
false
true
false
true', 'fn main() {
    // ваш код
}
', '&& — «и», || — «или», ! — «не».', '{"driver": "", "expected": ["false", "true", "false", "true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-compare-chain', 24, 'rust', 'Сравнения', 'x = 15. Напечатайте результаты: x > 10, x == 15, x != 15, x >= 20, и попадание в диапазон x >= 10 && x <= 20 — пять строк: true, true, false, false, true.

Ожидаемый вывод:
true
true
false
false
true', 'fn main() {
    // ваш код
}
', 'Результат сравнения — bool, его можно печатать прямо.', '{"driver": "", "expected": ["true", "true", "false", "false", "true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-fix-if-int', 25, 'rust', 'Исправьте: условие не bool', 'В if стоит число — это ошибка. Исправьте условие так, чтобы напечатать «не ноль» для n = 5.

Ожидаемый вывод:
не ноль', 'fn main() {
    let n = 5;
    if n {
        println!("не ноль");
    }
}
', 'Условие — явное сравнение n != 0.', '{"driver": "", "expected": ["не ноль"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-char-basic', 26, 'rust', 'Символы', 'c = ''ж''. Напечатайте сам символ, затем его код через as u32 («1078»), затем c.is_alphabetic() («true»), и ''7''.is_numeric() («true») — по строке.

Ожидаемый вывод:
ж
1078
true
true', 'fn main() {
    // ваш код
}
', '''ж'' as u32 — код символа в Юникоде.', '{"driver": "", "expected": ["ж", "1078", "true", "true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-char-case', 27, 'rust', 'Регистр символа', 'Для ''q'' напечатайте c.to_ascii_uppercase() («Q»), для ''Я'' — c.to_lowercase().next().unwrap() («я») и символ-цифру ''8''.to_digit(10).unwrap() + 1 («9») — три строки.

Ожидаемый вывод:
Q
я
9', 'fn main() {
    // ваш код
}
', 'to_lowercase возвращает итератор — берём первый символ через next().unwrap().', '{"driver": "", "expected": ["Q", "я", "9"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-char-shift', 28, 'rust', 'Сдвиг по алфавиту', 'Возьмите ''a'' и напечатайте символ, следующий за ним в таблице (через as u8 + 1 as char): «b». Затем так же получите ''z'' из ''a'' + 25: «z».

Ожидаемый вывод:
b
z', 'fn main() {
    // ваш код
}
', '(c as u8 + 1) as char', '{"driver": "", "expected": ["b", "z"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 3, 'r3-final-types', 29, 'rust', 'Итоговая: сводка типов', 'Объявите n: i32 = -17, x: f64 = 2.5, ok: bool = true, c: char = ''Я''. Напечатайте четыре строки через пробел в формате «n=-17 x=2.5 ok=true c=Я», затем отдельной строкой n.abs() as f64 * x («42.5»).

Ожидаемый вывод:
n=-17 x=2.5 ok=true c=Я
42.5', 'fn main() {
    // ваш код
}
', 'Сначала приведите n.abs() к f64 через as, затем умножьте на x.', '{"driver": "", "expected": ["n=-17 x=2.5 ok=true c=Я", "42.5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-add', 0, 'rust', 'Сумма двух', 'Напишите функцию add, которая принимает два числа i32 и возвращает их сумму.', 'fn add(a: i32, b: i32) -> i32 {
    todo!()
}
', 'Последнее выражение без точки с запятой станет результатом: a + b', '{"driver": "fn main() {\n    println!(\"{}\", add(2, 3));\n    println!(\"{}\", add(-10, 4));\n    println!(\"{}\", add(0, 0));\n}\n", "expected": ["5", "-6", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-square', 1, 'rust', 'Квадрат числа', 'Напишите функцию square(x: i32) -> i32, возвращающую квадрат числа.', 'fn square(x: i32) -> i32 {
    todo!()
}
', 'x * x — без return и без точки с запятой.', '{"driver": "fn main() {\n    println!(\"{}\", square(7));\n    println!(\"{}\", square(-3));\n    println!(\"{}\", square(0));\n}\n", "expected": ["49", "9", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-is-even', 2, 'rust', 'Чётное число', 'Напишите функцию is_even(n: i32) -> bool: true для чётных чисел, включая отрицательные и ноль.', 'fn is_even(n: i32) -> bool {
    todo!()
}
', 'Остаток от деления на 2 равен нулю. Для отрицательных n % 2 тоже -1 или 0: сравнение с 0 подходит.', '{"driver": "fn main() {\n    for n in [4, 7, 0, -2, -3] {\n        println!(\"{} {}\", n, is_even(n));\n    }\n}\n", "expected": ["4 true", "7 false", "0 true", "-2 true", "-3 false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-max-of-two', 3, 'rust', 'Большее из двух', 'Напишите функцию max_of_two(a, b), возвращающую большее из двух i32. Используйте if–else как выражение.', 'fn max_of_two(a: i32, b: i32) -> i32 {
    todo!()
}
', 'if a > b { a } else { b } — блок с выражениями без точек с запятой.', '{"driver": "fn main() {\n    println!(\"{}\", max_of_two(3, 9));\n    println!(\"{}\", max_of_two(9, 3));\n    println!(\"{}\", max_of_two(-5, -5));\n    println!(\"{}\", max_of_two(-1, -8));\n}\n", "expected": ["9", "9", "-5", "-1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-abs-diff', 4, 'rust', 'Разность по модулю', 'Напишите функцию abs_diff(a, b): расстояние между числами |a − b| для i32. Не используйте готовый метод — только if–else и вычитание.', 'fn abs_diff(a: i32, b: i32) -> i32 {
    todo!()
}
', 'Из большего вычтите меньшее.', '{"driver": "fn main() {\n    println!(\"{}\", abs_diff(10, 3));\n    println!(\"{}\", abs_diff(3, 10));\n    println!(\"{}\", abs_diff(-4, 6));\n    println!(\"{}\", abs_diff(5, 5));\n}\n", "expected": ["7", "7", "10", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-area-rect', 5, 'rust', 'Площадь и периметр', 'Напишите две функции для прямоугольника с целыми сторонами: area(w, h) — площадь и perimeter(w, h) — периметр.', 'fn area(w: i32, h: i32) -> i32 {
    todo!()
}

fn perimeter(w: i32, h: i32) -> i32 {
    todo!()
}
', 'area: w * h; perimeter: 2 * (w + h).', '{"driver": "fn main() {\n    println!(\"{}\", area(4, 5));\n    println!(\"{}\", perimeter(4, 5));\n    println!(\"{}\", area(10, 10));\n    println!(\"{}\", perimeter(1, 1));\n}\n", "expected": ["20", "18", "100", "4"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-c-to-f', 6, 'rust', 'Цельсий в Фаренгейт', 'Напишите функцию c_to_f(c: f64) -> f64: градусы Цельсия в Фаренгейты по формуле c · 9 / 5 + 32.', 'fn c_to_f(c: f64) -> f64 {
    todo!()
}
', 'Числа в формуле — дробные литералы: 9.0, 5.0, 32.0.', '{"driver": "fn main() {\n    println!(\"{:.1}\", c_to_f(0.0));\n    println!(\"{:.1}\", c_to_f(100.0));\n    println!(\"{:.1}\", c_to_f(-40.0));\n    println!(\"{:.1}\", c_to_f(36.6));\n}\n", "expected": ["32.0", "212.0", "-40.0", "97.9"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-greet', 7, 'rust', 'Приветствие', 'Напишите функцию greet(name: &str) -> String, возвращающую строку «Привет, <имя>!». Используйте макрос format!.', 'fn greet(name: &str) -> String {
    todo!()
}
', 'format!("Привет, {}!", name) возвращает String, а не печатает.', '{"driver": "fn main() {\n    println!(\"{}\", greet(\"Аня\"));\n    println!(\"{}\", greet(\"мир\"));\n}\n", "expected": ["Привет, Аня!", "Привет, мир!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-divmod', 8, 'rust', 'Частное и остаток', 'Напишите функцию divmod(a, b) -> (i32, i32): частное и остаток от деления a на b (b > 0, a ≥ 0).', 'fn divmod(a: i32, b: i32) -> (i32, i32) {
    todo!()
}
', 'Верните кортеж (a / b, a % b).', '{"driver": "fn main() {\n    let (q, r) = divmod(17, 5);\n    println!(\"{} {}\", q, r);\n    let p = divmod(9, 3);\n    println!(\"{} {}\", p.0, p.1);\n}\n", "expected": ["3 2", "3 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-min-max3', 9, 'rust', 'Наименьшее и наибольшее', 'Напишите функцию min_max(a, b, c) -> (i32, i32): наименьшее и наибольшее из трёх чисел. Можно пользоваться методами a.min(b) и a.max(b).', 'fn min_max(a: i32, b: i32, c: i32) -> (i32, i32) {
    todo!()
}
', 'a.min(b).min(c) и a.max(b).max(c)', '{"driver": "fn main() {\n    println!(\"{:?}\", min_max(3, 9, 1));\n    println!(\"{:?}\", min_max(-5, -2, -9));\n    println!(\"{:?}\", min_max(7, 7, 7));\n}\n", "expected": ["(1, 9)", "(-9, -2)", "(7, 7)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-sign', 10, 'rust', 'Знак числа', 'Напишите функцию sign(n: i32) -> i32: 1 для положительных, -1 для отрицательных, 0 для нуля. Одним выражением if – else if – else.', 'fn sign(n: i32) -> i32 {
    todo!()
}
', 'Цепочка if … else if … else — одно выражение; все ветки i32.', '{"driver": "fn main() {\n    for n in [5, -3, 0, 100, -100] {\n        println!(\"{}\", sign(n));\n    }\n}\n", "expected": ["1", "-1", "0", "1", "-1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-clamp', 11, 'rust', 'Зажать в диапазон', 'Напишите функцию clamp(x, lo, hi): если x меньше lo — вернуть lo, если больше hi — hi, иначе x. Используйте ранний return.', 'fn clamp(x: i32, lo: i32, hi: i32) -> i32 {
    todo!()
}
', 'Два раннего return, затем x — итоговое выражение.', '{"driver": "fn main() {\n    println!(\"{}\", clamp(5, 0, 10));\n    println!(\"{}\", clamp(-5, 0, 10));\n    println!(\"{}\", clamp(50, 0, 10));\n    println!(\"{}\", clamp(0, 0, 10));\n}\n", "expected": ["5", "0", "10", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-factorial', 12, 'rust', 'Факториал', 'Напишите функцию fact(n: u64) -> u64: факториал n! (0! = 1). Решите рекурсией.', 'fn fact(n: u64) -> u64 {
    todo!()
}
', 'База: n ≤ 1 → 1. Шаг: n * fact(n - 1).', '{"driver": "fn main() {\n    for n in [0, 1, 5, 10, 20] {\n        println!(\"{}\", fact(n));\n    }\n}\n", "expected": ["1", "1", "120", "3628800", "2432902008176640000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-fib', 13, 'rust', 'Числа Фибоначчи', 'Напишите функцию fib(n: u32) -> u64 рекурсией: fib(0) = 0, fib(1) = 1, fib(n) = fib(n−1) + fib(n−2).', 'fn fib(n: u32) -> u64 {
    todo!()
}
', 'Для n < 2 результат равен самому n; приведите его к u64 через as.', '{"driver": "fn main() {\n    for n in 0..=10 {\n        print!(\"{} \", fib(n));\n    }\n    println!();\n    println!(\"{}\", fib(25));\n}\n", "expected": ["0 1 1 2 3 5 8 13 21 34 55", "75025"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-gcd', 14, 'rust', 'НОД рекурсией', 'Напишите функцию gcd(a: u32, b: u32) -> u32 — наибольший общий делитель алгоритмом Евклида: gcd(a, 0) = a, иначе gcd(b, a % b).', 'fn gcd(a: u32, b: u32) -> u32 {
    todo!()
}
', 'Рекурсия сокращает пару (a, b) до (b, a % b), пока b не станет нулём.', '{"driver": "fn main() {\n    println!(\"{}\", gcd(48, 18));\n    println!(\"{}\", gcd(17, 5));\n    println!(\"{}\", gcd(100, 0));\n    println!(\"{}\", gcd(1_000_000_007, 998_244_353));\n}\n", "expected": ["6", "1", "100", "1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-power', 15, 'rust', 'Возведение в степень', 'Напишите функцию power(base: i64, exp: u32) -> i64 рекурсией, без pow: power(x, 0) = 1, power(x, n) = x · power(x, n−1).', 'fn power(base: i64, exp: u32) -> i64 {
    todo!()
}
', 'База: exp == 0 → 1.', '{"driver": "fn main() {\n    println!(\"{}\", power(2, 10));\n    println!(\"{}\", power(3, 4));\n    println!(\"{}\", power(-2, 3));\n    println!(\"{}\", power(7, 0));\n}\n", "expected": ["1024", "81", "-8", "1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-sum-to', 16, 'rust', 'Сумма до n', 'Напишите функцию sum_to(n: u32) -> u32 рекурсией: 1 + 2 + … + n (sum_to(0) = 0).', 'fn sum_to(n: u32) -> u32 {
    todo!()
}
', 'n + sum_to(n - 1)', '{"driver": "fn main() {\n    println!(\"{}\", sum_to(0));\n    println!(\"{}\", sum_to(5));\n    println!(\"{}\", sum_to(100));\n}\n", "expected": ["0", "15", "5050"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-leap', 17, 'rust', 'Високосный год', 'Напишите функцию is_leap(year: u32) -> bool: год високосный, если делится на 4, кроме годов, делящихся на 100, но не на 400.', 'fn is_leap(year: u32) -> bool {
    todo!()
}
', 'Условие целиком — одно логическое выражение с &&, ||.', '{"driver": "fn main() {\n    for y in [2000, 1900, 2024, 2023, 2100, 1600] {\n        println!(\"{} {}\", y, is_leap(y));\n    }\n}\n", "expected": ["2000 true", "1900 false", "2024 true", "2023 false", "2100 false", "1600 true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-between', 18, 'rust', 'Попадает в диапазон', 'Напишите функцию in_range(x, lo, hi) -> bool: true, если lo ≤ x ≤ hi (границы входят).', 'fn in_range(x: i32, lo: i32, hi: i32) -> bool {
    todo!()
}
', 'x >= lo && x <= hi', '{"driver": "fn main() {\n    println!(\"{}\", in_range(5, 1, 10));\n    println!(\"{}\", in_range(1, 1, 10));\n    println!(\"{}\", in_range(10, 1, 10));\n    println!(\"{}\", in_range(11, 1, 10));\n    println!(\"{}\", in_range(0, 1, 10));\n}\n", "expected": ["true", "true", "true", "false", "false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-swap', 19, 'rust', 'Поменять местами', 'Напишите функцию swap(p: (i32, i32)) -> (i32, i32), возвращающую пару с переставленными элементами.', 'fn swap(p: (i32, i32)) -> (i32, i32) {
    todo!()
}
', 'Доступ по номеру: p.0 и p.1; вернуть новый кортеж.', '{"driver": "fn main() {\n    println!(\"{:?}\", swap((1, 2)));\n    println!(\"{:?}\", swap((-5, 100)));\n}\n", "expected": ["(2, 1)", "(100, -5)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-stats', 20, 'rust', 'Сумма и среднее', 'Напишите функцию stats(a, b, c) -> (i32, f64): сумма трёх чисел и их среднее арифметическое (как f64).', 'fn stats(a: i32, b: i32, c: i32) -> (i32, f64) {
    todo!()
}
', 'Сначала sum, затем кортеж (sum, sum as f64 / 3.0).', '{"driver": "fn main() {\n    let (s, avg) = stats(4, 7, 10);\n    println!(\"{} {:.2}\", s, avg);\n    let (s, avg) = stats(1, 2, 2);\n    println!(\"{} {:.2}\", s, avg);\n}\n", "expected": ["21 7.00", "5 1.67"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-digit-sum', 21, 'rust', 'Сумма цифр', 'Напишите функцию digit_sum(n: u32) -> u32 рекурсией: сумма десятичных цифр числа. digit_sum(0) = 0, иначе n % 10 + digit_sum(n / 10).', 'fn digit_sum(n: u32) -> u32 {
    todo!()
}
', 'Последняя цифра — n % 10, остальные — n / 10.', '{"driver": "fn main() {\n    println!(\"{}\", digit_sum(0));\n    println!(\"{}\", digit_sum(123));\n    println!(\"{}\", digit_sum(99999));\n    println!(\"{}\", digit_sum(4_000_000_000));\n}\n", "expected": ["0", "6", "45", "4"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-count-digits', 22, 'rust', 'Количество цифр', 'Напишите функцию count_digits(n: u64) -> u32: сколько цифр в десятичной записи n (для 0 — одна цифра).', 'fn count_digits(n: u64) -> u32 {
    todo!()
}
', 'Если число меньше 10 — одна цифра; иначе 1 + количество цифр у n / 10.', '{"driver": "fn main() {\n    println!(\"{}\", count_digits(0));\n    println!(\"{}\", count_digits(9));\n    println!(\"{}\", count_digits(10));\n    println!(\"{}\", count_digits(123456789));\n    println!(\"{}\", count_digits(18_446_744_073_709_551_615));\n}\n", "expected": ["1", "1", "2", "9", "20"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-hypot', 23, 'rust', 'Гипотенуза', 'Напишите функцию hypot(a: f64, b: f64) -> f64: длина гипотенузы √(a² + b²).', 'fn hypot(a: f64, b: f64) -> f64 {
    todo!()
}
', '(a * a + b * b).sqrt()', '{"driver": "fn main() {\n    println!(\"{}\", hypot(3.0, 4.0));\n    println!(\"{:.4}\", hypot(1.0, 1.0));\n    println!(\"{}\", hypot(5.0, 12.0));\n}\n", "expected": ["5", "1.4142", "13"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-fix-no-return-type', 24, 'rust', 'Исправьте: нет типа результата', 'Функция double должна возвращать удвоенное число, но в сигнатуре нет типа результата. Исправьте сигнатуру — тело менять не нужно.', 'fn double(x: i32) {
    x * 2
}
', 'Добавьте -> i32 после скобок параметров.', '{"driver": "fn main() {\n    println!(\"{}\", double(21));\n    println!(\"{}\", double(-4));\n}\n", "expected": ["42", "-8"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-fix-semicolon', 25, 'rust', 'Исправьте: лишняя точка с запятой', 'Функция cube возвращает () вместо i32 из-за точки с запятой в конце. Исправьте.', 'fn cube(x: i32) -> i32 {
    x * x * x;
}
', 'Уберите ; в последней строке.', '{"driver": "fn main() {\n    println!(\"{}\", cube(3));\n    println!(\"{}\", cube(-2));\n}\n", "expected": ["27", "-8"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-fix-types', 26, 'rust', 'Исправьте: целое и дробное', 'Функция average должна вернуть среднее двух целых как f64, но (a + b) — целое, а делить его нужно на дробное 2.0. Исправьте тело функции: average(3, 4) = 3.5.', 'fn average(a: i32, b: i32) -> f64 {
    (a + b) / 2.0
}
', 'Сумму надо привести к f64: (a + b) as f64 / 2.0', '{"driver": "fn main() {\n    println!(\"{}\", average(3, 4));\n    println!(\"{}\", average(10, 20));\n}\n", "expected": ["3.5", "15"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-compose', 27, 'rust', 'Функции вместе', 'В коде уже есть функция add. Напишите triple(x), которая возвращает 3·x, используя только add (без операции *).', 'fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn triple(x: i32) -> i32 {
    todo!()
}
', 'add(add(x, x), x) — вызов внутри вызова.', '{"driver": "fn main() {\n    println!(\"{}\", triple(5));\n    println!(\"{}\", triple(-7));\n    println!(\"{}\", triple(0));\n}\n", "expected": ["15", "-21", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-fizz', 28, 'rust', 'FizzBuzz для одного числа', 'Напишите функцию fizz(n: u32) -> String: «FizzBuzz», если n делится на 15, «Fizz» — на 3, «Buzz» — на 5, иначе само число строкой. Одним выражением if – else if.', 'fn fizz(n: u32) -> String {
    todo!()
}
', 'Сначала проверяйте деление на 15. Число в строку превращает n.to_string().', '{"driver": "fn main() {\n    for n in [1, 3, 5, 15, 7, 30, 98] {\n        println!(\"{}\", fizz(n));\n    }\n}\n", "expected": ["1", "Fizz", "Buzz", "FizzBuzz", "7", "FizzBuzz", "98"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 4, 'r4-bmi-class', 29, 'rust', 'Категория ИМТ', 'Напишите функцию category(bmi: f64) -> &''static str: «недостаток» при bmi < 18.5, «норма» при bmi < 25.0, «избыток» при bmi < 30.0, иначе «ожирение».', 'fn category(bmi: f64) -> &''static str {
    todo!()
}
', 'Строковые литералы — &''static str: возвращать их из ветвей можно сразу.', '{"driver": "fn main() {\n    for b in [17.0, 18.5, 22.9, 25.0, 29.9, 35.0] {\n        println!(\"{}\", category(b));\n    }\n}\n", "expected": ["недостаток", "норма", "норма", "избыток", "избыток", "ожирение"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-if-sign', 0, 'rust', 'Знак числа', 'n = -7. Напечатайте «минус», если n < 0, «ноль», если n == 0, иначе «плюс». Используйте if – else if – else.

Ожидаемый вывод:
минус', 'fn main() {
    // ваш код
}
', 'Три ветки: if n < 0, else if n == 0, else.', '{"driver": "", "expected": ["минус"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-if-grade', 1, 'rust', 'Оценка по баллам', 'score = 78. Напечатайте оценку: «A» при score ≥ 90, «B» при ≥ 75, «C» при ≥ 60, иначе «D». Ожидается «B».

Ожидаемый вывод:
B', 'fn main() {
    // ваш код
}
', 'Проверяйте от высшего порога к низшему.', '{"driver": "", "expected": ["B"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-if-expr', 2, 'rust', 'if как выражение', 'Объявите x = 12. Запишите в let parity результат if-выражения: «чётное», если x % 2 == 0, иначе «нечётное». Напечатайте parity.

Ожидаемый вывод:
чётное', 'fn main() {
    // ваш код
}
', 'let parity = if … { "чётное" } else { "нечётное" };', '{"driver": "", "expected": ["чётное"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-max-of-three', 3, 'rust', 'Максимум из трёх', 'Даны a = 17, b = 42, c = 29. Найдите наибольшее с помощью if и напечатайте «42».

Ожидаемый вывод:
42', 'fn main() {
    // ваш код
}
', 'Если a не меньше обоих — это a; иначе сравните b и c.', '{"driver": "", "expected": ["42"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-for-count', 4, 'rust', 'Считаем от 1 до 5', 'Напечатайте числа от 1 до 5 включительно по одному на строке циклом for.

Ожидаемый вывод:
1
2
3
4
5', 'fn main() {
    // ваш код
}
', 'for i in 1..=5 { … } — диапазон с правой границей.', '{"driver": "", "expected": ["1", "2", "3", "4", "5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-for-exclusive', 5, 'rust', 'Диапазон без правой границы', 'Напечатайте числа 0, 1, 2, 3, 4 в одну строку через пробел (для строки без перевода используйте print!). В конце — перевод строки println!().

Ожидаемый вывод:
0 1 2 3 4', 'fn main() {
    // ваш код
}
', 'Пробел после каждого числа допустим: вывод сравнивается без пробелов на концах строк.', '{"driver": "", "expected": ["0 1 2 3 4"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-sum-1-100', 6, 'rust', 'Сумма от 1 до 100', 'Посчитайте и напечатайте сумму чисел от 1 до 100 включительно циклом for: «5050».

Ожидаемый вывод:
5050', 'fn main() {
    // ваш код
}
', 'Накопитель sum = 0, в цикле sum += i.', '{"driver": "", "expected": ["5050"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-sum-even', 7, 'rust', 'Сумма чётных', 'Посчитайте сумму чётных чисел от 1 до 100 включительно: «2550».

Ожидаемый вывод:
2550', 'fn main() {
    // ваш код
}
', 'Внутри цикла — if i % 2 == 0.', '{"driver": "", "expected": ["2550"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-factorial-loop', 8, 'rust', 'Факториал циклом', 'Посчитайте 10! = 1·2·…·10 циклом (u64) и напечатайте «3628800». Затем 20!: «2432902008176640000».

Ожидаемый вывод:
3628800
2432902008176640000', 'fn main() {
    // ваш код
}
', 'Накопитель произведения начинается с 1; для 20! нужен u64.', '{"driver": "", "expected": ["3628800", "2432902008176640000"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-multiplication-table', 9, 'rust', 'Таблица умножения', 'Напечатайте таблицу умножения на 7 от 1 до 10: десять строк «7 x 1 = 7», «7 x 2 = 14», … «7 x 10 = 70».

Ожидаемый вывод:
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70', 'fn main() {
    // ваш код
}
', 'println!("7 x {} = {}", i, 7 * i);', '{"driver": "", "expected": ["7 x 1 = 7", "7 x 2 = 14", "7 x 3 = 21", "7 x 4 = 28", "7 x 5 = 35", "7 x 6 = 42", "7 x 7 = 49", "7 x 8 = 56", "7 x 9 = 63", "7 x 10 = 70"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-countdown', 10, 'rust', 'Обратный отсчёт', 'Напечатайте числа от 5 до 1 по одному на строке, затем «Пуск!». Используйте rev() для диапазона.

Ожидаемый вывод:
5
4
3
2
1
Пуск!', 'fn main() {
    // ваш код
}
', 'for i in (1..=5).rev() { … }', '{"driver": "", "expected": ["5", "4", "3", "2", "1", "Пуск!"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-step-by', 11, 'rust', 'Шаг три', 'Напечатайте через пробел числа 0, 3, 6, …, 30 (метод step_by(3) у диапазона 0..=30) и перевод строки.

Ожидаемый вывод:
0 3 6 9 12 15 18 21 24 27 30', 'fn main() {
    // ваш код
}
', '(0..=30).step_by(3)', '{"driver": "", "expected": ["0 3 6 9 12 15 18 21 24 27 30"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-while-doubling', 12, 'rust', 'Сколько раз удвоить', 'Начните с x = 1. Пока x < 1000, удваивайте x и увеличивайте счётчик steps. Напечатайте «steps=10 x=1024».

Ожидаемый вывод:
steps=10 x=1024', 'fn main() {
    // ваш код
}
', 'while x < 1000 { x *= 2; steps += 1; }', '{"driver": "", "expected": ["steps=10 x=1024"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-loop-break', 13, 'rust', 'loop и break', 'С помощью loop найдите наименьшее n, для которого n * n > 200, и напечатайте «n=15 square=225».

Ожидаемый вывод:
n=15 square=225', 'fn main() {
    // ваш код
}
', 'Увеличивайте n и выходите по break, как только условие сработало.', '{"driver": "", "expected": ["n=15 square=225"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-loop-value', 14, 'rust', 'break со значением', 'Найдите loop-ом первое число, кратное и 7, и 11, большее 100, и сохраните его через break в переменную r. Напечатайте «154».

Ожидаемый вывод:
154', 'fn main() {
    // ваш код
}
', 'let r = loop { … break n; };', '{"driver": "", "expected": ["154"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-continue-odd', 15, 'rust', 'Только нечётные', 'Напечатайте по строке нечётные числа от 1 до 15, используя continue для пропуска чётных.

Ожидаемый вывод:
1
3
5
7
9
11
13
15', 'fn main() {
    // ваш код
}
', 'if i % 2 == 0 { continue; }', '{"driver": "", "expected": ["1", "3", "5", "7", "9", "11", "13", "15"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-fizzbuzz', 16, 'rust', 'FizzBuzz до 15', 'Для чисел 1…15 напечатайте по строке: «FizzBuzz» для кратных 15, «Fizz» для кратных 3, «Buzz» для кратных 5, иначе само число.

Ожидаемый вывод:
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz', 'fn main() {
    // ваш код
}
', 'Сначала проверяйте деление на 15.', '{"driver": "", "expected": ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-count-divisors', 17, 'rust', 'Делители числа', 'Посчитайте, сколько делителей у числа 360, и напечатайте «24».

Ожидаемый вывод:
24', 'fn main() {
    // ваш код
}
', 'Проверяйте остаток n % d для d от 1 до n.', '{"driver": "", "expected": ["24"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-is-prime', 18, 'rust', 'Простое ли 97', 'Проверьте, простое ли число 97 (делится только на 1 и на себя): переберите d от 2 до n−1 и найдите делитель. Напечатайте «простое» или «составное».

Ожидаемый вывод:
простое', 'fn main() {
    // ваш код
}
', 'Флаг prime = true; при нахождении делителя ставьте false и выходите break.', '{"driver": "", "expected": ["простое"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-primes-30', 19, 'rust', 'Простые до 30', 'Напечатайте все простые числа от 2 до 30 через пробел: «2 3 5 7 11 13 17 19 23 29». Внутри внешнего цикла проверяйте делимость вложенным циклом.

Ожидаемый вывод:
2 3 5 7 11 13 17 19 23 29', 'fn main() {
    // ваш код
}
', 'Внутри цикла по n запустите цикл по d.', '{"driver": "", "expected": ["2 3 5 7 11 13 17 19 23 29"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-gcd-loop', 20, 'rust', 'НОД циклом', 'a = 84, b = 36. Найдите наибольший общий делитель алгоритмом Евклида (while b != 0: пара (a, b) становится (b, a % b)) и напечатайте «12».

Ожидаемый вывод:
12', 'fn main() {
    // ваш код
}
', 'Три шага: t = a % b; a = b; b = t.', '{"driver": "", "expected": ["12"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-collatz', 21, 'rust', 'Гипотеза Коллатца', 'Начните с n = 27. Пока n != 1: если n чётное — делите пополам, иначе n = 3n + 1. Посчитайте число шагов steps и напечатайте «111». (Тип u64.)

Ожидаемый вывод:
111', 'fn main() {
    // ваш код
}
', 'Счётчик увеличивайте на каждом шаге внутри while.', '{"driver": "", "expected": ["111"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-digit-sum-loop', 22, 'rust', 'Сумма цифр циклом', 'n = 987654321. Посчитайте сумму его цифр циклом while (последняя цифра — n % 10, остаток — n / 10) и напечатайте «45».

Ожидаемый вывод:
45', 'fn main() {
    // ваш код
}
', 'Пока n > 0: sum += n % 10; n /= 10;', '{"driver": "", "expected": ["45"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-triangle', 23, 'rust', 'Треугольник из звёздочек', 'Напечатайте треугольник из пяти строк: в первой одна «*», во второй две, … в пятой пять. Для повторения символа используйте внутренний цикл или метод "*".repeat(n).

Ожидаемый вывод:
*
**
***
****
*****', 'fn main() {
    // ваш код
}
', '"*".repeat(i) повторяет строку i раз.', '{"driver": "", "expected": ["*", "**", "***", "****", "*****"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-nested-table', 24, 'rust', 'Таблица умножения 5×5', 'Напечатайте таблицу умножения от 1 до 5: пять строк, в каждой пять чисел через пробел (произведения i·j). Вложенные циклы for.

Ожидаемый вывод:
1 2 3 4 5
2 4 6 8 10
3 6 9 12 15
4 8 12 16 20
5 10 15 20 25', 'fn main() {
    // ваш код
}
', 'Внешний цикл — строки, внутренний — числа в строке; после внутреннего — println!().', '{"driver": "", "expected": ["1 2 3 4 5", "2 4 6 8 10", "3 6 9 12 15", "4 8 12 16 20", "5 10 15 20 25"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-labeled-break', 25, 'rust', 'Выход из вложенных циклов', 'Найдите первую пару (a, b), a < b, из диапазона 1..=20, для которой a * b = 91, и напечатайте «7 13». Выйдите из обоих циклов меткой ''outer.

Ожидаемый вывод:
7 13', 'fn main() {
    // ваш код
}
', '''outer: for … и break ''outer;', '{"driver": "", "expected": ["7 13"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-match-number', 26, 'rust', 'match по числу', 'Для n = 3 с помощью match напечатайте: «один» для 1, «два» для 2, «три» для 3, иначе «много».

Ожидаемый вывод:
три', 'fn main() {
    // ваш код
}
', 'match n { 1 => "один", …, _ => "много" }', '{"driver": "", "expected": ["три"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-match-range', 27, 'rust', 'match и диапазоны', 'Для возраста age = 34 с помощью match напечатайте категорию: 0..=12 — «ребёнок», 13..=17 — «подросток», 18..=64 — «взрослый», иначе «пожилой».

Ожидаемый вывод:
взрослый', 'fn main() {
    // ваш код
}
', 'Образец-диапазон: 0..=12 =>', '{"driver": "", "expected": ["взрослый"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-fix-off-by-one', 28, 'rust', 'Исправьте: потерялась последняя цифра', 'Программа должна напечатать сумму 1 + 2 + … + 10 = 55, но печатает 45. Исправьте диапазон.

Ожидаемый вывод:
55', 'fn main() {
    let mut s = 0;
    for i in 1..10 {
        s += i;
    }
    println!("{}", s);
}
', 'Включите правую границу: 1..=10.', '{"driver": "", "expected": ["55"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 5, 'r5-fix-condition', 29, 'rust', 'Исправьте: условие не bool', 'Программа не собирается: в if стоит присваивание вместо сравнения. Исправьте, чтобы напечатать «пять».

Ожидаемый вывод:
пять', 'fn main() {
    let x = 5;
    if x = 5 {
        println!("пять");
    }
}
', 'Сравнение — два знака равно: x == 5.', '{"driver": "", "expected": ["пять"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-literal', 0, 'rust', 'Литерал и длина', 'Объявите s = "Привет, мир!" и напечатайте две строки: саму строку, затем «bytes=…» и «chars=…» в одной строке: «bytes=21 chars=12».

Ожидаемый вывод:
Привет, мир!
bytes=21 chars=12', 'fn main() {
    // ваш код
}
', 'len() — байты, chars().count() — символы.', '{"driver": "", "expected": ["Привет, мир!", "bytes=21 chars=12"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-string-new', 1, 'rust', 'Строим String', 'Создайте пустую изменяемую String, допишите push_str("Rust"), push('' ''), push_str("любит"), push('' ''), push_str("тебя") и напечатайте «Rust любит тебя».

Ожидаемый вывод:
Rust любит тебя', 'fn main() {
    // ваш код
}
', 'push принимает символ в одинарных кавычках, push_str — строку.', '{"driver": "", "expected": ["Rust любит тебя"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-concat-plus', 2, 'rust', 'Склейка плюсом', 'Склейте String a = «раз» и &str «два» оператором +, затем добавьте «три» и напечатайте «раздватри». Левый операнд плюса — String.

Ожидаемый вывод:
раздватри', 'fn main() {
    // ваш код
}
', 'Слева String, справа &str.', '{"driver": "", "expected": ["раздватри"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-format', 3, 'rust', 'format!', 'name = "Аня", age = 30. С помощью format! соберите в переменную строку «Аня, 30 лет» и напечатайте её.

Ожидаемый вывод:
Аня, 30 лет', 'fn main() {
    // ваш код
}
', 'format!("{}, {} лет", name, age)', '{"driver": "", "expected": ["Аня, 30 лет"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-join', 4, 'rust', 'join', 'Склейте слова ["сыр", "хлеб", "молоко"] методом join с разделителем ", " и напечатайте «сыр, хлеб, молоко».

Ожидаемый вывод:
сыр, хлеб, молоко', 'fn main() {
    // ваш код
}
', 'words.join(", ")', '{"driver": "", "expected": ["сыр, хлеб, молоко"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-repeat', 5, 'rust', 'Повторение', 'Напечатайте строку из 20 тире «--------------------» методом repeat, затем «Rust» и снова 20 тире.

Ожидаемый вывод:
--------------------
Rust
--------------------', 'fn main() {
    // ваш код
}
', '"-".repeat(20)', '{"driver": "", "expected": ["--------------------", "Rust", "--------------------"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-upper-lower', 6, 'rust', 'Регистр', 's = "Привет, Мир". Напечатайте s.to_uppercase() и s.to_lowercase() — две строки: «ПРИВЕТ, МИР» и «привет, мир».

Ожидаемый вывод:
ПРИВЕТ, МИР
привет, мир', 'fn main() {
    // ваш код
}
', 'Методы возвращают новую строку.', '{"driver": "", "expected": ["ПРИВЕТ, МИР", "привет, мир"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-trim-replace', 7, 'rust', 'trim и replace', 's = "   много   пробелов   ". Напечатайте trim, а затем replace("много", "мало") у обрезанной строки: «много   пробелов» и «мало   пробелов».

Ожидаемый вывод:
много   пробелов
мало   пробелов', 'fn main() {
    // ваш код
}
', 'trim убирает пробелы только по краям.', '{"driver": "", "expected": ["много   пробелов", "мало   пробелов"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-contains', 8, 'rust', 'Поиск подстроки', 'text = "Rust — язык системного программирования". Напечатайте три строки: contains("язык"), starts_with("Rust"), ends_with("Go") → true, true, false.

Ожидаемый вывод:
true
true
false', 'fn main() {
    // ваш код
}
', 'Результат каждого метода — bool.', '{"driver": "", "expected": ["true", "true", "false"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-find', 9, 'rust', 'find', 'text = "hello world". Напечатайте позицию первого вхождения «o» (find, это Option, поэтому добавьте unwrap) и позицию «wor»: «4» и «6».

Ожидаемый вывод:
4
6', 'fn main() {
    // ваш код
}
', 'find возвращает Option<usize>; unwrap достаёт значение.', '{"driver": "", "expected": ["4", "6"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-chars-loop', 10, 'rust', 'Перебор символов', 'Для строки "раст" напечатайте каждый символ на отдельной строке циклом for по chars().

Ожидаемый вывод:
р
а
с
т', 'fn main() {
    // ваш код
}
', 'for c in "раст".chars() { … }', '{"driver": "", "expected": ["р", "а", "с", "т"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-count-vowels', 11, 'rust', 'Гласные', 'В строке "Программирование на Rust" посчитайте русские гласные «аеёиоуыэюя» (регистр не важен: сначала в нижний). Напечатайте «8».

Ожидаемый вывод:
8', 'fn main() {
    // ваш код
}
', '"…".contains(c) умеет искать символ.', '{"driver": "", "expected": ["8"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-reverse', 12, 'rust', 'Развернуть строку', 'Разверните строку "привет" методами chars().rev().collect::<String>() и напечатайте «тевирп».

Ожидаемый вывод:
тевирп', 'fn main() {
    // ваш код
}
', 'chars().rev() и collect в String.', '{"driver": "", "expected": ["тевирп"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-palindrome', 13, 'rust', 'Палиндром', 'Проверьте, является ли «А роза упала на лапу Азора» палиндромом, игнорируя пробелы и регистр. Напечатайте «true».

Ожидаемый вывод:
true', 'fn main() {
    // ваш код
}
', 'Уберите пробелы, приведите к нижнему регистру, сравните с перевёрнутой.', '{"driver": "", "expected": ["true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-words-count', 14, 'rust', 'Количество слов', 'Посчитайте слова в строке "  раз  два   три четыре " методом split_whitespace().count(): «4».

Ожидаемый вывод:
4', 'fn main() {
    // ваш код
}
', 'split_whitespace игнорирует лишние пробелы.', '{"driver": "", "expected": ["4"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-split-parse-sum', 15, 'rust', 'Сумма чисел из строки', 'Из строки "10, 20, 30, 5" извлеките числа (split по запятой, trim, parse::<i32>) и напечатайте сумму «65».

Ожидаемый вывод:
65', 'fn main() {
    // ваш код
}
', 'part.trim().parse::<i32>().unwrap()', '{"driver": "", "expected": ["65"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-lines', 16, 'rust', 'Строки текста', 'text = "раз\nдва\nтри". Напечатайте каждую строку с номером в формате «1: раз», «2: два», «3: три» (lines и enumerate).

Ожидаемый вывод:
1: раз
2: два
3: три', 'fn main() {
    // ваш код
}
', 'enumerate даёт пары (номер, значение); номер с нуля.', '{"driver": "", "expected": ["1: раз", "2: два", "3: три"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-slice', 17, 'rust', 'Срез строки', 'text = "Hello, Rust!". Напечатайте срезы: &text[0..5], &text[7..11] и &text[7..] — «Hello», «Rust» и «Rust!».

Ожидаемый вывод:
Hello
Rust
Rust!', 'fn main() {
    // ваш код
}
', 'Для ASCII-строки байты совпадают с символами.', '{"driver": "", "expected": ["Hello", "Rust", "Rust!"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-nth-char', 18, 'rust', 'n-й символ', 's = "привет". Напечатайте третий символ (индекс 2, через chars().nth(2)) и последний (chars().last()). Ожидается «и» и «т». Оба — Option, воспользуйтесь unwrap.

Ожидаемый вывод:
и
т', 'fn main() {
    // ваш код
}
', 'nth(n) возвращает Option<char>.', '{"driver": "", "expected": ["и", "т"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-char-indices', 19, 'rust', 'Позиции символов', 'Для строки "аб" напечатайте пары «позиция символ» методом char_indices: «0 а» и «2 б» (русская буква — 2 байта).

Ожидаемый вывод:
0 а
2 б', 'fn main() {
    // ваш код
}
', 'char_indices выдаёт смещение в байтах.', '{"driver": "", "expected": ["0 а", "2 б"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-format-width', 20, 'rust', 'Выравнивание', 'Напечатайте три строки: число 42 в поле шириной 8 с выравниванием вправо («[      42]»), слово «Rust» влево в поле 8 («[Rust    ]») и «hi» по центру в поле 8 с заполнителем «*» («[***hi***]»).

Ожидаемый вывод:
[      42]
[Rust    ]
[***hi***]', 'fn main() {
    // ваш код
}
', '{:>8}, {:<8}, {:*^8}', '{"driver": "", "expected": ["[      42]", "[Rust    ]", "[***hi***]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-format-float', 21, 'rust', 'Точность дробного', 'x = 3.14159265. Напечатайте x с 0, 2 и 4 знаками после запятой — «3», «3.14», «3.1416» (по строке).

Ожидаемый вывод:
3
3.14
3.1416', 'fn main() {
    // ваш код
}
', '{:.0}, {:.2}, {:.4}', '{"driver": "", "expected": ["3", "3.14", "3.1416"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-format-zero-pad', 22, 'rust', 'Нули слева', 'Напечатайте число 7 как «007» (поле ширины 3, нули слева: {:03}), а 255 в шестнадцатеричной записи с нулями в поле 4 и префиксом 0x: «0x00ff» (формат {:#06x}).

Ожидаемый вывод:
007
0x00ff', 'fn main() {
    // ваш код
}
', '{:03} и {:#06x}', '{"driver": "", "expected": ["007", "0x00ff"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-debug-format', 23, 'rust', 'Отладочный формат', 'Напечатайте строку "привет\n" через {:?} (в кавычках и с экранированием: «"привет\n"») и кортеж (1, "a", 2.5) через {:?}: «(1, "a", 2.5)».

Ожидаемый вывод:
"привет\n"
(1, "a", 2.5)', 'fn main() {
    // ваш код
}
', '{:?} — отладочное представление.', '{"driver": "", "expected": ["\"привет\\n\"", "(1, \"a\", 2.5)"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-compare', 24, 'rust', 'Сравнение строк', 'Напечатайте: «apple» < «banana» (true), «Zebra» < «apple» (true, заглавные раньше) и String::from("abc") == "abc" (true).

Ожидаемый вывод:
true
true
true', 'fn main() {
    // ваш код
}
', 'Строки сравниваются по байтам.', '{"driver": "", "expected": ["true", "true", "true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-fn-shout', 25, 'rust', 'Крик', 'Напишите функцию shout(s: &str) -> String: строка в верхнем регистре с тремя восклицательными знаками в конце.', 'fn shout(s: &str) -> String {
    todo!()
}
', 'format!("{}!!!", s.to_uppercase())', '{"driver": "fn main() {\n    println!(\"{}\", shout(\"привет\"));\n    println!(\"{}\", shout(\"Rust\"));\n}\n", "expected": ["ПРИВЕТ!!!", "RUST!!!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-fn-count-char', 26, 'rust', 'Сколько раз встречается', 'Напишите функцию count_char(s: &str, ch: char) -> usize: сколько раз символ ch встречается в s.', 'fn count_char(s: &str, ch: char) -> usize {
    todo!()
}
', 'Цикл по chars и счётчик.', '{"driver": "fn main() {\n    println!(\"{}\", count_char(\"абракадабра\", ''а''));\n    println!(\"{}\", count_char(\"hello\", ''z''));\n    println!(\"{}\", count_char(\"\", ''a''));\n}\n", "expected": ["5", "0", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-fn-first-word', 27, 'rust', 'Первое слово', 'Напишите функцию first_word(s: &str) -> &str: первое слово строки (до первого пробела; если пробелов нет — вся строка).', 'fn first_word(s: &str) -> &str {
    todo!()
}
', 'find('' '') возвращает позицию пробела; срез &s[..i].', '{"driver": "fn main() {\n    println!(\"{}\", first_word(\"hello world\"));\n    println!(\"{}\", first_word(\"один\"));\n    println!(\"{}\", first_word(\"привет мир\"));\n}\n", "expected": ["hello", "один", "привет"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-fn-capitalize', 28, 'rust', 'Заглавная первая буква', 'Напишите функцию capitalize(s: &str) -> String: первая буква заглавная, остальные без изменений (пустая строка — пустая).', 'fn capitalize(s: &str) -> String {
    todo!()
}
', 'chars().next() даёт первую букву, остаток — chars.as_str().', '{"driver": "fn main() {\n    println!(\"{}\", capitalize(\"привет\"));\n    println!(\"{}\", capitalize(\"rust\"));\n    println!(\"[{}]\", capitalize(\"\"));\n}\n", "expected": ["Привет", "Rust", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 6, 'r6-fn-caesar', 29, 'rust', 'Шифр Цезаря', 'Напишите функцию caesar(s: &str, shift: u8) -> String для латиницы a–z: каждую строчную букву сдвиньте на shift вперёд по кругу (z → a), остальные символы не меняйте.', 'fn caesar(s: &str, shift: u8) -> String {
    todo!()
}
', 'Номер буквы: c as u8 - b''a''; сдвиг по модулю 26; обратно + b''a''.', '{"driver": "fn main() {\n    println!(\"{}\", caesar(\"hello, world\", 3));\n    println!(\"{}\", caesar(\"xyz\", 3));\n    println!(\"{}\", caesar(\"abc\", 0));\n}\n", "expected": ["khoor, zruog", "abc", "abc"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-tuple-basic', 0, 'rust', 'Кортеж из трёх', 'Создайте кортеж person = ("Аня", 30, 1.68). Напечатайте его элементы по номеру через пробел: «Аня 30 1.68».

Ожидаемый вывод:
Аня 30 1.68', 'fn main() {
    // ваш код
}
', 'Доступ к элементам: person.0, person.1, person.2.', '{"driver": "", "expected": ["Аня 30 1.68"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-tuple-destructure', 1, 'rust', 'Разбор кортежа', 'Разберите кортеж (10, 20, 30) на переменные a, b, c одним let и напечатайте их сумму «60».

Ожидаемый вывод:
60', 'fn main() {
    // ваш код
}
', 'let (a, b, c) = (…);', '{"driver": "", "expected": ["60"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-tuple-debug', 2, 'rust', 'Печать кортежа', 'Напечатайте кортеж (1, "два", 3.0) в отладочном формате {:?}: «(1, "два", 3.0)».

Ожидаемый вывод:
(1, "два", 3.0)', 'fn main() {
    // ваш код
}
', 'Кортеж нельзя печатать через {} — нужен {:?}.', '{"driver": "", "expected": ["(1, \"два\", 3.0)"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-array-sum', 3, 'rust', 'Сумма массива', 'Объявите массив nums = [4, 8, 15, 16, 23, 42] и посчитайте сумму его элементов циклом for. Напечатайте «108».

Ожидаемый вывод:
108', 'fn main() {
    // ваш код
}
', 'Накопитель sum и цикл for x in nums.', '{"driver": "", "expected": ["108"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-array-len', 4, 'rust', 'Длина и элементы', 'Объявите массив из пяти нулей с помощью [0; 5], затем запишите в a[2] число 7. Напечатайте длину и сам массив в формате {:?}: «5» и «[0, 0, 7, 0, 0]».

Ожидаемый вывод:
5
[0, 0, 7, 0, 0]', 'fn main() {
    // ваш код
}
', 'Массив надо объявить как let mut a, чтобы присвоить элемент.', '{"driver": "", "expected": ["5", "[0, 0, 7, 0, 0]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-array-first-last', 5, 'rust', 'Первый и последний', 'Для массива [3, 6, 9, 12, 15] напечатайте первый и последний элементы через индексы (длина — len()). «3» и «15».

Ожидаемый вывод:
3
15', 'fn main() {
    // ваш код
}
', 'Последний индекс — a.len() - 1.', '{"driver": "", "expected": ["3", "15"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-array-get', 6, 'rust', 'Безопасный индекс', 'Для массива [10, 20, 30] напечатайте a.get(1) и a.get(7) в формате {:?}: «Some(20)» и «None».

Ожидаемый вывод:
Some(20)
None', 'fn main() {
    // ваш код
}
', 'get возвращает Option.', '{"driver": "", "expected": ["Some(20)", "None"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-slice-print', 7, 'rust', 'Срезы', 'Дан массив a = [1, 2, 3, 4, 5, 6]. Напечатайте срезы &a[1..4] и &a[..2] и &a[4..] через {:?}: «[2, 3, 4]», «[1, 2]», «[5, 6]».

Ожидаемый вывод:
[2, 3, 4]
[1, 2]
[5, 6]', 'fn main() {
    // ваш код
}
', 'Правая граница не входит.', '{"driver": "", "expected": ["[2, 3, 4]", "[1, 2]", "[5, 6]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-vec-push', 8, 'rust', 'Растим вектор', 'Создайте пустой вектор v: Vec<i32> и добавьте в цикле for числа 1…5 методом push. Напечатайте вектор через {:?}: «[1, 2, 3, 4, 5]» и его длину «5».

Ожидаемый вывод:
[1, 2, 3, 4, 5]
5', 'fn main() {
    // ваш код
}
', 'Vec::new() и v.push(i).', '{"driver": "", "expected": ["[1, 2, 3, 4, 5]", "5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-vec-pop', 9, 'rust', 'pop', 'Из вектора vec![1, 2, 3] удалите последний элемент методом pop и напечатайте его («Some(3)»), затем оставшийся вектор («[1, 2]»).

Ожидаемый вывод:
Some(3)
[1, 2]', 'fn main() {
    // ваш код
}
', 'pop возвращает Option.', '{"driver": "", "expected": ["Some(3)", "[1, 2]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-vec-evens', 10, 'rust', 'Чётные в вектор', 'Создайте вектор чётных чисел от 2 до 20 (цикл и push). Напечатайте вектор: «[2, 4, 6, 8, 10, 12, 14, 16, 18, 20]».

Ожидаемый вывод:
[2, 4, 6, 8, 10, 12, 14, 16, 18, 20]', 'fn main() {
    // ваш код
}
', 'Условие i % 2 == 0 внутри цикла.', '{"driver": "", "expected": ["[2, 4, 6, 8, 10, 12, 14, 16, 18, 20]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-vec-insert-remove', 11, 'rust', 'insert и remove', 'Начните с v = [1, 2, 3, 4]. Вставьте 99 на позицию 1 (insert), затем удалите элемент с индексом 3 (remove). Напечатайте результат «[1, 99, 2, 4]».

Ожидаемый вывод:
[1, 99, 2, 4]', 'fn main() {
    // ваш код
}
', 'После insert вектор [1, 99, 2, 3, 4]; remove(3) убирает тройку.', '{"driver": "", "expected": ["[1, 99, 2, 4]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-vec-iter-sum', 12, 'rust', 'Сумма и среднее', 'Для v = [3, 7, 2, 9, 4] напечатайте через iter(): сумму «25» и среднее арифметическое «5» (сумма / длина, целое деление; тип i32).

Ожидаемый вывод:
25
5', 'fn main() {
    // ваш код
}
', 'v.iter().sum() и приведение длины к i32.', '{"driver": "", "expected": ["25", "5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-vec-max-min', 13, 'rust', 'Наибольшее и наименьшее', 'Для v = [12, -5, 33, 0, 8] найдите максимум и минимум (iter().max(), iter().min() + unwrap): «33» и «-5».

Ожидаемый вывод:
33
-5', 'fn main() {
    // ваш код
}
', 'max() и min() возвращают Option.', '{"driver": "", "expected": ["33", "-5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-vec-mut-loop', 14, 'rust', 'Удвоить все', 'Удвойте каждый элемент вектора [1, 2, 3, 4] циклом for x in &mut v (*x *= 2). Напечатайте «[2, 4, 6, 8]».

Ожидаемый вывод:
[2, 4, 6, 8]', 'fn main() {
    // ваш код
}
', 'Звёздочка нужна, чтобы изменить само значение.', '{"driver": "", "expected": ["[2, 4, 6, 8]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-vec-sort', 15, 'rust', 'Сортировка', 'Отсортируйте вектор [5, 2, 9, 1, 7] по возрастанию и напечатайте «[1, 2, 5, 7, 9]», затем разверните (reverse) и напечатайте «[9, 7, 5, 2, 1]».

Ожидаемый вывод:
[1, 2, 5, 7, 9]
[9, 7, 5, 2, 1]', 'fn main() {
    // ваш код
}
', 'sort() и reverse() меняют вектор на месте.', '{"driver": "", "expected": ["[1, 2, 5, 7, 9]", "[9, 7, 5, 2, 1]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-vec-contains', 16, 'rust', 'Есть ли значение', 'Для v = [10, 20, 30, 40] напечатайте v.contains(&30) и v.contains(&35): «true» и «false».

Ожидаемый вывод:
true
false', 'fn main() {
    // ваш код
}
', 'contains принимает ссылку на значение.', '{"driver": "", "expected": ["true", "false"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-vec-dedup', 17, 'rust', 'Убрать повторы', 'Отсортируйте вектор [3, 1, 3, 2, 1, 2, 3] и уберите повторы методом dedup. Результат «[1, 2, 3]».

Ожидаемый вывод:
[1, 2, 3]', 'fn main() {
    // ваш код
}
', 'dedup убирает соседние дубликаты — поэтому сначала sort.', '{"driver": "", "expected": ["[1, 2, 3]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-vec-enumerate', 18, 'rust', 'Индексы и значения', 'Для v = ["a", "b", "c"] напечатайте по строке «0: a», «1: b», «2: c» (enumerate).

Ожидаемый вывод:
0: a
1: b
2: c', 'fn main() {
    // ваш код
}
', 'for (i, x) in v.iter().enumerate()', '{"driver": "", "expected": ["0: a", "1: b", "2: c"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-vec-filter-collect', 19, 'rust', 'Фильтр', 'Из вектора [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] соберите в новый вектор только числа, кратные 3 (filter + collect). «[3, 6, 9]».

Ожидаемый вывод:
[3, 6, 9]', 'fn main() {
    // ваш код
}
', 'v.iter().filter(|x| **x % 3 == 0).cloned().collect()', '{"driver": "", "expected": ["[3, 6, 9]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-vec-map-collect', 20, 'rust', 'Квадраты', 'Постройте вектор квадратов чисел 1…6 (map и collect): «[1, 4, 9, 16, 25, 36]».

Ожидаемый вывод:
[1, 4, 9, 16, 25, 36]', 'fn main() {
    // ваш код
}
', '(1..=6).map(|x| x * x).collect()', '{"driver": "", "expected": ["[1, 4, 9, 16, 25, 36]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-grid-print', 21, 'rust', 'Сетка 3×3', 'Объявите двумерный массив grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]] и напечатайте его построчно: три строки «1 2 3», «4 5 6», «7 8 9».

Ожидаемый вывод:
1 2 3
4 5 6
7 8 9', 'fn main() {
    // ваш код
}
', 'Каждую строку превратите в Vec<String> и склейте через join(" ").', '{"driver": "", "expected": ["1 2 3", "4 5 6", "7 8 9"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-grid-diag', 22, 'rust', 'Диагональ', 'Для той же сетки grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]] посчитайте сумму главной диагонали (элементы grid[i][i]): «15».

Ожидаемый вывод:
15', 'fn main() {
    // ваш код
}
', 'Цикл по i и grid[i][i].', '{"driver": "", "expected": ["15"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-fn-sum-slice', 23, 'rust', 'Сумма среза', 'Напишите функцию sum(v: &[i32]) -> i32, возвращающую сумму элементов среза.', 'fn sum(v: &[i32]) -> i32 {
    todo!()
}
', 'Срез принимает массив, вектор и часть вектора.', '{"driver": "fn main() {\n    let arr = [1, 2, 3];\n    let vec = vec![10, 20, 30, 40];\n    println!(\"{}\", sum(&arr));\n    println!(\"{}\", sum(&vec));\n    println!(\"{}\", sum(&vec[1..3]));\n    println!(\"{}\", sum(&[]));\n}\n", "expected": ["6", "100", "50", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-fn-max', 24, 'rust', 'Максимум среза', 'Напишите функцию largest(v: &[i32]) -> i32, возвращающую наибольший элемент (срез не пуст).', 'fn largest(v: &[i32]) -> i32 {
    todo!()
}
', 'Начните с v[0] и сравнивайте со всеми.', '{"driver": "fn main() {\n    println!(\"{}\", largest(&[3, 9, 2]));\n    println!(\"{}\", largest(&[-5, -2, -9]));\n    println!(\"{}\", largest(&[7]));\n}\n", "expected": ["9", "-2", "7"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-fn-reverse', 25, 'rust', 'Развернуть вектор', 'Напишите функцию reversed(v: &[i32]) -> Vec<i32>, возвращающую новый вектор с элементами в обратном порядке (исходный не менять).', 'fn reversed(v: &[i32]) -> Vec<i32> {
    todo!()
}
', 'v.to_vec() делает копию, которую можно изменить.', '{"driver": "fn main() {\n    let a = vec![1, 2, 3, 4];\n    println!(\"{:?}\", reversed(&a));\n    println!(\"{:?}\", a);\n    println!(\"{:?}\", reversed(&[]));\n}\n", "expected": ["[4, 3, 2, 1]", "[1, 2, 3, 4]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-fn-count-even', 26, 'rust', 'Сколько чётных', 'Напишите функцию count_even(v: &[i32]) -> usize: число чётных элементов (включая 0 и отрицательные).', 'fn count_even(v: &[i32]) -> usize {
    todo!()
}
', 'x % 2 == 0 для ссылки x работает, как для числа.', '{"driver": "fn main() {\n    println!(\"{}\", count_even(&[1, 2, 3, 4, 5, 6]));\n    println!(\"{}\", count_even(&[-2, 0, 7]));\n    println!(\"{}\", count_even(&[]));\n}\n", "expected": ["3", "2", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-fn-minmax-tuple', 27, 'rust', 'Минимум и максимум парой', 'Напишите функцию min_max(v: &[i32]) -> (i32, i32): пара (наименьшее, наибольшее) для непустого среза.', 'fn min_max(v: &[i32]) -> (i32, i32) {
    todo!()
}
', 'Две переменные lo и hi и кортеж в конце.', '{"driver": "fn main() {\n    println!(\"{:?}\", min_max(&[4, -1, 9, 3]));\n    println!(\"{:?}\", min_max(&[5]));\n    println!(\"{:?}\", min_max(&[2, 2, 2]));\n}\n", "expected": ["(-1, 9)", "(5, 5)", "(2, 2)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-fn-dot', 28, 'rust', 'Скалярное произведение', 'Напишите функцию dot(a: &[i32], b: &[i32]) -> i32: сумма произведений соответствующих элементов (срезы одной длины).', 'fn dot(a: &[i32], b: &[i32]) -> i32 {
    todo!()
}
', 'Цикл по индексам от 0 до a.len().', '{"driver": "fn main() {\n    println!(\"{}\", dot(&[1, 2, 3], &[4, 5, 6]));\n    println!(\"{}\", dot(&[], &[]));\n    println!(\"{}\", dot(&[-1, 2], &[3, 4]));\n}\n", "expected": ["32", "0", "5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 7, 'r7-fix-mut-vec', 29, 'rust', 'Исправьте: вектор без mut', 'Программа не собирается: метод push меняет вектор, а он объявлен неизменяемым. Исправьте объявление; результат «[1, 2, 3, 4]».

Ожидаемый вывод:
[1, 2, 3, 4]', 'fn main() {
    let v = vec![1, 2, 3];
    v.push(4);
    println!("{:?}", v);
}
', 'Добавьте mut: let mut v.', '{"driver": "", "expected": ["[1, 2, 3, 4]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-struct-create', 0, 'rust', 'Первая структура', 'Объявите структуру Point с полями x и y типа i32. Создайте точку (3, -4) и напечатайте «x=3 y=-4».

Ожидаемый вывод:
x=3 y=-4', 'fn main() {
    // ваш код
}
', 'struct Point { x: i32, y: i32 }; Point { x: 3, y: -4 }.', '{"driver": "", "expected": ["x=3 y=-4"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-struct-mut', 1, 'rust', 'Меняем поле', 'Объявите структуру Counter { value: u32 }, создайте изменяемый экземпляр со значением 0 и трижды увеличьте value на 5. Напечатайте «15».

Ожидаемый вывод:
15', 'fn main() {
    // ваш код
}
', 'let mut c — иначе поле не изменить.', '{"driver": "", "expected": ["15"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-struct-debug', 2, 'rust', 'Печать через Debug', 'Структуре Book { title: &str, pages: u32 } добавьте #[derive(Debug)] и напечатайте экземпляр {:?} и красиво {:#?}. Для книги «Rust», 500 страниц: сначала «Book { title: "Rust", pages: 500 }», затем многострочный вид.

Ожидаемый вывод:
Book { title: "Rust", pages: 500 }
Book {
    title: "Rust",
    pages: 500,
}', 'fn main() {
    // ваш код
}
', '#[derive(Debug)] над структурой; поле-ссылка требует ''static: &''static str.', '{"driver": "", "expected": ["Book { title: \"Rust\", pages: 500 }", "Book {", "    title: \"Rust\",", "    pages: 500,", "}"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-struct-shorthand', 3, 'rust', 'Сокращённая инициализация', 'Напишите функцию make_user(name: &str, age: u32) -> User, где User { name: String, age: u32 }, используя сокращённую запись (name и age совпадают с полями; для name нужно name.to_string()). Напечатайте «Аня 30».

Ожидаемый вывод:
Аня 30', 'fn main() {
    // ваш код
}
', 'let name = name.to_string(); затем User { name, age }.', '{"driver": "", "expected": ["Аня 30"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-struct-update', 4, 'rust', 'Обновление структуры', 'Config { width, height, title: &''static str }. Создайте base (800, 600, "окно"), затем big — копия с width = 1920 через ..base. Напечатайте «1920x600 окно».

Ожидаемый вывод:
1920x600 окно', 'fn main() {
    // ваш код
}
', 'Config { width: 1920, ..base }', '{"driver": "", "expected": ["1920x600 окно"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-impl-area', 5, 'rust', 'Метод area', 'Для структуры Rect { w: u32, h: u32 } напишите методы area(&self) -> u32 (площадь) и perimeter(&self) -> u32 (периметр).', 'struct Rect {
    w: u32,
    h: u32,
}

impl Rect {
    fn area(&self) -> u32 {
        todo!()
    }
    fn perimeter(&self) -> u32 {
        todo!()
    }
}
', 'self.w * self.h; 2 * (self.w + self.h)', '{"driver": "fn main() {\n    let r = Rect { w: 3, h: 5 };\n    println!(\"{} {}\", r.area(), r.perimeter());\n    let s = Rect { w: 10, h: 10 };\n    println!(\"{} {}\", s.area(), s.perimeter());\n}\n", "expected": ["15 16", "100 40"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-impl-new', 6, 'rust', 'Конструктор new', 'Добавьте структуре Circle { r: f64 } ассоциированную функцию new(r: f64) -> Circle и метод area(&self) -> f64 (π ≈ 3.14159).', 'struct Circle {
    r: f64,
}

impl Circle {
    fn new(r: f64) -> Circle {
        todo!()
    }
    fn area(&self) -> f64 {
        todo!()
    }
}
', 'Circle::new(r) — функция без self.', '{"driver": "fn main() {\n    let c = Circle::new(2.0);\n    println!(\"{:.3}\", c.area());\n    println!(\"{:.1}\", Circle::new(1.0).area());\n}\n", "expected": ["12.566", "3.1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-impl-mut-self', 7, 'rust', 'Счётчик с методами', 'Структуре Counter { n: u32 } добавьте методы new() -> Counter (n = 0), inc(&mut self), add(&mut self, k: u32) и get(&self) -> u32.', 'struct Counter {
    n: u32,
}

impl Counter {
    fn new() -> Counter {
        todo!()
    }
    fn inc(&mut self) {
        todo!()
    }
    fn add(&mut self, k: u32) {
        todo!()
    }
    fn get(&self) -> u32 {
        todo!()
    }
}
', '&mut self позволяет менять self.n.', '{"driver": "fn main() {\n    let mut c = Counter::new();\n    c.inc();\n    c.inc();\n    c.add(10);\n    println!(\"{}\", c.get());\n}\n", "expected": ["12"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-bank-account', 8, 'rust', 'Банковский счёт', 'Реализуйте Account { balance: i64 }: new(), deposit(&mut self, x: i64), withdraw(&mut self, x: i64) -> bool (false и без изменений, если средств не хватает; true и списание — иначе), balance(&self) -> i64.', 'struct Account {
    balance: i64,
}

impl Account {
    fn new() -> Account {
        todo!()
    }
    fn deposit(&mut self, x: i64) {
        todo!()
    }
    fn withdraw(&mut self, x: i64) -> bool {
        todo!()
    }
    fn balance(&self) -> i64 {
        todo!()
    }
}
', 'Проверка баланса внутри withdraw, возвращаем bool.', '{"driver": "fn main() {\n    let mut a = Account::new();\n    a.deposit(100);\n    println!(\"{}\", a.withdraw(30));\n    println!(\"{}\", a.withdraw(100));\n    println!(\"{}\", a.balance());\n}\n", "expected": ["true", "false", "70"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-point-distance', 9, 'rust', 'Расстояние между точками', 'У структуры Point { x: f64, y: f64 } напишите метод dist(&self, other: &Point) -> f64 — евклидово расстояние.', 'struct Point {
    x: f64,
    y: f64,
}

impl Point {
    fn dist(&self, other: &Point) -> f64 {
        todo!()
    }
}
', 'other передаётся ссылкой: a.dist(&b).', '{"driver": "fn main() {\n    let a = Point { x: 0.0, y: 0.0 };\n    let b = Point { x: 3.0, y: 4.0 };\n    println!(\"{}\", a.dist(&b));\n    println!(\"{}\", b.dist(&a));\n    println!(\"{}\", a.dist(&a));\n}\n", "expected": ["5", "5", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-tuple-struct', 10, 'rust', 'Кортежная структура', 'Объявите структуру Meters(f64) и функцию to_feet(m: Meters) -> f64: перевод метров в футы (1 м = 3.28084 фута).', 'struct Meters(f64);

fn to_feet(m: Meters) -> f64 {
    todo!()
}
', 'Доступ к полю кортежной структуры — m.0.', '{"driver": "fn main() {\n    println!(\"{:.3}\", to_feet(Meters(10.0)));\n    println!(\"{:.3}\", to_feet(Meters(0.5)));\n}\n", "expected": ["32.808", "1.640"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-color-struct', 11, 'rust', 'Цвет и яркость', 'Структура Color(u8, u8, u8) — RGB. Напишите функцию brightness(c: &Color) -> u32: среднее трёх компонент (целое деление на 3).', 'struct Color(u8, u8, u8);

fn brightness(c: &Color) -> u32 {
    todo!()
}
', 'Сложите как u32, иначе u8 переполнится.', '{"driver": "fn main() {\n    println!(\"{}\", brightness(&Color(255, 0, 0)));\n    println!(\"{}\", brightness(&Color(255, 255, 255)));\n    println!(\"{}\", brightness(&Color(10, 20, 31)));\n}\n", "expected": ["85", "255", "20"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-enum-basic', 12, 'rust', 'Направления', 'Enum Direction { Up, Down, Left, Right } и функция opposite(d: Direction) -> Direction, возвращающая противоположное направление. Для вывода добавьте derive(Debug).', '#[derive(Debug)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

fn opposite(d: Direction) -> Direction {
    todo!()
}
', 'match по четырём вариантам.', '{"driver": "fn main() {\n    println!(\"{:?}\", opposite(Direction::Up));\n    println!(\"{:?}\", opposite(Direction::Left));\n    println!(\"{:?}\", opposite(Direction::Right));\n}\n", "expected": ["Down", "Right", "Left"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-enum-coin', 13, 'rust', 'Монеты', 'Enum Coin { Penny, Nickel, Dime, Quarter } и функция value(c: &Coin) -> u32 в центах: 1, 5, 10, 25.', 'enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter,
}

fn value(c: &Coin) -> u32 {
    todo!()
}
', 'match c { Coin::Penny => 1, … }', '{"driver": "fn main() {\n    let coins = [Coin::Quarter, Coin::Dime, Coin::Penny, Coin::Penny];\n    let mut total = 0;\n    for c in &coins {\n        total += value(c);\n    }\n    println!(\"{}\", total);\n}\n", "expected": ["37"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-enum-shape', 14, 'rust', 'Фигуры', 'Enum Shape { Circle(f64), Rect(f64, f64), Square(f64) } и функция area(s: &Shape) -> f64 (π ≈ 3.14159).', 'enum Shape {
    Circle(f64),
    Rect(f64, f64),
    Square(f64),
}

fn area(s: &Shape) -> f64 {
    todo!()
}
', 'В образце сразу достаём данные: Shape::Rect(w, h).', '{"driver": "fn main() {\n    println!(\"{:.3}\", area(&Shape::Circle(2.0)));\n    println!(\"{}\", area(&Shape::Rect(3.0, 4.5)));\n    println!(\"{}\", area(&Shape::Square(5.0)));\n}\n", "expected": ["12.566", "13.5", "25"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-enum-method', 15, 'rust', 'Метод у enum', 'Enum Light { Red, Yellow, Green } с методом next(&self) -> Light: цикл Red → Green → Yellow → Red. Derive(Debug).', '#[derive(Debug)]
enum Light {
    Red,
    Yellow,
    Green,
}

impl Light {
    fn next(&self) -> Light {
        todo!()
    }
}
', 'Методы у enum пишутся в impl, как у struct.', '{"driver": "fn main() {\n    let mut l = Light::Red;\n    for _ in 0..4 {\n        print!(\"{:?} \", l);\n        l = l.next();\n    }\n    println!();\n}\n", "expected": ["Red Green Yellow Red"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-option-find', 16, 'rust', 'Поиск с Option', 'Напишите функцию find(v: &[i32], x: i32) -> Option<usize>: индекс первого вхождения x или None.', 'fn find(v: &[i32], x: i32) -> Option<usize> {
    todo!()
}
', 'return Some(i) внутри цикла, в конце None.', '{"driver": "fn main() {\n    println!(\"{:?}\", find(&[5, 7, 9, 7], 7));\n    println!(\"{:?}\", find(&[5, 7, 9], 4));\n    println!(\"{:?}\", find(&[], 1));\n}\n", "expected": ["Some(1)", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-option-divide', 17, 'rust', 'Безопасное деление', 'Напишите функцию safe_div(a: i32, b: i32) -> Option<i32>: None при b == 0, иначе частное.', 'fn safe_div(a: i32, b: i32) -> Option<i32> {
    todo!()
}
', 'Ветки if возвращают None и Some(…).', '{"driver": "fn main() {\n    println!(\"{:?}\", safe_div(10, 2));\n    println!(\"{:?}\", safe_div(7, 0));\n    println!(\"{:?}\", safe_div(-9, 3));\n}\n", "expected": ["Some(5)", "None", "Some(-3)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-option-unwrap-or', 18, 'rust', 'unwrap_or', 'Напишите функцию first_or(v: &[i32], default: i32) -> i32: первый элемент или default, если срез пуст. Используйте v.first() и unwrap_or.', 'fn first_or(v: &[i32], default: i32) -> i32 {
    todo!()
}
', 'v.first() даёт Option<&i32>; unwrap_or(&default), затем звёздочка.', '{"driver": "fn main() {\n    println!(\"{}\", first_or(&[4, 5], 0));\n    println!(\"{}\", first_or(&[], -1));\n}\n", "expected": ["4", "-1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-option-match', 19, 'rust', 'match по Option', 'Напишите функцию describe(x: Option<i32>) -> String: «нет значения» для None, «ноль» для Some(0), «число N» (N — значение) иначе.', 'fn describe(x: Option<i32>) -> String {
    todo!()
}
', 'Образец Some(0) — до общего Some(n).', '{"driver": "fn main() {\n    println!(\"{}\", describe(None));\n    println!(\"{}\", describe(Some(0)));\n    println!(\"{}\", describe(Some(42)));\n}\n", "expected": ["нет значения", "ноль", "число 42"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-if-let', 20, 'rust', 'if let', 'Напишите функцию print_first(v: &[&str]): если срез не пуст — печатает «первый: …», иначе «пусто». Используйте if let Some(x) = v.first().', 'fn print_first(v: &[&str]) {
    todo!()
}
', 'if let Some(x) = … { } else { }', '{"driver": "fn main() {\n    print_first(&[\"a\", \"b\"]);\n    print_first(&[]);\n}\n", "expected": ["первый: a", "пусто"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-result-parse', 21, 'rust', 'Result из parse', 'Напишите функцию to_num(s: &str) -> Result<i32, String>: Ok(число), если строка — целое, иначе Err("не число: <s>").', 'fn to_num(s: &str) -> Result<i32, String> {
    todo!()
}
', 'match s.parse::<i32>() { Ok(n) => …, Err(_) => … }', '{"driver": "fn main() {\n    println!(\"{:?}\", to_num(\"42\"));\n    println!(\"{:?}\", to_num(\"abc\"));\n    println!(\"{:?}\", to_num(\"-7\"));\n}\n", "expected": ["Ok(42)", "Err(\"не число: abc\")", "Ok(-7)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-result-div', 22, 'rust', 'Деление с ошибкой', 'Напишите функцию divide(a: f64, b: f64) -> Result<f64, String>: Err("деление на ноль"), если b == 0.0, иначе Ok(частное).', 'fn divide(a: f64, b: f64) -> Result<f64, String> {
    todo!()
}
', 'Err(String::from("…")) и Ok(a / b)', '{"driver": "fn main() {\n    println!(\"{:?}\", divide(1.0, 4.0));\n    println!(\"{:?}\", divide(5.0, 0.0));\n}\n", "expected": ["Ok(0.25)", "Err(\"деление на ноль\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-struct-vec', 23, 'rust', 'Вектор структур', 'Структура Student { name: String, grade: u32 }. Напишите функцию best(students: &[Student]) -> &str: имя студента с максимальной оценкой (первого из лучших). Список не пуст.', 'struct Student {
    name: String,
    grade: u32,
}

fn best(students: &[Student]) -> &str {
    todo!()
}
', 'Храните ссылку top на лучшего студента.', '{"driver": "fn main() {\n    let list = vec![\n        Student { name: String::from(\"Аня\"), grade: 4 },\n        Student { name: String::from(\"Боря\"), grade: 5 },\n        Student { name: String::from(\"Вера\"), grade: 5 },\n    ];\n    println!(\"{}\", best(&list));\n}\n", "expected": ["Боря"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-inventory', 24, 'rust', 'Склад', 'Структура Item { name: String, qty: u32 }. Функция total(items: &[Item]) -> u32 — суммарное количество, и функция find_qty(items: &[Item], name: &str) -> Option<u32>.', 'struct Item {
    name: String,
    qty: u32,
}

fn total(items: &[Item]) -> u32 {
    todo!()
}

fn find_qty(items: &[Item], name: &str) -> Option<u32> {
    todo!()
}
', 'it.name == name — сравнение String и &str работает.', '{"driver": "fn main() {\n    let items = vec![\n        Item { name: String::from(\"гвозди\"), qty: 120 },\n        Item { name: String::from(\"болты\"), qty: 45 },\n    ];\n    println!(\"{}\", total(&items));\n    println!(\"{:?}\", find_qty(&items, \"болты\"));\n    println!(\"{:?}\", find_qty(&items, \"гайки\"));\n}\n", "expected": ["165", "Some(45)", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-traffic-fsm', 25, 'rust', 'Автомат статусов заказа', 'Enum Status { New, Paid, Shipped, Done }. Метод advance(&self) -> Status переводит в следующий статус (Done остаётся Done), а is_final(&self) -> bool истинен только для Done. Derive(Debug).', '#[derive(Debug)]
enum Status {
    New,
    Paid,
    Shipped,
    Done,
}

impl Status {
    fn advance(&self) -> Status {
        todo!()
    }
    fn is_final(&self) -> bool {
        todo!()
    }
}
', 'matches!(self, Status::Done) — короткая проверка варианта.', '{"driver": "fn main() {\n    let mut s = Status::New;\n    while !s.is_final() {\n        print!(\"{:?} \", s);\n        s = s.advance();\n    }\n    println!(\"{:?}\", s);\n}\n", "expected": ["New Paid Shipped Done"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-fix-mut-struct', 26, 'rust', 'Исправьте: структура без mut', 'Программа не собирается: поле меняется у неизменяемой структуры. Исправьте объявление; результат «11».

Ожидаемый вывод:
11', 'struct S {
    n: i32,
}

fn main() {
    let s = S { n: 10 };
    s.n += 1;
    println!("{}", s.n);
}
', 'Добавьте mut к переменной s.', '{"driver": "", "expected": ["11"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-fix-missing-variant', 27, 'rust', 'Исправьте: match без всех вариантов', 'match не покрывает вариант Blue. Допишите ветку так, чтобы вывод был «синий» для Color::Blue.

Ожидаемый вывод:
синий', 'enum Color {
    Red,
    Green,
    Blue,
}

fn name(c: Color) -> &''static str {
    match c {
        Color::Red => "красный",
        Color::Green => "зелёный",
    }
}

fn main() {
    println!("{}", name(Color::Blue));
}
', 'Добавьте Color::Blue => "синий",', '{"driver": "", "expected": ["синий"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-fix-self', 28, 'rust', 'Исправьте: метод без &mut self', 'Метод inc должен менять поле, но объявлен с &self. Исправьте сигнатуру; результат «2».

Ожидаемый вывод:
2', 'struct C {
    n: u32,
}

impl C {
    fn inc(&self) {
        self.n += 1;
    }
}

fn main() {
    let mut c = C { n: 1 };
    c.inc();
    println!("{}", c.n);
}
', 'Замените &self на &mut self.', '{"driver": "", "expected": ["2"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 8, 'r8-vec-of-enum', 29, 'rust', 'Список покупок', 'Enum Item { Apple(u32), Milk(f64) } (число яблок и литры молока). Функция describe(items: &[Item]) -> String: для каждого элемента «N яблок» или «X л молока», через «; ».', 'enum Item {
    Apple(u32),
    Milk(f64),
}

fn describe(items: &[Item]) -> String {
    todo!()
}
', 'Соберите строки в Vec<String> и склейте join("; ").', '{"driver": "fn main() {\n    println!(\"{}\", describe(&[Item::Apple(3), Item::Milk(1.5)]));\n    println!(\"{}\", describe(&[]));\n    println!(\"{}\", describe(&[Item::Milk(2.0)]));\n}\n", "expected": ["3 яблок; 1.5 л молока", "", "2 л молока"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-shadowing', 0, 'rust', 'Затенение: смена типа под тем же именем', 'Напишите fn double_text(input: &str) -> i32: обрежьте пробелы по краям (trim), разберите число (parse) и верните его, умноженное на 2. Используйте затенение: три раза let input = ... с одним именем, тип меняется с &str на i32. Ввод всегда корректен (можно unwrap).', 'fn double_text(input: &str) -> i32 {
    todo!()
}
', 'let input: i32 = input.parse().unwrap(); — справа ещё старая &str, слева уже новая i32.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\"let in\", \"put = \")).count();\n    for s in [\"21\", \"  -4 \", \"\\t100\\n\"] {\n        println!(\"{}\", double_text(s));\n    }\n    println!(\"shadow lets: {}\", bad0 >= 2);\n}\n", "expected": ["42", "-8", "200", "shadow lets: true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-overflow-modes', 1, 'rust', 'Переполнение: четыре способа', 'Напишите fn add_modes(a: u8, b: u8) -> (u8, Option<u8>, u8, (u8, bool)): результат сложения по четырём правилам — с заворачиванием (wrapping), с проверкой (checked: None при переполнении), с насыщением (saturating) и overflowing (значение и флаг). Питон переполнения не знает, а процессор — знает.', 'fn add_modes(a: u8, b: u8) -> (u8, Option<u8>, u8, (u8, bool)) {
    todo!()
}
', 'У целых есть методы wrapping_add, checked_add, saturating_add, overflowing_add.', '{"driver": "fn main() {\n    for (a, b) in [(1, 2), (200, 55), (200, 56), (255, 255)] {\n        println!(\"{a}+{b}: {:?}\", add_modes(a, b));\n    }\n}\n", "expected": ["1+2: (3, Some(3), 3, (3, false))", "200+55: (255, Some(255), 255, (255, false))", "200+56: (0, None, 255, (0, true))", "255+255: (254, None, 255, (254, true))"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-casts', 2, 'rust', 'Приведение as: отрезать биты', 'Напишите fn casts(x: i32) -> (u8, i8, u16, f64): значение x, приведённое as к u8, i8 и u16, и x как f64, делённое на 2. Посмотрите, как as отрезает старшие биты (дополнительный код из главы про числа) — исключений нет.', 'fn casts(x: i32) -> (u8, i8, u16, f64) {
    todo!()
}
', 'x as u8 берёт младшие 8 бит; x as i8 трактует их как число со знаком.', '{"driver": "fn main() {\n    for x in [65, 300, -1, 70000, -129] {\n        println!(\"{x}: {:?}\", casts(x));\n    }\n    println!(\"{}\", 3.99_f64 as i32);\n    println!(\"{}\", (-1.5_f64) as u8);\n    println!(\"{}\", 300.0_f64 as u8);\n    println!(\"{}\", 65u8 as char);\n}\n", "expected": ["65: (65, 65, 65, 32.5)", "300: (44, 44, 300, 150.0)", "-1: (255, -1, 65535, -0.5)", "70000: (112, 112, 4464, 35000.0)", "-129: (127, 127, 65407, -64.5)", "3", "0", "255", "A"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-popcount', 3, 'rust', 'Подсчёт единиц руками', 'Напишите fn popcount(mut n: u32) -> u32 — число единичных битов — циклом со сдвигом и маской (n & 1, n >> 1). Метод count_ones использовать нельзя: проверка ищет его в вашем коде.', 'fn popcount(mut n: u32) -> u32 {
    todo!()
}
', 'while n != 0 { count += n & 1; n >>= 1; } — сдвиг вправо отбрасывает младший бит.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\"count\", \"_ones\")).count();\n    for n in [0u32, 1, 7, 255, 1 << 31, u32::MAX, 0b1010_1010] {\n        println!(\"{n:#b}: {}\", popcount(n));\n    }\n    println!(\"builtin used: {}\", bad0);\n}\n", "expected": ["0b0: 0", "0b1: 1", "0b111: 3", "0b11111111: 8", "0b10000000000000000000000000000000: 1", "0b11111111111111111111111111111111: 32", "0b10101010: 4", "builtin used: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-pydivmod', 4, 'rust', 'Деление как в Python', 'Напишите fn py_divmod(a: i32, b: i32) -> (i32, i32): целое деление и остаток по правилам питона (a // b, a % b): частное округляется вниз, остаток имеет знак делителя. Раст по умолчанию округляет к нулю, а остаток берёт знак делимого.', 'fn py_divmod(a: i32, b: i32) -> (i32, i32) {
    todo!()
}
', 'Если остаток не нулевой и его знак не совпадает со знаком b, уменьшите частное на 1 и добавьте b к остатку.', '{"driver": "fn main() {\n    for (a, b) in [(7, 2), (-7, 2), (7, -2), (-7, -2), (6, 3), (-6, 3), (0, 5)] {\n        println!(\"{a} // {b} = {:?}\", py_divmod(a, b));\n    }\n}\n", "expected": ["7 // 2 = (3, 1)", "-7 // 2 = (-4, 1)", "7 // -2 = (-4, -1)", "-7 // -2 = (3, -1)", "6 // 3 = (2, 0)", "-6 // 3 = (-2, 0)", "0 // 5 = (0, 0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-float-eq', 5, 'rust', 'Сравнение дробных с допуском', 'Напишите fn approx_eq(a: f64, b: f64) -> bool: числа равны, если |a − b| не больше 1e-9 · max(1, |a|, |b|). Точное сравнение 0.1 + 0.2 == 0.3 ложно в любом языке — вспомните главу про числа.', 'fn approx_eq(a: f64, b: f64) -> bool {
    todo!()
}
', 'У f64 есть методы abs() и max(): (a - b).abs() <= 1e-9 * масштаб.', '{"driver": "fn main() {\n    println!(\"{} {}\", 0.1 + 0.2 == 0.3, approx_eq(0.1 + 0.2, 0.3));\n    let mut s = 0.0;\n    for _ in 0..10 {\n        s += 0.1;\n    }\n    println!(\"{} {}\", s == 1.0, approx_eq(s, 1.0));\n    println!(\"{} {}\", approx_eq(1e12, 1e12 + 1.0), approx_eq(1.0, 1.001));\n    println!(\"{} {}\", approx_eq(0.0, 1e-12), approx_eq(0.0, 1e-3));\n}\n", "expected": ["false true", "false true", "true false", "true false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-tuple-minmax', 6, 'rust', 'Кортеж как результат', 'Напишите fn min_max(a: i32, b: i32, c: i32) -> (i32, i32): наименьшее и наибольшее из трёх. Результат разбирается на части: let (lo, hi) = min_max(...).', 'fn min_max(a: i32, b: i32, c: i32) -> (i32, i32) {
    todo!()
}
', 'Методы min и max можно соединять цепочкой: a.min(b).min(c).', '{"driver": "fn main() {\n    for (a, b, c) in [(1, 2, 3), (9, -4, 5), (7, 7, 7), (-1, -9, -5)] {\n        let (lo, hi) = min_max(a, b, c);\n        println!(\"{lo} {hi}\");\n    }\n}\n", "expected": ["1 3", "-4 9", "7 7", "-9 -1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-array-reverse', 7, 'rust', 'Массив на стеке: копия, а не ссылка', 'Напишите fn reversed(a: [i32; 5]) -> [i32; 5] — новый массив в обратном порядке (индексы и цикл for). Массив известного размера копируется целиком: пройдите по ячейкам и убедитесь, что исходник не изменился.', 'fn reversed(a: [i32; 5]) -> [i32; 5] {
    todo!()
}
', 'let mut out = [0; 5]; — массив из пяти нулей; out[4 - i] = a[i].', '{"driver": "fn main() {\n    let a = [1, 2, 3, 4, 5];\n    let b = reversed(a);\n    println!(\"{:?} {:?}\", a, b);\n    println!(\"{:?}\", reversed([10, 0, -3, 8, 8]));\n}\n", "expected": ["[1, 2, 3, 4, 5] [5, 4, 3, 2, 1]", "[8, 8, -3, 0, 10]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-text-stats', 8, 'rust', 'Символы и байты', 'Напишите fn text_stats(s: &str) -> (usize, usize): (длина в байтах, число символов). В питоне len(s) считает символы; в расте len() — байты, а символы считают через chars().count().', 'fn text_stats(s: &str) -> (usize, usize) {
    todo!()
}
', 's.len() — байты, s.chars().count() — символы.', '{"driver": "fn main() {\n    for s in [\"hello\", \"привет\", \"日本語\", \"a😀b\", \"\"] {\n        println!(\"{:?} -> {:?}\", s, text_stats(s));\n    }\n}\n", "expected": ["\"hello\" -> (5, 5)", "\"привет\" -> (12, 6)", "\"日本語\" -> (9, 3)", "\"a😀b\" -> (6, 3)", "\"\" -> (0, 0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-utf8-hex', 9, 'rust', 'Байты UTF-8 в шестнадцатеричном виде', 'Напишите fn hex_bytes(s: &str) -> String: байты строки в UTF-8, каждый как две шестнадцатеричные цифры, через пробел. Сверьтесь с главой про символы: «Ж» — d0 96.', 'fn hex_bytes(s: &str) -> String {
    todo!()
}
', 's.bytes() даёт u8; format!("{b:02x}") — две hex-цифры; join(" ") склеивает.', '{"driver": "fn main() {\n    for s in [\"A\", \"Ж\", \"€\", \"привет\", \"😀\"] {\n        println!(\"{s}: {}\", hex_bytes(s));\n    }\n}\n", "expected": ["A: 41", "Ж: d0 96", "€: e2 82 ac", "привет: d0 bf d1 80 d0 b8 d0 b2 d0 b5 d1 82", "😀: f0 9f 98 80"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-endianness', 10, 'rust', 'Порядок байтов в числе', 'Напишите fn byte_orders(n: u32) -> (String, String): байты числа n в порядке little-endian и big-endian, в hex через пробел. Методы u32::to_le_bytes и to_be_bytes.', 'fn byte_orders(n: u32) -> (String, String) {
    todo!()
}
', 'to_le_bytes() возвращает [u8; 4] — массив на стеке; обойдите его итератором .iter().', '{"driver": "fn main() {\n    for n in [0x12345678u32, 1, 0xdeadbeef, 256] {\n        let (le, be) = byte_orders(n);\n        println!(\"{n:#x}: LE [{le}] BE [{be}]\");\n    }\n}\n", "expected": ["0x12345678: LE [78 56 34 12] BE [12 34 56 78]", "0x1: LE [01 00 00 00] BE [00 00 00 01]", "0xdeadbeef: LE [ef be ad de] BE [de ad be ef]", "0x100: LE [00 01 00 00] BE [00 00 01 00]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-twos-complement', 11, 'rust', 'Дополнительный код вручную', 'Напишите fn to_bits(n: i8) -> String (8 двоичных цифр дополнительного кода: приведите n as u8 и выведите {:08b}) и fn from_bits(bits: &str) -> i8 (разберите строку u8::from_str_radix(bits, 2) и приведите as i8).', 'fn to_bits(n: i8) -> String {
    todo!()
}

fn from_bits(bits: &str) -> i8 {
    todo!()
}
', 'as между целыми одной ширины ничего не вычисляет — меняет трактовку тех же восьми бит.', '{"driver": "fn main() {\n    for n in [5, -5, 0, 127, -128, -1] {\n        let b = to_bits(n);\n        println!(\"{n}: {b} -> {}\", from_bits(&b));\n    }\n}\n", "expected": ["5: 00000101 -> 5", "-5: 11111011 -> -5", "0: 00000000 -> 0", "127: 01111111 -> 127", "-128: 10000000 -> -128", "-1: 11111111 -> -1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-sizes', 12, 'rust', 'Размеры типов в памяти', 'Напишите fn sizes() -> Vec<(&''static str, usize)>: пары (имя типа, std::mem::size_of) для: u8, i32, u64, char, bool, (u8, u32), [u16; 5], &str, usize — именно в этом порядке. Обратите внимание на выравнивание кортежа и на то, что &str — это два слова (указатель и длина).', 'fn sizes() -> Vec<(&''static str, usize)> {
    todo!()
}
', 'size_of::<T>() — функция времени компиляции. Кортеж (u8, u32) занимает 8 байт: u32 выровнен по четырём.', '{"driver": "fn main() {\n    for (name, bytes) in sizes() {\n        println!(\"{name}: {bytes}\");\n    }\n}\n", "expected": ["u8: 1", "i32: 4", "u64: 8", "char: 4", "bool: 1", "(u8, u32): 8", "[u16; 5]: 10", "&str: 16", "usize: 8"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-stack-direction', 13, 'rust', 'Куда растёт стек', 'Драйвер вызывает вложенные функции и записывает адреса их локальных переменных в срез addrs (от внешнего вызова к внутреннему). Напишите fn grows_down(addrs: &[usize]) -> bool: true, если каждый следующий адрес строго меньше предыдущего (стек растёт к меньшим адресам, как в главе про процессор).', 'fn grows_down(addrs: &[usize]) -> bool {
    todo!()
}
', 'Срез &[usize] — вид на массив чисел: перебирайте индексы 1..addrs.len().', '{"driver": "#[inline(never)]\nfn level(depth: u32, out: &mut Vec<usize>) {\n    let marker = std::hint::black_box(depth);\n    out.push(&marker as *const u32 as usize);\n    if depth > 0 {\n        level(depth - 1, out);\n    }\n    std::hint::black_box(&marker);\n}\n\nfn main() {\n    let mut addrs = Vec::new();\n    level(5, &mut addrs);\n    println!(\"{} frames\", addrs.len());\n    println!(\"grows down: {}\", grows_down(&addrs));\n    println!(\"{}\", grows_down(&[10, 20, 30]));\n    println!(\"{}\", grows_down(&[30, 20, 10]));\n    println!(\"{}\", grows_down(&[5]));\n}\n", "expected": ["6 frames", "grows down: true", "false", "true", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-recursion-limit', 14, 'rust', 'Глубокая рекурсия против стека', 'Рекурсивная sum_to(n) строит кадр на каждый шаг и для n = 20 миллионов переполняет стек (в питоне это был бы RecursionError на тысяче). Перепишите sum_to циклом с тем же результатом.', 'fn sum_to(n: u64) -> u64 {
    if n == 0 {
        0
    } else {
        n + std::hint::black_box(sum_to(n - 1))
    }
}
', 'Каждый рекурсивный вызов — новый кадр на стеке; цикл использует один кадр.', '{"driver": "fn main() {\n    println!(\"{}\", sum_to(10));\n    println!(\"{}\", sum_to(20_000_000));\n}\n", "expected": ["55", "200000010000000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-calendar', 15, 'rust', 'Високосный год и дни в месяце', 'Напишите fn is_leap(year: u32) -> bool и fn days_in_month(year: u32, month: u32) -> u32 (match по номеру месяца, в феврале учитывайте високосность). Для месяца вне 1..=12 вызовите panic!("bad month") — паника как в питоне ValueError, но без перехвата.', 'fn is_leap(year: u32) -> bool {
    todo!()
}

fn days_in_month(year: u32, month: u32) -> u32 {
    todo!()
}
', 'Шаблон 1 | 3 | 5 объединяет несколько значений в одной ветке match.', '{"driver": "fn main() {\n    for y in [1900, 2000, 2023, 2024] {\n        println!(\"{y}: leap={} feb={}\", is_leap(y), days_in_month(y, 2));\n    }\n    let total: u32 = (1..=12).map(|m| days_in_month(2024, m)).sum();\n    println!(\"{total}\");\n}\n", "expected": ["1900: leap=false feb=28", "2000: leap=true feb=29", "2023: leap=false feb=28", "2024: leap=true feb=29", "366"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-gcd-lcm', 16, 'rust', 'НОД, НОК и защита от переполнения', 'Напишите fn gcd(a: u64, b: u64) -> u64 (алгоритм Евклида в цикле) и fn lcm(a: u64, b: u64) -> Option<u64>: наименьшее общее кратное или None, если результат не помещается в u64 (используйте checked_mul).', 'fn gcd(a: u64, b: u64) -> u64 {
    todo!()
}

fn lcm(a: u64, b: u64) -> Option<u64> {
    todo!()
}
', 'lcm = a / gcd * b; умножение проверяйте методом checked_mul — он вернёт None при переполнении.', '{"driver": "fn main() {\n    println!(\"{} {} {}\", gcd(12, 18), gcd(17, 5), gcd(0, 9));\n    println!(\"{:?} {:?}\", lcm(4, 6), lcm(0, 5));\n    println!(\"{:?}\", lcm(1 << 40, (1 << 40) + 1));\n    println!(\"{:?}\", lcm(u64::MAX, 2));\n}\n", "expected": ["6 1 9", "Some(12) Some(0)", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-to-base', 17, 'rust', 'Число в любой системе счисления', 'Напишите fn to_base(mut n: u32, base: u32) -> String: запись n в системе с основанием 2..=36, цифры 0-9 и a-z. Для 0 вернуть "0". Python: format(n, ''b'') и int(s, base); здесь вы пишете это сами (char::from_digit).', 'fn to_base(mut n: u32, base: u32) -> String {
    todo!()
}
', 'Остатки получаются от младшей цифры к старшей — соберите их в Vec и переверните rev().', '{"driver": "fn main() {\n    for (n, b) in [(0, 2), (5, 2), (255, 16), (255, 2), (123456, 36), (35, 36), (64, 8)] {\n        println!(\"{n} base {b}: {}\", to_base(n, b));\n    }\n}\n", "expected": ["0 base 2: 0", "5 base 2: 101", "255 base 16: ff", "255 base 2: 11111111", "123456 base 36: 2n9c", "35 base 36: z", "64 base 8: 100"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-getsizeof', 18, 'rust', 'Размеры вместо getsizeof', 'В Python sys.getsizeof(5) возвращает 28. Напечатайте через size_of размеры в байтах для i8, i16, i32, i64, i128, f32, f64, bool, char, (u8, u32), [i32; 10] — одной строкой через пробел: «1 2 4 8 16 4 8 1 4 8 40».

Ожидаемый вывод:
1 2 4 8 16 4 8 1 4 8 40', 'fn main() {
    // ваш код
}
', 'use std::mem::size_of; size_of::<T>().', '{"driver": "", "expected": ["1 2 4 8 16 4 8 1 4 8 40"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-div-modes', 19, 'rust', 'Четыре результата деления', 'Для a = -7 и b = 2 напечатайте четыре строки: a / b, a % b, a.div_euclid(b), a.rem_euclid(b). Ожидается «-3», «-1», «-4», «1» (в Python: -7 // 2 = -4 и -7 % 2 = 1).

Ожидаемый вывод:
-3
-1
-4
1', 'fn main() {
    // ваш код
}
', 'div_euclid и rem_euclid совпадают с питоновскими // и % при положительном делителе.', '{"driver": "", "expected": ["-3", "-1", "-4", "1"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-u128-factorial', 20, 'rust', 'Факториал 30 без bigint', 'В Python 30! считается без проблем. В Rust он помещается в u128. Посчитайте 30! циклом и напечатайте «265252859812191058636308480000000».

Ожидаемый вывод:
265252859812191058636308480000000', 'fn main() {
    // ваш код
}
', 'Тип u128: let mut f: u128 = 1;', '{"driver": "", "expected": ["265252859812191058636308480000000"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-fact-checked', 21, 'rust', 'Факториал с проверкой переполнения', 'Напишите функцию fact(n: u32) -> Option<u64>: n! или None, если результат не помещается в u64 (используйте checked_mul).', 'fn fact(n: u32) -> Option<u64> {
    todo!()
}
', 'checked_mul возвращает Option; оператор ? выходит из функции с None.', '{"driver": "fn main() {\n    println!(\"{:?}\", fact(5));\n    println!(\"{:?}\", fact(20));\n    println!(\"{:?}\", fact(21));\n    println!(\"{:?}\", fact(0));\n}\n", "expected": ["Some(120)", "Some(2432902008176640000)", "None", "Some(1)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-py-round', 22, 'rust', 'Округление как в Python', 'Напишите функцию py_round(x: f64) -> i64: округление к ближайшему целому, а половинки — к чётному (как round в Python: 0.5 → 0, 1.5 → 2, 2.5 → 2, −0.5 → 0, −1.5 → −2).', 'fn py_round(x: f64) -> i64 {
    todo!()
}
', 'x.round() округляет половинки от нуля; если результат нечётный, а x — ровно половинка, вернитесь на единицу к нулю.', '{"driver": "fn main() {\n    for x in [0.5, 1.5, 2.5, -0.5, -1.5, 2.4, 2.6, -2.5] {\n        print!(\"{} \", py_round(x));\n    }\n    println!();\n}\n", "expected": ["0 2 2 0 -2 2 3 -2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-py-index', 23, 'rust', 'Отрицательные индексы', 'Напишите функцию py_get(v: &[i32], i: i32) -> Option<i32>: как v[i] в Python — отрицательный индекс считается с конца, выход за границы даёт None.', 'fn py_get(v: &[i32], i: i32) -> Option<i32> {
    todo!()
}
', 'Приведите len к i32, прибавьте его к отрицательному индексу и проверьте границы.', '{"driver": "fn main() {\n    let v = [10, 20, 30];\n    println!(\"{:?}\", py_get(&v, 0));\n    println!(\"{:?}\", py_get(&v, -1));\n    println!(\"{:?}\", py_get(&v, -3));\n    println!(\"{:?}\", py_get(&v, 3));\n    println!(\"{:?}\", py_get(&v, -4));\n}\n", "expected": ["Some(10)", "Some(30)", "Some(10)", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-to-bytes', 24, 'rust', 'to_bytes вручную', 'Напишите функции to_le(n: u32) -> [u8; 4] и from_le(b: [u8; 4]) -> u32 без to_le_bytes — через сдвиги >> и << и маску 0xFF.', 'fn to_le(n: u32) -> [u8; 4] {
    todo!()
}

fn from_le(b: [u8; 4]) -> u32 {
    todo!()
}
', 'Младший байт — n & 0xFF; следующий — (n >> 8) & 0xFF.', '{"driver": "fn main() {\n    println!(\"{:?}\", to_le(258));\n    println!(\"{:?}\", to_le(0xDEADBEEF));\n    println!(\"{}\", from_le([2, 1, 0, 0]));\n    println!(\"{}\", from_le(to_le(123456789)));\n}\n", "expected": ["[2, 1, 0, 0]", "[239, 190, 173, 222]", "258", "123456789"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-struct-layout', 25, 'rust', 'Размер структуры', 'Объявите две структуры с атрибутом #[repr(C)]: A { a: u8, b: u32, c: u8 } и B { b: u32, a: u8, c: u8 }. Напечатайте size_of::<A>() и size_of::<B>(): «12» и «8» — из-за добивки между полями.

Ожидаемый вывод:
12
8', 'fn main() {
    // ваш код
}
', '#[repr(C)] фиксирует порядок полей; порядок влияет на размер.', '{"driver": "", "expected": ["12", "8"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-strings-len', 26, 'rust', 'len в байтах и в символах', 'Для слов «привет», «hello», «日本語», «😀» напечатайте по строке: слово, число байт и число символов через пробел: «привет 12 6», «hello 5 5», «日本語 9 3», «😀 4 1».

Ожидаемый вывод:
привет 12 6
hello 5 5
日本語 9 3
😀 4 1', 'fn main() {
    // ваш код
}
', 'len() — байты, chars().count() — символы.', '{"driver": "", "expected": ["привет 12 6", "hello 5 5", "日本語 9 3", "😀 4 1"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-copy-vs-clone', 27, 'rust', 'Копия строки', 'Создайте a = String::from("раст"), клон b = a.clone(), допишите к b строку "!" и напечатайте обе: «раст» и «раст!». В Python для этого пришлось бы вызывать copy.

Ожидаемый вывод:
раст
раст!', 'fn main() {
    // ваш код
}
', 'clone() делает полную копию, поэтому a остаётся цела.', '{"driver": "", "expected": ["раст", "раст!"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-bool-sum', 28, 'rust', 'bool — не число', 'В Python sum([True, False, True]) = 2. В Rust bool нельзя складывать. Посчитайте число true в векторе [true, false, true, true, false] двумя способами: фильтром (iter().filter(|b| **b).count()) и приведением (b as i32). Напечатайте две строки «3» и «3».

Ожидаемый вывод:
3
3', 'fn main() {
    // ваш код
}
', 'true as i32 == 1; *x разыменовывает ссылку.', '{"driver": "", "expected": ["3", "3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 9, 'r9-mixed-average', 29, 'rust', 'Среднее без смешивания типов', 'В Python sum(v) / len(v) работает сразу. Для v = [3, 4, 4, 6] из i32 напечатайте среднее как дробное с двумя знаками: «4.25».

Ожидаемый вывод:
4.25', 'fn main() {
    // ваш код
}
', 'Приведите и сумму, и длину к f64.', '{"driver": "", "expected": ["4.25"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-args-sum', 0, 'rust', 'Python *args → срез', 'Python: def total(*args): return sum(args). Напишите total(v: &[i64]) -> i64, которая принимает любое количество чисел через срез.', 'fn total(v: &[i64]) -> i64 {
    todo!()
}
', 'v.iter().sum() — сумма элементов.', '{"driver": "fn main() {\n    println!(\"{}\", total(&[1, 2, 3]));\n    println!(\"{}\", total(&[]));\n    println!(\"{}\", total(&vec![10, -4]));\n}\n", "expected": ["6", "0", "6"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-default-arg', 1, 'rust', 'Значение по умолчанию', 'Python: def hi(name="мир"): return f"Привет, {name}!". Напишите hi(name: Option<&str>) -> String, подставляя «мир» при None.', 'fn hi(name: Option<&str>) -> String {
    todo!()
}
', 'unwrap_or("мир") подставит значение по умолчанию.', '{"driver": "fn main() {\n    println!(\"{}\", hi(None));\n    println!(\"{}\", hi(Some(\"Аня\")));\n}\n", "expected": ["Привет, мир!", "Привет, Аня!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-floor-divmod', 2, 'rust', 'divmod как в Python', 'Python: divmod(-7, 2) == (-4, 1). Напишите py_divmod(a: i32, b: i32) -> (i32, i32) с питоновскими частным (округление вниз) и остатком (знак делителя), b ≠ 0.', 'fn py_divmod(a: i32, b: i32) -> (i32, i32) {
    todo!()
}
', 'Если остаток не нуль и его знак не совпадает со знаком делителя — сдвиньте частное вниз.', '{"driver": "fn main() {\n    println!(\"{:?}\", py_divmod(7, 2));\n    println!(\"{:?}\", py_divmod(-7, 2));\n    println!(\"{:?}\", py_divmod(7, -2));\n    println!(\"{:?}\", py_divmod(-7, -2));\n    println!(\"{:?}\", py_divmod(6, 3));\n}\n", "expected": ["(3, 1)", "(-4, 1)", "(-4, -1)", "(3, -1)", "(2, 0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-chain-compare', 3, 'rust', 'Цепочка сравнений', 'Python: lo < x < hi. Напишите strictly_between(x: i32, lo: i32, hi: i32) -> bool — x строго между lo и hi.', 'fn strictly_between(x: i32, lo: i32, hi: i32) -> bool {
    todo!()
}
', 'Две проверки через &&.', '{"driver": "fn main() {\n    println!(\"{}\", strictly_between(5, 1, 10));\n    println!(\"{}\", strictly_between(1, 1, 10));\n    println!(\"{}\", strictly_between(10, 1, 10));\n    println!(\"{}\", strictly_between(0, 1, 10));\n}\n", "expected": ["true", "false", "false", "false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-elif-chain', 4, 'rust', 'elif → else if', 'Python: if/elif для категорий температуры. Напишите category(t: i32) -> &''static str: «мороз» при t < 0, «холодно» при t < 10, «тепло» при t < 25, иначе «жарко».', 'fn category(t: i32) -> &''static str {
    todo!()
}
', 'Цепочка if / else if / else — одно выражение.', '{"driver": "fn main() {\n    for t in [-5, 0, 9, 10, 24, 25, 40] {\n        println!(\"{} {}\", t, category(t));\n    }\n}\n", "expected": ["-5 мороз", "0 холодно", "9 холодно", "10 тепло", "24 тепло", "25 жарко", "40 жарко"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-match-grade', 5, 'rust', 'match вместо if-цепочки', 'Напишите grade(score: u32) -> char через match с диапазонами: 90..=100 → ''A'', 80..=89 → ''B'', 70..=79 → ''C'', 60..=69 → ''D'', иначе ''F''.', 'fn grade(score: u32) -> char {
    todo!()
}
', 'Образцы-диапазоны с ..=', '{"driver": "fn main() {\n    for s in [100, 90, 89, 75, 60, 59, 0] {\n        print!(\"{}\", grade(s));\n    }\n    println!();\n}\n", "expected": ["AABCDFF"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-match-tuple', 6, 'rust', 'FizzBuzz через match', 'Напишите fizz(n: u32) -> String: «FizzBuzz» / «Fizz» / «Buzz» / число. Используйте match по кортежу (n % 3, n % 5).', 'fn fizz(n: u32) -> String {
    todo!()
}
', 'match (a, b) { (0, 0) => …, (0, _) => … }', '{"driver": "fn main() {\n    for n in 1..=15 {\n        print!(\"{} \", fizz(n));\n    }\n    println!();\n}\n", "expected": ["1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-fn-pointer', 7, 'rust', 'Передача функции', 'Python: def apply(f, x): return f(x). Напишите apply(f: fn(i32) -> i32, x: i32) -> i32.', 'fn apply(f: fn(i32) -> i32, x: i32) -> i32 {
    todo!()
}
', 'Параметр f вызывается как обычная функция: f(x).', '{"driver": "fn main() {\n    fn double(x: i32) -> i32 {\n        x * 2\n    }\n    fn neg(x: i32) -> i32 {\n        -x\n    }\n    println!(\"{}\", apply(double, 21));\n    println!(\"{}\", apply(neg, 5));\n    println!(\"{}\", apply(|x| x * x, 7));\n}\n", "expected": ["42", "-5", "49"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-apply-twice', 8, 'rust', 'Применить дважды', 'Напишите apply_twice(f, x): применить функцию f к x два раза. Параметр f объявите как impl Fn(i32) -> i32.', 'fn apply_twice(f: impl Fn(i32) -> i32, x: i32) -> i32 {
    todo!()
}
', 'f(f(x)); замыкание может захватывать k.', '{"driver": "fn main() {\n    println!(\"{}\", apply_twice(|x| x + 3, 10));\n    let k = 5;\n    println!(\"{}\", apply_twice(|x| x * k, 2));\n    println!(\"{}\", apply_twice(|x| -x, 9));\n}\n", "expected": ["16", "50", "9"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-compose', 9, 'rust', 'Композиция функций', 'Python: lambda x: f(g(x)). Напишите compose(f, g, x) = f(g(x)) для f, g: impl Fn(i32) -> i32.', 'fn compose(f: impl Fn(i32) -> i32, g: impl Fn(i32) -> i32, x: i32) -> i32 {
    todo!()
}
', 'f(g(x)) — сначала g, потом f.', '{"driver": "fn main() {\n    println!(\"{}\", compose(|x| x + 1, |x| x * 2, 10));\n    println!(\"{}\", compose(|x| x * 2, |x| x + 1, 10));\n}\n", "expected": ["21", "22"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-any-neg', 10, 'rust', 'any', 'Python: any(x < 0 for x in v). Напишите has_negative(v: &[i32]) -> bool с помощью iter().any.', 'fn has_negative(v: &[i32]) -> bool {
    todo!()
}
', 'v.iter().any(|&x| x < 0)', '{"driver": "fn main() {\n    println!(\"{}\", has_negative(&[1, 2, 3]));\n    println!(\"{}\", has_negative(&[1, -2, 3]));\n    println!(\"{}\", has_negative(&[]));\n}\n", "expected": ["false", "true", "false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-all-pos', 11, 'rust', 'all', 'Python: all(x > 0 for x in v). Напишите all_positive(v: &[i32]) -> bool (для пустого среза — true).', 'fn all_positive(v: &[i32]) -> bool {
    todo!()
}
', 'all для пустой последовательности даёт true.', '{"driver": "fn main() {\n    println!(\"{}\", all_positive(&[1, 2, 3]));\n    println!(\"{}\", all_positive(&[1, 0, 3]));\n    println!(\"{}\", all_positive(&[]));\n}\n", "expected": ["true", "false", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-index-of', 12, 'rust', 'list.index без исключения', 'Python: v.index(x) бросает ValueError, если элемента нет. Напишите index_of(v: &[i32], x: i32) -> Option<usize> методом position.', 'fn index_of(v: &[i32], x: i32) -> Option<usize> {
    todo!()
}
', 'iter().position(|&e| e == x)', '{"driver": "fn main() {\n    println!(\"{:?}\", index_of(&[5, 7, 9, 7], 7));\n    println!(\"{:?}\", index_of(&[5, 7], 1));\n    println!(\"{:?}\", index_of(&[], 1));\n}\n", "expected": ["Some(1)", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-zip-dot', 13, 'rust', 'zip', 'Python: sum(a * b for a, b in zip(xs, ys)). Напишите dot(xs: &[i32], ys: &[i32]) -> i32 с помощью zip (длина — по короткому срезу).', 'fn dot(xs: &[i32], ys: &[i32]) -> i32 {
    todo!()
}
', 'xs.iter().zip(ys.iter()).map(|(a, b)| a * b).sum()', '{"driver": "fn main() {\n    println!(\"{}\", dot(&[1, 2, 3], &[4, 5, 6]));\n    println!(\"{}\", dot(&[1, 2, 3], &[10, 10]));\n    println!(\"{}\", dot(&[], &[1]));\n}\n", "expected": ["32", "30", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-comprehension', 14, 'rust', 'Генератор списка', 'Python: [x * x for x in v if x % 2 == 0]. Напишите even_squares(v: &[i32]) -> Vec<i32>.', 'fn even_squares(v: &[i32]) -> Vec<i32> {
    todo!()
}
', 'filter → map → collect', '{"driver": "fn main() {\n    println!(\"{:?}\", even_squares(&[1, 2, 3, 4, 5, 6]));\n    println!(\"{:?}\", even_squares(&[1, 3]));\n    println!(\"{:?}\", even_squares(&[-2, 0]));\n}\n", "expected": ["[4, 16, 36]", "[]", "[4, 0]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-lens', 15, 'rust', 'Длины слов', 'Python: [len(w) for w in words]. Напишите lens(words: &[&str]) -> Vec<usize>: число символов (не байтов!) в каждом слове.', 'fn lens(words: &[&str]) -> Vec<usize> {
    todo!()
}
', 'chars().count() — символы.', '{"driver": "fn main() {\n    println!(\"{:?}\", lens(&[\"привет\", \"hi\", \"日本語\", \"\"]));\n}\n", "expected": ["[6, 2, 3, 0]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-longest', 16, 'rust', 'max с ключом', 'Python: max(words, key=len). Напишите longest<''a>(words: &[&''a str]) -> &''a str — самое длинное по числу символов слово (при равенстве — первое). Срез не пуст.', 'fn longest<''a>(words: &[&''a str]) -> &''a str {
    todo!()
}
', 'Сравнивайте количество символов.', '{"driver": "fn main() {\n    println!(\"{}\", longest(&[\"a\", \"ccc\", \"bb\", \"ddd\"]));\n    println!(\"{}\", longest(&[\"один\"]));\n    println!(\"{}\", longest(&[\"аб\", \"вг\", \"дежз\"]));\n}\n", "expected": ["ccc", "один", "дежз"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-digits-sum', 17, 'rust', 'sum(map(int, str(n)))', 'Python: sum(int(c) for c in str(n)). Напишите digit_sum(n: u64) -> u32 через n.to_string() и chars().', 'fn digit_sum(n: u64) -> u32 {
    todo!()
}
', 'c.to_digit(10).unwrap()', '{"driver": "fn main() {\n    println!(\"{}\", digit_sum(0));\n    println!(\"{}\", digit_sum(12345));\n    println!(\"{}\", digit_sum(9_999_999_999));\n}\n", "expected": ["0", "15", "90"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-loop-value', 18, 'rust', 'while True', 'Python: while True: … break. Напишите first_pow2_above(n: u64) -> u64: наименьшая степень двойки, строго большая n. Используйте loop и break со значением.', 'fn first_pow2_above(n: u64) -> u64 {
    todo!()
}
', 'break p; возвращает значение из loop.', '{"driver": "fn main() {\n    println!(\"{}\", first_pow2_above(0));\n    println!(\"{}\", first_pow2_above(1));\n    println!(\"{}\", first_pow2_above(1000));\n    println!(\"{}\", first_pow2_above(1 << 40));\n}\n", "expected": ["1", "2", "1024", "2199023255552"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-for-else', 19, 'rust', 'for–else без else', 'Python: for-else для проверки простоты. Напишите is_prime(n: u32) -> bool (n ≥ 2 → true для простых). Для n < 2 — false. Перебирайте делители до √n.', 'fn is_prime(n: u32) -> bool {
    todo!()
}
', 'Ранний return false внутри цикла; true — после цикла.', '{"driver": "fn main() {\n    for n in [0, 1, 2, 3, 4, 17, 18, 97, 7919, 1_000_000_007] {\n        println!(\"{} {}\", n, is_prime(n));\n    }\n}\n", "expected": ["0 false", "1 false", "2 true", "3 true", "4 false", "17 true", "18 false", "97 true", "7919 true", "1000000007 true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-step-range', 20, 'rust', 'range со шагом', 'Python: list(range(start, stop, step)). Напишите range_step(start: i32, stop: i32, step: usize) -> Vec<i32> (step > 0, stop не включается).', 'fn range_step(start: i32, stop: i32, step: usize) -> Vec<i32> {
    todo!()
}
', '(start..stop).step_by(step).collect()', '{"driver": "fn main() {\n    println!(\"{:?}\", range_step(0, 10, 3));\n    println!(\"{:?}\", range_step(5, 5, 1));\n    println!(\"{:?}\", range_step(-3, 4, 2));\n}\n", "expected": ["[0, 3, 6, 9]", "[]", "[-3, -1, 1, 3]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-enumerate-lines', 21, 'rust', 'enumerate с единицы', 'Python: for i, line in enumerate(lines, 1): print(f"{i}: {line}"). Напишите numbered(lines: &[&str]) -> Vec<String> строки вида «1: …».', 'fn numbered(lines: &[&str]) -> Vec<String> {
    todo!()
}
', 'enumerate даёт индекс с нуля — прибавьте 1.', '{"driver": "fn main() {\n    for l in numbered(&[\"раз\", \"два\", \"три\"]) {\n        println!(\"{}\", l);\n    }\n}\n", "expected": ["1: раз", "2: два", "3: три"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-try-except', 22, 'rust', 'try/except → Result', 'Python: int(s) в try/except. Напишите parse_age(s: &str) -> Result<u8, String>: Ok(возраст) для целых 0..=150, иначе Err("…"): «не число», если разбор не удался, и «вне диапазона» для чисел вне 0..=150.', 'fn parse_age(s: &str) -> Result<u8, String> {
    todo!()
}
', 'match s.parse() с ранним return Err(…).', '{"driver": "fn main() {\n    for s in [\"30\", \" 7 \", \"abc\", \"200\", \"-1\", \"150\"] {\n        println!(\"{:?}\", parse_age(s));\n    }\n}\n", "expected": ["Ok(30)", "Ok(7)", "Err(\"не число\")", "Err(\"вне диапазона\")", "Err(\"вне диапазона\")", "Ok(150)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-raise', 23, 'rust', 'raise → Err', 'Python: def sqrt(x): if x < 0: raise ValueError. Напишите safe_sqrt(x: f64) -> Result<f64, String>: Err("отрицательное"), если x < 0, иначе Ok(√x).', 'fn safe_sqrt(x: f64) -> Result<f64, String> {
    todo!()
}
', 'Err(String::from("…")) и Ok(x.sqrt()).', '{"driver": "fn main() {\n    println!(\"{:?}\", safe_sqrt(16.0));\n    println!(\"{:?}\", safe_sqrt(-1.0));\n    println!(\"{:?}\", safe_sqrt(0.0));\n}\n", "expected": ["Ok(4.0)", "Err(\"отрицательное\")", "Ok(0.0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-question-mark', 24, 'rust', 'Оператор ?', 'Напишите sum_two(a: &str, b: &str) -> Result<i32, std::num::ParseIntError>: разберите обе строки и верните сумму. Используйте оператор ? вместо match.', 'fn sum_two(a: &str, b: &str) -> Result<i32, std::num::ParseIntError> {
    todo!()
}
', 'let x: i32 = a.trim().parse()?; при ошибке функция сразу возвращает Err.', '{"driver": "fn main() {\n    println!(\"{:?}\", sum_two(\"2\", \" 3\"));\n    println!(\"{}\", sum_two(\"2\", \"x\").is_err());\n    println!(\"{}\", sum_two(\"\", \"5\").is_err());\n}\n", "expected": ["Ok(5)", "true", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-first-even', 25, 'rust', 'Option из поиска', 'Python: next((x for x in v if x % 2 == 0), None). Напишите first_even(v: &[i32]) -> Option<i32>.', 'fn first_even(v: &[i32]) -> Option<i32> {
    todo!()
}
', 'iter().copied().find(…) возвращает Option.', '{"driver": "fn main() {\n    println!(\"{:?}\", first_even(&[1, 3, 4, 6]));\n    println!(\"{:?}\", first_even(&[1, 3]));\n    println!(\"{:?}\", first_even(&[]));\n}\n", "expected": ["Some(4)", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-password', 26, 'rust', 'Проверка пароля', 'Напишите is_valid(s: &str) -> bool: длина не меньше 8 символов, есть хотя бы одна цифра и хотя бы одна заглавная буква. Используйте ранние return.', 'fn is_valid(s: &str) -> bool {
    todo!()
}
', 'Три проверки: длина, цифра, заглавная.', '{"driver": "fn main() {\n    for p in [\"abc\", \"abcdefgh\", \"abcdefg1\", \"Abcdefg1\", \"Пароль123\", \"пароль123\"] {\n        println!(\"{} {}\", p, is_valid(p));\n    }\n}\n", "expected": ["abc false", "abcdefgh false", "abcdefg1 false", "Abcdefg1 true", "Пароль123 true", "пароль123 false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-clamp-all', 27, 'rust', 'Зажать все', 'Python: [max(lo, min(hi, x)) for x in v]. Напишите clamp_all(v: &[i32], lo: i32, hi: i32) -> Vec<i32>.', 'fn clamp_all(v: &[i32], lo: i32, hi: i32) -> Vec<i32> {
    todo!()
}
', 'x.max(lo).min(hi)', '{"driver": "fn main() {\n    println!(\"{:?}\", clamp_all(&[-5, 0, 5, 10, 15], 0, 10));\n    println!(\"{:?}\", clamp_all(&[], 0, 1));\n}\n", "expected": ["[0, 0, 5, 10, 10]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-config-default', 28, 'rust', 'Строитель вместо kwargs', 'Python: def window(width=800, height=600, title="окно"). Реализуйте структуру Config { width: u32, height: u32, title: String } с функцией default() (800, 600, «окно») и методами-«строителями» with_width(mut self, w: u32) -> Config и with_title(mut self, t: &str) -> Config.', 'struct Config {
    width: u32,
    height: u32,
    title: String,
}

impl Config {
    fn default() -> Config {
        todo!()
    }
    fn with_width(mut self, w: u32) -> Config {
        todo!()
    }
    fn with_title(mut self, t: &str) -> Config {
        todo!()
    }
}
', 'Метод принимает self по значению, меняет поле и возвращает self — цепочку можно продолжать.', '{"driver": "fn main() {\n    let a = Config::default();\n    println!(\"{} {} {}\", a.width, a.height, a.title);\n    let b = Config::default().with_width(1920).with_title(\"игра\");\n    println!(\"{} {} {}\", b.width, b.height, b.title);\n}\n", "expected": ["800 600 окно", "1920 600 игра"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 10, 'r10-gcd-lcm', 29, 'rust', 'НОД и НОК', 'Напишите gcd(a: u64, b: u64) -> u64 (Евклид) и lcm(a: u64, b: u64) -> u64 (НОК = a / gcd · b); lcm(0, x) = 0.', 'fn gcd(a: u64, b: u64) -> u64 {
    todo!()
}

fn lcm(a: u64, b: u64) -> u64 {
    todo!()
}
', 'Сначала делите, потом умножайте — так число не переполнится.', '{"driver": "fn main() {\n    println!(\"{}\", gcd(48, 18));\n    println!(\"{}\", lcm(4, 6));\n    println!(\"{}\", lcm(0, 5));\n    println!(\"{}\", lcm(21, 6));\n}\n", "expected": ["6", "12", "0", "42"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-char-len', 0, 'rust', 'len в символах', 'Python: len(s). Напишите char_len(s: &str) -> usize — число символов (не байтов).', 'fn char_len(s: &str) -> usize {
    todo!()
}
', 's.chars().count()', '{"driver": "fn main() {\n    println!(\"{}\", char_len(\"привет\"));\n    println!(\"{}\", char_len(\"a😀b\"));\n    println!(\"{}\", char_len(\"\"));\n}\n", "expected": ["6", "3", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-first-last', 1, 'rust', 's[0] и s[-1]', 'Python: s[0] и s[-1]. Напишите first_last(s: &str) -> Option<(char, char)>: первая и последняя буквы или None для пустой строки.', 'fn first_last(s: &str) -> Option<(char, char)> {
    todo!()
}
', 'Оператор ? вернёт None, если буквы нет.', '{"driver": "fn main() {\n    println!(\"{:?}\", first_last(\"привет\"));\n    println!(\"{:?}\", first_last(\"я\"));\n    println!(\"{:?}\", first_last(\"\"));\n}\n", "expected": ["Some((''п'', ''т''))", "Some((''я'', ''я''))", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-nth-char', 2, 'rust', 'Символ по номеру', 'Python: s[i]. Напишите char_at(s: &str, i: usize) -> Option<char>.', 'fn char_at(s: &str, i: usize) -> Option<char> {
    todo!()
}
', 's.chars().nth(i)', '{"driver": "fn main() {\n    println!(\"{:?}\", char_at(\"привет\", 2));\n    println!(\"{:?}\", char_at(\"привет\", 6));\n    println!(\"{:?}\", char_at(\"\", 0));\n}\n", "expected": ["Some(''и'')", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-substring', 3, 'rust', 'Срез по символам', 'Python: s[a:b] (по символам). Напишите substr(s: &str, a: usize, b: usize) -> String — символы с номерами a..b (b не включается), для границ за пределами строки — то, что есть.', 'fn substr(s: &str, a: usize, b: usize) -> String {
    todo!()
}
', 'skip(a).take(b - a) по chars().', '{"driver": "fn main() {\n    println!(\"{}\", substr(\"привет, мир\", 0, 6));\n    println!(\"{}\", substr(\"привет, мир\", 8, 20));\n    println!(\"{}\", substr(\"abc\", 2, 2));\n}\n", "expected": ["привет", "мир"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-strip', 4, 'rust', 'strip', 'Python: s.strip(). Напишите clean(s: &str) -> String: обрежьте пробелы по краям и сделайте строчными все буквы.', 'fn clean(s: &str) -> String {
    todo!()
}
', 'trim(), затем to_lowercase().', '{"driver": "fn main() {\n    println!(\"[{}]\", clean(\"  Hello World \\n\"));\n    println!(\"[{}]\", clean(\"ПРИВЕТ\"));\n    println!(\"[{}]\", clean(\"   \"));\n}\n", "expected": ["[hello world]", "[привет]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-find-minus-one', 5, 'rust', 'find без -1', 'Python: s.find(sub) возвращает -1, если нет. Напишите find_py(s: &str, sub: &str) -> i32 с таким же поведением, но позиция — номер символа, а не байта.', 'fn find_py(s: &str, sub: &str) -> i32 {
    todo!()
}
', 'find даёт байтовую позицию; число символов до неё — s[..i].chars().count().', '{"driver": "fn main() {\n    println!(\"{}\", find_py(\"hello\", \"ll\"));\n    println!(\"{}\", find_py(\"привет\", \"ве\"));\n    println!(\"{}\", find_py(\"abc\", \"z\"));\n}\n", "expected": ["2", "3", "-1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-count-sub', 6, 'rust', 'str.count', 'Python: s.count(sub). Напишите count_sub(s: &str, sub: &str) -> usize: число непересекающихся вхождений (sub не пуста).', 'fn count_sub(s: &str, sub: &str) -> usize {
    todo!()
}
', 's.matches(sub).count()', '{"driver": "fn main() {\n    println!(\"{}\", count_sub(\"abababa\", \"aba\"));\n    println!(\"{}\", count_sub(\"мама мыла раму\", \"ма\"));\n    println!(\"{}\", count_sub(\"abc\", \"z\"));\n}\n", "expected": ["2", "2", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-replace-first', 7, 'rust', 'replace с лимитом', 'Python: s.replace(a, b, 1). Напишите replace_first(s: &str, a: &str, b: &str) -> String — заменить только первое вхождение.', 'fn replace_first(s: &str, a: &str, b: &str) -> String {
    todo!()
}
', 'replacen(a, b, n)', '{"driver": "fn main() {\n    println!(\"{}\", replace_first(\"a-b-c\", \"-\", \"+\"));\n    println!(\"{}\", replace_first(\"abc\", \"z\", \"y\"));\n    println!(\"{}\", replace_first(\"раз раз раз\", \"раз\", \"два\"));\n}\n", "expected": ["a+b-c", "abc", "два раз раз"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-split-comma', 8, 'rust', 'split', 'Python: [p.strip() for p in s.split('','')]. Напишите split_trim(s: &str) -> Vec<String>.', 'fn split_trim(s: &str) -> Vec<String> {
    todo!()
}
', 'split('','') → map(trim, to_string) → collect', '{"driver": "fn main() {\n    println!(\"{:?}\", split_trim(\"a, b ,c\"));\n    println!(\"{:?}\", split_trim(\"один\"));\n    println!(\"{:?}\", split_trim(\"\"));\n}\n", "expected": ["[\"a\", \"b\", \"c\"]", "[\"один\"]", "[\"\"]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-split-once', 9, 'rust', 'Ключ и значение', 'Python: k, v = line.split(''='', 1). Напишите kv(line: &str) -> Option<(String, String)> через split_once; ключ и значение без пробелов по краям.', 'fn kv(line: &str) -> Option<(String, String)> {
    todo!()
}
', 'split_once возвращает Option<(&str, &str)>.', '{"driver": "fn main() {\n    println!(\"{:?}\", kv(\"name = Аня\"));\n    println!(\"{:?}\", kv(\"a=b=c\"));\n    println!(\"{:?}\", kv(\"нет равно\"));\n}\n", "expected": ["Some((\"name\", \"Аня\"))", "Some((\"a\", \"b=c\"))", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-words', 10, 'rust', 'Слова текста', 'Python: s.split(). Напишите words(s: &str) -> Vec<&str> через split_whitespace.', 'fn words(s: &str) -> Vec<&str> {
    todo!()
}
', 'split_whitespace().collect()', '{"driver": "fn main() {\n    println!(\"{:?}\", words(\"  раз   два\\tтри\\nчетыре \"));\n    println!(\"{:?}\", words(\"\"));\n}\n", "expected": ["[\"раз\", \"два\", \"три\", \"четыре\"]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-join', 11, 'rust', 'join', 'Python: '', ''.join(words). Напишите join_comma(words: &[&str]) -> String.', 'fn join_comma(words: &[&str]) -> String {
    todo!()
}
', 'words.join(", ")', '{"driver": "fn main() {\n    println!(\"{}\", join_comma(&[\"a\", \"b\", \"c\"]));\n    println!(\"[{}]\", join_comma(&[]));\n    println!(\"{}\", join_comma(&[\"один\"]));\n}\n", "expected": ["a, b, c", "[]", "один"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-fstring', 12, 'rust', 'f-строка', 'Python: f"{name}: {score:>5.1f}". Напишите line(name: &str, score: f64) -> String: имя, двоеточие, пробел и очки с одним знаком после запятой, выровненные вправо в поле шириной 5.', 'fn line(name: &str, score: f64) -> String {
    todo!()
}
', '{:>5.1} — ширина 5, одна цифра после точки.', '{"driver": "fn main() {\n    println!(\"[{}]\", line(\"Аня\", 93.456));\n    println!(\"[{}]\", line(\"Боря\", 7.0));\n    println!(\"[{}]\", line(\"Вера\", 100.0));\n}\n", "expected": ["[Аня:  93.5]", "[Боря:   7.0]", "[Вера: 100.0]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-title-case', 13, 'rust', 'title()', 'Python: s.title() для слов, разделённых пробелами. Напишите title(s: &str) -> String: каждое слово с заглавной буквы, остальные строчные; слова через один пробел.', 'fn title(s: &str) -> String {
    todo!()
}
', 'Первую букву — в верхний регистр, остальное — в нижний.', '{"driver": "fn main() {\n    println!(\"{}\", title(\"hello wORLD\"));\n    println!(\"{}\", title(\"  привет   мир \"));\n    println!(\"[{}]\", title(\"\"));\n}\n", "expected": ["Hello World", "Привет Мир", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-startswith', 14, 'rust', 'startswith и endswith', 'Python: s.startswith((''http://'', ''https://'')). Напишите is_url(s: &str) -> bool: строка начинается с http:// или https://.', 'fn is_url(s: &str) -> bool {
    todo!()
}
', 'Две проверки starts_with через ||.', '{"driver": "fn main() {\n    println!(\"{}\", is_url(\"http://a.ru\"));\n    println!(\"{}\", is_url(\"https://a.ru/x\"));\n    println!(\"{}\", is_url(\"ftp://a.ru\"));\n    println!(\"{}\", is_url(\"\"));\n}\n", "expected": ["true", "true", "false", "false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-isdigit', 15, 'rust', 'isdigit', 'Python: s.isdigit(). Напишите all_digits(s: &str) -> bool: строка непуста и состоит только из ASCII-цифр.', 'fn all_digits(s: &str) -> bool {
    todo!()
}
', 'chars().all(|c| c.is_ascii_digit()) и !s.is_empty()', '{"driver": "fn main() {\n    println!(\"{}\", all_digits(\"12345\"));\n    println!(\"{}\", all_digits(\"12a\"));\n    println!(\"{}\", all_digits(\"\"));\n    println!(\"{}\", all_digits(\"٣٤\"));\n}\n", "expected": ["true", "false", "false", "false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-ord-chr', 16, 'rust', 'ord и chr', 'Python: chr(ord(c) + 1). Напишите next_char(c: char) -> Option<char>: следующий по коду символ (None, если кода нет).', 'fn next_char(c: char) -> Option<char> {
    todo!()
}
', 'char::from_u32 возвращает None, если число — не символ.', '{"driver": "fn main() {\n    println!(\"{:?}\", next_char(''a''));\n    println!(\"{:?}\", next_char(''я''));\n    println!(\"{:?}\", next_char(''\\u{10FFFF}''));\n}\n", "expected": ["Some(''b'')", "Some(''ѐ'')", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-caesar-ru', 17, 'rust', 'Шифр Цезаря для русского', 'Напишите caesar_ru(s: &str, k: u32) -> String: сдвиг строчных русских букв а–я (33 буквы, включая ё) на k позиций вперёд по кругу; прочие символы не менять. Алфавит: «абвгдеёжзийклмнопрстуфхцчшщъыьэюя».', 'fn caesar_ru(s: &str, k: u32) -> String {
    todo!()
}
', 'Найдите позицию буквы в векторе алфавита и сдвиньте по модулю его длины.', '{"driver": "fn main() {\n    println!(\"{}\", caesar_ru(\"привет, мир!\", 3));\n    println!(\"{}\", caesar_ru(\"яя\", 1));\n    println!(\"{}\", caesar_ru(\"abc\", 5));\n}\n", "expected": ["тулезх, плу!", "аа", "abc"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-reverse-words', 18, 'rust', 'Слова в обратном порядке', 'Python: '' ''.join(s.split()[::-1]). Напишите reverse_words(s: &str) -> String.', 'fn reverse_words(s: &str) -> String {
    todo!()
}
', 'split_whitespace().rev() и join(" ")', '{"driver": "fn main() {\n    println!(\"{}\", reverse_words(\"раз два три\"));\n    println!(\"{}\", reverse_words(\"  один  \"));\n    println!(\"[{}]\", reverse_words(\"\"));\n}\n", "expected": ["три два раз", "один", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-anagram', 19, 'rust', 'Анаграммы', 'Python: sorted(a) == sorted(b). Напишите is_anagram(a: &str, b: &str) -> bool без учёта регистра и пробелов.', 'fn is_anagram(a: &str, b: &str) -> bool {
    todo!()
}
', 'Нормализуйте обе строки: без пробелов, в нижнем регистре, отсортированные.', '{"driver": "fn main() {\n    println!(\"{}\", is_anagram(\"Лунь\", \"Нуль\"));\n    println!(\"{}\", is_anagram(\"a b c\", \"cba\"));\n    println!(\"{}\", is_anagram(\"abc\", \"abd\"));\n}\n", "expected": ["true", "true", "false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-char-freq', 20, 'rust', 'Частоты символов', 'Python: Counter(s). Напишите top_char(s: &str) -> Option<(char, usize)>: самый частый символ и его счёт; при равенстве — тот, что встретился раньше. Для пустой строки — None. Используйте Vec пар (char, usize) без HashMap.', 'fn top_char(s: &str) -> Option<(char, usize)> {
    todo!()
}
', 'Храните пары в векторе; обновляйте найденную или добавляйте новую.', '{"driver": "fn main() {\n    println!(\"{:?}\", top_char(\"abracadabra\"));\n    println!(\"{:?}\", top_char(\"ааб\"));\n    println!(\"{:?}\", top_char(\"абв\"));\n    println!(\"{:?}\", top_char(\"\"));\n}\n", "expected": ["Some((''a'', 5))", "Some((''а'', 2))", "Some((''а'', 1))", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-wrap', 21, 'rust', 'Перенос строк', 'Напишите wrap(text: &str, width: usize) -> Vec<String>: разбейте слова по строкам так, чтобы каждая строка (слова через пробел) была не длиннее width символов (слово длиннее width — на отдельной строке).', 'fn wrap(text: &str, width: usize) -> Vec<String> {
    todo!()
}
', 'Копите текущую строку cur и отправляйте её в результат, когда слово не помещается.', '{"driver": "fn main() {\n    for l in wrap(\"раз два три четыре пять шесть семь\", 10) {\n        println!(\"[{}]\", l);\n    }\n    println!(\"{}\", wrap(\"\", 5).len());\n    println!(\"{:?}\", wrap(\"длинноеслово ок\", 5));\n}\n", "expected": ["[раз два]", "[три четыре]", "[пять шесть]", "[семь]", "0", "[\"длинноеслово\", \"ок\"]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-vowels', 22, 'rust', 'Гласные и согласные', 'Напишите count_vowels(s: &str) -> (usize, usize): число русских гласных «аеёиоуыэюя» и число остальных букв (регистр не важен; не буквы не считаются).', 'fn count_vowels(s: &str) -> (usize, usize) {
    todo!()
}
', 'Сначала проверяйте принадлежность гласным, затем is_alphabetic.', '{"driver": "fn main() {\n    println!(\"{:?}\", count_vowels(\"Привет, Мир!\"));\n    println!(\"{:?}\", count_vowels(\"123\"));\n    println!(\"{:?}\", count_vowels(\"Ёжик\"));\n}\n", "expected": ["(3, 6)", "(0, 0)", "(2, 2)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-compress', 23, 'rust', 'Сжатие повторов', 'Напишите rle(s: &str) -> String: каждый ряд одинаковых символов заменяется на символ и число повторов («aaabcc» → «a3b1c2»).', 'fn rle(s: &str) -> String {
    todo!()
}
', 'peekable() позволяет подсмотреть следующий символ.', '{"driver": "fn main() {\n    println!(\"{}\", rle(\"aaabcc\"));\n    println!(\"{}\", rle(\"ббббб\"));\n    println!(\"[{}]\", rle(\"\"));\n    println!(\"{}\", rle(\"abc\"));\n}\n", "expected": ["a3b1c2", "б5", "[]", "a1b1c1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-unrle', 24, 'rust', 'Распаковка', 'Обратная задача: unrle(s: &str) -> String распаковывает вид «a3b1c2» (после каждой буквы идут цифры её количества) в «aaabcc». Буквы — любые не-цифры.', 'fn unrle(s: &str) -> String {
    todo!()
}
', 'Накапливайте цифры в num и сбрасывайте при новой букве.', '{"driver": "fn main() {\n    println!(\"{}\", unrle(\"a3b1c2\"));\n    println!(\"{}\", unrle(\"б5\"));\n    println!(\"[{}]\", unrle(\"\"));\n    println!(\"{}\", unrle(\"x12\"));\n}\n", "expected": ["aaabcc", "ббббб", "[]", "xxxxxxxxxxxx"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-bytes-hex', 25, 'rust', 'encode → hex', 'Python: s.encode().hex(). Напишите to_hex(s: &str) -> String: байты UTF-8, каждый двумя шестнадцатеричными цифрами без пробелов.', 'fn to_hex(s: &str) -> String {
    todo!()
}
', 'format!("{:02x}", b) для каждого байта.', '{"driver": "fn main() {\n    println!(\"{}\", to_hex(\"A\"));\n    println!(\"{}\", to_hex(\"Ж\"));\n    println!(\"{}\", to_hex(\"привет\"));\n    println!(\"[{}]\", to_hex(\"\"));\n}\n", "expected": ["41", "d096", "d0bfd180d0b8d0b2d0b5d182", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-from-bytes', 26, 'rust', 'decode с ошибкой', 'Python: b.decode() может бросить UnicodeDecodeError. Напишите decode(b: &[u8]) -> Result<String, String>: Ok(строка) или Err("плохой UTF-8").', 'fn decode(b: &[u8]) -> Result<String, String> {
    todo!()
}
', 'String::from_utf8(b.to_vec())', '{"driver": "fn main() {\n    println!(\"{:?}\", decode(&[208, 159, 209, 128]));\n    println!(\"{:?}\", decode(&[0xff, 0xfe]));\n    println!(\"{:?}\", decode(&[]));\n}\n", "expected": ["Ok(\"Пр\")", "Err(\"плохой UTF-8\")", "Ok(\"\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-lossy', 27, 'rust', 'from_utf8_lossy', 'Напишите safe_text(b: &[u8]) -> String: превратите байты в строку, подменяя неверные последовательности символом «�» (метод String::from_utf8_lossy и to_string).', 'fn safe_text(b: &[u8]) -> String {
    todo!()
}
', 'from_utf8_lossy возвращает Cow; to_string делает String.', '{"driver": "fn main() {\n    println!(\"{}\", safe_text(&[104, 105]));\n    println!(\"{}\", safe_text(&[104, 0xff, 105]));\n}\n", "expected": ["hi", "h�i"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-sort-ci', 28, 'rust', 'Сортировка без учёта регистра', 'Python: sorted(words, key=str.lower). Напишите sort_ci(words: &[&str]) -> Vec<String>: слова по алфавиту без учёта регистра; при равенстве — исходный порядок (сортировка устойчива).', 'fn sort_ci(words: &[&str]) -> Vec<String> {
    todo!()
}
', 'sort_by_key(|w| w.to_lowercase())', '{"driver": "fn main() {\n    println!(\"{:?}\", sort_ci(&[\"banana\", \"Apple\", \"cherry\", \"apple\", \"Banana\"]));\n    println!(\"{:?}\", sort_ci(&[\"я\", \"А\", \"б\"]));\n}\n", "expected": ["[\"Apple\", \"apple\", \"banana\", \"Banana\", \"cherry\"]", "[\"А\", \"б\", \"я\"]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 11, 'r11-build', 29, 'rust', 'Строим длинную строку', 'Напишите numbers(n: u32) -> String: числа 1…n через запятую без пробелов («1,2,3»). Используйте String::with_capacity и push_str. Для n = 0 — пустая строка.', 'fn numbers(n: u32) -> String {
    todo!()
}
', 'push_str в цикле и запятая перед каждым числом, кроме первого.', '{"driver": "fn main() {\n    println!(\"{}\", numbers(5));\n    println!(\"[{}]\", numbers(0));\n    let big = numbers(100000);\n    println!(\"{} {}\", big.len(), &big[big.len() - 12..]);\n}\n", "expected": ["1,2,3,4,5", "[]", "588894 99999,100000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-last-neg', 0, 'rust', 'Отрицательные индексы', 'Python: l[-k]. Напишите from_end(v: &[i32], k: usize) -> Option<i32>: k-й элемент с конца (k = 1 — последний). Для k = 0 или k > len — None.', 'fn from_end(v: &[i32], k: usize) -> Option<i32> {
    todo!()
}
', 'Индекс — v.len() - k.', '{"driver": "fn main() {\n    let v = [10, 20, 30, 40];\n    println!(\"{:?}\", from_end(&v, 1));\n    println!(\"{:?}\", from_end(&v, 4));\n    println!(\"{:?}\", from_end(&v, 5));\n    println!(\"{:?}\", from_end(&v, 0));\n}\n", "expected": ["Some(40)", "Some(10)", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-rotate', 1, 'rust', 'Циклический сдвиг', 'Python: l[k:] + l[:k]. Напишите rotate_left(v: &[i32], k: usize) -> Vec<i32>: сдвиг влево на k (k может быть больше длины).', 'fn rotate_left(v: &[i32], k: usize) -> Vec<i32> {
    todo!()
}
', 'Сначала k %= len, потом склейте два среза.', '{"driver": "fn main() {\n    println!(\"{:?}\", rotate_left(&[1, 2, 3, 4, 5], 2));\n    println!(\"{:?}\", rotate_left(&[1, 2, 3], 7));\n    println!(\"{:?}\", rotate_left(&[], 3));\n}\n", "expected": ["[3, 4, 5, 1, 2]", "[2, 3, 1]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-step', 2, 'rust', 'Срез с шагом', 'Python: l[::2]. Напишите every_other(v: &[i32]) -> Vec<i32>: элементы с чётными индексами 0, 2, 4, …', 'fn every_other(v: &[i32]) -> Vec<i32> {
    todo!()
}
', 'iter().step_by(2).copied().collect()', '{"driver": "fn main() {\n    println!(\"{:?}\", every_other(&[1, 2, 3, 4, 5]));\n    println!(\"{:?}\", every_other(&[7]));\n    println!(\"{:?}\", every_other(&[]));\n}\n", "expected": ["[1, 3, 5]", "[7]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-remove-value', 3, 'rust', 'list.remove(x)', 'Python: l.remove(x) удаляет первое вхождение и бросает ValueError, если нет. Напишите remove_first(v: &mut Vec<i32>, x: i32) -> bool: true, если удалили.', 'fn remove_first(v: &mut Vec<i32>, x: i32) -> bool {
    todo!()
}
', 'position даёт индекс первого, remove(i) удаляет его.', '{"driver": "fn main() {\n    let mut v = vec![1, 2, 3, 2];\n    println!(\"{}\", remove_first(&mut v, 2));\n    println!(\"{:?}\", v);\n    println!(\"{}\", remove_first(&mut v, 9));\n    println!(\"{:?}\", v);\n}\n", "expected": ["true", "[1, 3, 2]", "false", "[1, 3, 2]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-remove-all', 4, 'rust', 'Удалить все', 'Python: [x for x in l if x != v]. Напишите remove_all(v: &mut Vec<i32>, x: i32) — удалить все вхождения за один проход, используя retain.', 'fn remove_all(v: &mut Vec<i32>, x: i32) {
    todo!()
}
', 'v.retain(|&e| e != x)', '{"driver": "fn main() {\n    let mut v = vec![1, 2, 3, 2, 2, 4];\n    remove_all(&mut v, 2);\n    println!(\"{:?}\", v);\n    remove_all(&mut v, 9);\n    println!(\"{:?}\", v);\n}\n", "expected": ["[1, 3, 4]", "[1, 3, 4]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-dedup-order', 5, 'rust', 'Уникальные с порядком', 'Python: list(dict.fromkeys(l)). Напишите unique(v: &[i32]) -> Vec<i32>: убрать повторы, сохранив порядок первых вхождений. Без HashSet (только вектор и contains).', 'fn unique(v: &[i32]) -> Vec<i32> {
    todo!()
}
', 'Проверяйте out.contains(&x) перед push.', '{"driver": "fn main() {\n    println!(\"{:?}\", unique(&[3, 1, 3, 2, 1, 2]));\n    println!(\"{:?}\", unique(&[]));\n    println!(\"{:?}\", unique(&[5, 5, 5]));\n}\n", "expected": ["[3, 1, 2]", "[]", "[5]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-chunks', 6, 'rust', 'Пачки', 'Напишите batches(v: &[i32], n: usize) -> Vec<Vec<i32>>: разбейте на пачки по n элементов (последняя может быть короче), n > 0. Используйте chunks.', 'fn batches(v: &[i32], n: usize) -> Vec<Vec<i32>> {
    todo!()
}
', 'v.chunks(n).map(|c| c.to_vec()).collect()', '{"driver": "fn main() {\n    println!(\"{:?}\", batches(&[1, 2, 3, 4, 5, 6, 7], 3));\n    println!(\"{:?}\", batches(&[1, 2], 5));\n    println!(\"{:?}\", batches(&[], 2));\n}\n", "expected": ["[[1, 2, 3], [4, 5, 6], [7]]", "[[1, 2]]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-windows', 7, 'rust', 'Скользящее окно', 'Напишите moving_sums(v: &[i32], k: usize) -> Vec<i32>: суммы всех окон из k подряд идущих элементов (k > 0). Используйте windows.', 'fn moving_sums(v: &[i32], k: usize) -> Vec<i32> {
    todo!()
}
', 'windows(k) выдаёт срезы длины k.', '{"driver": "fn main() {\n    println!(\"{:?}\", moving_sums(&[1, 2, 3, 4, 5], 3));\n    println!(\"{:?}\", moving_sums(&[1, 2], 3));\n    println!(\"{:?}\", moving_sums(&[4], 1));\n}\n", "expected": ["[6, 9, 12]", "[]", "[4]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-is-sorted', 8, 'rust', 'Отсортирован ли', 'Напишите is_sorted(v: &[i32]) -> bool: элементы не убывают. Используйте windows(2).', 'fn is_sorted(v: &[i32]) -> bool {
    todo!()
}
', 'all для пустой последовательности — true.', '{"driver": "fn main() {\n    println!(\"{}\", is_sorted(&[1, 2, 2, 5]));\n    println!(\"{}\", is_sorted(&[1, 3, 2]));\n    println!(\"{}\", is_sorted(&[]));\n    println!(\"{}\", is_sorted(&[9]));\n}\n", "expected": ["true", "false", "true", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-sort-desc', 9, 'rust', 'sorted(reverse=True)', 'Python: sorted(l, reverse=True). Напишите sorted_desc(v: &[i32]) -> Vec<i32> — отсортированная копия по убыванию; исходный срез не меняется.', 'fn sorted_desc(v: &[i32]) -> Vec<i32> {
    todo!()
}
', 'to_vec() и sort_by(|a, b| b.cmp(a))', '{"driver": "fn main() {\n    let a = [3, 1, 4, 1, 5];\n    println!(\"{:?}\", sorted_desc(&a));\n    println!(\"{:?}\", a);\n}\n", "expected": ["[5, 4, 3, 1, 1]", "[3, 1, 4, 1, 5]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-sort-key', 10, 'rust', 'key=len', 'Python: sorted(words, key=len). Напишите by_len(words: &[&str]) -> Vec<String>: слова по возрастанию длины в символах; при равной длине — в исходном порядке.', 'fn by_len(words: &[&str]) -> Vec<String> {
    todo!()
}
', 'sort_by_key устойчива.', '{"driver": "fn main() {\n    println!(\"{:?}\", by_len(&[\"ccc\", \"a\", \"bb\", \"dd\", \"e\"]));\n    println!(\"{:?}\", by_len(&[\"привет\", \"мир\", \"я\"]));\n}\n", "expected": ["[\"a\", \"e\", \"bb\", \"dd\", \"ccc\"]", "[\"я\", \"мир\", \"привет\"]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-top-k', 11, 'rust', 'Топ-k', 'Python: sorted(l, reverse=True)[:k]. Напишите top_k(v: &[i32], k: usize) -> Vec<i32>: k наибольших по убыванию (если элементов меньше — все).', 'fn top_k(v: &[i32], k: usize) -> Vec<i32> {
    todo!()
}
', 'sort_by, затем truncate(k).', '{"driver": "fn main() {\n    println!(\"{:?}\", top_k(&[5, 1, 9, 3, 7], 3));\n    println!(\"{:?}\", top_k(&[2, 1], 5));\n    println!(\"{:?}\", top_k(&[4, 4, 1], 2));\n}\n", "expected": ["[9, 7, 5]", "[2, 1]", "[4, 4]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-binary-search', 12, 'rust', 'bisect', 'Python: bisect.bisect_left(l, x). Напишите insert_pos(v: &[i32], x: i32) -> usize: позиция, куда вставить x, чтобы сохранить порядок (слева от равных). Срез отсортирован. Используйте partition_point.', 'fn insert_pos(v: &[i32], x: i32) -> usize {
    todo!()
}
', 'partition_point(|&e| e < x)', '{"driver": "fn main() {\n    let v = [1, 3, 3, 5, 8];\n    println!(\"{}\", insert_pos(&v, 0));\n    println!(\"{}\", insert_pos(&v, 3));\n    println!(\"{}\", insert_pos(&v, 4));\n    println!(\"{}\", insert_pos(&v, 9));\n}\n", "expected": ["0", "1", "3", "5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-zip-pairs', 13, 'rust', 'zip', 'Python: list(zip(a, b)). Напишите pairs(a: &[i32], b: &[&str]) -> Vec<(i32, String)>: пары по короткому из двух срезов.', 'fn pairs(a: &[i32], b: &[&str]) -> Vec<(i32, String)> {
    todo!()
}
', 'a.iter().zip(b.iter())', '{"driver": "fn main() {\n    println!(\"{:?}\", pairs(&[1, 2, 3], &[\"a\", \"b\"]));\n    println!(\"{:?}\", pairs(&[], &[\"a\"]));\n}\n", "expected": ["[(1, \"a\"), (2, \"b\")]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-enumerate-rev', 14, 'rust', 'Индексы с конца', 'Напишите last_index_of(v: &[i32], x: i32) -> Option<usize>: индекс последнего вхождения x или None. Используйте iter().rposition.', 'fn last_index_of(v: &[i32], x: i32) -> Option<usize> {
    todo!()
}
', 'rposition ищет с конца.', '{"driver": "fn main() {\n    println!(\"{:?}\", last_index_of(&[1, 2, 3, 2, 1], 2));\n    println!(\"{:?}\", last_index_of(&[1, 2], 5));\n    println!(\"{:?}\", last_index_of(&[], 1));\n}\n", "expected": ["Some(3)", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-flatten', 15, 'rust', 'Склеить списки', 'Python: [x for row in rows for x in row]. Напишите flatten(rows: &[Vec<i32>]) -> Vec<i32>.', 'fn flatten(rows: &[Vec<i32>]) -> Vec<i32> {
    todo!()
}
', 'rows.iter().flatten().copied().collect()', '{"driver": "fn main() {\n    println!(\"{:?}\", flatten(&[vec![1, 2], vec![], vec![3]]));\n    println!(\"{:?}\", flatten(&[]));\n}\n", "expected": ["[1, 2, 3]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-transpose', 16, 'rust', 'Транспонирование', 'Python: list(zip(*m)). Напишите transpose(m: &[Vec<i32>]) -> Vec<Vec<i32>> для прямоугольной матрицы (все строки одной длины; пустая матрица → пустая).', 'fn transpose(m: &[Vec<i32>]) -> Vec<Vec<i32>> {
    todo!()
}
', 't[j][i] = m[i][j]', '{"driver": "fn main() {\n    println!(\"{:?}\", transpose(&[vec![1, 2, 3], vec![4, 5, 6]]));\n    println!(\"{:?}\", transpose(&[vec![7]]));\n    println!(\"{:?}\", transpose(&[]));\n}\n", "expected": ["[[1, 4], [2, 5], [3, 6]]", "[[7]]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-grid-trap', 17, 'rust', 'Ловушка [[0]*n]*m', 'Напишите make_grid(rows: usize, cols: usize) -> Vec<Vec<i32>>, заполненную нулями; строки независимы. После вызова driver меняет ячейку, и меняется только одна строка.', 'fn make_grid(rows: usize, cols: usize) -> Vec<Vec<i32>> {
    todo!()
}
', 'vec![vec![0; cols]; rows]', '{"driver": "fn main() {\n    let mut g = make_grid(2, 3);\n    g[0][1] = 7;\n    println!(\"{:?}\", g);\n    println!(\"{:?}\", make_grid(0, 5));\n}\n", "expected": ["[[0, 7, 0], [0, 0, 0]]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-flat-index', 18, 'rust', 'Плоская матрица', 'Матрица хранится одним вектором построчно, ширина w. Напишите get(m: &[i32], w: usize, row: usize, col: usize) -> Option<i32>: элемент или None, если вне границ (col ≥ w или индекс за концом).', 'fn get(m: &[i32], w: usize, row: usize, col: usize) -> Option<i32> {
    todo!()
}
', 'Индекс row * w + col; проверьте col < w отдельно.', '{"driver": "fn main() {\n    let m = [1, 2, 3, 4, 5, 6];\n    println!(\"{:?}\", get(&m, 3, 1, 2));\n    println!(\"{:?}\", get(&m, 3, 2, 0));\n    println!(\"{:?}\", get(&m, 3, 0, 3));\n    println!(\"{:?}\", get(&m, 3, 0, 0));\n}\n", "expected": ["Some(6)", "None", "None", "Some(1)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-stack-brackets', 19, 'rust', 'Стек скобок', 'Напишите balanced(s: &str) -> bool: правильна ли расстановка скобок ()[]{} (Vec как стек).', 'fn balanced(s: &str) -> bool {
    todo!()
}
', 'push открывающих, pop и сравнение при закрывающих.', '{"driver": "fn main() {\n    for s in [\"([]{})\", \"([)]\", \"((\", \"\", \"a(b)c\", \")(\"] {\n        println!(\"{:?} {}\", s, balanced(s));\n    }\n}\n", "expected": ["\"([]{})\" true", "\"([)]\" false", "\"((\" false", "\"\" true", "\"a(b)c\" true", "\")(\" false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-queue', 20, 'rust', 'Очередь на VecDeque', 'Напишите josephus(n: usize, k: usize) -> usize: задача Иосифа Флавия — n человек по кругу, каждый k-й выбывает; вернуть номер (с 1) последнего оставшегося. Используйте VecDeque.', 'fn josephus(n: usize, k: usize) -> usize {
    todo!()
}
', 'k - 1 раз переносим из начала в конец, затем удаляем.', '{"driver": "fn main() {\n    println!(\"{}\", josephus(7, 3));\n    println!(\"{}\", josephus(1, 5));\n    println!(\"{}\", josephus(10, 2));\n    println!(\"{}\", josephus(5000, 7));\n}\n", "expected": ["4", "1", "5", "4173"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-bfs-grid', 21, 'rust', 'Кратчайший путь по сетке', 'Напишите shortest(grid: &[&str]) -> Option<usize>: длина кратчайшего пути из ''S'' в ''E'' по клеткам ''.'' (вверх, вниз, влево, вправо), ''#'' — стена. None, если пути нет. Поиск в ширину на VecDeque.', 'fn shortest(grid: &[&str]) -> Option<usize> {
    todo!()
}
', 'dist хранит расстояния; очередь VecDeque из клеток.', '{"driver": "fn main() {\n    println!(\"{:?}\", shortest(&[\"S.#\", \"..#\", \"#.E\"]));\n    println!(\"{:?}\", shortest(&[\"S#E\"]));\n    println!(\"{:?}\", shortest(&[\"SE\"]));\n}\n", "expected": ["Some(4)", "None", "Some(1)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-heap-kth', 22, 'rust', 'k-е по величине', 'Python: heapq.nlargest(k, l)[-1]. Напишите kth_largest(v: &[i32], k: usize) -> Option<i32>: k-е по величине (k = 1 — наибольшее) через BinaryHeap. None, если k = 0 или k > len.', 'fn kth_largest(v: &[i32], k: usize) -> Option<i32> {
    todo!()
}
', 'BinaryHeap — куча-максимум; pop даёт наибольшее.', '{"driver": "fn main() {\n    println!(\"{:?}\", kth_largest(&[3, 1, 4, 1, 5, 9, 2, 6], 3));\n    println!(\"{:?}\", kth_largest(&[1], 2));\n    println!(\"{:?}\", kth_largest(&[5, 5], 2));\n}\n", "expected": ["Some(5)", "None", "Some(5)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-capacity', 23, 'rust', 'Ёмкость вектора', 'Напишите growth(n: usize) -> Vec<usize>: создайте пустой Vec<u8>, добавьте n элементов и запишите в результат значение capacity() каждый раз, когда оно меняется (без повторов подряд). Для первых n = 20 результат будет строго возрастающим.', 'fn growth(n: usize) -> Vec<usize> {
    todo!()
}
', 'Запоминайте capacity после каждого push и сравнивайте с последним.', '{"driver": "fn main() {\n    let g = growth(100);\n    println!(\"{}\", g.windows(2).all(|w| w[0] < w[1]));\n    println!(\"{}\", g[0] >= 1);\n    println!(\"{}\", *g.last().unwrap() >= 100);\n}\n", "expected": ["true", "true", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-split-at', 24, 'rust', 'Разделить пополам', 'Напишите halves(v: &[i32]) -> (Vec<i32>, Vec<i32>): левая половина (длина len / 2) и правая (остальное). Используйте split_at.', 'fn halves(v: &[i32]) -> (Vec<i32>, Vec<i32>) {
    todo!()
}
', 'split_at(mid) возвращает два среза.', '{"driver": "fn main() {\n    println!(\"{:?}\", halves(&[1, 2, 3, 4, 5]));\n    println!(\"{:?}\", halves(&[1, 2]));\n    println!(\"{:?}\", halves(&[]));\n}\n", "expected": ["([1, 2], [3, 4, 5])", "([1], [2])", "([], [])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-drain', 25, 'rust', 'Вынуть диапазон', 'Напишите cut(v: &mut Vec<i32>, a: usize, b: usize) -> Vec<i32>: удалить элементы a..b из v и вернуть их (drain).', 'fn cut(v: &mut Vec<i32>, a: usize, b: usize) -> Vec<i32> {
    todo!()
}
', 'v.drain(a..b).collect()', '{"driver": "fn main() {\n    let mut v = vec![0, 1, 2, 3, 4, 5];\n    let d = cut(&mut v, 1, 4);\n    println!(\"{:?} {:?}\", d, v);\n    let e = cut(&mut v, 0, 0);\n    println!(\"{:?} {:?}\", e, v);\n}\n", "expected": ["[1, 2, 3] [0, 4, 5]", "[] [0, 4, 5]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-argmax', 26, 'rust', 'Индекс максимума', 'Python: l.index(max(l)). Напишите argmax(v: &[i32]) -> Option<usize>: индекс первого наибольшего элемента или None для пустого среза.', 'fn argmax(v: &[i32]) -> Option<usize> {
    todo!()
}
', 'Строгое сравнение сохранит индекс первого.', '{"driver": "fn main() {\n    println!(\"{:?}\", argmax(&[3, 9, 2, 9]));\n    println!(\"{:?}\", argmax(&[-5]));\n    println!(\"{:?}\", argmax(&[]));\n}\n", "expected": ["Some(1)", "Some(0)", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-prefix-sums', 27, 'rust', 'Префиксные суммы', 'Python: list(itertools.accumulate(l)). Напишите prefix_sums(v: &[i32]) -> Vec<i32>: частичные суммы (i-й элемент — сумма первых i + 1).', 'fn prefix_sums(v: &[i32]) -> Vec<i32> {
    todo!()
}
', 'Замыкание может менять внешнюю переменную s.', '{"driver": "fn main() {\n    println!(\"{:?}\", prefix_sums(&[1, 2, 3, 4]));\n    println!(\"{:?}\", prefix_sums(&[5, -5, 5]));\n    println!(\"{:?}\", prefix_sums(&[]));\n}\n", "expected": ["[1, 3, 6, 10]", "[5, 0, 5]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-two-sum', 28, 'rust', 'Два числа с суммой', 'Напишите two_sum(v: &[i32], target: i32) -> Option<(usize, usize)>: индексы i < j, для которых v[i] + v[j] = target (первая найденная пара при переборе i, затем j).', 'fn two_sum(v: &[i32], target: i32) -> Option<(usize, usize)> {
    todo!()
}
', 'Два вложенных цикла, j начинается с i + 1.', '{"driver": "fn main() {\n    println!(\"{:?}\", two_sum(&[2, 7, 11, 15], 9));\n    println!(\"{:?}\", two_sum(&[3, 2, 4], 6));\n    println!(\"{:?}\", two_sum(&[1, 2], 10));\n}\n", "expected": ["Some((0, 1))", "Some((1, 2))", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 12, 'r12-merge', 29, 'rust', 'Слияние отсортированных', 'Напишите merge(a: &[i32], b: &[i32]) -> Vec<i32>: слейте два отсортированных среза в один отсортированный вектор за линейное время (двумя индексами).', 'fn merge(a: &[i32], b: &[i32]) -> Vec<i32> {
    todo!()
}
', 'После цикла допишите хвосты обоих срезов.', '{"driver": "fn main() {\n    println!(\"{:?}\", merge(&[1, 3, 5], &[2, 4, 6, 8]));\n    println!(\"{:?}\", merge(&[], &[1]));\n    println!(\"{:?}\", merge(&[1, 1], &[1]));\n}\n", "expected": ["[1, 2, 3, 4, 5, 6, 8]", "[1]", "[1, 1, 1]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-class-basic', 0, 'rust', 'Класс → struct', 'Python: class Dog с name и методом speak() → «<имя>: гав!». Напишите структуру Dog { name: String }, функцию new(name: &str) -> Dog и метод speak(&self) -> String.', 'struct Dog {
    name: String,
}

impl Dog {
    fn new(name: &str) -> Dog {
        todo!()
    }
    fn speak(&self) -> String {
        todo!()
    }
}
', 'format!("{}: гав!", self.name)', '{"driver": "fn main() {\n    let d = Dog::new(\"Бобик\");\n    println!(\"{}\", d.speak());\n    println!(\"{}\", Dog::new(\"Шарик\").speak());\n}\n", "expected": ["Бобик: гав!", "Шарик: гав!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-property', 1, 'rust', 'property', 'Python: @property celsius / fahrenheit. Структура Temp { celsius: f64 } с методом fahrenheit(&self) -> f64 (c · 9/5 + 32) и set_fahrenheit(&mut self, f: f64) (обновляет celsius).', 'struct Temp {
    celsius: f64,
}

impl Temp {
    fn fahrenheit(&self) -> f64 {
        todo!()
    }
    fn set_fahrenheit(&mut self, f: f64) {
        todo!()
    }
}
', 'Формулы: c·9/5+32 и (f−32)·5/9.', '{"driver": "fn main() {\n    let mut t = Temp { celsius: 100.0 };\n    println!(\"{}\", t.fahrenheit());\n    t.set_fahrenheit(32.0);\n    println!(\"{}\", t.celsius);\n    t.set_fahrenheit(212.0);\n    println!(\"{}\", t.celsius);\n}\n", "expected": ["212", "0", "100"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-classmethod', 2, 'rust', 'classmethod', 'Python: Color.from_hex("#ff8000"). Структура Color { r: u8, g: u8, b: u8 } и ассоциированная функция from_hex(s: &str) -> Color для строки вида «#rrggbb» (используйте u8::from_str_radix(&s[1..3], 16).unwrap()).', 'struct Color {
    r: u8,
    g: u8,
    b: u8,
}

impl Color {
    fn from_hex(s: &str) -> Color {
        todo!()
    }
}
', 'u8::from_str_radix(&s[1..3], 16).unwrap()', '{"driver": "fn main() {\n    let c = Color::from_hex(\"#ff8000\");\n    println!(\"{} {} {}\", c.r, c.g, c.b);\n    let d = Color::from_hex(\"#000a0b\");\n    println!(\"{} {} {}\", d.r, d.g, d.b);\n}\n", "expected": ["255 128 0", "0 10 11"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-composition', 3, 'rust', 'Композиция вместо наследования', 'Python: class Employee(Person). Структуры Person { name: String } и Employee { person: Person, salary: u32 }; у Employee метод describe(&self) -> String: «<имя> зарабатывает <salary>».', 'struct Person {
    name: String,
}

struct Employee {
    person: Person,
    salary: u32,
}

impl Employee {
    fn describe(&self) -> String {
        todo!()
    }
}
', 'self.person.name — поле вложенной структуры.', '{"driver": "fn main() {\n    let e = Employee { person: Person { name: String::from(\"Аня\") }, salary: 120 };\n    println!(\"{}\", e.describe());\n}\n", "expected": ["Аня зарабатывает 120"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-trait-basic', 4, 'rust', 'Первый трейт', 'Трейт Animal с методом sound(&self) -> String; структуры Dog и Cat реализуют его: «гав» и «мяу». Функция chorus(a: &impl Animal) -> String возвращает звук, повторённый три раза через пробел.', 'trait Animal {
    fn sound(&self) -> String;
}

struct Dog;
struct Cat;

impl Animal for Dog {
    fn sound(&self) -> String {
        todo!()
    }
}

impl Animal for Cat {
    fn sound(&self) -> String {
        todo!()
    }
}

fn chorus(a: &impl Animal) -> String {
    todo!()
}
', 'impl Animal for Dog { … } — отдельный блок для каждого типа.', '{"driver": "fn main() {\n    println!(\"{}\", chorus(&Dog));\n    println!(\"{}\", chorus(&Cat));\n}\n", "expected": ["гав гав гав", "мяу мяу мяу"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-trait-default', 5, 'rust', 'Метод по умолчанию', 'Трейт Greeter: метод name(&self) -> String обязателен, а greet(&self) -> String имеет реализацию по умолчанию: «Привет, <имя>!». Структура English реализует только name; структура Formal переопределяет greet: «Здравствуйте, <имя>.».', 'trait Greeter {
    fn name(&self) -> String;
    fn greet(&self) -> String {
        todo!()
    }
}

struct English;
struct Formal;

impl Greeter for English {
    fn name(&self) -> String {
        todo!()
    }
}

impl Greeter for Formal {
    fn name(&self) -> String {
        todo!()
    }
    fn greet(&self) -> String {
        todo!()
    }
}
', 'Метод по умолчанию вызывает обязательный: self.name().', '{"driver": "fn main() {\n    println!(\"{}\", English.greet());\n    println!(\"{}\", Formal.greet());\n}\n", "expected": ["Привет, друг!", "Здравствуйте, коллега."]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-dyn-shapes', 6, 'rust', 'Вектор фигур', 'Трейт Shape с area(&self) -> f64; структуры Circle { r }, Rect { w, h } реализуют его (π ≈ 3.14159). Функция total_area(shapes: &[Box<dyn Shape>]) -> f64 — сумма площадей.', 'trait Shape {
    fn area(&self) -> f64;
}

struct Circle {
    r: f64,
}
struct Rect {
    w: f64,
    h: f64,
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        todo!()
    }
}
impl Shape for Rect {
    fn area(&self) -> f64 {
        todo!()
    }
}

fn total_area(shapes: &[Box<dyn Shape>]) -> f64 {
    todo!()
}
', 'shapes.iter().map(|s| s.area()).sum()', '{"driver": "fn main() {\n    let v: Vec<Box<dyn Shape>> = vec![Box::new(Circle { r: 1.0 }), Box::new(Rect { w: 2.0, h: 3.0 })];\n    println!(\"{:.5}\", total_area(&v));\n    println!(\"{}\", total_area(&[]) == 0.0);\n}\n", "expected": ["9.14159", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-display', 7, 'rust', 'Display для точки', 'Реализуйте fmt::Display для структуры Point { x: i32, y: i32 }: вывод «(x, y)». Тогда println!("{}", p) и p.to_string() дадут «(1, -2)».', 'use std::fmt;

struct Point {
    x: i32,
    y: i32,
}

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}
', 'write!(f, "({}, {})", self.x, self.y)', '{"driver": "fn main() {\n    let p = Point { x: 1, y: -2 };\n    println!(\"{}\", p);\n    println!(\"{}\", p.to_string().len());\n    println!(\"[{}]\", Point { x: 0, y: 0 });\n}\n", "expected": ["(1, -2)", "7", "[(0, 0)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-debug-derive', 8, 'rust', 'Debug и PartialEq', 'Добавьте структуре Pair { a: i32, b: i32 } атрибуты derive(Debug, PartialEq, Clone), чтобы работали печать {:?}, сравнение == и clone().', 'struct Pair {
    a: i32,
    b: i32,
}
', '#[derive(Debug, PartialEq, Clone)] над struct.', '{"driver": "fn main() {\n    let p = Pair { a: 1, b: 2 };\n    let q = p.clone();\n    println!(\"{:?}\", p);\n    println!(\"{}\", p == q);\n    println!(\"{}\", p == Pair { a: 1, b: 3 });\n}\n", "expected": ["Pair { a: 1, b: 2 }", "true", "false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-ord-derive', 9, 'rust', 'Порядок версий', 'Структура Version(u32, u32, u32) с derive(PartialEq, Eq, PartialOrd, Ord, Debug): версии сравниваются лексикографически. Дополните функцию newest(v: &[Version]) -> Version, вернув наибольшую (v не пуст; Version нужно ещё Clone и Copy).', 'struct Version(u32, u32, u32);

fn newest(v: &[Version]) -> Version {
    todo!()
}
', 'derive(Ord) сравнивает поля по порядку; iter().max().', '{"driver": "fn main() {\n    let v = [Version(1, 9, 0), Version(2, 0, 1), Version(2, 0, 0)];\n    println!(\"{:?}\", newest(&v));\n    println!(\"{}\", Version(1, 10, 0) > Version(1, 9, 99));\n}\n", "expected": ["Version(2, 0, 1)", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-vec2-add', 10, 'rust', 'Сложение векторов', 'Реализуйте для Vec2 { x: f64, y: f64 } операторы + и − (трейты Add и Sub). Derive(Debug, PartialEq, Clone, Copy) уже есть.', 'use std::ops::{Add, Sub};

#[derive(Debug, PartialEq, Clone, Copy)]
struct Vec2 {
    x: f64,
    y: f64,
}

impl Add for Vec2 {
    type Output = Vec2;
    fn add(self, o: Vec2) -> Vec2 {
        todo!()
    }
}

impl Sub for Vec2 {
    type Output = Vec2;
    fn sub(self, o: Vec2) -> Vec2 {
        todo!()
    }
}
', 'Складывайте покомпонентно.', '{"driver": "fn main() {\n    let a = Vec2 { x: 1.0, y: 2.0 };\n    let b = Vec2 { x: 0.5, y: -1.0 };\n    println!(\"{:?}\", a + b);\n    println!(\"{:?}\", a - b);\n    println!(\"{:?}\", a + b - b == a);\n}\n", "expected": ["Vec2 { x: 1.5, y: 1.0 }", "Vec2 { x: 0.5, y: 3.0 }", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-vec2-scalar', 11, 'rust', 'Умножение на число', 'Для Vec2 реализуйте Mul<f64> (вектор × число) и Neg (унарный минус).', 'use std::ops::{Mul, Neg};

#[derive(Debug, PartialEq, Clone, Copy)]
struct Vec2 {
    x: f64,
    y: f64,
}

impl Mul<f64> for Vec2 {
    type Output = Vec2;
    fn mul(self, k: f64) -> Vec2 {
        todo!()
    }
}

impl Neg for Vec2 {
    type Output = Vec2;
    fn neg(self) -> Vec2 {
        todo!()
    }
}
', 'impl Mul<f64> for Vec2 — тип правого операнда в угловых скобках.', '{"driver": "fn main() {\n    let a = Vec2 { x: 1.0, y: -2.0 };\n    println!(\"{:?}\", a * 3.0);\n    println!(\"{:?}\", -a);\n    println!(\"{:?}\", -(a * 0.5));\n}\n", "expected": ["Vec2 { x: 3.0, y: -6.0 }", "Vec2 { x: -1.0, y: 2.0 }", "Vec2 { x: -0.5, y: 1.0 }"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-vec2-dot', 12, 'rust', 'Скалярное произведение', 'Для Vec2 реализуйте Mul<Vec2> с Output = f64 (скалярное произведение): a * b = a.x·b.x + a.y·b.y.', 'use std::ops::Mul;

#[derive(Debug, Clone, Copy)]
struct Vec2 {
    x: f64,
    y: f64,
}

impl Mul<Vec2> for Vec2 {
    type Output = f64;
    fn mul(self, o: Vec2) -> f64 {
        todo!()
    }
}
', 'Output может быть другого типа, чем сами операнды.', '{"driver": "fn main() {\n    let a = Vec2 { x: 1.0, y: 2.0 };\n    let b = Vec2 { x: 3.0, y: 4.0 };\n    println!(\"{}\", a * b);\n    println!(\"{}\", a * Vec2 { x: 0.0, y: 0.0 });\n}\n", "expected": ["11", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-add-assign', 13, 'rust', '+=', 'Для Money(i64) (копейки) реализуйте Add и AddAssign, чтобы работали a + b и a += b. Derive(Debug, Clone, Copy, PartialEq) уже есть.', 'use std::ops::{Add, AddAssign};

#[derive(Debug, Clone, Copy, PartialEq)]
struct Money(i64);

impl Add for Money {
    type Output = Money;
    fn add(self, o: Money) -> Money {
        todo!()
    }
}

impl AddAssign for Money {
    fn add_assign(&mut self, o: Money) {
        todo!()
    }
}
', 'add_assign принимает &mut self и ничего не возвращает.', '{"driver": "fn main() {\n    let mut m = Money(100);\n    m += Money(250);\n    println!(\"{:?}\", m);\n    println!(\"{:?}\", m + Money(5));\n    println!(\"{:?}\", m);\n}\n", "expected": ["Money(350)", "Money(355)", "Money(350)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-index', 14, 'rust', 'Индексация матрицы', 'Структура Matrix { w: usize, data: Vec<i32> } (построчно). Реализуйте Index<(usize, usize)> и IndexMut<(usize, usize)>, чтобы работало m[(r, c)] для чтения и записи.', 'use std::ops::{Index, IndexMut};

struct Matrix {
    w: usize,
    data: Vec<i32>,
}

impl Index<(usize, usize)> for Matrix {
    type Output = i32;
    fn index(&self, (r, c): (usize, usize)) -> &i32 {
        todo!()
    }
}

impl IndexMut<(usize, usize)> for Matrix {
    fn index_mut(&mut self, (r, c): (usize, usize)) -> &mut i32 {
        todo!()
    }
}
', '&self.data[r * self.w + c] и &mut …', '{"driver": "fn main() {\n    let mut m = Matrix { w: 3, data: vec![0; 6] };\n    m[(1, 2)] = 7;\n    m[(0, 0)] += 5;\n    println!(\"{} {} {}\", m[(1, 2)], m[(0, 0)], m[(1, 1)]);\n    println!(\"{:?}\", m.data);\n}\n", "expected": ["7 5 0", "[5, 0, 0, 0, 0, 7]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-fraction', 15, 'rust', 'Дробь', 'Структура Frac { n: i64, d: i64 } с функцией new(n, d) -> Frac, сокращающей дробь по НОД и держащей знаменатель положительным, и операторами Add, Mul, а также Display «n/d» (при d = 1 — просто «n»).', 'use std::fmt;
use std::ops::{Add, Mul};

#[derive(Debug, Clone, Copy, PartialEq)]
struct Frac {
    n: i64,
    d: i64,
}

fn gcd(a: i64, b: i64) -> i64 {
    if b == 0 { a.abs() } else { gcd(b, a % b) }
}

impl Frac {
    fn new(n: i64, d: i64) -> Frac {
        todo!()
    }
}

impl Add for Frac {
    type Output = Frac;
    fn add(self, o: Frac) -> Frac {
        todo!()
    }
}

impl Mul for Frac {
    type Output = Frac;
    fn mul(self, o: Frac) -> Frac {
        todo!()
    }
}

impl fmt::Display for Frac {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}
', 'Сначала сокращайте по НОД, затем нормализуйте знак знаменателя.', '{"driver": "fn main() {\n    let a = Frac::new(1, 2);\n    let b = Frac::new(1, 3);\n    println!(\"{}\", a + b);\n    println!(\"{}\", a * b);\n    println!(\"{}\", Frac::new(2, 4));\n    println!(\"{}\", Frac::new(3, -6));\n    println!(\"{}\", Frac::new(1, 2) + Frac::new(1, 2));\n}\n", "expected": ["5/6", "1/6", "1/2", "-1/2", "1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-iterator', 16, 'rust', 'Свой итератор', 'Структура Countdown { n: u32 } реализует Iterator<Item = u32>: next() отдаёт n, n−1, …, 1, затем None.', 'struct Countdown {
    n: u32,
}

impl Iterator for Countdown {
    type Item = u32;
    fn next(&mut self) -> Option<u32> {
        todo!()
    }
}
', 'Состояние хранится в self; когда n == 0 — None. Остальные методы итератора достаются даром.', '{"driver": "fn main() {\n    for x in (Countdown { n: 3 }) {\n        print!(\"{} \", x);\n    }\n    println!();\n    let s: u32 = Countdown { n: 100 }.sum();\n    println!(\"{}\", s);\n    let v: Vec<u32> = Countdown { n: 5 }.filter(|x| x % 2 == 1).collect();\n    println!(\"{:?}\", v);\n}\n", "expected": ["3 2 1", "5050", "[5, 3, 1]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-fib-iter', 17, 'rust', 'Итератор Фибоначчи', 'Структура Fib { a: u64, b: u64 } реализует Iterator<Item = u64>: 0, 1, 1, 2, 3, 5, … (бесконечный). Добавьте функцию fib() -> Fib, возвращающую начальное состояние.', 'struct Fib {
    a: u64,
    b: u64,
}

fn fib() -> Fib {
    todo!()
}

impl Iterator for Fib {
    type Item = u64;
    fn next(&mut self) -> Option<u64> {
        todo!()
    }
}
', 'Бесконечный итератор — всегда Some; ограничивает take.', '{"driver": "fn main() {\n    let v: Vec<u64> = fib().take(10).collect();\n    println!(\"{:?}\", v);\n    println!(\"{:?}\", fib().skip(50).next());\n    println!(\"{:?}\", fib().take_while(|&x| x < 100).last());\n}\n", "expected": ["[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]", "Some(12586269025)", "Some(89)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-drop', 18, 'rust', 'Drop', 'Структура Noisy { name: String } печатает при уничтожении «drop <имя>». Реализуйте Drop; порядок вывода покажет driver.', 'struct Noisy {
    name: String,
}

impl Drop for Noisy {
    fn drop(&mut self) {
        todo!()
    }
}
', 'println!("drop {}", self.name)', '{"driver": "fn main() {\n    let _a = Noisy { name: String::from(\"a\") };\n    {\n        let _b = Noisy { name: String::from(\"b\") };\n        println!(\"inner\");\n    }\n    let c = Noisy { name: String::from(\"c\") };\n    drop(c);\n    println!(\"end\");\n}\n", "expected": ["inner", "drop b", "drop c", "end", "drop a"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-default', 19, 'rust', 'Default', 'Структура Settings { volume: u8, name: String, muted: bool } с derive(Debug, Default). Добавьте derive и напишите функцию quiet() -> Settings: значения по умолчанию, но muted = true (через ..Default::default()).', 'struct Settings {
    volume: u8,
    name: String,
    muted: bool,
}

fn quiet() -> Settings {
    todo!()
}
', '#[derive(Debug, Default)] и ..Default::default().', '{"driver": "fn main() {\n    println!(\"{:?}\", Settings::default());\n    println!(\"{:?}\", quiet());\n}\n", "expected": ["Settings { volume: 0, name: \"\", muted: false }", "Settings { volume: 0, name: \"\", muted: true }"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-builder', 20, 'rust', 'Строитель с цепочкой', 'Структура Pizza { size: u32, cheese: bool, toppings: Vec<String> }. Напишите Pizza::new(size), методы with_cheese(mut self) -> Pizza и with_topping(mut self, t: &str) -> Pizza, а также describe(&self) -> String вида «30 см, сыр, начинки: гриб, лук» (без сыра — без «сыр»; без начинок — без «начинки»).', 'struct Pizza {
    size: u32,
    cheese: bool,
    toppings: Vec<String>,
}

impl Pizza {
    fn new(size: u32) -> Pizza {
        todo!()
    }
    fn with_cheese(mut self) -> Pizza {
        todo!()
    }
    fn with_topping(mut self, t: &str) -> Pizza {
        todo!()
    }
    fn describe(&self) -> String {
        todo!()
    }
}
', 'Методы-строители принимают self по значению и возвращают его.', '{"driver": "fn main() {\n    println!(\"{}\", Pizza::new(30).with_cheese().with_topping(\"гриб\").with_topping(\"лук\").describe());\n    println!(\"{}\", Pizza::new(25).describe());\n    println!(\"{}\", Pizza::new(40).with_topping(\"ананас\").describe());\n}\n", "expected": ["30 см, сыр, начинки: гриб, лук", "25 см", "40 см, начинки: ананас"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-newtype', 21, 'rust', 'Newtype: обёртка вектора', 'Реализуйте fmt::Display для обёртки struct Wrapper(Vec<String>): вывод «[a, b, c]» (элементы через запятую с пробелом).', 'use std::fmt;

struct Wrapper(Vec<String>);

impl fmt::Display for Wrapper {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}
', 'self.0 — вектор внутри обёртки.', '{"driver": "fn main() {\n    let w = Wrapper(vec![String::from(\"a\"), String::from(\"b\"), String::from(\"c\")]);\n    println!(\"{}\", w);\n    println!(\"{}\", Wrapper(vec![]));\n}\n", "expected": ["[a, b, c]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-stack-struct', 22, 'rust', 'Стек как структура', 'Структура Stack { items: Vec<i32> } с методами new(), push(&mut self, x), pop(&mut self) -> Option<i32>, peek(&self) -> Option<i32>, len(&self) -> usize и is_empty(&self) -> bool.', 'struct Stack {
    items: Vec<i32>,
}

impl Stack {
    fn new() -> Stack {
        todo!()
    }
    fn push(&mut self, x: i32) {
        todo!()
    }
    fn pop(&mut self) -> Option<i32> {
        todo!()
    }
    fn peek(&self) -> Option<i32> {
        todo!()
    }
    fn len(&self) -> usize {
        todo!()
    }
    fn is_empty(&self) -> bool {
        todo!()
    }
}
', 'Методы делегируют вектору внутри.', '{"driver": "fn main() {\n    let mut s = Stack::new();\n    println!(\"{} {:?}\", s.is_empty(), s.pop());\n    s.push(1);\n    s.push(2);\n    println!(\"{:?} {}\", s.peek(), s.len());\n    println!(\"{:?} {:?} {:?}\", s.pop(), s.pop(), s.pop());\n}\n", "expected": ["true None", "Some(2) 2", "Some(2) Some(1) None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-queue-struct', 23, 'rust', 'Очередь на двух стеках', 'Реализуйте очередь Queue { inbox: Vec<i32>, outbox: Vec<i32> } с push(x), pop() -> Option<i32> (FIFO) и len(). Когда outbox пуст, переложите в него все элементы inbox в обратном порядке.', 'struct Queue {
    inbox: Vec<i32>,
    outbox: Vec<i32>,
}

impl Queue {
    fn new() -> Queue {
        todo!()
    }
    fn push(&mut self, x: i32) {
        todo!()
    }
    fn pop(&mut self) -> Option<i32> {
        todo!()
    }
    fn len(&self) -> usize {
        todo!()
    }
}
', 'Перекладывание из inbox в outbox переворачивает порядок.', '{"driver": "fn main() {\n    let mut q = Queue::new();\n    q.push(1);\n    q.push(2);\n    q.push(3);\n    println!(\"{:?}\", q.pop());\n    q.push(4);\n    println!(\"{:?} {:?} {:?} {:?}\", q.pop(), q.pop(), q.pop(), q.pop());\n    println!(\"{}\", q.len());\n}\n", "expected": ["Some(1)", "Some(2) Some(3) Some(4) None", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-trait-plugins', 24, 'rust', 'Плагины', 'Трейт Plugin { fn name(&self) -> String; fn run(&self, x: i32) -> i32; }. Структуры Doubler и AddN { n: i32 } его реализуют (имена «doubler» и «add»). Функция pipeline(ps: &[Box<dyn Plugin>], x: i32) -> i32 последовательно применяет плагины.', 'trait Plugin {
    fn name(&self) -> String;
    fn run(&self, x: i32) -> i32;
}

struct Doubler;
struct AddN {
    n: i32,
}

impl Plugin for Doubler {
    fn name(&self) -> String {
        todo!()
    }
    fn run(&self, x: i32) -> i32 {
        todo!()
    }
}

impl Plugin for AddN {
    fn name(&self) -> String {
        todo!()
    }
    fn run(&self, x: i32) -> i32 {
        todo!()
    }
}

fn pipeline(ps: &[Box<dyn Plugin>], x: i32) -> i32 {
    todo!()
}
', 'Цикл по &[Box<dyn Plugin>] и вызов p.run(v).', '{"driver": "fn main() {\n    let ps: Vec<Box<dyn Plugin>> = vec![Box::new(Doubler), Box::new(AddN { n: 5 }), Box::new(Doubler)];\n    println!(\"{}\", pipeline(&ps, 3));\n    let names: Vec<String> = ps.iter().map(|p| p.name()).collect();\n    println!(\"{}\", names.join(\",\"));\n}\n", "expected": ["22", "doubler,add,doubler"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-generic-trait', 25, 'rust', 'Обобщённая функция с трейтом', 'Напишите функцию largest<T: PartialOrd + Copy>(v: &[T]) -> T, возвращающую наибольший элемент среза (не пуст). Она должна работать и для i32, и для f64, и для char.', 'fn largest<T: PartialOrd + Copy>(v: &[T]) -> T {
    todo!()
}
', 'Ограничение T: PartialOrd + Copy позволяет сравнивать и копировать.', '{"driver": "fn main() {\n    println!(\"{}\", largest(&[3, 9, 2]));\n    println!(\"{}\", largest(&[1.5, -2.0]));\n    println!(\"{}\", largest(&[''a'', ''я'', ''z'']));\n}\n", "expected": ["9", "1.5", "я"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-from-trait', 26, 'rust', 'From для преобразований', 'Структура Celsius(f64) и Fahrenheit(f64). Реализуйте From<Celsius> for Fahrenheit (c · 9/5 + 32); тогда Fahrenheit::from(c) и c.into() работают.', 'struct Celsius(f64);
struct Fahrenheit(f64);

impl From<Celsius> for Fahrenheit {
    fn from(c: Celsius) -> Fahrenheit {
        todo!()
    }
}
', 'Fahrenheit(c.0 * 9.0 / 5.0 + 32.0)', '{"driver": "fn main() {\n    let f = Fahrenheit::from(Celsius(100.0));\n    println!(\"{}\", f.0);\n    let g: Fahrenheit = Celsius(-40.0).into();\n    println!(\"{}\", g.0);\n}\n", "expected": ["212", "-40"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-partial-eq-manual', 27, 'rust', 'Своё равенство', 'Структура Name(String): два имени равны без учёта регистра. Реализуйте PartialEq вручную (метод eq).', 'struct Name(String);

impl PartialEq for Name {
    fn eq(&self, other: &Name) -> bool {
        todo!()
    }
}
', 'Сравнивайте нижние регистры строк.', '{"driver": "fn main() {\n    let a = Name(String::from(\"Аня\"));\n    let b = Name(String::from(\"аНЯ\"));\n    let c = Name(String::from(\"Боря\"));\n    println!(\"{}\", a == b);\n    println!(\"{}\", a == c);\n    println!(\"{}\", a != c);\n}\n", "expected": ["true", "false", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-partial-ord-manual', 28, 'rust', 'Своя сортировка', 'Структура Prio(u32): порядок обратный — большее число «меньше» (идёт раньше). Реализуйте PartialOrd вручную (partial_cmp). PartialEq выведен через derive.', '#[derive(PartialEq, Debug)]
struct Prio(u32);

impl PartialOrd for Prio {
    fn partial_cmp(&self, other: &Prio) -> Option<std::cmp::Ordering> {
        todo!()
    }
}
', 'Поменяйте местами операнды: other.0.partial_cmp(&self.0).', '{"driver": "fn main() {\n    let mut v = vec![Prio(2), Prio(9), Prio(5)];\n    v.sort_by(|a, b| a.partial_cmp(b).unwrap());\n    println!(\"{:?}\", v);\n    println!(\"{}\", Prio(9) < Prio(2));\n}\n", "expected": ["[Prio(9), Prio(5), Prio(2)]", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 13, 'r13-trait-zero', 29, 'rust', 'Трейт со статической функцией', 'Трейт Zero { fn zero() -> Self; }. Реализуйте его для i32 и f64. Функция sum_all<T: Zero + std::ops::Add<Output = T> + Copy>(v: &[T]) -> T складывает элементы, начиная с T::zero().', 'trait Zero {
    fn zero() -> Self;
}

impl Zero for i32 {
    fn zero() -> i32 {
        todo!()
    }
}

impl Zero for f64 {
    fn zero() -> f64 {
        todo!()
    }
}

fn sum_all<T: Zero + std::ops::Add<Output = T> + Copy>(v: &[T]) -> T {
    todo!()
}
', 'T::zero() вызывается через имя параметра типа.', '{"driver": "fn main() {\n    println!(\"{}\", sum_all(&[1, 2, 3]));\n    println!(\"{}\", sum_all(&[0.5, 0.25]));\n    println!(\"{}\", sum_all::<i32>(&[]));\n}\n", "expected": ["6", "0.75", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-word-count', 0, 'rust', 'Counter', 'Python: Counter(words). Напишите count_words(text: &str) -> Vec<(String, usize)>: частоты слов (split_whitespace, в нижнем регистре), по убыванию частоты, при равных — по алфавиту.', 'use std::collections::HashMap;

fn count_words(text: &str) -> Vec<(String, usize)> {
    todo!()
}
', 'entry().or_insert(0) и сортировка пар.', '{"driver": "fn main() {\n    println!(\"{:?}\", count_words(\"a b A c b a\"));\n    println!(\"{:?}\", count_words(\"\"));\n}\n", "expected": ["[(\"a\", 3), (\"b\", 2), (\"c\", 1)]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-get-default', 1, 'rust', 'd.get(k, default)', 'Python: d.get(k, 0). Напишите lookup(m: &HashMap<String, i32>, k: &str) -> i32 — значение по ключу или 0.', 'use std::collections::HashMap;

fn lookup(m: &HashMap<String, i32>, k: &str) -> i32 {
    todo!()
}
', 'get(k).copied().unwrap_or(0)', '{"driver": "fn main() {\n    let mut m = HashMap::new();\n    m.insert(String::from(\"a\"), 5);\n    println!(\"{}\", lookup(&m, \"a\"));\n    println!(\"{}\", lookup(&m, \"z\"));\n}\n", "expected": ["5", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-invert', 2, 'rust', 'Инвертировать словарь', 'Python: {v: k for k, v in d.items()}. Напишите invert(m: &HashMap<String, i32>) -> HashMap<i32, String> (значения уникальны).', 'use std::collections::HashMap;

fn invert(m: &HashMap<String, i32>) -> HashMap<i32, String> {
    todo!()
}
', 'iter().map(|(k, v)| (*v, k.clone())).collect()', '{"driver": "fn main() {\n    let mut m = HashMap::new();\n    m.insert(String::from(\"a\"), 1);\n    m.insert(String::from(\"b\"), 2);\n    let r = invert(&m);\n    println!(\"{} {} {}\", r.len(), r[&1], r[&2]);\n}\n", "expected": ["2 a b"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-group-by-len', 3, 'rust', 'Группировка по длине', 'Python: defaultdict(list). Напишите group_by_len(words: &[&str]) -> BTreeMap<usize, Vec<String>>: слова по длине в символах (внутри — в исходном порядке).', 'use std::collections::BTreeMap;

fn group_by_len(words: &[&str]) -> BTreeMap<usize, Vec<String>> {
    todo!()
}
', 'entry(len).or_default().push(…)', '{"driver": "fn main() {\n    println!(\"{:?}\", group_by_len(&[\"a\", \"bb\", \"c\", \"dd\", \"eee\"]));\n    println!(\"{:?}\", group_by_len(&[]));\n}\n", "expected": ["{1: [\"a\", \"c\"], 2: [\"bb\", \"dd\"], 3: [\"eee\"]}", "{}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-anagram-groups', 4, 'rust', 'Группы анаграмм', 'Напишите group_anagrams(words: &[&str]) -> Vec<Vec<String>>: слова-анаграммы вместе; группы отсортированы по первому слову, слова внутри групп — в исходном порядке. Ключ — отсортированные буквы.', 'use std::collections::HashMap;

fn group_anagrams(words: &[&str]) -> Vec<Vec<String>> {
    todo!()
}
', 'Ключ Vec<char> — подходит: Vec реализует Hash.', '{"driver": "fn main() {\n    println!(\"{:?}\", group_anagrams(&[\"tea\", \"eat\", \"tan\", \"ate\", \"nat\", \"bat\"]));\n}\n", "expected": ["[[\"bat\"], [\"tan\", \"nat\"], [\"tea\", \"eat\", \"ate\"]]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-two-sum-map', 5, 'rust', 'Два числа за один проход', 'Напишите two_sum(v: &[i32], target: i32) -> Option<(usize, usize)>: индексы (i, j), i < j, с v[i] + v[j] = target, за один проход с HashMap «значение → индекс». Для первой найденной при проходе j пары.', 'use std::collections::HashMap;

fn two_sum(v: &[i32], target: i32) -> Option<(usize, usize)> {
    todo!()
}
', 'Для каждого x ищем target - x среди уже просмотренных.', '{"driver": "fn main() {\n    println!(\"{:?}\", two_sum(&[2, 7, 11, 15], 9));\n    println!(\"{:?}\", two_sum(&[3, 2, 4], 6));\n    println!(\"{:?}\", two_sum(&[1, 2], 10));\n    let big: Vec<i32> = (0..200000).collect();\n    println!(\"{:?}\", two_sum(&big, 399997));\n}\n", "expected": ["Some((0, 1))", "Some((1, 2))", "None", "Some((199998, 199999))"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-merge-sum', 6, 'rust', 'Слияние со сложением', 'Python: Counter(a) + Counter(b). Напишите merge_sum(a: &HashMap<String, i32>, b: &HashMap<String, i32>) -> BTreeMap<String, i32>: ключи объединяются, значения при совпадении складываются.', 'use std::collections::{BTreeMap, HashMap};

fn merge_sum(a: &HashMap<String, i32>, b: &HashMap<String, i32>) -> BTreeMap<String, i32> {
    todo!()
}
', 'Обойдите обе карты и накапливайте в одну.', '{"driver": "fn main() {\n    let mut a = HashMap::new();\n    a.insert(String::from(\"x\"), 1);\n    a.insert(String::from(\"y\"), 2);\n    let mut b = HashMap::new();\n    b.insert(String::from(\"y\"), 10);\n    b.insert(String::from(\"z\"), 5);\n    println!(\"{:?}\", merge_sum(&a, &b));\n}\n", "expected": ["{\"x\": 1, \"y\": 12, \"z\": 5}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-dict-from-zip', 7, 'rust', 'dict(zip(k, v))', 'Напишите zip_map(keys: &[&str], vals: &[i32]) -> BTreeMap<String, i32> — пары по короткому из двух срезов.', 'use std::collections::BTreeMap;

fn zip_map(keys: &[&str], vals: &[i32]) -> BTreeMap<String, i32> {
    todo!()
}
', 'zip + collect в BTreeMap.', '{"driver": "fn main() {\n    println!(\"{:?}\", zip_map(&[\"a\", \"b\", \"c\"], &[1, 2]));\n    println!(\"{:?}\", zip_map(&[], &[1]));\n}\n", "expected": ["{\"a\": 1, \"b\": 2}", "{}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-top-n', 8, 'rust', 'Топ слов', 'Напишите top_words(text: &str, n: usize) -> Vec<String>: n самых частых слов (в нижнем регистре); при равных частотах — по алфавиту.', 'use std::collections::HashMap;

fn top_words(text: &str, n: usize) -> Vec<String> {
    todo!()
}
', 'Сначала счёт, затем sort_by и take(n).', '{"driver": "fn main() {\n    println!(\"{:?}\", top_words(\"the cat and the dog and the bird\", 2));\n    println!(\"{:?}\", top_words(\"a b c\", 5));\n    println!(\"{:?}\", top_words(\"\", 3));\n}\n", "expected": ["[\"the\", \"and\"]", "[\"a\", \"b\", \"c\"]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-entry-and-modify', 9, 'rust', 'and_modify', 'Напишите apply(events: &[(&str, i32)]) -> BTreeMap<String, i32>: для каждого события (ключ, значение) — если ключ уже есть, прибавить значение, иначе поставить его (and_modify + or_insert).', 'use std::collections::BTreeMap;

fn apply(events: &[(&str, i32)]) -> BTreeMap<String, i32> {
    todo!()
}
', 'm.entry(k).and_modify(|e| *e += v).or_insert(v)', '{"driver": "fn main() {\n    println!(\"{:?}\", apply(&[(\"a\", 1), (\"b\", 2), (\"a\", 10)]));\n    println!(\"{:?}\", apply(&[]));\n}\n", "expected": ["{\"a\": 11, \"b\": 2}", "{}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-btree-range', 10, 'rust', 'Диапазон ключей', 'Напишите between(m: &BTreeMap<i32, String>, lo: i32, hi: i32) -> Vec<String>: значения для ключей из [lo, hi] по возрастанию ключа (метод range).', 'use std::collections::BTreeMap;

fn between(m: &BTreeMap<i32, String>, lo: i32, hi: i32) -> Vec<String> {
    todo!()
}
', 'm.range(lo..=hi)', '{"driver": "fn main() {\n    let mut m = BTreeMap::new();\n    for (k, v) in [(5, \"e\"), (1, \"a\"), (3, \"c\"), (4, \"d\"), (2, \"b\")] {\n        m.insert(k, v.to_string());\n    }\n    println!(\"{:?}\", between(&m, 2, 4));\n    println!(\"{:?}\", between(&m, 6, 9));\n    println!(\"{:?}\", between(&m, 0, 1));\n}\n", "expected": ["[\"b\", \"c\", \"d\"]", "[]", "[\"a\"]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-first-last', 11, 'rust', 'Минимальный и максимальный ключ', 'Напишите extremes(m: &BTreeMap<i32, i32>) -> Option<(i32, i32)>: (наименьший ключ, наибольший ключ) или None для пустой карты (first_key_value, last_key_value).', 'use std::collections::BTreeMap;

fn extremes(m: &BTreeMap<i32, i32>) -> Option<(i32, i32)> {
    todo!()
}
', 'first_key_value() возвращает Option<(&K, &V)>.', '{"driver": "fn main() {\n    let mut m = BTreeMap::new();\n    println!(\"{:?}\", extremes(&m));\n    m.insert(5, 0);\n    m.insert(-2, 1);\n    m.insert(9, 2);\n    println!(\"{:?}\", extremes(&m));\n}\n", "expected": ["None", "Some((-2, 9))"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-set-ops', 12, 'rust', 'Операции над множествами', 'Напишите set_ops(a: &[i32], b: &[i32]) -> (Vec<i32>, Vec<i32>, Vec<i32>): объединение, пересечение и разность a − b, каждый результат отсортирован по возрастанию.', 'use std::collections::HashSet;

fn set_ops(a: &[i32], b: &[i32]) -> (Vec<i32>, Vec<i32>, Vec<i32>) {
    todo!()
}
', 'union, intersection, difference — итераторы; соберите в Vec и отсортируйте.', '{"driver": "fn main() {\n    println!(\"{:?}\", set_ops(&[1, 2, 3, 3], &[3, 4, 5]));\n    println!(\"{:?}\", set_ops(&[], &[1]));\n}\n", "expected": ["([1, 2, 3, 4, 5], [3], [1, 2])", "([1], [], [])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-unique-count', 13, 'rust', 'Сколько различных', 'Python: len(set(l)). Напишите distinct(v: &[i32]) -> usize.', 'use std::collections::HashSet;

fn distinct(v: &[i32]) -> usize {
    todo!()
}
', 'collect в HashSet и len().', '{"driver": "fn main() {\n    println!(\"{}\", distinct(&[1, 2, 2, 3, 3, 3]));\n    println!(\"{}\", distinct(&[]));\n    let big: Vec<i32> = (0..300000).map(|x| x % 1000).collect();\n    println!(\"{}\", distinct(&big));\n}\n", "expected": ["3", "0", "1000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-has-duplicates', 14, 'rust', 'Есть ли дубликаты', 'Напишите has_duplicates(v: &[i32]) -> bool за линейное время: HashSet и ранний выход при повторе (insert возвращает false).', 'use std::collections::HashSet;

fn has_duplicates(v: &[i32]) -> bool {
    todo!()
}
', 'if !seen.insert(x) { return true; }', '{"driver": "fn main() {\n    println!(\"{}\", has_duplicates(&[1, 2, 3]));\n    println!(\"{}\", has_duplicates(&[1, 2, 1]));\n    let big: Vec<i32> = (0..500000).collect();\n    println!(\"{}\", has_duplicates(&big));\n}\n", "expected": ["false", "true", "false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-common-chars', 15, 'rust', 'Общие буквы', 'Напишите common(a: &str, b: &str) -> String: буквы, которые есть в обеих строках (без повторов), по алфавиту.', 'use std::collections::HashSet;

fn common(a: &str, b: &str) -> String {
    todo!()
}
', 'Пересечение двух HashSet<char>.', '{"driver": "fn main() {\n    println!(\"{}\", common(\"hello\", \"world\"));\n    println!(\"[{}]\", common(\"abc\", \"xyz\"));\n    println!(\"{}\", common(\"привет\", \"тире\"));\n}\n", "expected": ["lo", "[]", "еирт"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-pangram', 16, 'rust', 'Панграмма', 'Напишите is_pangram(s: &str) -> bool: содержит ли строка все 26 букв латиницы (регистр не важен).', 'use std::collections::HashSet;

fn is_pangram(s: &str) -> bool {
    todo!()
}
', 'Соберите множество букв и проверьте размер.', '{"driver": "fn main() {\n    println!(\"{}\", is_pangram(\"The quick brown fox jumps over the lazy dog\"));\n    println!(\"{}\", is_pangram(\"hello world\"));\n    println!(\"{}\", is_pangram(\"\"));\n}\n", "expected": ["true", "false", "false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-lru-like', 17, 'rust', 'Первый неповторяющийся', 'Python: Counter + проход. Напишите first_unique(v: &[i32]) -> Option<i32>: первый элемент, встречающийся ровно один раз.', 'use std::collections::HashMap;

fn first_unique(v: &[i32]) -> Option<i32> {
    todo!()
}
', 'Первый проход считает, второй ищет count == 1.', '{"driver": "fn main() {\n    println!(\"{:?}\", first_unique(&[4, 5, 4, 6, 5, 7]));\n    println!(\"{:?}\", first_unique(&[1, 1]));\n    println!(\"{:?}\", first_unique(&[]));\n}\n", "expected": ["Some(6)", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-char-histogram', 18, 'rust', 'Гистограмма символов', 'Напишите histogram(s: &str) -> BTreeMap<char, usize>: сколько раз встречается каждый символ (без пробелов).', 'use std::collections::BTreeMap;

fn histogram(s: &str) -> BTreeMap<char, usize> {
    todo!()
}
', 'BTreeMap хранит ключи отсортированными.', '{"driver": "fn main() {\n    println!(\"{:?}\", histogram(\"hello world\"));\n    println!(\"{:?}\", histogram(\"\"));\n}\n", "expected": ["{''d'': 1, ''e'': 1, ''h'': 1, ''l'': 3, ''o'': 2, ''r'': 1, ''w'': 1}", "{}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-inventory', 19, 'rust', 'Склад', 'Напишите update_stock(stock: &mut HashMap<String, u32>, op: &str, item: &str, n: u32) -> Result<(), String>: «add» увеличивает остаток; «take» уменьшает (Err("нет товара"), если ключа нет, и Err("мало"), если остаток меньше n; при остатке 0 ключ удаляется); иные операции — Err("операция").', 'use std::collections::HashMap;

fn update_stock(stock: &mut HashMap<String, u32>, op: &str, item: &str, n: u32) -> Result<(), String> {
    todo!()
}
', 'get_mut даёт &mut значения; remove при нуле.', '{"driver": "fn main() {\n    let mut s = HashMap::new();\n    println!(\"{:?}\", update_stock(&mut s, \"add\", \"гвозди\", 10));\n    println!(\"{:?}\", update_stock(&mut s, \"take\", \"гвозди\", 4));\n    println!(\"{:?}\", update_stock(&mut s, \"take\", \"гвозди\", 7));\n    println!(\"{:?}\", update_stock(&mut s, \"take\", \"болты\", 1));\n    println!(\"{:?}\", update_stock(&mut s, \"take\", \"гвозди\", 6));\n    println!(\"{}\", s.len());\n    println!(\"{:?}\", update_stock(&mut s, \"sell\", \"x\", 1));\n}\n", "expected": ["Ok(())", "Ok(())", "Err(\"мало\")", "Err(\"нет товара\")", "Ok(())", "0", "Err(\"операция\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-index', 20, 'rust', 'Индекс слов', 'Напишите build_index(docs: &[&str]) -> BTreeMap<String, Vec<usize>>: для каждого слова (в нижнем регистре) — номера документов (с 0, без повторов, по возрастанию), где оно встречается.', 'use std::collections::BTreeMap;

fn build_index(docs: &[&str]) -> BTreeMap<String, Vec<usize>> {
    todo!()
}
', 'Проверьте last() перед push, чтобы не дублировать номер.', '{"driver": "fn main() {\n    println!(\"{:?}\", build_index(&[\"Rust is fast\", \"rust is safe\", \"Go is fast fast\"]));\n}\n", "expected": ["{\"fast\": [0, 2], \"go\": [2], \"is\": [0, 1, 2], \"rust\": [0, 1], \"safe\": [1]}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-memo-fib', 21, 'rust', 'Мемоизация', 'Напишите fib(n: u64, memo: &mut HashMap<u64, u64>) -> u64 с мемоизацией (аналог @lru_cache): fib(0)=0, fib(1)=1. Для n = 90 вычисление мгновенно.', 'use std::collections::HashMap;

fn fib(n: u64, memo: &mut HashMap<u64, u64>) -> u64 {
    todo!()
}
', 'Сначала смотрим в memo, потом считаем и сохраняем.', '{"driver": "fn main() {\n    let mut memo = HashMap::new();\n    println!(\"{}\", fib(10, &mut memo));\n    println!(\"{}\", fib(90, &mut memo));\n    println!(\"{}\", memo.len());\n}\n", "expected": ["55", "2880067194370816120", "89"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-lookup-table', 22, 'rust', 'Таблица соответствий', 'Напишите roman_to_int(s: &str) -> u32: римское число в обычное (I=1, V=5, X=10, L=50, C=100, D=500, M=1000; меньшая цифра перед большей вычитается). Используйте HashMap<char, u32> или match.', 'use std::collections::HashMap;

fn roman_to_int(s: &str) -> u32 {
    todo!()
}
', 'Если следующая цифра больше, текущую вычитаем.', '{"driver": "fn main() {\n    for s in [\"III\", \"IV\", \"IX\", \"LVIII\", \"MCMXCIV\", \"MMXXVI\"] {\n        println!(\"{} {}\", s, roman_to_int(s));\n    }\n}\n", "expected": ["III 3", "IV 4", "IX 9", "LVIII 58", "MCMXCIV 1994", "MMXXVI 2026"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-cache', 23, 'rust', 'Кэш с лимитом', 'Реализуйте структуру Cache с полями map: HashMap<String, i32>, order: Vec<String>, cap: usize. Функция new(cap) создаёт пустой кэш; put(&mut self, k: &str, v: i32) добавляет пару и при превышении cap вытесняет самый старый ключ (FIFO); при обновлении существующего ключа порядок не меняется; get(&self, k: &str) -> Option<i32>.', 'use std::collections::HashMap;

struct Cache {
    map: HashMap<String, i32>,
    order: Vec<String>,
    cap: usize,
}

impl Cache {
    fn new(cap: usize) -> Cache {
        todo!()
    }
    fn put(&mut self, k: &str, v: i32) {
        todo!()
    }
    fn get(&self, k: &str) -> Option<i32> {
        todo!()
    }
}
', 'При вытеснении удалите первый элемент order и его ключ в map.', '{"driver": "fn main() {\n    let mut c = Cache::new(2);\n    c.put(\"a\", 1);\n    c.put(\"b\", 2);\n    c.put(\"a\", 10);\n    c.put(\"c\", 3);\n    println!(\"{:?} {:?} {:?}\", c.get(\"a\"), c.get(\"b\"), c.get(\"c\"));\n}\n", "expected": ["None Some(2) Some(3)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-bimap', 24, 'rust', 'Двунаправленное соответствие', 'Напишите is_isomorphic(a: &str, b: &str) -> bool: можно ли заменить буквы a на буквы b так, чтобы получить b (каждая буква отображается в одну и ту же, разные — в разные; строки одной длины).', 'use std::collections::HashMap;

fn is_isomorphic(a: &str, b: &str) -> bool {
    todo!()
}
', 'Две карты: a → b и b → a.', '{"driver": "fn main() {\n    println!(\"{}\", is_isomorphic(\"egg\", \"add\"));\n    println!(\"{}\", is_isomorphic(\"foo\", \"bar\"));\n    println!(\"{}\", is_isomorphic(\"paper\", \"title\"));\n    println!(\"{}\", is_isomorphic(\"ab\", \"aa\"));\n    println!(\"{}\", is_isomorphic(\"\", \"\"));\n}\n", "expected": ["true", "false", "true", "false", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-graph-degrees', 25, 'rust', 'Степени вершин графа', 'Напишите degrees(edges: &[(u32, u32)]) -> BTreeMap<u32, usize>: степень каждой вершины неориентированного графа (каждое ребро увеличивает степень обоих концов; петля (v, v) считается дважды).', 'use std::collections::BTreeMap;

fn degrees(edges: &[(u32, u32)]) -> BTreeMap<u32, usize> {
    todo!()
}
', 'Два entry на ребро.', '{"driver": "fn main() {\n    println!(\"{:?}\", degrees(&[(1, 2), (2, 3), (3, 1), (3, 4)]));\n    println!(\"{:?}\", degrees(&[(5, 5)]));\n    println!(\"{:?}\", degrees(&[]));\n}\n", "expected": ["{1: 2, 2: 2, 3: 3, 4: 1}", "{5: 2}", "{}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-adjacency', 26, 'rust', 'Список смежности', 'Напишите adjacency(edges: &[(u32, u32)]) -> BTreeMap<u32, Vec<u32>>: для каждой вершины — отсортированный список соседей неориентированного графа без повторов.', 'use std::collections::BTreeMap;

fn adjacency(edges: &[(u32, u32)]) -> BTreeMap<u32, Vec<u32>> {
    todo!()
}
', 'or_default().push в обе стороны; потом sort и dedup.', '{"driver": "fn main() {\n    println!(\"{:?}\", adjacency(&[(1, 2), (1, 3), (2, 3), (1, 2)]));\n    println!(\"{:?}\", adjacency(&[]));\n}\n", "expected": ["{1: [2, 3], 2: [1, 3], 3: [1, 2]}", "{}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-sorted-by-value', 27, 'rust', 'Сортировка по значению', 'Python: sorted(d.items(), key=lambda kv: kv[1]). Напишите by_value(m: &HashMap<String, i32>) -> Vec<(String, i32)>: пары по возрастанию значения, при равных — по ключу.', 'use std::collections::HashMap;

fn by_value(m: &HashMap<String, i32>) -> Vec<(String, i32)> {
    todo!()
}
', 'sort_by с then для разрешения равенства.', '{"driver": "fn main() {\n    let mut m = HashMap::new();\n    m.insert(String::from(\"b\"), 2);\n    m.insert(String::from(\"a\"), 2);\n    m.insert(String::from(\"c\"), -1);\n    println!(\"{:?}\", by_value(&m));\n}\n", "expected": ["[(\"c\", -1), (\"a\", 2), (\"b\", 2)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-struct-key', 28, 'rust', 'Структура как ключ', 'Добавьте структуре Pos { x: i32, y: i32 } нужные derive (Hash, PartialEq, Eq, Clone, Copy, Debug) и напишите visited(path: &[(i32, i32)]) -> usize: сколько различных клеток посещено (HashSet<Pos>).', 'use std::collections::HashSet;

struct Pos {
    x: i32,
    y: i32,
}

fn visited(path: &[(i32, i32)]) -> usize {
    todo!()
}
', '#[derive(Hash, PartialEq, Eq)] делает структуру пригодной как ключ.', '{"driver": "fn main() {\n    println!(\"{}\", visited(&[(0, 0), (1, 0), (1, 1), (0, 0), (1, 0)]));\n    println!(\"{}\", visited(&[]));\n}\n", "expected": ["3", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 14, 'r14-sym-diff', 29, 'rust', 'Что изменилось', 'Напишите changed(old: &[&str], new: &[&str]) -> Vec<String>: слова, которые есть ровно в одном из списков (симметрическая разность), по алфавиту.', 'use std::collections::HashSet;

fn changed(old: &[&str], new: &[&str]) -> Vec<String> {
    todo!()
}
', 'symmetric_difference возвращает итератор.', '{"driver": "fn main() {\n    println!(\"{:?}\", changed(&[\"a\", \"b\", \"c\"], &[\"b\", \"c\", \"d\"]));\n    println!(\"{:?}\", changed(&[\"x\"], &[\"x\"]));\n}\n", "expected": ["[\"a\", \"d\"]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-drop-impl', 0, 'rust', 'Drop: убираем за собой', 'Тип Guard хранит имя. Реализуйте для него Drop так, чтобы при уничтожении печаталась строка «drop <имя>». Остальное сделает компилятор: он сам вставит вызовы на закрывающих скобках и в обратном порядке.', 'struct Guard {
    name: String,
}

impl Drop for Guard {
    fn drop(&mut self) {
        todo!()
    }
}
', 'В drop достаточно println!("drop {}", self.name); вызывать его самому не нужно.', '{"driver": "fn main() {\n    let _a = Guard { name: String::from(\"a\") };\n    {\n        let _b = Guard { name: String::from(\"b\") };\n        let _c = Guard { name: String::from(\"c\") };\n        println!(\"inner\");\n    }\n    let d = Guard { name: String::from(\"d\") };\n    drop(d);\n    println!(\"end\");\n}\n", "expected": ["inner", "drop c", "drop b", "drop d", "end", "drop a"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-scope-order', 1, 'rust', 'Порядок уничтожения: режиссируем вывод', 'Тип Guard уже готов: new печатает «make <имя>», а при уничтожении печатается «drop <имя>». Напишите функцию scenario(), чтобы программа напечатала ровно такие строки: make a, make b, drop b, mid, make c, drop c, end, drop a. Подсказка: что-то нужно уничтожить вручную, что-то — закрывающей скобкой блока.', 'struct Guard(&''static str);

impl Guard {
    fn new(name: &''static str) -> Guard {
        println!("make {name}");
        Guard(name)
    }
}

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn scenario() {
    // ваш код
}
', 'drop(b) уничтожает b сразу; внутренний блок { … } уничтожает c на своей скобке; a живёт до конца функции.', '{"driver": "fn main() {\n    scenario();\n}\n", "expected": ["make a", "make b", "drop b", "mid", "make c", "drop c", "end", "drop a"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-move-fix', 2, 'rust', 'Исправьте: значение использовано после переезда', 'Код не компилируется: let upper = name; перемещает строку, и дальше name использовать нельзя. Исправьте describe так, чтобы функция возвращала «<исходная> -> <заглавными>»: например, «rust -> RUST».', 'fn describe(name: String) -> String {
    let upper = name;
    format!("{} -> {}", name, upper.to_uppercase())
}
', 'Нужны две независимые строки — значит, одну из них создайте через .clone().', '{"driver": "fn main() {\n    println!(\"{}\", describe(String::from(\"rust\")));\n    println!(\"{}\", describe(String::from(\"привет\")));\n}\n", "expected": ["rust -> RUST", "привет -> ПРИВЕТ"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-return-ownership', 3, 'rust', 'Вернуть владение: кортеж и цепочка', 'Функции забирают строку по значению. exclaim(s) дописывает в конец «!» и возвращает строку. measure(s) возвращает пару (строка, длина в байтах), чтобы вызывающий не потерял владение.', 'fn exclaim(s: String) -> String {
    todo!()
}

fn measure(s: String) -> (String, usize) {
    todo!()
}
', 'Параметр, который меняется, объявляют как mut s. Длину возьмите до того, как отдадите s в кортеж.', '{"driver": "fn main() {\n    let s = String::from(\"привет\");\n    let s = exclaim(s);\n    let (s, n) = measure(s);\n    println!(\"{s} {n}\");\n    let (s, n) = measure(exclaim(s));\n    println!(\"{s} {n}\");\n}\n", "expected": ["привет! 13", "привет!! 14"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-array-copy', 4, 'rust', 'Массивы и кортежи копируются', 'Массив [i32; 4] и кортеж (i32, i32) целиком лежат на стеке и копируются побитно. Напишите doubled(a) — массив с удвоенными элементами и swapped(p) — кортеж с переставленными местами числами. После вызова исходные значения остаются доступными.', 'fn doubled(a: [i32; 4]) -> [i32; 4] {
    todo!()
}

fn swapped(p: (i32, i32)) -> (i32, i32) {
    todo!()
}
', 'Параметр mut a — это локальная копия; исходный массив у вызывающего не меняется.', '{"driver": "fn main() {\n    let a = [1, 2, 3, 4];\n    let b = doubled(a);\n    println!(\"{:?} {:?}\", a, b);\n    let p = (7, 9);\n    let q = swapped(p);\n    println!(\"{:?} {:?}\", p, q);\n}\n", "expected": ["[1, 2, 3, 4] [2, 4, 6, 8]", "(7, 9) (9, 7)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-derive-copy', 5, 'rust', 'Исправьте: сделайте Point копируемым', 'Код не компилируется: Point переезжает в shift, а потом используется снова. Тип состоит из двух i32, поэтому его можно сделать Copy. Правьте только атрибут derive над структурой (Debug нужен для вывода).', '#[derive(Debug)]
struct Point {
    x: i32,
    y: i32,
}

fn shift(p: Point, dx: i32, dy: i32) -> Point {
    Point { x: p.x + dx, y: p.y + dy }
}
', '#[derive(Debug, Clone, Copy)] — Copy требует и Clone.', '{"driver": "fn main() {\n    let p = Point { x: 1, y: 2 };\n    let q = shift(p, 10, 20);\n    println!(\"{:?} {:?}\", p, q);\n    println!(\"{} байт\", std::mem::size_of::<Point>());\n}\n", "expected": ["Point { x: 1, y: 2 } Point { x: 11, y: 22 }", "8 байт"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-two-clones', 6, 'rust', 'Ровно два клона', 'Напишите triple(s) → (String, String, String): три одинаковые строки. Условие: в коде ровно два вызова .clone() — третья строка получается перемещением самой s. Каждый лишний клон — лишний malloc и memcpy.', 'fn triple(s: String) -> (String, String, String) {
    todo!()
}
', 'Порядок важен: сначала клоны, а последним — сама s, которая переезжает в кортеж.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\".clo\", \"ne()\")).count();\n    println!(\"{:?}\", triple(String::from(\"ab\")));\n    let (x, y, z) = triple(String::from(\"xyz\"));\n    println!(\"{}\", x == y && y == z);\n    println!(\"clones: {}\", bad0);\n}\n", "expected": ["(\"ab\", \"ab\", \"ab\")", "true", "clones: 2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-box-new', 7, 'rust', 'Box: значение в куче', 'Напишите boxed_sum(a, b) → Box<i32> с суммой, положенной в кучу, и unbox_double(b: Box<i32>) → i32: удвоенное значение из коробки (звёздочка разыменовывает Box).', 'fn boxed_sum(a: i32, b: i32) -> Box<i32> {
    todo!()
}

fn unbox_double(b: Box<i32>) -> i32 {
    todo!()
}
', 'Box::new(значение) кладёт значение в кучу; *b достаёт его обратно.', '{"driver": "fn main() {\n    let b = boxed_sum(20, 22);\n    println!(\"{}\", b);\n    println!(\"{}\", unbox_double(b));\n    println!(\"{} {} {}\", std::mem::size_of::<i32>(), std::mem::size_of::<Box<i32>>(), std::mem::size_of::<String>());\n}\n", "expected": ["42", "84", "4 8 24"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-box-list', 8, 'rust', 'Список на Box: рекурсивный тип', 'Перечисление List хранит голову и хвост в Box. Напишите range_list(from, to) — список from, from+1, …, to (включительно; пустой, если from > to), sum(list) — сумму, to_vec(list) — элементы в порядке списка. Функции забирают список по значению.', 'enum List {
    Cons(i32, Box<List>),
    Nil,
}
use List::{Cons, Nil};

fn range_list(from: i32, to: i32) -> List {
    todo!()
}

fn sum(list: List) -> i32 {
    match list {
        Nil => todo!(),
        Cons(v, rest) => todo!(),
    }
}

fn to_vec(list: List) -> Vec<i32> {
    todo!()
}
', '*rest достаёт список из коробки и переносит владение; на Nil рекурсия заканчивается.', '{"driver": "fn main() {\n    println!(\"{}\", sum(range_list(1, 10)));\n    println!(\"{:?}\", to_vec(range_list(3, 7)));\n    println!(\"{:?} {}\", to_vec(range_list(5, 1)), sum(Nil));\n    println!(\"{}\", std::mem::size_of::<Box<List>>());\n}\n", "expected": ["55", "[3, 4, 5, 6, 7]", "[] 0", "8"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-recursive-fix', 9, 'rust', 'Исправьте: тип бесконечного размера', 'Выражение Expr содержит другие выражения прямо внутри себя — размер такого типа бесконечен, и код не собирается. Исправьте определение enum (функция eval и её *a, *b уже написаны для Box).', 'enum Expr {
    Num(i64),
    Add(Expr, Expr),
    Mul(Expr, Expr),
}

fn eval(e: Expr) -> i64 {
    match e {
        Expr::Num(n) => n,
        Expr::Add(a, b) => eval(*a) + eval(*b),
        Expr::Mul(a, b) => eval(*a) * eval(*b),
    }
}
', 'Рекурсивные поля нужно положить в Box<Expr>: тогда размер определяется указателем.', '{"driver": "fn main() {\n    use Expr::*;\n    let e = Add(Box::new(Num(2)), Box::new(Mul(Box::new(Num(3)), Box::new(Num(4)))));\n    println!(\"{}\", eval(e));\n    println!(\"{}\", eval(Mul(Box::new(Num(-5)), Box::new(Num(6)))));\n}\n", "expected": ["14", "-30"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-field-order', 10, 'rust', 'Порядок полей — порядок drop', 'Поля структуры уничтожаются в порядке объявления. Сейчас при уничтожении Pair сначала печатается «drop right». Измените определение структуры (конструктор new не трогайте) так, чтобы сначала шло «drop left», а затем «drop right».', 'struct Guard(&''static str);

impl Guard {
    fn new(name: &''static str) -> Guard {
        println!("make {name}");
        Guard(name)
    }
}

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

struct Pair {
    right: Guard,
    left: Guard,
}

impl Pair {
    fn new() -> Pair {
        let left = Guard::new("left");
        let right = Guard::new("right");
        Pair { right, left }
    }
}
', 'Поля структуры освобождаются сверху вниз, как они записаны в определении.', '{"driver": "fn main() {\n    {\n        let _p = Pair::new();\n        println!(\"alive\");\n    }\n    println!(\"done\");\n}\n", "expected": ["make left", "make right", "alive", "drop left", "drop right", "done"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-option-take', 11, 'rust', 'Option::take: вынуть и оставить None', 'Структура Slot хранит необязательную строку. Реализуйте put(&mut self, s) — положить строку и вернуть прежнюю (Option<String>), take(&mut self) — забрать строку, оставив None, и is_empty(&self). Подсказка: у Option есть методы replace и take. Ссылки &self и &mut self — тема следующей главы: пока считайте их разрешением читать или менять Slot на месте.', 'struct Slot {
    item: Option<String>,
}

impl Slot {
    fn put(&mut self, s: String) -> Option<String> {
        todo!()
    }

    fn take(&mut self) -> Option<String> {
        todo!()
    }

    fn is_empty(&self) -> bool {
        todo!()
    }
}
', 'self.item.replace(s) и self.item.take() возвращают старое значение, не копируя его.', '{"driver": "fn main() {\n    let mut s = Slot { item: None };\n    println!(\"{:?}\", s.put(String::from(\"a\")));\n    println!(\"{:?}\", s.put(String::from(\"b\")));\n    println!(\"{:?}\", s.take());\n    println!(\"{:?} {}\", s.take(), s.is_empty());\n}\n", "expected": ["None", "Some(\"a\")", "Some(\"b\")", "None true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-mem-swap', 12, 'rust', 'mem::swap и mem::take', 'rotate(a, b, c) сдвигает значения по кругу: a получает значение b, b — значение c, c — прежнее значение a. Копировать строки нельзя — используйте std::mem::swap. drain(log) возвращает содержимое строки и оставляет её пустой (std::mem::take).', 'fn rotate(a: &mut String, b: &mut String, c: &mut String) {
    todo!()
}

fn drain(log: &mut String) -> String {
    todo!()
}
', 'Два свопа подряд: сначала (a, b), затем (b, c). mem::take оставляет String::default(), то есть пустую строку.', '{"driver": "fn main() {\n    let mut a = String::from(\"1\");\n    let mut b = String::from(\"2\");\n    let mut c = String::from(\"3\");\n    rotate(&mut a, &mut b, &mut c);\n    println!(\"{a} {b} {c}\");\n    let mut log = String::from(\"boot ok\");\n    let got = drain(&mut log);\n    println!(\"{:?} {:?}\", got, log);\n}\n", "expected": ["2 3 1", "\"boot ok\" \"\""]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-rc-count', 13, 'rust', 'Rc: много владельцев одного значения', 'Напишите share(s, n) → Vec<Rc<String>> (n ≥ 1): вектор из n владельцев ОДНОЙ строки в куче. Данные копироваться не должны: создайте один Rc, а остальные получите через Rc::clone.', 'use std::rc::Rc;

fn share(s: &str, n: usize) -> Vec<Rc<String>> {
    todo!()
}
', 'Rc::clone(&first) увеличивает счётчик и не копирует строку; последний владелец — сама first.', '{"driver": "fn main() {\n    let v = share(\"hello\", 4);\n    println!(\"{} {}\", v.len(), Rc::strong_count(&v[0]));\n    println!(\"{}\", v.iter().all(|r| Rc::ptr_eq(r, &v[0])));\n    println!(\"{}\", v[3]);\n    drop(v);\n}\n", "expected": ["4 4", "true", "hello"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-rc-drop', 14, 'rust', 'Rc: уничтожение при последнем владельце', 'Guard печатает «drop shared», когда уничтожается. Напишите fan_out(g, n) → Vec<Rc<Guard>> (n ≥ 1): n владельцев одного Guard, исходный g перемещается внутрь (клон создаёт ещё одного владельца, перемещение — нет).', 'use std::rc::Rc;

struct Guard(&''static str);

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn fan_out(g: Rc<Guard>, n: usize) -> Vec<Rc<Guard>> {
    todo!()
}
', 'Значение уничтожается ровно один раз — когда счётчик достигает нуля. Лишних клонов быть не должно.', '{"driver": "fn main() {\n    let mut v = fan_out(Rc::new(Guard(\"shared\")), 3);\n    println!(\"owners: {}\", Rc::strong_count(&v[0]));\n    v.pop();\n    println!(\"owners: {}\", Rc::strong_count(&v[0]));\n    v.pop();\n    println!(\"owners: {}\", Rc::strong_count(&v[0]));\n    println!(\"last\");\n    v.pop();\n    println!(\"end\");\n}\n", "expected": ["owners: 3", "owners: 2", "owners: 1", "last", "drop shared", "end"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-loop-move', 15, 'rust', 'Исправьте: значение переехало в первой итерации', 'Функция repeat должна вернуть n копий строки. Компилятор ругается: s перемещена в push на первой итерации цикла. Исправьте минимальной правкой.', 'fn repeat(s: String, n: usize) -> Vec<String> {
    let mut v = Vec::new();
    for _ in 0..n {
        v.push(s);
    }
    v
}
', 'В каждую ячейку нужна своя строка: push(s.clone()).', '{"driver": "fn main() {\n    println!(\"{:?}\", repeat(String::from(\"ab\"), 3));\n    println!(\"{:?}\", repeat(String::from(\"x\"), 0));\n}\n", "expected": ["[\"ab\", \"ab\", \"ab\"]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-index-move', 16, 'rust', 'Исправьте: нельзя вынуть элемент по индексу', 'split_first(names) → (String, Vec<String>): первое имя и оставшиеся. names[0] не компилируется — из вектора нельзя вынуть владение по индексу. Исправьте, не используя clone: у Vec есть метод, который удаляет элемент и отдаёт его владельцу.', 'fn split_first(mut names: Vec<String>) -> (String, Vec<String>) {
    let first = names[0];
    names.remove(0);
    (first, names)
}
', 'remove(0) удаляет элемент и возвращает его — владение переходит к вам.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\".clo\", \"ne()\")).count();\n    let (first, rest) = split_first(vec![String::from(\"anna\"), String::from(\"bob\"), String::from(\"carl\")]);\n    println!(\"first={first} rest={:?}\", rest);\n    println!(\"clones: {}\", bad0);\n}\n", "expected": ["first=anna rest=[\"bob\", \"carl\"]", "clones: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-pipeline', 17, 'rust', 'Конвейер: владение перетекает из функции в функцию', 'Напишите три функции, которые забирают вектор и возвращают его: append(v, x) — добавить в конец; dedup_sorted(v) — отсортировать по возрастанию и убрать повторы; top(v, k) — оставить k наибольших в порядке убывания.', 'fn append(v: Vec<i32>, x: i32) -> Vec<i32> {
    todo!()
}

fn dedup_sorted(v: Vec<i32>) -> Vec<i32> {
    todo!()
}

fn top(v: Vec<i32>, k: usize) -> Vec<i32> {
    todo!()
}
', 'Параметр с mut можно менять внутри; после изменения верните его, и владение уйдёт дальше по цепочке.', '{"driver": "fn main() {\n    let v = vec![5, 3, 5, 1, 9];\n    let v = append(append(v, 7), 3);\n    let v = dedup_sorted(v);\n    println!(\"{:?}\", v);\n    println!(\"{:?}\", top(v, 3));\n    println!(\"{:?}\", top(dedup_sorted(vec![2, 2, 1]), 5));\n}\n", "expected": ["[1, 3, 5, 7, 9]", "[9, 7, 5]", "[2, 1]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-struct-update', 18, 'rust', 'Структура: пересобрать с новым полем', 'Config владеет строкой. with_name(c, name) возвращает конфигурацию с новым именем и остальными полями прежними — используйте синтаксис обновления структуры «..c». into_parts(c) разбирает конфигурацию на (имя, число попыток).', '#[derive(Debug)]
struct Config {
    name: String,
    retries: u32,
    verbose: bool,
}

fn with_name(c: Config, name: &str) -> Config {
    todo!()
}

fn into_parts(c: Config) -> (String, u32) {
    todo!()
}
', 'Config { name: ..., ..c } берёт недостающие поля из c; старое имя при этом просто уничтожится.', '{"driver": "fn main() {\n    let c = Config { name: String::from(\"old\"), retries: 3, verbose: true };\n    let c = with_name(c, \"new\");\n    println!(\"{:?}\", c);\n    println!(\"{:?}\", into_parts(c));\n}\n", "expected": ["Config { name: \"new\", retries: 3, verbose: true }", "(\"new\", 3)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-shadow-drop', 19, 'rust', 'RAII: блокировка отпускается сама', 'Lock имитирует блокировку: Lock::acquire(name) печатает «lock <name>» и возвращает значение, а при уничтожении печатается «unlock <name>». Реализуйте acquire и Drop. Следите за затенением: второй let l не уничтожает первую блокировку.', 'struct Lock {
    name: String,
}

impl Lock {
    fn acquire(name: &str) -> Lock {
        todo!()
    }
}

impl Drop for Lock {
    fn drop(&mut self) {
        todo!()
    }
}
', 'Затенение скрывает имя, но не уничтожает значение: A живёт до конца функции и освобождается последней.', '{"driver": "fn main() {\n    let l = Lock::acquire(\"A\");\n    let l = Lock::acquire(\"B\");\n    {\n        let _x = Lock::acquire(\"C\");\n    }\n    println!(\"body {}\", l.name);\n}\n", "expected": ["lock A", "lock B", "lock C", "unlock C", "body B", "unlock B", "unlock A"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-underscore', 20, 'rust', 'Подчёркивание: _ и _name', 'Guard печатает «make <имя>» при создании и «drop <имя>» при уничтожении. Напишите probe() так, чтобы вывод был: make temp, drop temp, make keep, body, drop keep. Значение, присвоенное голому «_», уничтожается сразу; значение в переменной _keep живёт до конца блока.', 'struct Guard(&''static str);

impl Guard {
    fn new(name: &''static str) -> Guard {
        println!("make {name}");
        Guard(name)
    }
}

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn probe() {
    // ваш код
}
', 'let _ = … не создаёт привязки, значение умирает на этой же строке; let _keep = … привязку создаёт.', '{"driver": "fn main() {\n    probe();\n}\n", "expected": ["make temp", "drop temp", "make keep", "body", "drop keep"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-sizes', 21, 'rust', 'Copy или нет: три типа', 'Опишите три типа. Meters(f64) — копируемый. Segment { from: Meters, to: Meters } — тоже копируемый. Label { text: String } — не копируемый (владеет кучей). Добавьте нужные derive к определениям. Программа проверит Copy и напечатает размеры: 8, 24 и 16 байт.', 'struct Meters(f64);

struct Segment {
    from: Meters,
    to: Meters,
}

struct Label {
    text: String,
}
', 'Copy можно получить только у типа, все поля которого Copy; для Copy нужен ещё и Clone: #[derive(Clone, Copy)].', '{"driver": "fn need_copy<T: Copy>(_: T) {}\n\nfn main() {\n    need_copy(Meters(1.5));\n    need_copy(Segment { from: Meters(0.0), to: Meters(2.0) });\n    let l = Label { text: String::from(\"a\") };\n    let _m = l;\n    println!(\"{} {} {}\", std::mem::size_of::<Meters>(), std::mem::size_of::<Label>(), std::mem::size_of::<Segment>());\n}\n", "expected": ["8 24 16"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-capacity', 22, 'rust', 'Ёмкость растёт: String::push', 'Напишите capacity_trace(n) → Vec<usize>: создайте пустую String::new(), n раз добавьте символ ''x'' и верните все различные значения ёмкости (capacity) в порядке появления, начиная с начальной. Видно, как буфер в куче растёт рывками, а не на каждом символе.', 'fn capacity_trace(n: usize) -> Vec<usize> {
    todo!()
}
', 'Запоминайте последнее увиденное значение ёмкости и добавляйте новое только если оно изменилось.', '{"driver": "fn main() {\n    println!(\"{:?}\", capacity_trace(0));\n    println!(\"{:?}\", capacity_trace(100));\n    println!(\"{:?}\", capacity_trace(1000));\n}\n", "expected": ["[0]", "[0, 8, 16, 32, 64, 128]", "[0, 8, 16, 32, 64, 128, 256, 512, 1024]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-move-ptr', 23, 'rust', 'Переезд не трогает кучу', 'as_ptr() возвращает адрес буфера в куче. move_keeps_buffer(s) переносит строку в новую переменную и возвращает, остался ли адрес буфера тем же (true). clone_new_buffer(s) клонирует строку и возвращает, отличается ли адрес копии от адреса оригинала (true).', 'fn move_keeps_buffer(s: String) -> bool {
    todo!()
}

fn clone_new_buffer(s: String) -> bool {
    todo!()
}
', 'Запомните s.as_ptr() до переезда и сравните с as_ptr() у новой переменной.', '{"driver": "fn main() {\n    println!(\"{}\", move_keeps_buffer(String::from(\"hello world\")));\n    println!(\"{}\", clone_new_buffer(String::from(\"hello world\")));\n}\n", "expected": ["true", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-stack-list', 24, 'rust', 'Стек на связном списке из Box', 'Реализуйте стек на односвязном списке. Stack::new() — пустой; push(v) кладёт значение в начало; pop() снимает и возвращает Option<i32>; peek(&self) показывает верхнее без снятия. Хранится голова Option<Box<Node>>: при push старую голову забирайте через take().', 'struct Node {
    val: i32,
    next: Option<Box<Node>>,
}

struct Stack {
    head: Option<Box<Node>>,
}

impl Stack {
    fn new() -> Stack {
        todo!()
    }

    fn push(&mut self, v: i32) {
        todo!()
    }

    fn pop(&mut self) -> Option<i32> {
        todo!()
    }

    fn peek(&self) -> Option<i32> {
        todo!()
    }
}
', 'push: let old = self.head.take(); затем self.head = Some(Box::new(Node { val: v, next: old })). pop: take() и перенос n.next в head.', '{"driver": "fn main() {\n    let mut s = Stack::new();\n    println!(\"{:?} {:?}\", s.pop(), s.peek());\n    for i in 1..=4 {\n        s.push(i * 10);\n    }\n    println!(\"{:?}\", s.peek());\n    println!(\"{:?} {:?}\", s.pop(), s.pop());\n    s.push(99);\n    let mut out = Vec::new();\n    while let Some(v) = s.pop() {\n        out.push(v);\n    }\n    println!(\"{:?} {:?}\", out, s.peek());\n}\n", "expected": ["None None", "Some(40)", "Some(40) Some(30)", "[99, 20, 10] None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-reverse-list', 25, 'rust', 'Разворот списка перемещениями', 'Напишите reverse(head) → Option<Box<Node>>: разверните односвязный список, не создавая новых узлов и не клонируя — только переставляя указатели (владение узлов переходит по цепочке). Условие: ни одного .clone().', 'struct Node {
    val: i32,
    next: Option<Box<Node>>,
}

fn reverse(head: Option<Box<Node>>) -> Option<Box<Node>> {
    todo!()
}
', 'Идём по списку: отцепляем хвост через node.next.take(), направляем next на уже развёрнутую часть, и node становится новой головой.', '{"driver": "fn build(v: &[i32]) -> Option<Box<Node>> {\n    let mut head = None;\n    for &x in v.iter().rev() {\n        head = Some(Box::new(Node { val: x, next: head }));\n    }\n    head\n}\n\nfn dump(mut l: Option<Box<Node>>) -> Vec<i32> {\n    let mut out = Vec::new();\n    while let Some(n) = l {\n        out.push(n.val);\n        l = n.next;\n    }\n    out\n}\n\nfn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\".clo\", \"ne()\")).count();\n    println!(\"{:?}\", dump(reverse(build(&[1, 2, 3, 4, 5]))));\n    println!(\"{:?}\", dump(reverse(build(&[7]))));\n    println!(\"{:?}\", dump(reverse(build(&[]))));\n    println!(\"clones: {}\", bad0);\n}\n", "expected": ["[5, 4, 3, 2, 1]", "[7]", "[]", "clones: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-bst-insert', 26, 'rust', 'Двоичное дерево на Option<Box<…>>', 'Узел дерева владеет левым и правым поддеревом через Option<Box<TNode>>. Напишите insert(link, key) → Link: вставка в дерево поиска (повторы игнорируются), функция забирает дерево и возвращает его обратно; и in_order(link, out) — обход слева направо с записью ключей в out. Подсказка: поддерево перед рекурсией забирайте через take().', 'struct TNode {
    key: i32,
    left: Link,
    right: Link,
}

type Link = Option<Box<TNode>>;

fn insert(link: Link, key: i32) -> Link {
    todo!()
}

fn in_order(link: Link, out: &mut Vec<i32>) {
    todo!()
}
', 'Some(mut n) → сравните ключи, перезапишите n.left или n.right результатом insert(n.left.take(), key) и верните Some(n).', '{"driver": "fn main() {\n    let mut root: Link = None;\n    for k in [5, 3, 8, 1, 4, 7, 9, 3, 5] {\n        root = insert(root, k);\n    }\n    let mut out = Vec::new();\n    in_order(root, &mut out);\n    println!(\"{:?}\", out);\n    let mut empty = Vec::new();\n    in_order(None, &mut empty);\n    println!(\"{}\", empty.len());\n}\n", "expected": ["[1, 3, 4, 5, 7, 8, 9]", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-rc-tail', 27, 'rust', 'Rc: общий хвост у двух списков', 'Cons-список, у которого хвост лежит в Rc. Напишите shared_tail() → (Rc<List>, Rc<List>, Rc<List>): хвост [10] и два списка a = 1 → хвост, b = 2 → хвост, которые делят один хвост без копирования (вернуть кортеж (tail, a, b)). И sum(&List) — сумма элементов.', 'use std::rc::Rc;

enum List {
    Cons(i32, Rc<List>),
    Nil,
}
use List::{Cons, Nil};

fn shared_tail() -> (Rc<List>, Rc<List>, Rc<List>) {
    todo!()
}

fn sum(l: &List) -> i32 {
    todo!()
}
', 'Хвост создайте один раз и в каждый из двух списков отдайте Rc::clone(&tail): счётчик хвоста станет 3.', '{"driver": "fn main() {\n    let (tail, a, b) = shared_tail();\n    println!(\"{}\", Rc::strong_count(&tail));\n    println!(\"{} {} {}\", sum(&tail), sum(&a), sum(&b));\n    drop(a);\n    println!(\"{}\", Rc::strong_count(&tail));\n}\n", "expected": ["3", "10 11 12", "2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-sizeof', 28, 'rust', 'Размеры типов: стек и куча', 'Напишите sizes() → [usize; 7]: std::mem::size_of для типов u8, i32, Box<i32>, String, Vec<u8>, Option<Box<i32>>, Option<i32> — именно в этом порядке. Обратите внимание на 24 байта у String и Vec (три слова) и на то, что Option<Box<i32>> не толще указателя.', 'fn sizes() -> [usize; 7] {
    todo!()
}
', 'size_of::<Тип>() — дженерик-функция из std::mem; тип пишут в угловых скобках.', '{"driver": "fn main() {\n    println!(\"{:?}\", sizes());\n}\n", "expected": ["[1, 4, 8, 24, 24, 8, 8]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 15, 'r15-moved-args', 29, 'rust', 'Исправьте: аргументы переехали в longest', 'report возвращает «<самая длинная> (из <a> и <b>)». Но longest забирает обе строки, и в format! их уже нет. Исправьте report: нужны ровно два клона, а longest менять не нужно.', 'fn longest(a: String, b: String) -> String {
    if a.len() >= b.len() { a } else { b }
}

fn report(a: String, b: String) -> String {
    let winner = longest(a, b);
    format!("{winner} (из {a} и {b})")
}
', 'longest(a.clone(), b.clone()) отдаёт функции копии, а оригиналы остаются у report.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\".clo\", \"ne()\")).count();\n    println!(\"{}\", report(String::from(\"apple\"), String::from(\"fig\")));\n    println!(\"{}\", report(String::from(\"kiwi\"), String::from(\"plum\")));\n    println!(\"clones: {}\", bad0);\n}\n", "expected": ["apple (из apple и fig)", "kiwi (из kiwi и plum)", "clones: 2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-count-vowels', 0, 'rust', 'Заём для чтения: &str', 'Напишите count_vowels(s: &str) -> usize: сколько в строке гласных. Гласные — русские а е ё и о у ы э ю я и латинские a e i o u, регистр не важен. Функция только читает: после вызова строка остаётся у владельца.', 'fn count_vowels(s: &str) -> usize {
    todo!()
}
', 's.chars() перебирает символы; to_lowercase() у char возвращает итератор — возьмите первый символ через .next().unwrap().', '{"driver": "fn main() {\n    let s = String::from(\"Привет, Rust\");\n    println!(\"{}\", count_vowels(&s));\n    println!(\"{s}\");\n    println!(\"{} {}\", count_vowels(\"ЁЖ AEIOU\"), count_vowels(\"\"));\n}\n", "expected": ["3", "Привет, Rust", "6 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-add-all', 1, 'rust', '&mut Vec и срез: пишем через ссылку', 'Напишите add_all(dst: &mut Vec<i32>, extra: &[i32]): дописать в конец dst все элементы среза extra (копируя числа). Вызывающий передаёт &mut v и &[..]: в вызове сразу видно, кто читается, а кто меняется.', 'fn add_all(dst: &mut Vec<i32>, extra: &[i32]) {
    todo!()
}
', 'for &x in extra даёт числа по значению (i32 — Copy); затем dst.push(x).', '{"driver": "fn main() {\n    let mut v = vec![1];\n    add_all(&mut v, &[2, 3]);\n    add_all(&mut v, &[]);\n    let more = vec![4, 5];\n    add_all(&mut v, &more);\n    println!(\"{:?} {:?}\", v, more);\n}\n", "expected": ["[1, 2, 3, 4, 5] [4, 5]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-swap-ends', 2, 'rust', 'Меняем концы среза', 'Напишите swap_ends(v: &mut [i32]): поменять местами первый и последний элементы среза. Для пустого среза и среза из одного элемента ничего не делать. Функция должна принимать и массив, и вектор, и часть вектора.', 'fn swap_ends(v: &mut [i32]) {
    todo!()
}
', 'У среза есть метод swap(i, j); не забудьте про длину меньше двух.', '{"driver": "fn main() {\n    let mut a = [1, 2, 3, 4];\n    swap_ends(&mut a);\n    let mut v = vec![10, 20, 30];\n    swap_ends(&mut v);\n    swap_ends(&mut v[1..]);\n    let mut one = [7];\n    swap_ends(&mut one);\n    let mut none: [i32; 0] = [];\n    swap_ends(&mut none);\n    println!(\"{:?} {:?} {:?} {:?}\", a, v, one, none);\n}\n", "expected": ["[4, 2, 3, 1] [30, 10, 20] [7] []"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-fix-two-mut', 3, 'rust', 'Исправьте: две изменяемые ссылки сразу', 'Компилятор не даёт держать две изменяемые ссылки на один вектор одновременно. Исправьте build так, чтобы он возвращал [1, 2], оставив работу через &mut: заём должен закончиться до того, как начнётся следующий.', 'fn build() -> Vec<i32> {
    let mut v = Vec::new();
    let a = &mut v;
    let b = &mut v;
    a.push(1);
    b.push(2);
    v
}
', 'Первая ссылка живёт до последнего использования: используйте её полностью, и только потом берите вторую.', '{"driver": "fn main() {\n    println!(\"{:?}\", build());\n}\n", "expected": ["[1, 2]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-fix-read-push', 4, 'rust', 'Исправьте: ссылка на элемент и push', 'grow_with_first должна дописать в конец вектора сначала число 100, а затем копию его первого элемента. Код не компилируется: ссылка first ещё жива, когда вызывается push(100). Исправьте минимально: число можно скопировать из-под ссылки.', 'fn grow_with_first(v: &mut Vec<i32>) {
    let first = &v[0];
    v.push(100);
    v.push(*first);
}
', 'let first = v[0]; — i32 копируется, заём сразу заканчивается.', '{"driver": "fn main() {\n    let mut v = vec![5, 7];\n    grow_with_first(&mut v);\n    println!(\"{:?}\", v);\n    grow_with_first(&mut v);\n    println!(\"{:?}\", v);\n}\n", "expected": ["[5, 7, 100, 5]", "[5, 7, 100, 5, 100, 5]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-fix-dangle', 5, 'rust', 'Исправьте: ссылка на локальную строку', 'greeting строит строку «Привет, <имя>!» и пытается вернуть ссылку на неё, но локальная строка уничтожается при выходе из функции. Исправьте: верните владение, а не ссылку.', 'fn greeting(name: &str) -> &str {
    let s = format!("Привет, {name}!");
    &s
}
', 'Тип результата — String; последнее выражение функции может быть самим format!.', '{"driver": "fn main() {\n    println!(\"{}\", greeting(\"Rust\"));\n    let g = greeting(\"мир\");\n    println!(\"{} ({} байт)\", g, g.len());\n}\n", "expected": ["Привет, Rust!", "Привет, мир! (21 байт)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-longest', 6, 'rust', 'Время жизни: longest', 'Напишите longest<''a>(a: &''a str, b: &''a str) -> &''a str: вернуть более длинную строку (по байтам); при равной длине — первую. Результат — ссылка на один из аргументов, а не новая строка.', 'fn longest<''a>(a: &''a str, b: &''a str) -> &''a str {
    todo!()
}
', 'Сравните len() и верните ту ссылку, которая подходит; аннотации ''a уже в сигнатуре.', '{"driver": "fn main() {\n    let s1 = String::from(\"abcd\");\n    let n;\n    {\n        let s2 = String::from(\"xyz\");\n        n = longest(&s1, &s2).len();\n    }\n    println!(\"{n}\");\n    println!(\"{} {}\", longest(\"aa\", \"bb\"), longest(\"привет\", \"hello\"));\n}\n", "expected": ["4", "aa привет"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-first-word', 7, 'rust', 'Срез первого слова', 'Напишите first_word(s: &str) -> &str: первое слово — подряд идущие непробельные символы; ведущие пробельные символы пропускаются; если слов нет, вернуть пустую строку. Результат — срез исходной строки, а не новая строка.', 'fn first_word(s: &str) -> &str {
    todo!()
}
', 'split_whitespace().next() возвращает Option<&str>; unwrap_or("") даёт пустой срез.', '{"driver": "fn main() {\n    for s in [\"hello world\", \"  padded  text\", \"\", \"   \", \"один\", \"тут много слов\"] {\n        println!(\"{:?}\", first_word(s));\n    }\n    let owned = String::from(\"take me home\");\n    let w = first_word(&owned);\n    println!(\"{} {}\", w, w.as_ptr() == owned.as_ptr());\n}\n", "expected": ["\"hello\"", "\"padded\"", "\"\"", "\"\"", "\"один\"", "\"тут\"", "take true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-lifetime-fix', 8, 'rust', 'Исправьте: нет времени жизни у результата', 'pick(a, b, first) возвращает a или b в зависимости от флага. Компилятор не знает, к какому аргументу привязан результат. Допишите параметр времени жизни в сигнатуру.', 'fn pick(a: &str, b: &str, first: bool) -> &str {
    if first { a } else { b }
}
', 'fn pick<''a>(a: &''a str, b: &''a str, first: bool) -> &''a str.', '{"driver": "fn main() {\n    let x = String::from(\"левая\");\n    let y = String::from(\"правая\");\n    println!(\"{} {}\", pick(&x, &y, true), pick(&x, &y, false));\n}\n", "expected": ["левая правая"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-slice-split', 9, 'rust', 'Две половины одного среза', 'Напишите halves(v: &[i32]) -> (&[i32], &[i32]): левая половина длиной len/2 (округление вниз) и остаток. Данные не копируются: обе части — срезы исходного.', 'fn halves(v: &[i32]) -> (&[i32], &[i32]) {
    todo!()
}
', 'У среза есть метод split_at(mid), который возвращает пару срезов.', '{"driver": "fn main() {\n    let v = vec![1, 2, 3, 4, 5];\n    let (l, r) = halves(&v);\n    println!(\"{:?} {:?}\", l, r);\n    println!(\"{} {}\", l.as_ptr() == v.as_ptr(), r.as_ptr() == v[2..].as_ptr());\n    println!(\"{:?}\", halves(&[]));\n    println!(\"{:?}\", halves(&[9]));\n}\n", "expected": ["[1, 2] [3, 4, 5]", "true true", "([], [])", "([], [9])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-max-mut', 10, 'rust', 'Option<&mut T>: ссылка на максимум', 'Напишите max_mut(v: &mut [i32]) -> Option<&mut i32>: изменяемая ссылка на наибольший элемент (None для пустого среза). Через неё вызывающий сможет записать в массив новое значение.', 'fn max_mut(v: &mut [i32]) -> Option<&mut i32> {
    todo!()
}
', 'iter_mut() выдаёт &mut i32; max_by_key(|x| **x) выбирает наибольший, не копируя элементы.', '{"driver": "fn main() {\n    let mut v = [3, 9, 2];\n    if let Some(m) = max_mut(&mut v) {\n        *m = 0;\n    }\n    println!(\"{:?}\", v);\n    if let Some(m) = max_mut(&mut v) {\n        *m += 100;\n    }\n    println!(\"{:?}\", v);\n    println!(\"{:?}\", max_mut(&mut []));\n}\n", "expected": ["[3, 0, 2]", "[103, 0, 2]", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-fix-nll', 11, 'rust', 'Исправьте: прочитали, а потом push', 'log_and_grow возвращает последний элемент вектора и добавляет в конец 100. Ссылка last ещё нужна, когда вызывается push. Исправьте так, чтобы функция вернула последний элемент ДО добавления (для [1, 2] вернуть 2).', 'fn log_and_grow(v: &mut Vec<i32>) -> i32 {
    let last = v.last().unwrap();
    v.push(100);
    *last
}
', 'Достаточно разыменовать сразу: let last = *v.last().unwrap(); — заём закончится на этой строке.', '{"driver": "fn main() {\n    let mut v = vec![1, 2];\n    println!(\"{}\", log_and_grow(&mut v));\n    println!(\"{}\", log_and_grow(&mut v));\n    println!(\"{:?}\", v);\n}\n", "expected": ["2", "100", "[1, 2, 100, 100]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-iter-kinds', 12, 'rust', 'Три способа обойти вектор', 'sum_ref(v: &Vec<i32>) → сумма (цикл по ссылке); double_in_place(v: &mut Vec<i32>) — удвоить все элементы на месте (изменяемые ссылки); consume(v: Vec<i32>) → i32 — сумма с забором элементов (вектор уничтожается).', 'fn sum_ref(v: &Vec<i32>) -> i32 {
    todo!()
}

fn double_in_place(v: &mut Vec<i32>) {
    todo!()
}

fn consume(v: Vec<i32>) -> i32 {
    todo!()
}
', 'for x in v (v: &Vec) даёт &i32; v.iter_mut() — &mut i32 (значение меняют через *x); for x in v (v: Vec) — i32.', '{"driver": "fn main() {\n    let mut v = vec![1, 2, 3];\n    println!(\"{}\", sum_ref(&v));\n    double_in_place(&mut v);\n    println!(\"{:?}\", v);\n    println!(\"{}\", consume(v));\n}\n", "expected": ["6", "[2, 4, 6]", "12"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-parser', 13, 'rust', 'Структура со ссылкой: Parser<''a>', 'Parser хранит срез текста и позицию. Parser::new(text) создаёт разборщик; next_word(&mut self) возвращает следующее слово (непробельные символы) как срез ИСХОДНОГО текста или None, когда слов больше нет. Слова должны жить столько же, сколько текст, а не столько, сколько сам разборщик (&''a str в результате).', 'struct Parser<''a> {
    text: &''a str,
    pos: usize,
}

impl<''a> Parser<''a> {
    fn new(text: &''a str) -> Parser<''a> {
        todo!()
    }

    fn next_word(&mut self) -> Option<&''a str> {
        todo!()
    }
}
', 'Ищите начало слова после trim_start, конец — по первому пробельному символу; сдвигайте self.pos за слово.', '{"driver": "fn main() {\n    let text = String::from(\"  hello   rust world \");\n    let mut words = Vec::new();\n    {\n        let mut p = Parser::new(&text);\n        while let Some(w) = p.next_word() {\n            words.push(w);\n        }\n    }\n    println!(\"{:?}\", words);\n    let mut q = Parser::new(\"привет мир\");\n    println!(\"{:?} {:?} {:?}\", q.next_word(), q.next_word(), q.next_word());\n    println!(\"{:?}\", Parser::new(\"   \").next_word());\n}\n", "expected": ["[\"hello\", \"rust\", \"world\"]", "Some(\"привет\") Some(\"мир\") None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-method-forms', 14, 'rust', 'Три формы self', 'Counter считает события. new() — со нулём; get(&self) читает значение; inc(&mut self) увеличивает на 1; finish(self) забирает счётчик и возвращает итог. Выберите для каждого метода нужную форму: после finish использовать счётчик уже нельзя.', 'struct Counter {
    n: u32,
}

impl Counter {
    fn new() -> Counter {
        todo!()
    }

    fn get(&self) -> u32 {
        todo!()
    }

    fn inc(&mut self) {
        todo!()
    }

    fn finish(self) -> u32 {
        todo!()
    }
}
', 'Сигнатуры уже даны: &self читает, &mut self меняет поле через self.n += 1, self передаёт поле дальше.', '{"driver": "fn main() {\n    let mut c = Counter::new();\n    println!(\"{}\", c.get());\n    c.inc();\n    c.inc();\n    c.inc();\n    println!(\"{}\", c.get());\n    println!(\"{}\", c.finish());\n}\n", "expected": ["0", "3", "3"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-fix-method-self', 15, 'rust', 'Исправьте: метод меняет поле через &self', 'add должен увеличить количество монет, но метод принимает &self — менять поле через разделяемую ссылку нельзя. Исправьте сигнатуру метода (вызывающий код уже использует let mut).', 'struct Wallet {
    coins: u32,
}

impl Wallet {
    fn add(&self, n: u32) {
        self.coins += n;
    }

    fn total(&self) -> u32 {
        self.coins
    }
}
', 'fn add(&mut self, n: u32) — изменяемая ссылка на self.', '{"driver": "fn main() {\n    let mut w = Wallet { coins: 1 };\n    w.add(4);\n    w.add(5);\n    println!(\"{}\", w.total());\n}\n", "expected": ["10"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-swap-values', 16, 'rust', 'Обмен через две &mut без mem::swap', 'Напишите swap_values(a: &mut i32, b: &mut i32): поменять значения местами, не используя std::mem::swap и метод swap. Две &mut на РАЗНЫЕ значения проверщик допускает; в вызывающем коде обе переменные объявлены mut.', 'fn swap_values(a: &mut i32, b: &mut i32) {
    todo!()
}
', 'Нужна временная переменная: tmp = *a; *a = *b; *b = tmp;', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\"sw\", \"ap(\")).count();\n    let mut x = 1;\n    let mut y = 2;\n    swap_values(&mut x, &mut y);\n    println!(\"{x} {y}\");\n    swap_values(&mut x, &mut y);\n    println!(\"{x} {y}\");\n    println!(\"swap calls: {}\", bad0);\n}\n", "expected": ["2 1", "1 2", "swap calls: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-reborrow', 17, 'rust', 'Перезаимствование: передаём &mut дальше', 'bump(x: &mut i32) прибавляет единицу — он уже готов. Напишите bump_n(x: &mut i32, n: u32): вызвать bump ровно n раз с тем же x. &mut не копируется, но передача в функцию создаёт временный заём, и x можно использовать снова.', 'fn bump(x: &mut i32) {
    *x += 1;
}

fn bump_n(x: &mut i32, n: u32) {
    todo!()
}
', 'В цикле просто пишите bump(x); — каждый вызов заимствует x на время вызова.', '{"driver": "fn main() {\n    let mut v = 10;\n    bump_n(&mut v, 5);\n    println!(\"{v}\");\n    bump_n(&mut v, 0);\n    bump(&mut v);\n    println!(\"{v}\");\n}\n", "expected": ["15", "16"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-split-halves-mut', 18, 'rust', 'split_at_mut: два писателя, разные части', 'Напишите reshape(v: &mut [i32]): левую половину (len/2 элементов) обнулить, а каждый элемент правой половины заменить суммой соответствующих исходных элементов левой и правой (для пары i: right[i] = left_old[i] + right_old[i]; если правая половина длиннее, лишний последний остаётся прежним). Используйте split_at_mut: две изменяемые ссылки на непересекающиеся части разрешены.', 'fn reshape(v: &mut [i32]) {
    todo!()
}
', 'let (left, right) = v.split_at_mut(mid); — обе части можно менять одновременно.', '{"driver": "fn main() {\n    let mut a = [1, 2, 3, 4, 5, 6];\n    reshape(&mut a);\n    println!(\"{:?}\", a);\n    let mut b = vec![5, 6, 7];\n    reshape(&mut b);\n    println!(\"{:?}\", b);\n    let mut c: Vec<i32> = vec![];\n    reshape(&mut c);\n    println!(\"{:?}\", c);\n}\n", "expected": ["[0, 0, 0, 5, 7, 9]", "[0, 11, 7]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-fix-iter-invalidate', 19, 'rust', 'Исправьте: изменяем вектор во время обхода', 'dup_evens дописывает в конец вектора копии всех чётных чисел (порядок: исходные элементы, затем копии чётных в исходном порядке). Цикл по &v держит заём, а push меняет вектор — не компилируется. Исправьте: сначала соберите копии, потом добавьте.', 'fn dup_evens(mut v: Vec<i32>) -> Vec<i32> {
    for x in &v {
        if x % 2 == 0 {
            v.push(*x);
        }
    }
    v
}
', 'Заведите отдельный вектор extra, заполните его в цикле, а после цикла вызовите v.extend(extra).', '{"driver": "fn main() {\n    println!(\"{:?}\", dup_evens(vec![1, 2, 3, 4]));\n    println!(\"{:?}\", dup_evens(vec![]));\n    println!(\"{:?}\", dup_evens(vec![7, 9]));\n}\n", "expected": ["[1, 2, 3, 4, 2, 4]", "[]", "[7, 9]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-initial-char', 20, 'rust', 'Срез по границе символа', 'initial(s: &str) -> &str возвращает первый символ строки как срез (пустая строка → пустой срез). Заготовка берёт один БАЙТ и падает на кириллице: границы среза обязаны попадать на границу символа UTF-8. Исправьте.', 'fn initial(s: &str) -> &str {
    &s[..1]
}
', 'char_indices() выдаёт пары (байтовое смещение, символ): смещение второго символа — конец первого; если второго нет, подойдёт вся строка.', '{"driver": "fn main() {\n    for s in [\"rust\", \"привет\", \"Ёж\", \"\", \"я\"] {\n        println!(\"{:?}\", initial(s));\n    }\n}\n", "expected": ["\"r\"", "\"п\"", "\"Ё\"", "\"\"", "\"я\""]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-stack-addr', 21, 'rust', 'Стек растёт вниз', 'Напишите inner(outer: usize) -> bool с атрибутом #[inline(never)]: заведите локальную переменную, получите её адрес (as *const u64 as usize) и верните, меньше ли он адреса outer. И grows_down() -> bool: локальная переменная, её адрес передаётся в inner. Результат должен быть true: кадр вложенного вызова лежит ниже. Значения оберните в std::hint::black_box, чтобы оптимизатор их не убрал.', '#[inline(never)]
fn inner(outer: usize) -> bool {
    todo!()
}

fn grows_down() -> bool {
    todo!()
}
', 'let y = black_box(0u64); let ay = &y as *const u64 as usize; — то же в grows_down; в inner сравнивайте ay < outer.', '{"driver": "fn main() {\n    println!(\"{}\", grows_down());\n}\n", "expected": ["true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-ptr-eq', 22, 'rust', 'Равны значения или это один объект', 'same_text(a, b) — true, если строки равны по содержимому (==). same_object(a, b) — true, только если обе ссылки указывают на ОДИН объект в памяти (std::ptr::eq). Это аналоги == и is из питона.', 'fn same_text(a: &String, b: &String) -> bool {
    todo!()
}

fn same_object(a: &String, b: &String) -> bool {
    todo!()
}
', 'a == b сравнивает значения за ссылками; ptr::eq(a, b) — сами адреса.', '{"driver": "fn main() {\n    let x = String::from(\"hi\");\n    let y = String::from(\"hi\");\n    println!(\"{} {}\", same_text(&x, &y), same_object(&x, &y));\n    println!(\"{} {}\", same_text(&x, &x), same_object(&x, &x));\n}\n", "expected": ["true false", "true true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-trim-all', 23, 'rust', 'Срезы в векторе: trim_all', 'Напишите trim_all<''a>(lines: &[&''a str]) -> Vec<&''a str>: вектор срезов, каждый обрезан по краям от пробельных символов. Новых строк не создаётся — только срезы исходных строк, поэтому результат живёт столько же, сколько исходные тексты (время жизни ''a).', 'fn trim_all<''a>(lines: &[&''a str]) -> Vec<&''a str> {
    todo!()
}
', 's.trim() у &''a str возвращает &''a str; соберите результат через map(...).collect().', '{"driver": "fn main() {\n    let text = String::from(\"  alpha \\n beta\\t\");\n    let parts: Vec<&str> = text.split(''\\n'').collect();\n    let t = trim_all(&parts);\n    println!(\"{:?}\", t);\n    println!(\"{:?}\", trim_all(&[\"  \", \"x \", \"\"]));\n}\n", "expected": ["[\"alpha\", \"beta\"]", "[\"\", \"x\", \"\"]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-longest-word', 24, 'rust', 'Самое длинное слово', 'Напишите longest_word(text: &str) -> &str: самое длинное слово текста (слова разделены пробельными символами; длина — в символах, не в байтах; при равенстве — первое; пустой текст → ""). Верните срез текста.', 'fn longest_word(text: &str) -> &str {
    todo!()
}
', 'Храните лучший срез в переменной типа &str и заменяйте её, когда нашли слово длиннее по chars().count().', '{"driver": "fn main() {\n    println!(\"{:?}\", longest_word(\"a bb ccc dd\"));\n    println!(\"{:?}\", longest_word(\"привет мир кот\"));\n    println!(\"{:?}\", longest_word(\"ab cd\"));\n    println!(\"{:?}\", longest_word(\"  \"));\n}\n", "expected": ["\"ccc\"", "\"привет\"", "\"ab\"", "\"\""]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-struct-ref-fix', 25, 'rust', 'Исправьте: у структуры со ссылкой нет времени жизни', 'Highlight хранит срез текста и смещение, mark(text, from, to) строит выделение. Компилятор требует указать время жизни. Допишите параметры в определение структуры и в сигнатуру функции.', 'struct Highlight {
    text: &str,
    start: usize,
}

fn mark(text: &str, from: usize, to: usize) -> Highlight {
    Highlight { text: &text[from..to], start: from }
}
', 'struct Highlight<''a> { text: &''a str, … } и fn mark<''a>(text: &''a str, …) -> Highlight<''a>.', '{"driver": "fn main() {\n    let doc = String::from(\"borrow checker is strict\");\n    let h = mark(&doc, 7, 14);\n    println!(\"{} @ {}\", h.text, h.start);\n}\n", "expected": ["checker @ 7"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-fix-outlive', 26, 'rust', 'Исправьте: значение живёт недостаточно долго', 'outer_len сравнивает входную строку с временной строкой и возвращает длину большей. Ссылка result переживает временную строку b, и компилятор отказывается собирать код. Исправьте, не меняя longest и не выводя b за пределы блока: длину нужно взять, пока b ещё жива.', 'fn longest<''a>(a: &''a str, b: &''a str) -> &''a str {
    if a.len() >= b.len() { a } else { b }
}

fn outer_len(a: &str) -> usize {
    let result;
    {
        let b = String::from("temporary");
        result = longest(a, &b);
    }
    result.len()
}
', 'Замените result на число: n = longest(a, &b).len(); внутри блока.', '{"driver": "fn main() {\n    println!(\"{}\", outer_len(\"hi\"));\n    println!(\"{}\", outer_len(\"a longer phrase here\"));\n}\n", "expected": ["9", "20"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-longest-row', 27, 'rust', 'Ссылка на самую длинную строку сетки', 'grid — вектор строк (векторов). longest_row(grid: &[Vec<i32>]) -> Option<&Vec<i32>> возвращает ссылку на самую длинную строку (при равенстве — первую; пустая сетка → None). push_to_longest(grid: &mut [Vec<i32>], x) добавляет x в конец той же самой строки (первой из самых длинных).', 'fn longest_row(grid: &[Vec<i32>]) -> Option<&Vec<i32>> {
    todo!()
}

fn push_to_longest(grid: &mut [Vec<i32>], x: i32) {
    todo!()
}
', 'Для push нужен индекс: найдите его читающим обходом (заём закончится), а потом возьмите &mut grid[i].', '{"driver": "fn main() {\n    let mut grid = vec![vec![1], vec![2, 3], vec![4, 5], vec![]];\n    println!(\"{:?}\", longest_row(&grid));\n    push_to_longest(&mut grid, 9);\n    println!(\"{:?}\", grid);\n    println!(\"{:?}\", longest_row(&[]));\n    let mut empty: Vec<Vec<i32>> = vec![];\n    push_to_longest(&mut empty, 1);\n    println!(\"{:?}\", empty);\n}\n", "expected": ["Some([2, 3])", "[[1], [2, 3, 9], [4, 5], []]", "None", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-first-negative', 28, 'rust', 'Option<&mut i32>: первое отрицательное', 'Напишите first_negative(v: &mut [i32]) -> Option<&mut i32>: изменяемая ссылка на первый отрицательный элемент (None, если таких нет). Через неё вызывающий исправляет значение прямо в массиве.', 'fn first_negative(v: &mut [i32]) -> Option<&mut i32> {
    todo!()
}
', 'iter_mut().find(|x| **x < 0): в замыкании x имеет тип &&mut i32, поэтому две звёздочки.', '{"driver": "fn main() {\n    let mut v = [3, -1, 4, -5];\n    while let Some(x) = first_negative(&mut v) {\n        *x = 0;\n    }\n    println!(\"{:?}\", v);\n    println!(\"{:?}\", first_negative(&mut [1, 2]));\n}\n", "expected": ["[3, 0, 4, 0]", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 16, 'r16-fix-report', 29, 'rust', 'Исправьте: ссылка на первый элемент и clear', 'report(names) возвращает строку «первое — <имя>; осталось <N>» и очищает вектор. Ссылка first на элемент вектора ещё нужна, когда вектор очищается. Исправьте: сделайте независимую копию имени.', 'fn report(names: &mut Vec<String>) -> String {
    let first = &names[0];
    names.clear();
    format!("первое — {}; осталось {}", first, names.len())
}
', 'names[0].clone() даёт новую String, не связанную с вектором.', '{"driver": "fn main() {\n    let mut names = vec![String::from(\"anna\"), String::from(\"bob\")];\n    println!(\"{}\", report(&mut names));\n    println!(\"{:?}\", names);\n}\n", "expected": ["первое — anna; осталось 0", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-point-new', 0, 'rust', 'Структура и методы: Point', 'Опишите методы Point: origin() — точка (0, 0); new(x, y); manhattan(&self, other: &Point) → |dx| + |dy|; translate(&mut self, dx, dy) — сдвинуть на месте.', 'struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn origin() -> Point {
        todo!()
    }

    fn new(x: i32, y: i32) -> Point {
        todo!()
    }

    fn manhattan(&self, other: &Point) -> i32 {
        todo!()
    }

    fn translate(&mut self, dx: i32, dy: i32) {
        todo!()
    }
}
', 'Сокращённая запись поля: Point { x, y }, если имена параметров совпадают с именами полей.', '{"driver": "fn main() {\n    let o = Point::origin();\n    let mut p = Point::new(3, -4);\n    println!(\"{}\", p.manhattan(&o));\n    p.translate(-3, 4);\n    println!(\"{} {} {}\", p.x, p.y, p.manhattan(&o));\n}\n", "expected": ["7", "0 0 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-rect-methods', 1, 'rust', 'Прямоугольник: &self, &mut self', 'Rect { w, h } (u32). Методы: area(&self), perimeter(&self), is_square(&self), can_hold(&self, other: &Rect) — помещается ли other целиком (обе стороны строго меньше или равны) и scale(&mut self, k: u32) — умножить обе стороны на k.', 'struct Rect {
    w: u32,
    h: u32,
}

impl Rect {
    fn area(&self) -> u32 {
        todo!()
    }

    fn perimeter(&self) -> u32 {
        todo!()
    }

    fn is_square(&self) -> bool {
        todo!()
    }

    fn can_hold(&self, other: &Rect) -> bool {
        todo!()
    }

    fn scale(&mut self, k: u32) {
        todo!()
    }
}
', 'В can_hold сравнивайте обе стороны: self.w >= other.w && self.h >= other.h.', '{"driver": "fn main() {\n    let mut r = Rect { w: 4, h: 3 };\n    let small = Rect { w: 2, h: 2 };\n    println!(\"{} {} {}\", r.area(), r.perimeter(), r.is_square());\n    println!(\"{} {}\", r.can_hold(&small), small.can_hold(&r));\n    r.scale(2);\n    println!(\"{} {}\", r.w, r.h);\n    println!(\"{}\", Rect { w: 5, h: 5 }.is_square());\n}\n", "expected": ["12 14 false", "true false", "8 6", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-derive-debug', 2, 'rust', 'derive: Debug, Clone, PartialEq, Default', 'Код не собирается: драйвер печатает User через {:?}, клонирует, сравнивает через == и создаёт значение по умолчанию. Добавьте над структурой один атрибут derive с нужными четырьмя именами.', 'struct User {
    name: String,
    age: u32,
    active: bool,
}
', '#[derive(Debug, Clone, PartialEq, Default)] — все поля уже умеют всё это, поэтому derive сработает.', '{"driver": "fn main() {\n    let u = User { name: String::from(\"Анна\"), age: 30, active: true };\n    let v = u.clone();\n    println!(\"{:?}\", u);\n    println!(\"{}\", u == v);\n    let d = User::default();\n    println!(\"{:?} {}\", d, d == u);\n    println!(\"{:#?}\", v);\n}\n", "expected": ["User { name: \"Анна\", age: 30, active: true }", "true", "User { name: \"\", age: 0, active: false } false", "User {", "    name: \"Анна\",", "    age: 30,", "    active: true,", "}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-display-impl', 3, 'rust', 'Display вручную', 'Реализуйте std::fmt::Display: для Point — «(x, y)»; для Temp — «21.5°C» или «70.7°F» (одно знак после запятой). Тогда работают {} и to_string().', 'use std::fmt;

struct Point {
    x: i32,
    y: i32,
}

enum Temp {
    C(f64),
    F(f64),
}

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}

impl fmt::Display for Temp {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}
', 'write!(f, "({}, {})", self.x, self.y); для Temp — match self { Temp::C(t) => write!(...), ... }.', '{"driver": "fn main() {\n    let p = Point { x: 3, y: -1 };\n    println!(\"{} [{:>10}]\", p, p.to_string());\n    println!(\"{} {}\", Temp::C(21.5), Temp::F(70.66));\n}\n", "expected": ["(3, -1) [   (3, -1)]", "21.5°C 70.7°F"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-repr-c', 4, 'rust', 'Выравнивание: repr(C) и порядок полей', 'Три структуры с полями u8, u32, u8. Tight — по умолчанию (раст сам переставляет поля): 8 байт. Wide — те же поля, но в раскладке языка си (#[repr(C)]): 12 байт. Packed — #[repr(C)], но поля расположите так, чтобы размер стал 8. Заготовка даёт для всех трёх размер 8: исправьте Wide и Packed.', 'struct Tight {
    a: u8,
    b: u32,
    c: u8,
}

struct Wide {
    a: u8,
    b: u32,
    c: u8,
}

struct Packed {
    a: u8,
    b: u32,
    c: u8,
}
', 'В repr(C) поля идут по порядку, и после каждого вставляется выравнивание: u8, [3 пустых], u32, u8, [3 пустых] = 12. Поставьте u32 первым.', '{"driver": "fn main() {\n    use std::mem::{align_of, size_of};\n    println!(\"{} {} {}\", size_of::<Tight>(), size_of::<Wide>(), size_of::<Packed>());\n    println!(\"{}\", align_of::<Wide>());\n}\n", "expected": ["8 12 8", "4"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-enum-shape', 5, 'rust', 'enum Shape: площадь и периметр', 'Shape — Circle(r), Rect(w, h) или Tri(a, b, c) (стороны). area(&self) → f64 (для треугольника — формула Герона), perimeter(&self) → f64. π берите из std::f64::consts::PI.', 'use std::f64::consts::PI;

enum Shape {
    Circle(f64),
    Rect(f64, f64),
    Tri(f64, f64, f64),
}

impl Shape {
    fn area(&self) -> f64 {
        todo!()
    }

    fn perimeter(&self) -> f64 {
        todo!()
    }
}
', 'match self даёт привязки-ссылки: r, w, h — это &f64, арифметика с ними работает.', '{"driver": "fn main() {\n    let shapes = [Shape::Circle(1.0), Shape::Rect(3.0, 4.0), Shape::Tri(3.0, 4.0, 5.0)];\n    for s in &shapes {\n        println!(\"{:.2} {:.2}\", s.area(), s.perimeter());\n    }\n}\n", "expected": ["3.14 6.28", "12.00 14.00", "6.00 12.00"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-enum-size', 6, 'rust', 'Размеры перечислений', 'Напишите sizes() → [usize; 6]: size_of для Dir (перечисление из четырёх вариантов без данных), Option<u8>, Option<u32>, Option<Box<i32>>, Option<&str>, Result<u8, u8> — в этом порядке. Подумайте, где нужен тег, а где его заменяет ниша.', 'enum Dir {
    N,
    E,
    S,
    W,
}

fn sizes() -> [usize; 6] {
    todo!()
}
', 'size_of::<Тип>() из std::mem; Option<&str> — это срез (16 байт) с нишей в указателе.', '{"driver": "fn main() {\n    let _ = [Dir::N, Dir::E, Dir::S, Dir::W];\n    println!(\"{:?}\", sizes());\n}\n", "expected": ["[1, 2, 8, 8, 16, 2]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-match-coin', 7, 'rust', 'match: монеты', 'enum Coin { Penny, Nickel, Dime, Quarter(u32) } — у четвертака есть год чеканки. cents(&Coin) → u32: 1, 5, 10 и 25; но четвертак до 1980 года (не включая) считается коллекционным и стоит 100. total(&[Coin]) → u32 — сумма.', 'enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter(u32),
}

fn cents(c: &Coin) -> u32 {
    todo!()
}

fn total(coins: &[Coin]) -> u32 {
    todo!()
}
', 'Ветвь с охраной Quarter(year) if *year < 1980 должна идти раньше общей Quarter(_).', '{"driver": "fn main() {\n    let v = [Coin::Penny, Coin::Dime, Coin::Quarter(1999), Coin::Quarter(1960), Coin::Nickel];\n    println!(\"{}\", total(&v));\n    println!(\"{} {}\", cents(&Coin::Quarter(1980)), cents(&Coin::Quarter(1979)));\n    println!(\"{}\", total(&[]));\n}\n", "expected": ["141", "25 100", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-match-ranges', 8, 'rust', 'match: диапазоны, | , @ и охрана', 'classify(n: i32) → String одним match: отрицательное → "negative"; 0 → "zero"; цифра 1..=9 → "digit N" (с самим числом); 10, 20 или 30 → "round"; остальные чётные → "even"; прочие → "odd".', 'fn classify(n: i32) -> String {
    todo!()
}
', 'Порядок ветвей важен: специальные случаи выше общих. Шаблон d @ 1..=9 привязывает число к имени d.', '{"driver": "fn main() {\n    for n in [-5, 0, 7, 20, 14, 15, 100, 11] {\n        println!(\"{n}: {}\", classify(n));\n    }\n}\n", "expected": ["-5: negative", "0: zero", "7: digit 7", "20: round", "14: even", "15: odd", "100: even", "11: odd"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-match-tuple', 9, 'rust', 'match по кортежу: FizzBuzz без if', 'fizzbuzz(n: u32) → String одним match по паре (n % 3, n % 5): «FizzBuzz», «Fizz», «Buzz» или само число. Слово if в коде использовать нельзя.', 'fn fizzbuzz(n: u32) -> String {
    todo!()
}
', 'Образец (0, _) означает: остаток по 3 равен нулю, остаток по 5 не важен.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\"i\", \"f \")).count();\n    let line: Vec<String> = (1..=15).map(fizzbuzz).collect();\n    println!(\"{}\", line.join(\" \"));\n    println!(\"{} {}\", fizzbuzz(30), fizzbuzz(31));\n    println!(\"ifs: {}\", bad0);\n}\n", "expected": ["1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz", "FizzBuzz 31", "ifs: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-match-slice', 10, 'rust', 'Образцы на срезах', 'describe(v: &[i32]) → String одним match с образцами срезов: пустой → "empty"; один элемент → "one: X"; два → "two: A, B"; больше → "many: FIRST..LAST" (первый и последний).', 'fn describe(v: &[i32]) -> String {
    todo!()
}
', 'Образец [first, .., last] подходит срезу из двух и более элементов; двухэлементный образец поставьте раньше.', '{"driver": "fn main() {\n    println!(\"{}\", describe(&[]));\n    println!(\"{}\", describe(&[7]));\n    println!(\"{}\", describe(&[1, 2]));\n    println!(\"{}\", describe(&[1, 2, 3, 4, 5]));\n    println!(\"{}\", describe(&vec![9, 8, 7]));\n}\n", "expected": ["empty", "one: 7", "two: 1, 2", "many: 1..5", "many: 9..7"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-option-div', 11, 'rust', 'Option и оператор ?', 'safe_div(a, b) → Option<i32> (None при b == 0). parse_pair(s) → Option<(i32, i32)>: строка вида "3,4" (без пробелов), любая ошибка → None. ratio(s) → Option<i32>: разобрать пару и безопасно разделить; здесь используйте оператор ?. Вызов unwrap() запрещён.', 'fn safe_div(a: i32, b: i32) -> Option<i32> {
    todo!()
}

fn parse_pair(s: &str) -> Option<(i32, i32)> {
    todo!()
}

fn ratio(s: &str) -> Option<i32> {
    todo!()
}
', 'l.parse::<i32>().ok()? превращает Result в Option и сразу возвращает None при ошибке; split_once('','') тоже Option.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\"unw\", \"rap(\")).count();\n    for s in [\"12,4\", \"7,0\", \"x,1\", \"5\", \"-9,3\", \"1,2,3\"] {\n        println!(\"{:?}\", ratio(s));\n    }\n    println!(\"{:?} {:?}\", safe_div(1, 0), parse_pair(\"8,2\"));\n    println!(\"unwraps: {}\", bad0);\n}\n", "expected": ["Some(3)", "None", "None", "None", "Some(-3)", "None", "None Some((8, 2))", "unwraps: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-option-combinators', 12, 'rust', 'Комбинаторы Option без match', 'first_even_square(v) → Option<i32>: квадрат первого чётного числа. name_len(name: Option<&str>) → usize: длина имени или 0. parse_or(s, default) → i32: число из строки или default. Условие: ни match, ни if let — только методы Option и Result (map, and_then, unwrap_or, find...).', 'fn first_even_square(v: &[i32]) -> Option<i32> {
    todo!()
}

fn name_len(name: Option<&str>) -> usize {
    todo!()
}

fn parse_or(s: &str, default: i32) -> i32 {
    todo!()
}
', 'find возвращает Option<&i32>; map превращает значение внутри. Для разбора строки: s.trim().parse().unwrap_or(default).', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\"mat\", \"ch \")).count();\n    let bad1 = src.matches(concat!(\"if \", \"let \")).count();\n    println!(\"{:?} {:?}\", first_even_square(&[3, 5, 6, 8]), first_even_square(&[1, 3]));\n    println!(\"{} {}\", name_len(Some(\"Анна\")), name_len(None));\n    println!(\"{} {} {}\", parse_or(\" 42 \", 0), parse_or(\"abc\", -1), parse_or(\"\", 7));\n    println!(\"banned: {} {}\", bad0, bad1);\n}\n", "expected": ["Some(36) None", "8 0", "42 -1 7", "banned: 0 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-let-else', 13, 'rust', 'let else и if let', 'parse_kv(line) → String: строка вида "ключ=значение"; через let else разобрать по первому «=», иначе вернуть "bad"; результат — «ключ -> значение» (обе части с обрезанными пробелами). show(o: Option<i32>) → String: «got N», если число есть, иначе «nothing» — через if let / else.', 'fn parse_kv(line: &str) -> String {
    todo!()
}

fn show(o: Option<i32>) -> String {
    todo!()
}
', 'let Some((k, v)) = … else { return …; }; — после этой строки k и v уже обычные срезы.', '{"driver": "fn main() {\n    println!(\"{}\", parse_kv(\"name = rust\"));\n    println!(\"{}\", parse_kv(\"novalue\"));\n    println!(\"{}\", parse_kv(\"a=b=c\"));\n    println!(\"{} {}\", show(Some(5)), show(None));\n}\n", "expected": ["name -> rust", "bad", "a -> b=c", "got 5 nothing"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-rpn', 14, 'rust', 'Стек и while let: обратная польская запись', 'eval_rpn(tokens: &[&str]) → Option<i64>: вычислить выражение в обратной польской записи: числа и операторы + - * /. Стек — Vec<i64>. None, если не хватает операндов, делитель равен нулю, токен не распознан или в конце на стеке не ровно одно число.', 'fn eval_rpn(tokens: &[&str]) -> Option<i64> {
    todo!()
}
', 'Для оператора достаньте b = pop()?, затем a = pop()? (порядок!). Остальные токены разберите как числа через parse().ok()?.', '{"driver": "fn main() {\n    println!(\"{:?}\", eval_rpn(&[\"3\", \"4\", \"+\", \"2\", \"*\"]));\n    println!(\"{:?}\", eval_rpn(&[\"5\", \"1\", \"2\", \"+\", \"4\", \"*\", \"+\", \"3\", \"-\"]));\n    println!(\"{:?}\", eval_rpn(&[\"1\", \"+\"]));\n    println!(\"{:?}\", eval_rpn(&[\"4\", \"0\", \"/\"]));\n    println!(\"{:?}\", eval_rpn(&[\"1\", \"2\"]));\n    println!(\"{:?}\", eval_rpn(&[\"x\"]));\n    println!(\"{:?}\", eval_rpn(&[]));\n}\n", "expected": ["Some(14)", "Some(14)", "None", "None", "None", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-state-machine', 15, 'rust', 'Автомат состояний: дверь', 'Door — Open, Closed, Locked(код). apply(self, Action) → Door: Open + Close → Closed; Closed + Open → Open; Closed + Lock(c) → Locked(c); Locked(c) + Unlock(x) → Closed, если x == c, иначе остаётся Locked(c). Любое другое действие — состояние не меняется. Метод принимает self по значению.', '#[derive(Debug, PartialEq)]
enum Door {
    Open,
    Closed,
    Locked(u32),
}

enum Action {
    Open,
    Close,
    Lock(u32),
    Unlock(u32),
}

impl Door {
    fn apply(self, action: Action) -> Door {
        todo!()
    }
}
', 'Матч по паре (self, action) читается как таблица переходов; последняя ветвь (state, _) => state возвращает прежнее состояние.', '{"driver": "fn main() {\n    use Action::*;\n    let mut d = Door::Open;\n    for a in [Lock(1), Close, Lock(1234), Open, Unlock(1), Unlock(1234), Open] {\n        d = d.apply(a);\n        println!(\"{:?}\", d);\n    }\n    println!(\"{}\", Door::Closed.apply(Close) == Door::Closed);\n}\n", "expected": ["Open", "Closed", "Locked(1234)", "Locked(1234)", "Locked(1234)", "Closed", "Open", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-direction', 16, 'rust', 'enum без данных: Direction', 'Direction — N, E, S, W (derive Debug, Clone, Copy, PartialEq). turn_right(self), turn_left(self), opposite(self), from_char(c: char) → Option<Direction> (буквы N E S W в любом регистре) и to_char(self) → char (заглавная).', '#[derive(Debug, Clone, Copy, PartialEq)]
enum Direction {
    N,
    E,
    S,
    W,
}

impl Direction {
    fn turn_right(self) -> Direction {
        todo!()
    }

    fn turn_left(self) -> Direction {
        todo!()
    }

    fn opposite(self) -> Direction {
        todo!()
    }

    fn from_char(c: char) -> Option<Direction> {
        todo!()
    }

    fn to_char(self) -> char {
        todo!()
    }
}
', 'Тип Copy: self по значению можно использовать повторно. opposite — два поворота направо.', '{"driver": "fn main() {\n    let mut d = Direction::N;\n    for _ in 0..5 {\n        print!(\"{} \", d.to_char());\n        d = d.turn_right();\n    }\n    println!();\n    println!(\"{:?} {:?}\", Direction::W.turn_left(), Direction::E.opposite());\n    println!(\"{:?} {:?} {:?}\", Direction::from_char(''s''), Direction::from_char(''W''), Direction::from_char(''x''));\n}\n", "expected": ["N E S W N", "S W", "Some(S) Some(W) None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-fix-match-ref', 17, 'rust', 'Исправьте: нельзя переместить из заимствованного', 'display_name возвращает прозвище, а если его нет — имя. Метод получает &Person, а match пытается ПЕРЕМЕСТИТЬ строку из поля за ссылкой. Исправьте так, чтобы Person остался у владельца.', 'struct Person {
    name: String,
    nickname: Option<String>,
}

fn display_name(p: &Person) -> String {
    match p.nickname {
        Some(n) => n,
        None => p.name.clone(),
    }
}
', 'match &p.nickname даёт привязку n: &String; вернуть нужно владельца — n.clone().', '{"driver": "fn main() {\n    let a = Person { name: String::from(\"Александр\"), nickname: Some(String::from(\"Саша\")) };\n    let b = Person { name: String::from(\"Борис\"), nickname: None };\n    println!(\"{} {}\", display_name(&a), display_name(&b));\n    println!(\"{} {}\", a.name, display_name(&a));\n}\n", "expected": ["Саша Борис", "Александр Саша"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-match-mut', 18, 'rust', 'Изменение внутри Option', 'increment_if_some(o: &mut Option<i32>) — прибавить 1, если значение есть. take_or(o: &mut Option<String>, default: &str) → String: забрать значение из o (в o остаётся None) или вернуть default. append_default(o: &mut Option<Vec<i32>>, x) — добавить x в вектор; если вектора ещё нет, создать.', 'fn increment_if_some(o: &mut Option<i32>) {
    todo!()
}

fn take_or(o: &mut Option<String>, default: &str) -> String {
    todo!()
}

fn append_default(o: &mut Option<Vec<i32>>, x: i32) {
    todo!()
}
', 'if let Some(x) = o даёт x: &mut i32 (match ergonomics); o.take() и get_or_insert_with избавляют от лишних match.', '{"driver": "fn main() {\n    let mut a = Some(5);\n    let mut b: Option<i32> = None;\n    increment_if_some(&mut a);\n    increment_if_some(&mut b);\n    println!(\"{:?} {:?}\", a, b);\n    let mut s = Some(String::from(\"hi\"));\n    println!(\"{} {} {:?}\", take_or(&mut s, \"def\"), take_or(&mut s, \"def\"), s);\n    let mut v = None;\n    append_default(&mut v, 1);\n    append_default(&mut v, 2);\n    println!(\"{:?}\", v);\n}\n", "expected": ["Some(6) None", "hi def None", "Some([1, 2])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-fix-move-in-match', 19, 'rust', 'Исправьте: значение переехало в match', 'describe сначала разбирает msg через match, а затем печатает его же через {:?}. match перемещает строку из варианта, и msg после него недоступно. Исправьте минимальной правкой (data нужны и текст, и сам msg).', 'fn describe(msg: Option<String>) -> String {
    let text = match msg {
        Some(s) => s,
        None => String::from("пусто"),
    };
    format!("{text} ({:?})", msg)
}
', 'match &msg разбирает ссылку: привязка s — &String, а msg остаётся целым.', '{"driver": "fn main() {\n    println!(\"{}\", describe(Some(String::from(\"привет\"))));\n    println!(\"{}\", describe(None));\n}\n", "expected": ["привет (Some(\"привет\"))", "пусто (None)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-expr-eval', 20, 'rust', 'Дерево выражений: eval', 'Expr — Num(i64), Add, Mul (по два Box<Expr>) и Neg (один). Напишите eval(e: &Expr) → i64 рекурсивным match. Ссылка на Box<Expr> автоматически приводится к &Expr, так что eval(a) работает.', 'enum Expr {
    Num(i64),
    Add(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
    Neg(Box<Expr>),
}

fn eval(e: &Expr) -> i64 {
    todo!()
}
', 'Num(n) даёт n: &i64 — разыменуйте: *n. Для Neg: -eval(a).', '{"driver": "fn num(n: i64) -> Box<Expr> {\n    Box::new(Expr::Num(n))\n}\n\nfn main() {\n    let e = Expr::Add(num(2), Box::new(Expr::Mul(num(3), Box::new(Expr::Neg(num(4))))));\n    println!(\"{}\", eval(&e));\n    println!(\"{}\", eval(&Expr::Num(7)));\n    println!(\"{}\", eval(&Expr::Neg(Box::new(Expr::Neg(num(5))))));\n}\n", "expected": ["-10", "7", "5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-expr-show', 21, 'rust', 'Дерево выражений: show', 'Тот же Expr. Напишите show(e: &Expr) → String: Num → число; Add → «(A + B)»; Mul → «(A * B)»; Neg → «-A».', 'enum Expr {
    Num(i64),
    Add(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
    Neg(Box<Expr>),
}

fn show(e: &Expr) -> String {
    todo!()
}
', 'Для вложенных частей вызывайте show(a), show(b) и вставляйте результаты в format!.', '{"driver": "fn num(n: i64) -> Box<Expr> {\n    Box::new(Expr::Num(n))\n}\n\nfn main() {\n    let e = Expr::Add(num(2), Box::new(Expr::Mul(num(3), Box::new(Expr::Neg(num(4))))));\n    println!(\"{}\", show(&e));\n    println!(\"{}\", show(&Expr::Num(-7)));\n}\n", "expected": ["(2 + (3 * -4))", "-7"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-derive-ord', 22, 'rust', 'derive(Ord): порядок полей — порядок сравнения', 'Version { major, minor, patch } выводит PartialOrd и Ord, но поля записаны в неправильном порядке, поэтому версии сортируются неверно. Исправьте определение структуры, ничего больше не меняя: 1.2.9 < 1.10.0 < 2.0.0.', '#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
struct Version {
    patch: u32,
    minor: u32,
    major: u32,
}
', 'Лексикографическое сравнение идёт в порядке полей в определении: сначала major, потом minor, потом patch.', '{"driver": "fn main() {\n    let mut v = vec![\n        Version { major: 2, minor: 0, patch: 0 },\n        Version { major: 1, minor: 10, patch: 0 },\n        Version { major: 1, minor: 2, patch: 9 },\n        Version { major: 1, minor: 2, patch: 10 },\n    ];\n    v.sort();\n    for x in &v {\n        print!(\"{}.{}.{} \", x.major, x.minor, x.patch);\n    }\n    println!();\n    let m = v.iter().max().unwrap();\n    println!(\"{}.{}.{} {}\", m.major, m.minor, m.patch, v[0] < v[1]);\n}\n", "expected": ["1.2.9 1.2.10 1.10.0 2.0.0", "2.0.0 true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-default', 23, 'rust', 'Default вручную и ..Default::default()', 'Settings: retries: u32, timeout_ms: u64, verbose: bool, name: String, proxy: Option<String>. Реализуйте Default: retries 3, timeout_ms 5000, verbose false, name "app", proxy None. quiet() → Settings: все значения по умолчанию, кроме retries = 0 (используйте ..Default::default()).', '#[derive(Debug)]
struct Settings {
    retries: u32,
    timeout_ms: u64,
    verbose: bool,
    name: String,
    proxy: Option<String>,
}

impl Default for Settings {
    fn default() -> Settings {
        todo!()
    }
}

fn quiet() -> Settings {
    todo!()
}
', 'Синтаксис обновления: Settings { retries: 0, ..Default::default() } берёт остальные поля из значения по умолчанию.', '{"driver": "fn main() {\n    println!(\"{:?}\", Settings::default());\n    println!(\"{:?}\", quiet());\n    let s = Settings { verbose: true, ..Settings::default() };\n    println!(\"{} {}\", s.verbose, s.name);\n}\n", "expected": ["Settings { retries: 3, timeout_ms: 5000, verbose: false, name: \"app\", proxy: None }", "Settings { retries: 0, timeout_ms: 5000, verbose: false, name: \"app\", proxy: None }", "true app"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-builder', 24, 'rust', 'Строитель: цепочка методов с self', 'RequestBuilder собирает запрос. new(url), header(self, k, v) → Self (добавить заголовок), timeout(self, t: u32) → Self, build(self) → Request. Request::describe(&self) → String: «GET <url> timeout=<t> [k: v, k2: v2]»; без заголовков — «[]». Таймаут по умолчанию 30. Методы принимают self по значению и возвращают его обратно.', 'struct Request {
    url: String,
    headers: Vec<(String, String)>,
    timeout: u32,
}

struct RequestBuilder {
    url: String,
    headers: Vec<(String, String)>,
    timeout: u32,
}

impl RequestBuilder {
    fn new(url: &str) -> RequestBuilder {
        todo!()
    }

    fn header(mut self, k: &str, v: &str) -> RequestBuilder {
        todo!()
    }

    fn timeout(mut self, t: u32) -> RequestBuilder {
        todo!()
    }

    fn build(self) -> Request {
        todo!()
    }
}

impl Request {
    fn describe(&self) -> String {
        todo!()
    }
}
', 'Каждый метод изменяет self и возвращает его: self.headers.push(...); self.', '{"driver": "fn main() {\n    let r = RequestBuilder::new(\"http://a.b/\")\n        .header(\"Accept\", \"text/html\")\n        .timeout(5)\n        .header(\"X-Id\", \"7\")\n        .build();\n    println!(\"{}\", r.describe());\n    println!(\"{}\", RequestBuilder::new(\"/x\").build().describe());\n}\n", "expected": ["GET http://a.b/ timeout=5 [Accept: text/html, X-Id: 7]", "GET /x timeout=30 []"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-inventory', 25, 'rust', 'Инвентарь: &, &mut и Option<&T>', 'Item { name: String, qty: u32, price_cents: u64 }. total_value(items: &[Item]) → u64 — сумма qty × price. cheapest(items: &[Item]) → Option<&Item> — позиция с наименьшей ценой за штуку (первая из равных; пустой список → None). restock(items: &mut [Item], name: &str, n: u32) → bool — увеличить qty позиции с таким именем, true если нашли.', 'struct Item {
    name: String,
    qty: u32,
    price_cents: u64,
}

fn total_value(items: &[Item]) -> u64 {
    todo!()
}

fn cheapest(items: &[Item]) -> Option<&Item> {
    todo!()
}

fn restock(items: &mut [Item], name: &str, n: u32) -> bool {
    todo!()
}
', 'Для restock: for it in items.iter_mut() даёт &mut Item; return true прямо из цикла.', '{"driver": "fn main() {\n    let mut items = vec![\n        Item { name: \"pen\".into(), qty: 10, price_cents: 150 },\n        Item { name: \"book\".into(), qty: 2, price_cents: 1200 },\n        Item { name: \"clip\".into(), qty: 100, price_cents: 5 },\n        Item { name: \"tape\".into(), qty: 1, price_cents: 5 },\n    ];\n    println!(\"{}\", total_value(&items));\n    println!(\"{}\", cheapest(&items).map(|i| i.name.as_str()).unwrap_or(\"-\"));\n    println!(\"{} {}\", restock(&mut items, \"book\", 3), restock(&mut items, \"gum\", 1));\n    println!(\"{} {}\", items[1].qty, total_value(&items));\n    println!(\"{}\", cheapest(&[]).is_none());\n}\n", "expected": ["4405", "clip", "true false", "5 8005", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-matrix', 26, 'rust', 'Матрица в одном Vec: row-major', 'Matrix { rows, cols, data: Vec<i32> } хранит элементы построчно: индекс (r, c) → r * cols + c (как двумерный массив в памяти). new(rows, cols) — нули; get(&self, r, c) → Option<i32> (None вне границ); set(&mut self, r, c, v) → bool (false вне границ); transpose(&self) → Matrix.', 'struct Matrix {
    rows: usize,
    cols: usize,
    data: Vec<i32>,
}

impl Matrix {
    fn new(rows: usize, cols: usize) -> Matrix {
        todo!()
    }

    fn get(&self, r: usize, c: usize) -> Option<i32> {
        todo!()
    }

    fn set(&mut self, r: usize, c: usize, v: i32) -> bool {
        todo!()
    }

    fn transpose(&self) -> Matrix {
        todo!()
    }
}
', 'Индекс в одномерном Vec: r * cols + c; при транспонировании у новой матрицы строк столько, сколько столбцов у старой.', '{"driver": "fn main() {\n    let mut m = Matrix::new(2, 3);\n    let mut k = 1;\n    for r in 0..2 {\n        for c in 0..3 {\n            m.set(r, c, k);\n            k += 1;\n        }\n    }\n    println!(\"{:?}\", m.data);\n    let t = m.transpose();\n    println!(\"{} {} {:?}\", t.rows, t.cols, t.data);\n    println!(\"{:?} {:?} {}\", m.get(1, 2), m.get(2, 0), m.set(0, 3, 1));\n}\n", "expected": ["[1, 2, 3, 4, 5, 6]", "3 2 [1, 4, 2, 5, 3, 6]", "Some(6) None false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-value-tree', 27, 'rust', 'Размеченное объединение: Value', 'Value — Int(i64), Float(f64), Text(String) или List(Vec<Value>). total(&Value) → f64 — сумма всех чисел (в том числе вложенных в списки; текст не считается). depth(&Value) → usize: 0 для не списка, для списка — 1 + наибольшая глубина элементов (пустой список — 1). texts(&Value) → Vec<String> — все строки в порядке обхода.', 'enum Value {
    Int(i64),
    Float(f64),
    Text(String),
    List(Vec<Value>),
}

fn total(v: &Value) -> f64 {
    todo!()
}

fn depth(v: &Value) -> usize {
    todo!()
}

fn texts(v: &Value) -> Vec<String> {
    todo!()
}
', 'Список обрабатывается рекурсивно: items.iter().map(total).sum(); max() по пустому итератору даёт None — подойдёт unwrap_or(0).', '{"driver": "fn main() {\n    use Value::*;\n    let v = List(vec![\n        Int(2),\n        Text(\"a\".into()),\n        List(vec![Float(1.5), List(vec![Text(\"b\".into()), Int(10)])]),\n        Text(\"c\".into()),\n    ]);\n    println!(\"{} {} {:?}\", total(&v), depth(&v), texts(&v));\n    println!(\"{} {} {:?}\", total(&Int(5)), depth(&List(vec![])), texts(&Float(1.0)));\n}\n", "expected": ["13.5 3 [\"a\", \"b\", \"c\"]", "5 1 []"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-json', 28, 'rust', 'Рендер JSON из enum', 'Json — Null, Bool, Num(f64), Str(String), Arr(Vec<Json>), Obj(Vec<(String, Json)>). render(&self) → String: компактный JSON без пробелов: null, true/false, число как в {}, строка в двойных кавычках (экранируйте \" и \\), массив [a,b], объект {"k":v,...} в порядке вектора.', 'enum Json {
    Null,
    Bool(bool),
    Num(f64),
    Str(String),
    Arr(Vec<Json>),
    Obj(Vec<(String, Json)>),
}

impl Json {
    fn render(&self) -> String {
        todo!()
    }
}
', 'Вспомогательная функция quote(s) экранирует символы по одному; в format! фигурные скобки удваивают: {{ и }}.', '{"driver": "fn main() {\n    use Json::*;\n    let j = Obj(vec![\n        (\"name\".to_string(), Str(\"Анна \\\"Ню\\\"\".to_string())),\n        (\"age\".to_string(), Num(30.0)),\n        (\"pi\".to_string(), Num(3.5)),\n        (\"tags\".to_string(), Arr(vec![Bool(true), Null, Str(\"a\\\\b\".to_string())])),\n        (\"empty\".to_string(), Arr(vec![])),\n    ]);\n    println!(\"{}\", j.render());\n    println!(\"{}\", Null.render());\n}\n", "expected": ["{\"name\":\"Анна \\\"Ню\\\"\",\"age\":30,\"pi\":3.5,\"tags\":[true,null,\"a\\\\b\"],\"empty\":[]}", "null"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 17, 'r17-event-log', 29, 'rust', 'Журнал событий: struct-варианты', 'Event — Login { user }, Logout { user }, Purchase { user, cents: u32 } (struct-варианты). summarize(events: &[Event]) → (usize, u32, Vec<String>): число входов, сумма покупок в центах и имена пользователей, которые остались в системе (вошли и не вышли) — в порядке последнего входа без выхода.', 'enum Event {
    Login { user: String },
    Logout { user: String },
    Purchase { user: String, cents: u32 },
}

fn summarize(events: &[Event]) -> (usize, u32, Vec<String>) {
    todo!()
}
', 'Образец Event::Purchase { cents, .. } берёт нужное поле и пропускает остальные.', '{"driver": "fn main() {\n    let ev = vec![\n        Event::Login { user: \"ann\".into() },\n        Event::Login { user: \"bob\".into() },\n        Event::Purchase { user: \"ann\".into(), cents: 500 },\n        Event::Logout { user: \"ann\".into() },\n        Event::Login { user: \"cat\".into() },\n        Event::Purchase { user: \"cat\".into(), cents: 250 },\n        Event::Logout { user: \"zed\".into() },\n    ];\n    println!(\"{:?}\", summarize(&ev));\n    println!(\"{:?}\", summarize(&[]));\n}\n", "expected": ["(3, 750, [\"bob\", \"cat\"])", "(0, 0, [])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-vec-stats', 0, 'rust', 'Vec: минимум, максимум, среднее', 'stats(v: &[i32]) → Option<(i32, i32, f64)>: минимум, максимум и среднее арифметическое; для пустого среза — None.', 'fn stats(v: &[i32]) -> Option<(i32, i32, f64)> {
    todo!()
}
', 'min() и max() возвращают Option<&i32>; сумму считайте в i64, чтобы не переполнить i32.', '{"driver": "fn main() {\n    println!(\"{:?}\", stats(&[3, -1, 4, 1, 5]));\n    println!(\"{:?}\", stats(&[7]));\n    println!(\"{:?}\", stats(&[]));\n    println!(\"{:?}\", stats(&vec![i32::MAX, i32::MAX]));\n}\n", "expected": ["Some((-1, 5, 2.4))", "Some((7, 7, 7.0))", "None", "Some((2147483647, 2147483647, 2147483647.0))"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-vec-clean', 1, 'rust', 'Vec: retain, sort, dedup', 'clean(v: &mut Vec<i32>) приводит вектор в порядок на месте: убирает отрицательные числа, сортирует по возрастанию, убирает повторы. Новый вектор создавать не нужно.', 'fn clean(v: &mut Vec<i32>) {
    todo!()
}
', 'retain(|&x| x >= 0) оставляет подходящие элементы; dedup убирает соседние повторы, поэтому сначала sort.', '{"driver": "fn main() {\n    let mut v = vec![5, -2, 3, 5, 0, -7, 3, 9, 0];\n    clean(&mut v);\n    println!(\"{:?}\", v);\n    let mut e: Vec<i32> = vec![-1, -2];\n    clean(&mut e);\n    println!(\"{:?} {}\", e, e.is_empty());\n}\n", "expected": ["[0, 3, 5, 9]", "[] true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-chunks', 2, 'rust', 'Срезы Vec: chunks и windows', 'chunked(v, n) → Vec<Vec<i32>>: разбить на куски по n элементов (последний может быть короче; n ≥ 1). window_sums(v, k) → Vec<i32>: суммы всех подряд идущих окон длины k (k ≥ 1; если окно не помещается — пустой вектор).', 'fn chunked(v: &[i32], n: usize) -> Vec<Vec<i32>> {
    todo!()
}

fn window_sums(v: &[i32], k: usize) -> Vec<i32> {
    todo!()
}
', 'chunks(n) и windows(k) — методы срезов; каждый элемент — тоже срез, to_vec() копирует его.', '{"driver": "fn main() {\n    println!(\"{:?}\", chunked(&[1, 2, 3, 4, 5, 6, 7], 3));\n    println!(\"{:?}\", chunked(&[], 2));\n    println!(\"{:?}\", window_sums(&[1, 2, 3, 4, 5], 2));\n    println!(\"{:?}\", window_sums(&[1, 2], 3));\n    println!(\"{:?}\", window_sums(&[4, 4, 4], 3));\n}\n", "expected": ["[[1, 2, 3], [4, 5, 6], [7]]", "[]", "[3, 5, 7, 9]", "[]", "[12]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-vec-reallocs', 3, 'rust', 'Сколько раз вырастет буфер', 'reallocs(n, start_cap) → usize: создайте Vec<u64> через with_capacity(start_cap), добавьте n чисел и верните, сколько раз за это изменилась ёмкость (capacity). Сравните с reallocs(100, 100): ровно ноль — резервировать ёмкость заранее выгодно.', 'fn reallocs(n: usize, start_cap: usize) -> usize {
    todo!()
}
', 'Запоминайте последнюю ёмкость и считайте, сколько раз она менялась после push.', '{"driver": "fn main() {\n    println!(\"{} {}\", reallocs(0, 0), reallocs(1, 0));\n    println!(\"{} {}\", reallocs(100, 0), reallocs(100, 100));\n    println!(\"{} {}\", reallocs(1000, 0), reallocs(1000, 1000));\n    println!(\"{}\", reallocs(100, 60));\n}\n", "expected": ["0 1", "6 0", "9 0", "1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-drain-evens', 4, 'rust', 'Разделить вектор на месте', 'take_evens(v: &mut Vec<i32>) → Vec<i32>: убрать из v все чётные числа и вернуть их в прежнем порядке; в v остаются нечётные (тоже в прежнем порядке). Копировать элементы не нужно: числа просто переезжают.', 'fn take_evens(v: &mut Vec<i32>) -> Vec<i32> {
    todo!()
}
', 'drain(..) выдаёт элементы с владением; partition делит их на два вектора по условию.', '{"driver": "fn main() {\n    let mut v = vec![1, 2, 3, 4, 5, 6, 8];\n    let e = take_evens(&mut v);\n    println!(\"{:?} {:?}\", e, v);\n    let mut w: Vec<i32> = vec![];\n    println!(\"{:?} {:?}\", take_evens(&mut w), w);\n}\n", "expected": ["[2, 4, 6, 8] [1, 3, 5]", "[] []"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-pascal', 5, 'rust', 'Vec<Vec<>>: треугольник Паскаля', 'pascal(n) → Vec<Vec<u64>>: первые n строк треугольника Паскаля (в первой строке одна единица). Каждая строка строится из предыдущей.', 'fn pascal(n: usize) -> Vec<Vec<u64>> {
    todo!()
}
', 'Внутренний элемент равен сумме двух элементов предыдущей строки: rows[i-1][j-1] + rows[i-1][j].', '{"driver": "fn main() {\n    for row in pascal(6) {\n        println!(\"{:?}\", row);\n    }\n    println!(\"{}\", pascal(0).len());\n    println!(\"{}\", pascal(60)[59][30]);\n}\n", "expected": ["[1]", "[1, 1]", "[1, 2, 1]", "[1, 3, 3, 1]", "[1, 4, 6, 4, 1]", "[1, 5, 10, 10, 5, 1]", "0", "59132290782430712"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-iter-pipeline', 6, 'rust', 'Итераторы вместо циклов', 'sum_sq_odd(v) → i32 — сумма квадратов нечётных; dot(a, b) → i32 — скалярное произведение (zip); running_max(v) → Vec<i32> — максимум на каждом префиксе (scan). Слово for в коде использовать нельзя — только адаптеры итераторов.', 'fn sum_sq_odd(v: &[i32]) -> i32 {
    todo!()
}

fn dot(a: &[i32], b: &[i32]) -> i32 {
    todo!()
}

fn running_max(v: &[i32]) -> Vec<i32> {
    todo!()
}
', 'scan(начальное, |состояние, элемент| …) хранит изменяемое состояние между шагами и возвращает Some(следующее значение).', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\"fo\", \"r \")).count();\n    println!(\"{}\", sum_sq_odd(&[1, 2, 3, 4, 5]));\n    println!(\"{}\", dot(&[1, 2, 3], &[4, 5, 6]));\n    println!(\"{:?}\", running_max(&[3, 1, 4, 1, 5, 2, 6]));\n    println!(\"{} {:?}\", dot(&[1, 2], &[3]), running_max(&[]));\n    println!(\"loops: {}\", bad0);\n}\n", "expected": ["35", "32", "[3, 3, 4, 4, 5, 5, 6]", "3 []", "loops: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-closure-capture', 7, 'rust', 'Замыкания и захват', 'count_above(v, threshold) → usize: сколько элементов больше порога (порог захватывается замыканием). running_total(v) → Vec<i32>: нарастающие суммы; замыкание изменяет захваченную переменную sum. apply_n(f: fn(i32) -> i32, n, x) → i32: применить функцию n раз.', 'fn count_above(v: &[i32], threshold: i32) -> usize {
    todo!()
}

fn running_total(v: &[i32]) -> Vec<i32> {
    todo!()
}

fn apply_n(f: fn(i32) -> i32, n: u32, x: i32) -> i32 {
    todo!()
}
', 'Замыкание |&x| sum += x … изменяет внешнюю sum — она должна быть mut; функция принимается как fn(i32) -> i32, и обычное замыкание без захвата подходит.', '{"driver": "fn double(x: i32) -> i32 {\n    x * 2\n}\n\nfn main() {\n    println!(\"{} {}\", count_above(&[1, 5, 10, 15], 5), count_above(&[], 0));\n    println!(\"{:?}\", running_total(&[1, 2, 3, 4]));\n    println!(\"{} {}\", apply_n(double, 5, 1), apply_n(|x| x - 1, 3, 10));\n}\n", "expected": ["2 0", "[1, 3, 6, 10]", "32 7"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-fix-collect', 8, 'rust', 'Исправьте: collect без типа', 'squares_sum возводит элементы в квадрат, собирает их и суммирует. Компилятор не может определить, в какую коллекцию собирать. Исправьте одной правкой.', 'fn squares_sum(v: &[i32]) -> i32 {
    let squares = v.iter().map(|x| x * x).collect();
    squares.iter().sum()
}
', 'collect::<Vec<i32>>() или тип у переменной: let squares: Vec<i32> = ….', '{"driver": "fn main() {\n    println!(\"{} {}\", squares_sum(&[1, 2, 3]), squares_sum(&[]));\n}\n", "expected": ["14 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-caesar', 9, 'rust', 'String: шифр Цезаря', 'caesar(s: &str, k: u8) → String: сдвинуть каждую латинскую букву на k вперёд по кругу (0 ≤ k ≤ 25), регистр сохранить; остальные символы (в том числе кириллицу) оставить как есть.', 'fn caesar(s: &str, k: u8) -> String {
    todo!()
}
', 'c as u8 - b''a'' + k даёт позицию в алфавите; % 26 заворачивает по кругу; collect() из итератора char в String.', '{"driver": "fn main() {\n    println!(\"{}\", caesar(\"Hello, World!\", 3));\n    println!(\"{}\", caesar(\"xyz XYZ\", 3));\n    println!(\"{}\", caesar(\"привет abc\", 1));\n    println!(\"{}\", caesar(&caesar(\"Round trip\", 7), 19));\n}\n", "expected": ["Khoor, Zruog!", "abc ABC", "привет bcd", "Round trip"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-utf8-stats', 10, 'rust', 'Символы и байты', 'char_stats(s) → (usize, usize): число символов и число байт. is_palindrome(s) → bool: палиндром, если игнорировать регистр и все символы, кроме букв и цифр. reverse_words(s) → String: слова в обратном порядке, через один пробел.', 'fn char_stats(s: &str) -> (usize, usize) {
    todo!()
}

fn is_palindrome(s: &str) -> bool {
    todo!()
}

fn reverse_words(s: &str) -> String {
    todo!()
}
', 'Соберите Vec<char> из букв и цифр в нижнем регистре и сравните его с самим собой в обратном порядке.', '{"driver": "fn main() {\n    println!(\"{:?} {:?}\", char_stats(\"привет\"), char_stats(\"abc\"));\n    println!(\"{} {}\", is_palindrome(\"А роза упала на лапу Азора\"), is_palindrome(\"не палиндром\"));\n    println!(\"{}\", is_palindrome(\"A man, a plan, a canal: Panama\"));\n    println!(\"{:?}\", reverse_words(\"  один  два три \"));\n}\n", "expected": ["(6, 12) (3, 3)", "true false", "true", "\"три два один\""]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-title-case', 11, 'rust', 'Первая буква заглавная', 'title_case(s) → String: каждое слово с заглавной буквы, остальные буквы строчные (работает и с кириллицей); слова разделяются в результате ровно одним пробелом.', 'fn title_case(s: &str) -> String {
    todo!()
}
', 'chars() даёт первую букву, а остаток — cs.as_str(); to_uppercase() возвращает итератор, соберите его в String.', '{"driver": "fn main() {\n    println!(\"{}\", title_case(\"hELLO   wORLD\"));\n    println!(\"{}\", title_case(\"привет мир\"));\n    println!(\"{:?}\", title_case(\"   \"));\n    println!(\"{}\", title_case(\"rust\"));\n}\n", "expected": ["Hello World", "Привет Мир", "\"\"", "Rust"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-fix-string-add', 12, 'rust', 'Исправьте: + забрал строку', 'join3 склеивает три строки и дописывает «(из a b c)». Оператор + забирает левый операнд, и a после него использовать нельзя. Исправьте, чтобы функция вернула, например, «xyz (из x y z)».', 'fn join3(a: String, b: String, c: String) -> String {
    let ab = a + &b;
    let abc = ab + &c;
    format!("{abc} (из {a} {b} {c})")
}
', 'format! не забирает аргументы, поэтому после него строки остаются доступны.', '{"driver": "fn main() {\n    println!(\"{}\", join3(\"x\".into(), \"y\".into(), \"z\".into()));\n    println!(\"{}\", join3(\"при\".into(), \"вет\".into(), \"!\".into()));\n}\n", "expected": ["xyz (из x y z)", "привет! (из при вет !)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-word-count', 13, 'rust', 'HashMap и entry: частоты слов', 'word_count(text) → Vec<(String, usize)>: слова (последовательности букв; всё остальное — разделители; регистр не важен) с количеством вхождений, отсортированные по убыванию количества, затем по алфавиту. Подсчёт — через entry.', 'use std::collections::HashMap;

fn word_count(text: &str) -> Vec<(String, usize)> {
    todo!()
}
', 'split(|c: char| !c.is_alphabetic()) разбивает по небуквам; *m.entry(слово).or_insert(0) += 1 считает; сортировка — sort_by с then.', '{"driver": "fn main() {\n    let r = word_count(\"The fox, the DOG; the end. Fox? dog!\");\n    println!(\"{:?}\", r);\n    println!(\"{:?}\", word_count(\"Привет, привет, мир!\"));\n    println!(\"{:?}\", word_count(\"...  \"));\n}\n", "expected": ["[(\"the\", 3), (\"dog\", 2), (\"fox\", 2), (\"end\", 1)]", "[(\"привет\", 2), (\"мир\", 1)]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-group-by-len', 14, 'rust', 'Группировка по длине', 'group_by_len(words: &[&str]) → BTreeMap<usize, Vec<String>>: ключ — длина слова в символах, значение — слова этой длины в порядке появления. Используйте entry(…).or_insert_with(Vec::new).', 'use std::collections::BTreeMap;

fn group_by_len(words: &[&str]) -> BTreeMap<usize, Vec<String>> {
    todo!()
}
', 'or_insert_with(Vec::new) создаёт пустой вектор только если ключа ещё нет; push вызывается на возвращённой &mut.', '{"driver": "fn main() {\n    let m = group_by_len(&[\"a\", \"bb\", \"cc\", \"d\", \"привет\", \"eee\", \"мир\", \"ё\"]);\n    println!(\"{:?}\", m);\n    println!(\"{}\", group_by_len(&[]).len());\n}\n", "expected": ["{1: [\"a\", \"d\", \"ё\"], 2: [\"bb\", \"cc\"], 3: [\"eee\", \"мир\"], 6: [\"привет\"]}", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-two-sum', 15, 'rust', 'Два числа за один проход: HashMap', 'two_sum(v: &[i64], target) → Option<(usize, usize)>: индексы i < j с v[i] + v[j] = target; из всех пар нужна та, у которой j наименьшее (при равных j — наименьшее i). Входы большие, поэтому двойной цикл не уложится в лимит: используйте HashMap «значение → индекс» и один проход.', 'fn two_sum(v: &[i64], target: i64) -> Option<(usize, usize)> {
    todo!()
}
', 'Идите по элементам; для текущего x проверьте, есть ли в таблице target - x, и только потом кладите x в таблицу.', '{"driver": "fn main() {\n    println!(\"{:?}\", two_sum(&[2, 7, 11, 15], 9));\n    println!(\"{:?}\", two_sum(&[3, 3], 6));\n    println!(\"{:?}\", two_sum(&[1, 2, 3], 100));\n    let n = 400_000usize;\n    let v: Vec<i64> = (0..n as i64).map(|i| i * 3 + 1).collect();\n    let target = v[n - 2] + v[n - 1];\n    println!(\"{:?}\", two_sum(&v, target));\n}\n", "expected": ["Some((0, 1))", "Some((0, 1))", "None", "Some((399998, 399999))"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-anagrams', 16, 'rust', 'Анаграммы: ключ из отсортированных букв', 'anagram_groups(words: &[&str]) → Vec<Vec<String>>: сгруппируйте слова-анаграммы (регистр не важен, но слова сохраняются как есть). Верните только группы из двух и более слов; слова внутри группы — в порядке появления; группы — в порядке возрастания ключа (букв слова по алфавиту).', 'fn anagram_groups(words: &[&str]) -> Vec<Vec<String>> {
    todo!()
}
', 'Ключ группы — слово, у которого буквы отсортированы; BTreeMap сам упорядочит группы по ключу.', '{"driver": "fn main() {\n    println!(\"{:?}\", anagram_groups(&[\"listen\", \"silent\", \"enlist\", \"google\", \"gogole\", \"cat\", \"act\", \"Tac\", \"dog\"]));\n    println!(\"{:?}\", anagram_groups(&[\"один\", \"два\"]));\n    println!(\"{:?}\", anagram_groups(&[]));\n}\n", "expected": ["[[\"cat\", \"act\", \"Tac\"], [\"google\", \"gogole\"], [\"listen\", \"silent\", \"enlist\"]]", "[]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-merge-counts', 17, 'rust', 'Слияние словарей с владением', 'merge_counts(a, b) → BTreeMap<String, i32>: объединить два словаря счётчиков, складывая значения для общих ключей. Оба словаря передаются по значению: ключи-строки должны переехать, а не копироваться.', 'use std::collections::{BTreeMap, HashMap};

fn merge_counts(a: HashMap<String, i32>, b: HashMap<String, i32>) -> BTreeMap<String, i32> {
    todo!()
}
', 'into_iter() у HashMap отдаёт пары (String, i32) с владением; chain соединяет два итератора.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\".clo\", \"ne()\")).count();\n    let mut a = HashMap::new();\n    a.insert(String::from(\"x\"), 1);\n    a.insert(String::from(\"y\"), 2);\n    let mut b = HashMap::new();\n    b.insert(String::from(\"y\"), 10);\n    b.insert(String::from(\"z\"), 5);\n    println!(\"{:?}\", merge_counts(a, b));\n    println!(\"{:?}\", merge_counts(HashMap::new(), HashMap::new()));\n    println!(\"clones: {}\", bad0);\n}\n", "expected": ["{\"x\": 1, \"y\": 12, \"z\": 5}", "{}", "clones: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-fix-key-move', 18, 'rust', 'Исправьте: ключ переехал в таблицу', 'index(words) → (HashMap<String, usize>, usize): отображение «слово → последний индекс» и суммарная длина всех слов в байтах. Код не собирается: w переезжает в insert, а затем читается. Исправьте минимальной правкой.', 'use std::collections::HashMap;

fn index(words: Vec<String>) -> (HashMap<String, usize>, usize) {
    let mut m = HashMap::new();
    let mut total = 0;
    for (i, w) in words.into_iter().enumerate() {
        m.insert(w, i);
        total += w.len();
    }
    (m, total)
}
', 'Прочитайте w.len() до insert: после insert строка принадлежит таблице. Клонировать не нужно.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\".clo\", \"ne()\")).count();\n    let (m, total) = index(vec![\"aa\".into(), \"b\".into(), \"aa\".into(), \"привет\".into()]);\n    let mut items: Vec<_> = m.iter().collect();\n    items.sort();\n    println!(\"{:?} {}\", items, total);\n    println!(\"clones: {}\", bad0);\n}\n", "expected": ["[(\"aa\", 2), (\"b\", 1), (\"привет\", 3)] 17", "clones: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-parse-age', 19, 'rust', 'Result<u8, String> и виды ошибок разбора', 'parse_age(s) → Result<u8, String>: разберите строку как u8 и верните понятное сообщение: пустая строка → "пусто"; не число (в том числе отрицательное) → "не число"; больше 255 → "слишком велико"; число больше 150 → "нереальный возраст". Вид ошибки узнают через e.kind() и IntErrorKind.', 'use std::num::IntErrorKind;

fn parse_age(s: &str) -> Result<u8, String> {
    todo!()
}
', 'Охрана в match: Ok(n) if n > 150 => …; для ошибок — match e.kind() { IntErrorKind::Empty => …, … }.', '{"driver": "fn main() {\n    for s in [\"42\", \"\", \"abc\", \"-5\", \"300\", \"200\", \"150\", \"0\"] {\n        println!(\"{:?} -> {:?}\", s, parse_age(s));\n    }\n}\n", "expected": ["\"42\" -> Ok(42)", "\"\" -> Err(\"пусто\")", "\"abc\" -> Err(\"не число\")", "\"-5\" -> Err(\"не число\")", "\"300\" -> Err(\"слишком велико\")", "\"200\" -> Err(\"нереальный возраст\")", "\"150\" -> Ok(150)", "\"0\" -> Ok(0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-question-mark', 20, 'rust', 'Оператор ?: цепочка разборов', 'sum_strs(a, b) → Result<i32, ParseIntError>: разобрать обе строки и сложить; average(items: &[&str]) → Result<f64, ParseIntError>: среднее значение чисел (пустой набор → 0.0). Оператор ? обязателен.', 'use std::num::ParseIntError;

fn sum_strs(a: &str, b: &str) -> Result<i32, ParseIntError> {
    todo!()
}

fn average(items: &[&str]) -> Result<f64, ParseIntError> {
    todo!()
}
', 'let x: i32 = a.trim().parse()?; — при ошибке функция сразу вернёт Err.', '{"driver": "fn main() {\n    println!(\"{:?}\", sum_strs(\"3\", \" 4 \"));\n    match sum_strs(\"3\", \"x\") {\n        Ok(v) => println!(\"{v}\"),\n        Err(e) => println!(\"ошибка: {e}\"),\n    }\n    println!(\"{:?}\", average(&[\"1\", \"2\", \"4\"]));\n    println!(\"{:?} {}\", average(&[]), average(&[\"1\", \"\"]).is_err());\n    match average(&[\"99999999999\"]) {\n        Ok(v) => println!(\"{v}\"),\n        Err(e) => println!(\"ошибка: {e}\"),\n    }\n}\n", "expected": ["Ok(7)", "ошибка: invalid digit found in string", "Ok(2.3333333333333335)", "Ok(0.0) true", "ошибка: number too large to fit in target type"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-custom-error', 21, 'rust', 'Своя ошибка: enum, Display, From', 'AppError — Empty, Parse(ParseIntError), Negative(i32). Реализуйте Display («пустая строка» / «не число: <причина>» / «отрицательное: N»), std::error::Error и From<ParseIntError>, затем parse_positive(s) → Result<u32, AppError>: строка с обрезанными пробелами; пустая → Empty; не число → Parse (через ?); меньше нуля → Negative.', 'use std::fmt;
use std::num::ParseIntError;

#[derive(Debug)]
enum AppError {
    Empty,
    Parse(ParseIntError),
    Negative(i32),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}

fn parse_positive(s: &str) -> Result<u32, AppError> {
    todo!()
}
', 'impl From<ParseIntError> for AppError { fn from(e) -> AppError { AppError::Parse(e) } } — тогда ? преобразует ошибку сам.', '{"driver": "fn main() {\n    for s in [\"17\", \"  \", \"x1\", \"-3\", \" 0 \"] {\n        match parse_positive(s) {\n            Ok(n) => println!(\"ok {n}\"),\n            Err(e) => println!(\"{e}\"),\n        }\n    }\n    let e: Box<dyn std::error::Error> = Box::new(AppError::Negative(-1));\n    println!(\"{e}\");\n    println!(\"{:?}\", parse_positive(\"\"));\n}\n", "expected": ["ok 17", "пустая строка", "не число: invalid digit found in string", "отрицательное: -3", "ok 0", "отрицательное: -1", "Err(Empty)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-box-dyn-error', 22, 'rust', 'Box<dyn Error>: любая ошибка', 'run(a, b) → Result<i32, Box<dyn Error>>: разобрать оба аргумента как i32 (ошибка разбора пробрасывается через ?) и разделить a на b; при b == 0 вернуть собственную ошибку «деление на ноль» (строку можно превратить в Box<dyn Error> через .into()).', 'use std::error::Error;

fn run(a: &str, b: &str) -> Result<i32, Box<dyn Error>> {
    todo!()
}
', 'Err("текст".into()) строит Box<dyn Error> из строки; ? сам упаковывает ParseIntError.', '{"driver": "fn main() {\n    for (a, b) in [(\"84\", \"2\"), (\"1\", \"0\"), (\"x\", \"1\"), (\"5\", \"\"), (\"-9\", \"3\")] {\n        match run(a, b) {\n            Ok(v) => println!(\"{v}\"),\n            Err(e) => println!(\"ошибка: {e}\"),\n        }\n    }\n}\n", "expected": ["42", "ошибка: деление на ноль", "ошибка: invalid digit found in string", "ошибка: cannot parse integer from empty string", "-3"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-map-err', 23, 'rust', 'map_err: понятное сообщение', 'read_port(s) → Result<u16, String>: порт из строки. Ошибка разбора превращается в «bad port ''<s>'': <причина>» через map_err, а значение 0 — в «port 0 reserved». Допустимые значения: 1..=65535.', 'fn read_port(s: &str) -> Result<u16, String> {
    todo!()
}
', 'map_err(|e| format!(…)) меняет только ошибку; после него ? пробрасывает уже String.', '{"driver": "fn main() {\n    for s in [\"8080\", \"0\", \"70000\", \"http\", \" 443 \", \"\"] {\n        println!(\"{:?}\", read_port(s));\n    }\n}\n", "expected": ["Ok(8080)", "Err(\"port 0 reserved\")", "Err(\"bad port ''70000'': number too large to fit in target type\")", "Err(\"bad port ''http'': invalid digit found in string\")", "Ok(443)", "Err(\"bad port '''': cannot parse integer from empty string\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-collect-result', 24, 'rust', 'collect в Result<Vec<_>, _>', 'parse_all(items) → Result<Vec<i32>, ParseIntError>: разобрать все строки; при первой ошибке вернуть её (один collect). sum_valid(items) → i32: сумма только корректных чисел, ошибки пропускаются (filter_map + ok).', 'use std::num::ParseIntError;

fn parse_all(items: &[&str]) -> Result<Vec<i32>, ParseIntError> {
    todo!()
}

fn sum_valid(items: &[&str]) -> i32 {
    todo!()
}
', 'collect() в Result<Vec<_>, _> берёт итератор из Result и останавливается на первой ошибке; ok() превращает Result в Option.', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_all(&[\"1\", \" 2 \", \"3\"]));\n    println!(\"{:?}\", parse_all(&[\"1\", \"x\", \"3\", \"y\"]));\n    println!(\"{:?}\", parse_all(&[]));\n    println!(\"{} {}\", sum_valid(&[\"1\", \"x\", \"30\", \"\"]), sum_valid(&[]));\n}\n", "expected": ["Ok([1, 2, 3])", "Err(ParseIntError { kind: InvalidDigit })", "Ok([])", "31 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-ok-or', 25, 'rust', 'ok_or: из Option в Result', 'lookup(m: &HashMap<&str, i32>, key) → Result<i32, String>: значение по ключу или ошибка «нет ключа <key>» (ok_or_else). first_digit(s) → Result<u32, String>: значение первой цифры строки или ошибка «нет цифр» (используйте chars, find и to_digit).', 'use std::collections::HashMap;

fn lookup(m: &HashMap<&str, i32>, key: &str) -> Result<i32, String> {
    todo!()
}

fn first_digit(s: &str) -> Result<u32, String> {
    todo!()
}
', 'get возвращает Option<&i32>; copied() даёт Option<i32>; ok_or_else(|| …) превращает None в Err.', '{"driver": "fn main() {\n    let mut m = HashMap::new();\n    m.insert(\"a\", 1);\n    m.insert(\"b\", 2);\n    println!(\"{:?} {:?}\", lookup(&m, \"a\"), lookup(&m, \"z\"));\n    println!(\"{:?} {:?} {:?}\", first_digit(\"abc7x9\"), first_digit(\"none\"), first_digit(\"\"));\n}\n", "expected": ["Ok(1) Err(\"нет ключа z\")", "Ok(7) Err(\"нет цифр\") Err(\"нет цифр\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-fix-question-mark', 26, 'rust', 'Исправьте: ? в функции без Result', 'double разбирает строку и удваивает число. Оператор ? использован в функции, которая возвращает просто i32 — компилятор отвечает ошибкой. Исправьте сигнатуру (результат — Result<i32, ParseIntError>), тело меняется минимально.', 'use std::num::ParseIntError;

fn double(s: &str) -> i32 {
    let n: i32 = s.trim().parse()?;
    n * 2
}
', 'Тип функции — Result<i32, ParseIntError>, последнее выражение — Ok(n * 2).', '{"driver": "fn main() {\n    println!(\"{:?} {:?}\", double(\"21\"), double(\" -4 \"));\n    println!(\"{}\", double(\"z\").is_err());\n}\n", "expected": ["Ok(42) Ok(-8)", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-unwind-drop', 27, 'rust', 'Паника разматывает стек и вызывает drop', 'Guard печатает «drop g» при уничтожении. Напишите risky(): создайте Guard и затем вызовите panic!("boom"). Драйвер перехватит панику через catch_unwind и покажет, что Guard всё равно был уничтожен: сначала выведется «drop g», затем «caught».', 'struct Guard(&''static str);

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn risky() {
    // создайте Guard и вызовите panic!
}
', 'let _g = Guard("g"); — привязка с именем живёт до конца функции, и при панике drop вызывается во время размотки.', '{"driver": "fn main() {\n    std::panic::set_hook(Box::new(|_| {}));\n    let r = std::panic::catch_unwind(|| risky());\n    println!(\"{}\", if r.is_err() { \"caught\" } else { \"no panic\" });\n}\n", "expected": ["drop g", "caught"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-retry', 28, 'rust', 'Повторные попытки: замыкание FnMut', 'retry(n, f) → Result<i32, String>: вызывайте f(попытка) для попыток 1, 2, …, n, пока не получите Ok; верните первый Ok или последнюю ошибку (n = 0 → «нет попыток»). f — замыкание FnMut(u32) -> Result<i32, String>, оно может менять захваченные переменные.', 'fn retry(n: u32, mut f: impl FnMut(u32) -> Result<i32, String>) -> Result<i32, String> {
    todo!()
}
', 'Храните последнюю ошибку в переменной и возвращайте её после цикла; Ok — сразу через return.', '{"driver": "fn main() {\n    let mut calls = 0;\n    let r = retry(5, |k| {\n        calls += 1;\n        if k < 3 { Err(format!(\"fail {k}\")) } else { Ok(k as i32 * 10) }\n    });\n    println!(\"{:?} calls={}\", r, calls);\n    println!(\"{:?}\", retry(3, |k| Err(format!(\"fail {k}\"))));\n    println!(\"{:?}\", retry(0, |_| Ok(1)));\n}\n", "expected": ["Ok(30) calls=3", "Err(\"fail 3\")", "Err(\"нет попыток\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 18, 'r18-config-parser', 29, 'rust', 'Разбор конфигурации с номерами строк', 'parse_config(text) → Result<BTreeMap<String, String>, String>: строки «ключ = значение»; пустые строки и строки, начинающиеся с «#», пропускаются; пробелы по краям ключа и значения обрезаются. Первая же ошибка: «line N: нет ''=''», «line N: пустой ключ» или «line N: дубликат ключа K» (N — номер строки с единицы).', 'use std::collections::BTreeMap;

fn parse_config(text: &str) -> Result<BTreeMap<String, String>, String> {
    todo!()
}
', 'lines().enumerate() даёт индекс с нуля — добавьте 1; split_once(''='') делит по первому знаку равенства.', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_config(\"# comment\\nname = app\\n\\nport=8080\\nmode =  fast = yes\\n\"));\n    println!(\"{:?}\", parse_config(\"a=1\\nbroken\\nb=2\"));\n    println!(\"{:?}\", parse_config(\"a=1\\n = 5\"));\n    println!(\"{:?}\", parse_config(\"x=1\\ny=2\\nx=3\"));\n    println!(\"{:?}\", parse_config(\"\"));\n}\n", "expected": ["Ok({\"mode\": \"fast = yes\", \"name\": \"app\", \"port\": \"8080\"})", "Err(\"line 2: нет ''=''\")", "Err(\"line 2: пустой ключ\")", "Err(\"line 3: дубликат ключа x\")", "Ok({})"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-largest', 0, 'rust', 'Обобщённая функция: наибольший элемент', 'Напишите largest<T: PartialOrd>(v: &[T]) → Option<&T>: ссылка на наибольший элемент среза (при равных — первый), None для пустого среза. Функция должна работать и с числами, и с дробными, и со строками.', 'fn largest<T: PartialOrd>(v: &[T]) -> Option<&T> {
    todo!()
}
', 'v.first()? даёт первый элемент или сразу возвращает None; сравнивайте ссылки: x > best.', '{"driver": "fn main() {\n    println!(\"{:?}\", largest(&[3, 9, 2, 9]));\n    println!(\"{:?}\", largest(&[1.5, -2.0, 0.25]));\n    println!(\"{:?}\", largest(&[\"pear\", \"apple\", \"zebra\", \"mango\"]));\n    let e: [i32; 0] = [];\n    println!(\"{:?}\", largest(&e));\n}\n", "expected": ["Some(9)", "Some(1.5)", "Some(\"zebra\")", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-fix-bound', 1, 'rust', 'Исправьте: у T нет сравнения', 'max_of возвращает большее из двух значений. Код не компилируется: компилятор не знает, что T умеет сравниваться. Исправьте сигнатуру — добавьте ограничение трейта, тело менять не нужно.', 'fn max_of<T>(a: T, b: T) -> T {
    if a > b { a } else { b }
}
', 'fn max_of<T: PartialOrd>(…) — после двоеточия идёт трейт, который нужен для знака >.', '{"driver": "fn main() {\n    println!(\"{}\", max_of(3, 9));\n    println!(\"{}\", max_of(\"pear\", \"apple\"));\n    println!(\"{}\", max_of(2.5, -1.0));\n    println!(\"{}\", max_of(''a'', ''z''));\n}\n", "expected": ["9", "pear", "2.5", "z"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-pair', 2, 'rust', 'Обобщённая структура Pair<T>', 'Pair<T> хранит два значения одного типа. new(a, b); swap(self) → Pair<T> с переставленными значениями; larger(&self) → &T — ссылка на большее (доступна только для T: PartialOrd; при равенстве — первое).', 'struct Pair<T> {
    a: T,
    b: T,
}

impl<T> Pair<T> {
    fn new(a: T, b: T) -> Pair<T> {
        todo!()
    }

    fn swap(self) -> Pair<T> {
        todo!()
    }
}

impl<T: PartialOrd> Pair<T> {
    fn larger(&self) -> &T {
        todo!()
    }
}
', 'swap забирает self по значению, поэтому поля можно просто переставить без клонирования.', '{"driver": "fn main() {\n    let p = Pair::new(3, 8);\n    println!(\"{}\", p.larger());\n    let q = p.swap();\n    println!(\"{} {}\", q.a, q.b);\n    let s = Pair::new(String::from(\"kiwi\"), String::from(\"fig\")).swap();\n    println!(\"{} {} {}\", s.a, s.b, s.larger());\n}\n", "expected": ["8", "8 3", "fig kiwi kiwi"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-trait-shape', 3, 'rust', 'Трейт Shape и реализации', 'Трейт Shape уже объявлен: area(&self) → f64 и name(&self) → String. Реализуйте его для Circle (радиус), Rect (две стороны) и Square (сторона): имена «circle», «rect», «square». total_area(shapes: &[Box<dyn Shape>]) → f64 — сумма площадей.', 'use std::f64::consts::PI;

trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> String;
}

struct Circle(f64);
struct Rect(f64, f64);
struct Square(f64);

impl Shape for Circle {
    fn area(&self) -> f64 {
        todo!()
    }
    fn name(&self) -> String {
        todo!()
    }
}

// реализуйте Shape для Rect и Square

fn total_area(shapes: &[Box<dyn Shape>]) -> f64 {
    todo!()
}
', 'Для Rect: self.0 * self.1. total_area: shapes.iter().map(|s| s.area()).sum().', '{"driver": "fn main() {\n    let shapes: Vec<Box<dyn Shape>> = vec![Box::new(Circle(1.0)), Box::new(Rect(2.0, 3.0)), Box::new(Square(4.0))];\n    for s in &shapes {\n        println!(\"{} {:.2}\", s.name(), s.area());\n    }\n    println!(\"{:.3}\", total_area(&shapes));\n    println!(\"{}\", total_area(&[]) == 0.0);\n}\n", "expected": ["circle 3.14", "rect 6.00", "square 16.00", "25.142", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-default-method', 4, 'rust', 'Метод по умолчанию и переопределение', 'Трейт Describe: обязательный метод name(&self) → String и метод по умолчанию describe(&self) → String = «<name>: описание отсутствует». Реализуйте для Cat (используйте метод по умолчанию) и для Dog (переопределите describe: «<name> лает»).', 'trait Describe {
    fn name(&self) -> String;
    // добавьте describe с реализацией по умолчанию
}

struct Cat;
struct Dog {
    nick: String,
}

// impl Describe for Cat / Dog
', 'В трейте у describe есть тело, а в impl для Cat его не пишут; для Dog пишут свой describe.', '{"driver": "fn main() {\n    println!(\"{}\", Cat.describe());\n    let d = Dog { nick: \"Рекс\".into() };\n    println!(\"{} | {}\", d.name(), d.describe());\n}\n", "expected": ["cat: описание отсутствует", "Рекс | Рекс лает"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-supertrait', 5, 'rust', 'Супертрейт: Named: Display', 'Трейт Tagged требует Display (супертрейт): tag(&self) → String по умолчанию «<ЗНАЧЕНИЕ>» — результат Display, обёрнутый в угловые скобки. Реализуйте Tagged для Point (Display — «(x, y)») и для u32 (Display уже есть).', 'use std::fmt;

struct Point {
    x: i32,
    y: i32,
}

// impl fmt::Display for Point — «(x, y)»

trait Tagged: fmt::Display {
    // tag по умолчанию
}

// impl Tagged for Point и для u32
', 'Внутри трейта можно пользоваться Display у self благодаря супертрейту: format!("<{}>", self).', '{"driver": "fn main() {\n    println!(\"{}\", Point { x: 1, y: -2 }.tag());\n    println!(\"{}\", 42u32.tag());\n}\n", "expected": ["<(1, -2)>", "<42>"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-ops-complex', 6, 'rust', 'Операторы: комплексные числа', 'Для Complex { re, im } (f64, Copy) реализуйте Add, Sub, Mul, Neg и Display в виде «1+2i» / «1-2i» (числа через {}, знак перед мнимой частью, модуль мнимой части). Умножение: (a+bi)(c+di) = (ac−bd) + (ad+bc)i.', 'use std::fmt;
use std::ops::{Add, Mul, Neg, Sub};

#[derive(Debug, Clone, Copy, PartialEq)]
struct Complex {
    re: f64,
    im: f64,
}

// impl Add, Sub, Mul, Neg, Display
', 'Каждая операция — метод своего трейта с type Output = Complex; Neg строит значение с обратными знаками.', '{"driver": "fn main() {\n    let a = Complex { re: 1.0, im: 2.0 };\n    let b = Complex { re: 3.0, im: -1.0 };\n    println!(\"{} {} {}\", a + b, a - b, a * b);\n    println!(\"{} {}\", -a, (a * b) * -b);\n    println!(\"{}\", a == Complex { re: 1.0, im: 2.0 });\n}\n", "expected": ["4+1i -2+3i 5+5i", "-1-2i -20-10i", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-ops-assign-index', 7, 'rust', 'AddAssign, Mul<f64> и Index', 'Vec2 { x, y } (f64, Copy): реализуйте AddAssign (v += w), Mul<f64> (v * 2.0) и Mul<Vec2> for f64 (2.0 * v). Grid { w, h, data } хранит клетки построчно: Index<(usize, usize)> и IndexMut<(usize, usize)> по (строка, столбец).', 'use std::ops::{AddAssign, Index, IndexMut, Mul};

#[derive(Debug, Clone, Copy, PartialEq)]
struct Vec2 {
    x: f64,
    y: f64,
}

struct Grid {
    w: usize,
    h: usize,
    data: Vec<i32>,
}

impl Grid {
    fn new(h: usize, w: usize) -> Grid {
        Grid { w, h, data: vec![0; w * h] }
    }
}

// impl AddAssign, Mul<f64>, Mul<Vec2> for f64, Index, IndexMut
', 'Index возвращает ссылку: &self.data[r * self.w + c]; IndexMut — изменяемую ссылку на тот же элемент.', '{"driver": "fn main() {\n    let mut v = Vec2 { x: 1.0, y: 2.0 };\n    v += Vec2 { x: 0.5, y: 0.5 };\n    println!(\"{:?} {:?} {:?}\", v, v * 2.0, 3.0 * v);\n    let mut g = Grid::new(2, 3);\n    g[(0, 1)] = 7;\n    g[(1, 2)] += 5;\n    g[(1, 2)] *= 2;\n    println!(\"{} {} {:?}\", g[(0, 1)], g[(1, 2)], g.data);\n}\n", "expected": ["Vec2 { x: 1.5, y: 2.5 } Vec2 { x: 3.0, y: 5.0 } Vec2 { x: 4.5, y: 7.5 }", "7 10 [0, 7, 0, 0, 0, 10]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-ord-card', 8, 'rust', 'Ручной Ord: масть, затем ранг', 'Card { rank: u8, suit: Suit } с Suit: Clubs < Diamonds < Hearts < Spades. Порядок карт: сначала масть, затем ранг (поля в структуре идут в другом порядке, поэтому derive не подойдёт). Реализуйте Ord и PartialOrd вручную (partial_cmp вызывает cmp); PartialEq и Eq — derive.', 'use std::cmp::Ordering;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Suit {
    Clubs,
    Diamonds,
    Hearts,
    Spades,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct Card {
    rank: u8,
    suit: Suit,
}

// impl Ord for Card и PartialOrd for Card
', 'Сравните кортежи (масть как число, ранг): у кортежей порядок лексикографический, а Suit as u8 берёт номер варианта.', '{"driver": "fn main() {\n    use Suit::*;\n    let mut v = vec![\n        Card { rank: 10, suit: Hearts },\n        Card { rank: 2, suit: Spades },\n        Card { rank: 14, suit: Clubs },\n        Card { rank: 3, suit: Hearts },\n        Card { rank: 2, suit: Clubs },\n    ];\n    v.sort();\n    for c in &v {\n        print!(\"{}{:?} \", c.rank, c.suit);\n    }\n    println!();\n    println!(\"{:?}\", v.iter().max());\n    println!(\"{}\", Card { rank: 2, suit: Spades } > Card { rank: 14, suit: Hearts });\n}\n", "expected": ["2Clubs 14Clubs 3Hearts 10Hearts 2Spades", "Some(Card { rank: 2, suit: Spades })", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-partialord-float', 9, 'rust', 'Полный порядок для f64: total_cmp', 'f64 не реализует Ord из-за NaN. Оберните число: Score(f64) и реализуйте PartialEq, Eq, PartialOrd и Ord через f64::total_cmp (NaN считается наибольшим). Тогда Vec<Score> можно отсортировать методом sort.', 'use std::cmp::Ordering;

#[derive(Debug, Clone, Copy)]
struct Score(f64);

// impl PartialEq, Eq, PartialOrd, Ord for Score
', 'cmp = self.0.total_cmp(&other.0); остальные три трейта выражаются через него.', '{"driver": "fn main() {\n    let mut v: Vec<Score> = [3.5, -1.0, f64::NAN, 2.0, -0.0, 0.0].iter().map(|&x| Score(x)).collect();\n    v.sort();\n    println!(\"{:?}\", v.iter().map(|s| s.0).collect::<Vec<_>>());\n    println!(\"{:?}\", v.iter().max().map(|s| s.0.is_nan()));\n    println!(\"{}\", Score(1.0) < Score(2.0));\n}\n", "expected": ["[-1.0, -0.0, 0.0, 2.0, 3.5, NaN]", "Some(true)", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-mono-name', 10, 'rust', 'Мономорфизация: тип и размер', 'Напишите describe<T>(_: &T) → String: «<имя типа> = <размер> байт» — имя через std::any::type_name::<T>(), размер через size_of::<T>(). Каждый вызов с новым T — это отдельная копия функции, которую компилятор создал при сборке.', 'fn describe<T>(_: &T) -> String {
    todo!()
}
', 'type_name и size_of — функции std; тип указывают через turbofish: type_name::<T>().', '{"driver": "fn main() {\n    println!(\"{}\", describe(&1i32));\n    println!(\"{}\", describe(&1u8));\n    println!(\"{}\", describe(&\"text\"));\n    println!(\"{}\", describe(&vec![1u8, 2]));\n    println!(\"{}\", describe(&(1i32, 2u8)));\n    println!(\"{}\", describe(&Some(Box::new(3i32))));\n}\n", "expected": ["i32 = 4 байт", "u8 = 1 байт", "&str = 16 байт", "alloc::vec::Vec<u8> = 24 байт", "(i32, u8) = 8 байт", "core::option::Option<alloc::boxed::Box<i32>> = 8 байт"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-dyn-size', 11, 'rust', 'Размер толстого указателя', 'Напишите sizes() → [usize; 5]: size_of для &i32, &dyn Shape, Box<dyn Shape>, &[i32], Box<i32> — в таком порядке. Какие из них «толстые» (два слова), а какие — обычные указатели?', 'trait Shape {
    fn area(&self) -> f64;
}

fn sizes() -> [usize; 5] {
    todo!()
}
', 'Срез и трейт-объект хранят дополнительное слово: длину или адрес vtable.', '{"driver": "struct Unit;\nimpl Shape for Unit {\n    fn area(&self) -> f64 {\n        1.0\n    }\n}\n\nfn main() {\n    println!(\"{:?}\", sizes());\n    let b: Box<dyn Shape> = Box::new(Unit);\n    println!(\"{}\", b.area());\n}\n", "expected": ["[8, 16, 16, 16, 8]", "1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-impl-trait-arg', 12, 'rust', 'impl Trait в аргументе', 'join_all(items: &[impl Display], sep: &str) → String: элементы, склеенные разделителем. print_each(items: impl IntoIterator<Item = impl Display>) → Vec<String>: каждый элемент в виде строки «[x]».', 'use std::fmt::Display;

fn join_all(items: &[impl Display], sep: &str) -> String {
    todo!()
}

fn print_each(items: impl IntoIterator<Item = impl Display>) -> Vec<String> {
    todo!()
}
', 'to_string() есть у любого Display; IntoIterator принимает и вектор, и массив, и диапазон.', '{"driver": "fn main() {\n    println!(\"{}\", join_all(&[1, 2, 3], \"-\"));\n    println!(\"{}\", join_all(&[\"a\", \"b\"], \", \"));\n    println!(\"{}\", join_all(&[1.5, 2.25], \" | \"));\n    println!(\"{:?}\", print_each(vec![10, 20]));\n    println!(\"{:?}\", print_each([\"x\", \"y\", \"z\"]));\n    println!(\"{:?}\", print_each(1..=3));\n}\n", "expected": ["1-2-3", "a, b", "1.5 | 2.25", "[\"[10]\", \"[20]\"]", "[\"[x]\", \"[y]\", \"[z]\"]", "[\"[1]\", \"[2]\", \"[3]\"]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-impl-trait-return', 13, 'rust', 'impl Trait в результате', 'evens(limit) → impl Iterator<Item = u32>: чётные числа меньше limit; squares(v: &[i32]) → impl Iterator<Item = i32> + ''_: квадраты элементов среза. Конкретный тип итератора наружу не раскрывается.', 'fn evens(limit: u32) -> impl Iterator<Item = u32> {
    todo!()
}

fn squares(v: &[i32]) -> impl Iterator<Item = i32> + ''_ {
    todo!()
}
', 'В evens достаточно (0..limit).filter(...) — компилятор сам выведет тип; ''_ связывает время жизни итератора со срезом.', '{"driver": "fn main() {\n    println!(\"{:?}\", evens(10).collect::<Vec<_>>());\n    println!(\"{}\", evens(1000).sum::<u32>());\n    let data = vec![1, -2, 3];\n    println!(\"{:?}\", squares(&data).collect::<Vec<_>>());\n    println!(\"{}\", squares(&data).max().unwrap());\n}\n", "expected": ["[0, 2, 4, 6, 8]", "249500", "[1, 4, 9]", "9"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-where-clause', 14, 'rust', 'Блок where', 'count_matching<T, F>(v: &[T], pred: F) → usize where F: Fn(&T) → bool. show_pairs<K, V>(items: &[(K, V)]) → String where K: Display, V: Debug: «ключ=значение» (значение через {:?}) через «; ». Ограничения пишите в where.', 'use std::fmt::{Debug, Display};

fn count_matching<T, F>(v: &[T], pred: F) -> usize
where
    F: Fn(&T) -> bool,
{
    todo!()
}

fn show_pairs<K, V>(items: &[(K, V)]) -> String
where
    K: Display,
    V: Debug,
{
    todo!()
}
', 'filter(|x| pred(x)) — внутри filter элемент имеет тип &&T, а pred ждёт &T; при вызове pred(x) раст сам разыменует.', '{"driver": "fn main() {\n    println!(\"{}\", count_matching(&[1, 2, 3, 4, 5], |x| x % 2 == 1));\n    println!(\"{}\", count_matching(&[\"a\", \"bb\", \"ccc\"], |s| s.len() > 1));\n    println!(\"{}\", show_pairs(&[(\"a\", 1), (\"b\", 2)]));\n    println!(\"{}\", show_pairs(&[(1, \"x\"), (2, \"y\")]));\n    println!(\"{:?}\", show_pairs::<i32, i32>(&[]));\n}\n", "expected": ["3", "2", "a=1; b=2", "1=\"x\"; 2=\"y\"", "\"\""]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-plugin-registry', 15, 'rust', 'Плагины: Vec<Box<dyn Plugin>>', 'Трейт Plugin: name(&self) → &str и run(&mut self, input: &str) → String. Реализуйте Upper (переводит в верхний регистр), Reverse (переворачивает символы) и Counter (возвращает «#N: input», где N — номер вызова с единицы). run_all(plugins: &mut [Box<dyn Plugin>], input) → Vec<String> «имя: результат».', 'trait Plugin {
    fn name(&self) -> &str;
    fn run(&mut self, input: &str) -> String;
}

struct Upper;
struct Reverse;
struct Counter {
    calls: u32,
}

// impl Plugin для трёх типов

fn run_all(plugins: &mut [Box<dyn Plugin>], input: &str) -> Vec<String> {
    todo!()
}
', 'Метод run изменяет плагин, поэтому нужен iter_mut(); имя возьмите заранее (to_string), иначе заём от name() помешает вызвать run.', '{"driver": "fn main() {\n    let mut ps: Vec<Box<dyn Plugin>> = vec![Box::new(Upper), Box::new(Reverse), Box::new(Counter { calls: 0 })];\n    for line in run_all(&mut ps, \"привет\") {\n        println!(\"{line}\");\n    }\n    println!(\"{:?}\", run_all(&mut ps, \"abc\"));\n    println!(\"{}\", std::mem::size_of::<Box<dyn Plugin>>());\n}\n", "expected": ["upper: ПРИВЕТ", "reverse: тевирп", "counter: #1: привет", "[\"upper: ABC\", \"reverse: cba\", \"counter: #2: abc\"]", "16"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-fib-iterator', 16, 'rust', 'Свой итератор: Фибоначчи', 'Структура Fib реализует Iterator<Item = u64>: 0, 1, 1, 2, 3, 5, … (бесконечно; при переполнении итератор заканчивается — используйте checked_add). Fib::new() создаёт начало ряда. Все адаптеры (take, filter, sum) приходят сами.', 'struct Fib {
    a: u64,
    b: u64,
}

impl Fib {
    fn new() -> Fib {
        todo!()
    }
}

impl Iterator for Fib {
    type Item = u64;

    fn next(&mut self) -> Option<u64> {
        todo!()
    }
}
', 'Верните текущее a, затем сдвиньте пару (a, b) = (b, a + b); checked_add с ? завершит итератор при переполнении.', '{"driver": "fn main() {\n    println!(\"{:?}\", Fib::new().take(10).collect::<Vec<_>>());\n    println!(\"{}\", Fib::new().take_while(|&x| x < 4_000_000).filter(|x| x % 2 == 0).sum::<u64>());\n    println!(\"{:?}\", Fib::new().skip(5).step_by(3).take(4).collect::<Vec<_>>());\n    println!(\"{}\", Fib::new().count());\n    println!(\"{:?}\", Fib::new().last());\n}\n", "expected": ["[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]", "4613732", "[5, 21, 89, 377]", "92", "Some(4660046610375530309)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-steps-double-ended', 17, 'rust', 'Итератор с двух концов', 'Steps { cur, end, step } — как диапазон с шагом: next выдаёт cur, cur+step, … пока < end; next_back выдаёт последний элемент (последний шаг перед end). Реализуйте Iterator и DoubleEndedIterator; тогда работает .rev(). Считайте, что step ≥ 1, end ≥ cur.', 'struct Steps {
    cur: u32,
    end: u32,
    step: u32,
}

impl Steps {
    fn new(start: u32, end: u32, step: u32) -> Steps {
        Steps { cur: start, end, step }
    }
}

impl Iterator for Steps {
    type Item = u32;
    fn next(&mut self) -> Option<u32> {
        todo!()
    }
}

impl DoubleEndedIterator for Steps {
    fn next_back(&mut self) -> Option<u32> {
        todo!()
    }
}
', 'next_back: сколько шагов помещается до end — (end - cur - 1) / step; последний элемент cur + n*step, и end сдвигается на него.', '{"driver": "fn main() {\n    println!(\"{:?}\", Steps::new(0, 10, 3).collect::<Vec<_>>());\n    println!(\"{:?}\", Steps::new(0, 10, 3).rev().collect::<Vec<_>>());\n    let mut s = Steps::new(1, 20, 4);\n    println!(\"{:?} {:?} {:?}\", s.next(), s.next_back(), s.next());\n    println!(\"{:?}\", s.collect::<Vec<_>>());\n    println!(\"{:?}\", Steps::new(5, 5, 1).next_back());\n}\n", "expected": ["[0, 3, 6, 9]", "[9, 6, 3, 0]", "Some(1) Some(17) Some(5)", "[9, 13]", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-assoc-const', 18, 'rust', 'Константа в трейте', 'Трейт Polygon: const SIDES: u32 и метод по умолчанию angle_sum() → u32 = (SIDES − 2) × 180. Реализуйте для Triangle (3), Square (4), Hexagon (6). total_sides<A: Polygon, B: Polygon>() → u32 — сумма SIDES двух типов (без значений: тип передают параметром).', 'trait Polygon {
    const SIDES: u32;
    // angle_sum по умолчанию
}

struct Triangle;
struct Square;
struct Hexagon;

// impl Polygon для трёх типов

fn total_sides<A: Polygon, B: Polygon>() -> u32 {
    todo!()
}
', 'Внутри трейта константу называют Self::SIDES; у типа без данных size_of равен нулю.', '{"driver": "fn main() {\n    println!(\"{} {} {}\", Triangle::SIDES, Square::angle_sum(), Hexagon::angle_sum());\n    println!(\"{}\", total_sides::<Triangle, Hexagon>());\n    println!(\"{}\", total_sides::<Square, Square>());\n    println!(\"{}\", std::mem::size_of::<Hexagon>());\n}\n", "expected": ["3 360 720", "9", "8", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-generic-stack', 19, 'rust', 'Stack<T> и условный impl', 'Stack<T> на Vec<T>: new, push, pop → Option<T>, peek → Option<&T>, len, is_empty. Отдельный блок impl<T: Display> Stack<T> добавляет show() → String: элементы от вершины к основанию через « > » (пустой — «(пусто)»).', 'use std::fmt::Display;

struct Stack<T> {
    items: Vec<T>,
}

impl<T> Stack<T> {
    fn new() -> Stack<T> {
        todo!()
    }
    fn push(&mut self, x: T) {
        todo!()
    }
    fn pop(&mut self) -> Option<T> {
        todo!()
    }
    fn peek(&self) -> Option<&T> {
        todo!()
    }
    fn len(&self) -> usize {
        todo!()
    }
    fn is_empty(&self) -> bool {
        todo!()
    }
}

impl<T: Display> Stack<T> {
    fn show(&self) -> String {
        todo!()
    }
}
', 'show идёт по items.iter().rev() — вершина стека в конце вектора.', '{"driver": "fn main() {\n    let mut s = Stack::new();\n    println!(\"{} {}\", s.is_empty(), s.show());\n    for i in [1, 2, 3] {\n        s.push(i);\n    }\n    println!(\"{} {:?} {}\", s.len(), s.peek(), s.show());\n    println!(\"{:?} {:?}\", s.pop(), s.pop());\n    let mut t: Stack<String> = Stack::new();\n    t.push(\"a\".into());\n    t.push(\"b\".into());\n    println!(\"{}\", t.show());\n    let mut v: Stack<Vec<u8>> = Stack::new();\n    v.push(vec![1]);\n    println!(\"{} {}\", v.len(), std::mem::size_of::<Stack<u8>>());\n}\n", "expected": ["true (пусто)", "3 Some(3) 3 > 2 > 1", "Some(3) Some(2)", "b > a", "1 24"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-blanket-impl', 20, 'rust', 'Общая реализация для всех T: Display', 'Трейт Shout с методом shout(&self) → String. Одной общей реализацией impl<T: Display> Shout for T сделайте метод доступным у чисел, строк и ваших типов: результат — текст в верхнем регистре с «!» в конце. Для Money(i64) реализуйте Display («<n> руб.»).', 'use std::fmt::{self, Display};

trait Shout {
    fn shout(&self) -> String;
}

// impl<T: Display> Shout for T

struct Money(i64);

// impl Display for Money
', 'Общая реализация сработает для любого типа с Display — в том числе для Money после реализации Display.', '{"driver": "fn main() {\n    println!(\"{}\", \"hello\".shout());\n    println!(\"{}\", 42.shout());\n    println!(\"{}\", 2.5f32.shout());\n    println!(\"{}\", ''x''.shout());\n    println!(\"{}\", Money(99).shout());\n    println!(\"{}\", String::from(\"привет\").shout());\n}\n", "expected": ["HELLO!", "42!", "2.5!", "X!", "99 РУБ.!", "ПРИВЕТ!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-from-into', 21, 'rust', 'From и Into: температуры', 'Celsius(f64) и Fahrenheit(f64). Реализуйте From<Celsius> for Fahrenheit (f = c·9/5 + 32) и From<Fahrenheit> for Celsius. to_f(t: impl Into<Fahrenheit>) → f64 принимает любую из шкал. Into получается бесплатно.', '#[derive(Debug, Clone, Copy)]
struct Celsius(f64);
#[derive(Debug, Clone, Copy)]
struct Fahrenheit(f64);

// impl From<Celsius> for Fahrenheit и From<Fahrenheit> for Celsius

fn to_f(t: impl Into<Fahrenheit>) -> f64 {
    todo!()
}
', 'impl From<A> for B даёт A::into() → B без дополнительного кода; to_f просто вызывает t.into().', '{"driver": "fn main() {\n    let f: Fahrenheit = Celsius(100.0).into();\n    println!(\"{:.1}\", f.0);\n    let c = Celsius::from(Fahrenheit(212.0));\n    println!(\"{:.1}\", c.0);\n    println!(\"{:.1} {:.1}\", to_f(Celsius(-40.0)), to_f(Fahrenheit(50.0)));\n    println!(\"{:.1}\", to_f(Fahrenheit(32.0)));\n}\n", "expected": ["212.0", "100.0", "-40.0 50.0", "32.0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-try-from', 22, 'rust', 'TryFrom: проверенное значение', 'Percent(u8) хранит число от 0 до 100. Реализуйте TryFrom<i32> for Percent с Error = String: «вне диапазона: N» при N < 0 или N > 100. parse_all(v: &[i32]) → Result<Vec<Percent>, String> — все или первая ошибка.', '#[derive(Debug, PartialEq)]
struct Percent(u8);

// impl TryFrom<i32> for Percent

fn parse_all(v: &[i32]) -> Result<Vec<Percent>, String> {
    todo!()
}
', 'try_into появляется бесплатно; collect в Result<Vec<_>, _> остановится на первой ошибке.', '{"driver": "fn main() {\n    println!(\"{:?}\", Percent::try_from(50));\n    println!(\"{:?}\", Percent::try_from(101));\n    let r: Result<Percent, _> = (-5).try_into();\n    println!(\"{:?}\", r);\n    println!(\"{:?}\", parse_all(&[0, 10, 100]));\n    println!(\"{:?}\", parse_all(&[10, 200, -1]));\n}\n", "expected": ["Ok(Percent(50))", "Err(\"вне диапазона: 101\")", "Err(\"вне диапазона: -5\")", "Ok([Percent(0), Percent(10), Percent(100)])", "Err(\"вне диапазона: 200\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-fromstr', 23, 'rust', 'FromStr: разбор Point', 'Point { x, y } (i32). Реализуйте FromStr: «3,4» (пробелы вокруг чисел допускаются). Ошибки ParsePointError: Missing — нет запятой или частей больше двух; BadNumber(строка) — часть не число. После этого работает "3,4".parse::<Point>().', 'use std::str::FromStr;

#[derive(Debug, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug, PartialEq)]
enum ParsePointError {
    Missing,
    BadNumber(String),
}

// impl FromStr for Point
', 'Разбейте по '','', проверьте длину, а числа разбирайте замыканием с map_err и оператором ?.', '{"driver": "fn main() {\n    println!(\"{:?}\", \"3,4\".parse::<Point>());\n    println!(\"{:?}\", \" 5 , -6 \".parse::<Point>());\n    println!(\"{:?}\", \"7\".parse::<Point>());\n    println!(\"{:?}\", \"a,1\".parse::<Point>());\n    println!(\"{:?}\", \"1,2,3\".parse::<Point>());\n    let p: Point = \"0,0\".parse().unwrap();\n    println!(\"{}\", p == Point { x: 0, y: 0 });\n}\n", "expected": ["Ok(Point { x: 3, y: 4 })", "Ok(Point { x: 5, y: -6 })", "Err(Missing)", "Err(BadNumber(\"a\"))", "Err(Missing)", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-asref', 24, 'rust', 'AsRef: принять всё похожее на строку', 'total_len<S: AsRef<str>>(items: &[S]) → usize — сумма длин в байтах (подойдут &str и String). checksum<B: AsRef<[u8]>>(b: B) → u32 — сумма байтов (подойдут Vec<u8>, массив, &str, String).', 'fn total_len<S: AsRef<str>>(items: &[S]) -> usize {
    todo!()
}

fn checksum<B: AsRef<[u8]>>(b: B) -> u32 {
    todo!()
}
', 'as_ref() даёт &str или &[u8] — дальше обычная работа со срезом.', '{"driver": "fn main() {\n    println!(\"{}\", total_len(&[\"ab\", \"cde\"]));\n    println!(\"{}\", total_len(&[String::from(\"привет\"), String::from(\"x\")]));\n    println!(\"{}\", checksum(vec![1u8, 2, 3]));\n    println!(\"{}\", checksum([10u8, 20]));\n    println!(\"{}\", checksum(\"AB\"));\n    println!(\"{}\", checksum(String::from(\"a\")));\n}\n", "expected": ["5", "13", "6", "30", "131", "97"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-sum-trait', 25, 'rust', 'impl Sum для своего типа', 'Money(i64) (Copy): реализуйте Add и два трейта std::iter::Sum — для Money и для &Money, чтобы работали v.iter().sum::<Money>() и v.into_iter().sum::<Money>().', 'use std::iter::Sum;
use std::ops::Add;

#[derive(Debug, Clone, Copy, PartialEq)]
struct Money(i64);

// impl Add, Sum<Money>, Sum<&Money>
', 'Sum — это свёртка fold с начальным Money(0); для &Money разыменуйте элемент.', '{"driver": "fn main() {\n    let v = vec![Money(100), Money(250), Money(-30)];\n    let by_ref: Money = v.iter().sum();\n    let by_val = v.clone().into_iter().sum::<Money>();\n    println!(\"{:?} {:?} {}\", by_ref, by_val, by_ref == by_val);\n    println!(\"{:?}\", Vec::<Money>::new().into_iter().sum::<Money>());\n    println!(\"{:?}\", (1..=4).map(|n| Money(n * 10)).sum::<Money>());\n}\n", "expected": ["Money(320) Money(320) true", "Money(0)", "Money(100)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-default-generic', 26, 'rust', 'Default в обобщённом коде', 'defaults<A: Default, B: Default>() → (A, B) — пара значений по умолчанию. or_default<T: Default + PartialEq>(v: T) → Option<T>: None, если значение равно умолчанию. Settings (derive Default): retries: u32, name: String, verbose: bool, ratio: f64, tags: Vec<String>.', 'fn defaults<A: Default, B: Default>() -> (A, B) {
    todo!()
}

fn or_default<T: Default + PartialEq>(v: T) -> Option<T> {
    todo!()
}

struct Settings {
    retries: u32,
    name: String,
    verbose: bool,
    ratio: f64,
    tags: Vec<String>,
}
', 'T::default() доступен благодаря ограничению; для Settings достаточно #[derive(Debug, Default)].', '{"driver": "fn main() {\n    let (a, b): (i32, String) = defaults();\n    println!(\"{:?} {:?}\", a, b);\n    let t = defaults::<bool, Vec<u8>>();\n    println!(\"{:?}\", t);\n    println!(\"{:?} {:?} {:?}\", or_default(0), or_default(5), or_default(String::new()));\n    println!(\"{:?}\", or_default(String::from(\"x\")));\n    println!(\"{:?}\", Settings::default());\n    println!(\"{:?}\", Settings { retries: 3, ..Default::default() });\n}\n", "expected": ["0 \"\"", "(false, [])", "None Some(5) None", "Some(\"x\")", "Settings { retries: 0, name: \"\", verbose: false, ratio: 0.0, tags: [] }", "Settings { retries: 3, name: \"\", verbose: false, ratio: 0.0, tags: [] }"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-visitor', 27, 'rust', 'Visitor с ассоциированным типом', 'Expr — Num(i64), Add(Box<Expr>, Box<Expr>), Mul(Box<Expr>, Box<Expr>). Трейт Visitor имеет type Out и методы num(n), add(a, b), mul(a, b) (результаты уже обработанных частей). Напишите walk<V: Visitor>(e: &Expr, v: &mut V) → V::Out и два посетителя: Eval (Out = i64) и Show (Out = String: «(a + b)», «(a * b)», число).', 'enum Expr {
    Num(i64),
    Add(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
}

trait Visitor {
    type Out;
    fn num(&mut self, n: i64) -> Self::Out;
    fn add(&mut self, a: Self::Out, b: Self::Out) -> Self::Out;
    fn mul(&mut self, a: Self::Out, b: Self::Out) -> Self::Out;
}

fn walk<V: Visitor>(e: &Expr, v: &mut V) -> V::Out {
    todo!()
}

struct Eval;
struct Show;

// impl Visitor for Eval и Show
', 'walk сначала обходит дочерние узлы, а потом передаёт их результаты методу посетителя.', '{"driver": "fn num(n: i64) -> Box<Expr> {\n    Box::new(Expr::Num(n))\n}\n\nfn main() {\n    let e = Expr::Add(num(2), Box::new(Expr::Mul(num(3), num(4))));\n    println!(\"{}\", walk(&e, &mut Eval));\n    println!(\"{}\", walk(&e, &mut Show));\n    println!(\"{}\", walk(&Expr::Num(-5), &mut Show));\n}\n", "expected": ["14", "(2 + (3 * 4))", "-5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-type-state', 28, 'rust', 'Состояния в типе: Door<Open> и Door<Closed>', 'Door<S> хранит счётчик открываний и PhantomData<S>. Door<Closed>::new() → закрытая; у Door<Closed> есть open(self) → Door<Open> (счётчик +1); у Door<Open> — close(self) → Door<Closed> и opened(&self) → u32. Состояние — часть типа: вызвать open у открытой двери нельзя, и в памяти это ничего не стоит.', 'use std::marker::PhantomData;

struct Open;
struct Closed;

struct Door<S> {
    opened: u32,
    _s: PhantomData<S>,
}

// impl Door<Closed> { new, open }
// impl Door<Open> { close, opened }
', 'Состояние хранится только в типе: PhantomData ничего не занимает, поэтому размер Door равен размеру счётчика.', '{"driver": "fn main() {\n    let d = Door::new();\n    let d = d.open();\n    println!(\"{}\", d.opened());\n    let d = d.close().open().close().open();\n    println!(\"{}\", d.opened());\n    println!(\"{} {}\", std::mem::size_of::<Door<Open>>(), std::mem::size_of::<Door<Closed>>());\n    println!(\"{} {}\", std::mem::size_of::<Open>(), std::mem::size_of::<PhantomData<Closed>>());\n}\n", "expected": ["1", "3", "4 4", "0 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 19, 'r19-top-n', 29, 'rust', 'Обобщённый топ-N по трейту', 'Трейт Scored: score(&self) → i64. top_n<T: Scored + Clone>(items: &[T], n: usize) → Vec<T>: n лучших по убыванию счёта (при равных счетах сохраняется исходный порядок — сортировка устойчива). best<T: Scored>(items: &[T]) → Option<&T>: первый элемент с наибольшим счётом. Player { name, points } реализует Scored.', 'trait Scored {
    fn score(&self) -> i64;
}

#[derive(Debug, Clone)]
struct Player {
    name: String,
    points: i64,
}

// impl Scored for Player

fn top_n<T: Scored + Clone>(items: &[T], n: usize) -> Vec<T> {
    todo!()
}

fn best<T: Scored>(items: &[T]) -> Option<&T> {
    todo!()
}
', 'sort_by устойчив: для равных счетов порядок исходного среза сохраняется; truncate(n) оставляет первые n.', '{"driver": "fn main() {\n    let p = |n: &str, s| Player { name: n.to_string(), points: s };\n    let v = vec![p(\"ann\", 50), p(\"bob\", 80), p(\"cat\", 80), p(\"dan\", 10), p(\"eve\", 65)];\n    let top = top_n(&v, 3);\n    let names: Vec<&str> = top.iter().map(|x| x.name.as_str()).collect();\n    println!(\"{:?}\", names);\n    println!(\"{:?}\", top_n(&v, 10).len());\n    println!(\"{:?}\", best(&v).map(|x| &x.name));\n    println!(\"{:?}\", best::<Player>(&[]).is_none());\n}\n", "expected": ["[\"bob\", \"cat\", \"eve\"]", "5", "Some(\"bob\")", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-compose', 0, 'rust', 'Композиция функций', 'compose(f, g) → impl Fn(A) → C: возвращает функцию «сначала f, затем g». Работает для любых типов: числа → строки → длины. Результат — замыкание, которое владеет обеими функциями.', 'fn compose<A, B, C>(f: impl Fn(A) -> B, g: impl Fn(B) -> C) -> impl Fn(A) -> C {
    todo!()
}
', 'Верните move |x| g(f(x)): move нужен, чтобы замыкание забрало f и g — иначе оно переживёт их.', '{"driver": "fn main() {\n    let inc_then_double = compose(|x: i32| x + 1, |x: i32| x * 2);\n    println!(\"{}\", inc_then_double(4));\n    let to_len = compose(|n: i32| n.to_string(), |s: String| s.len());\n    println!(\"{} {}\", to_len(12345), to_len(-7));\n    let shout = compose(|s: &str| s.to_uppercase(), |s: String| s + \"!\");\n    println!(\"{}\", shout(\"привет\"));\n}\n", "expected": ["10", "5 2", "ПРИВЕТ!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-make-adder', 1, 'rust', 'Фабрики замыканий', 'make_adder(n) → impl Fn(i32) → i32 прибавляет n; make_counter() → impl FnMut() → u32 при каждом вызове возвращает 1, 2, 3, …; make_accumulator(start) → impl FnMut(i32) → i32 добавляет число к сумме и возвращает её.', 'fn make_adder(n: i32) -> impl Fn(i32) -> i32 {
    todo!()
}

fn make_counter() -> impl FnMut() -> u32 {
    todo!()
}

fn make_accumulator(start: i32) -> impl FnMut(i32) -> i32 {
    todo!()
}
', 'Захваченную переменную замыкание держит внутри себя: каждое созданное замыкание — со своей копией счётчика.', '{"driver": "fn main() {\n    let add5 = make_adder(5);\n    println!(\"{} {}\", add5(1), add5(-5));\n    let mut c = make_counter();\n    let mut d = make_counter();\n    println!(\"{} {} {} {}\", c(), c(), d(), c());\n    let mut acc = make_accumulator(100);\n    println!(\"{} {} {}\", acc(1), acc(10), acc(-111));\n}\n", "expected": ["6 0", "1 2 1 3", "101 111 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-apply-n', 2, 'rust', 'Функции высшего порядка', 'apply_n(f, n, x) — применить Fn(i32) → i32 к x ровно n раз. twice(f) → impl Fn(i32) → i32 — «f дважды». iterate_until(f, x, limit) → Vec<i32> — значения x, f(x), f(f(x)), … пока они меньше limit.', 'fn apply_n<F: Fn(i32) -> i32>(f: F, n: u32, x: i32) -> i32 {
    todo!()
}

fn twice(f: impl Fn(i32) -> i32) -> impl Fn(i32) -> i32 {
    todo!()
}

fn iterate_until(f: impl Fn(i32) -> i32, x: i32, limit: i32) -> Vec<i32> {
    todo!()
}
', 'apply_n — свёртка по диапазону (0..n): fold(x, |acc, _| f(acc)).', '{"driver": "fn main() {\n    println!(\"{}\", apply_n(|x| x * 2, 10, 1));\n    println!(\"{}\", apply_n(|x| x + 3, 0, 7));\n    let add10 = twice(|x| x + 5);\n    println!(\"{} {}\", add10(1), twice(twice(|x| x * 3))(1));\n    println!(\"{:?}\", iterate_until(|x| x * 2 + 1, 1, 100));\n    println!(\"{:?}\", iterate_until(|x| x + 1, 50, 10));\n}\n", "expected": ["1024", "7", "11 81", "[1, 3, 7, 15, 31, 63]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-fix-move', 3, 'rust', 'Исправьте: замыкание переживёт функцию', 'make_greeter возвращает замыкание, которое здоровается по имени. Компилятор отвечает: замыкание может пережить локальную переменную, на которую ссылается. Исправьте одним словом.', 'fn make_greeter(name: String) -> impl Fn() -> String {
    || format!("Привет, {name}!")
}
', 'Слово move перед вертикальными чертами: name переедет в замыкание.', '{"driver": "fn main() {\n    let g = make_greeter(String::from(\"Аня\"));\n    println!(\"{}\", g());\n    println!(\"{}\", g());\n    let h = make_greeter(\"Борис\".to_string());\n    println!(\"{}\", h());\n}\n", "expected": ["Привет, Аня!", "Привет, Аня!", "Привет, Борис!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-fix-fnonce', 4, 'rust', 'Исправьте: замыкание вызывается один раз', 'run_once вызывает переданное замыкание единственный раз, но объявлено как F: Fn. Замыкание из драйвера потребляет строку (FnOnce), и сборка падает. Исправьте ограничение трейта.', 'fn run_once<F: Fn() -> String>(f: F) -> String {
    f()
}
', 'FnOnce — самый слабый трейт: подходит и замыканию, которое отдаёт захваченное значение.', '{"driver": "fn main() {\n    let s = String::from(\"уникальная строка\");\n    println!(\"{}\", run_once(move || s));\n    println!(\"{}\", run_once(|| String::from(\"статическая\")));\n    let v = vec![1, 2, 3];\n    println!(\"{}\", run_once(move || format!(\"{:?}\", v)));\n}\n", "expected": ["уникальная строка", "статическая", "[1, 2, 3]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-repeat-call', 5, 'rust', 'FnMut: повторять действие', 'repeat_call(n, f: impl FnMut()) вызывает f ровно n раз. times_table(n, f: impl FnMut(u32, u32)) вызывает f(i, j) для всех 1 ≤ i ≤ j ≤ n в порядке (1,1), (1,2), …, (2,2), …. Накопление результата выполняет замыкание вызывающего.', 'fn repeat_call(n: u32, mut f: impl FnMut()) {
    todo!()
}

fn times_table(n: u32, mut f: impl FnMut(u32, u32)) {
    todo!()
}
', 'Параметр f объявлен mut, чтобы его можно было вызывать: FnMut меняет своё состояние при каждом вызове.', '{"driver": "fn main() {\n    let mut count = 0;\n    repeat_call(5, || count += 2);\n    println!(\"{}\", count);\n    let mut log = Vec::new();\n    repeat_call(3, || log.push(\"tick\"));\n    println!(\"{:?}\", log);\n    let mut pairs = String::new();\n    times_table(3, |i, j| pairs.push_str(&format!(\"{}x{}={} \", i, j, i * j)));\n    println!(\"{}\", pairs.trim_end());\n    let mut sum = 0;\n    times_table(10, |i, j| sum += i * j);\n    println!(\"{}\", sum);\n}\n", "expected": ["10", "[\"tick\", \"tick\", \"tick\"]", "1x1=1 1x2=2 1x3=3 2x2=4 2x3=6 3x3=9", "1705"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-sort-closures', 6, 'rust', 'Сортировка с замыканиями', 'sort_words(v: &mut Vec<String>) — по длине, при равенстве по алфавиту. sort_scores(v: &mut Vec<(String, i32)>) — по убыванию очков, при равенстве по имени. sort_floats(v: &mut Vec<f64>) — по возрастанию через partial_cmp (NaN нет).', 'fn sort_words(v: &mut Vec<String>) {
    todo!()
}

fn sort_scores(v: &mut Vec<(String, i32)>) {
    todo!()
}

fn sort_floats(v: &mut Vec<f64>) {
    todo!()
}
', 'Для вторичного порядка используйте .then_with(|| …) после первого cmp.', '{"driver": "fn main() {\n    let mut w: Vec<String> = [\"pear\", \"fig\", \"apple\", \"kiwi\", \"date\"].iter().map(|s| s.to_string()).collect();\n    sort_words(&mut w);\n    println!(\"{:?}\", w);\n    let mut s = vec![(\"bob\".to_string(), 5), (\"ann\".to_string(), 9), (\"cat\".to_string(), 5)];\n    sort_scores(&mut s);\n    println!(\"{:?}\", s);\n    let mut f = vec![2.5, -1.0, 3.25, 0.0];\n    sort_floats(&mut f);\n    println!(\"{:?}\", f);\n}\n", "expected": ["[\"fig\", \"date\", \"kiwi\", \"pear\", \"apple\"]", "[(\"ann\", 9), (\"bob\", 5), (\"cat\", 5)]", "[-1.0, 0.0, 2.5, 3.25]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-keep-if', 7, 'rust', 'Обобщённый фильтр с замыканием', 'keep_if<T>(v: Vec<T>, pred: impl Fn(&T) → bool) → Vec<T> — оставить подходящие (элементы переезжают, без клонирования). split_by<T>(v: Vec<T>, pred: impl Fn(&T) → bool) → (Vec<T>, Vec<T>) — подходящие и остальные.', 'fn keep_if<T>(v: Vec<T>, pred: impl Fn(&T) -> bool) -> Vec<T> {
    todo!()
}

fn split_by<T>(v: Vec<T>, pred: impl Fn(&T) -> bool) -> (Vec<T>, Vec<T>) {
    todo!()
}
', 'into_iter() забирает элементы; filter получает &&T, но pred(x) принимает &T — раст разыменует сам.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\".clo\", \"ne()\")).count();\n    println!(\"{:?}\", keep_if(vec![1, 2, 3, 4, 5, 6], |x| x % 3 == 0));\n    println!(\"{:?}\", keep_if(vec![\"a\".to_string(), \"bb\".to_string(), \"c\".to_string()], |s| s.len() == 1));\n    let (short, long) = split_by(vec![\"tree\", \"a\", \"forest\", \"ox\"], |s| s.len() <= 2);\n    println!(\"{:?} {:?}\", short, long);\n    println!(\"clones: {}\", bad0);\n}\n", "expected": ["[3, 6]", "[\"a\", \"c\"]", "[\"a\", \"ox\"] [\"tree\", \"forest\"]", "clones: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-memo', 8, 'rust', 'Кеш вычислений: Memo<F>', 'Memo<F: Fn(u64) → u64> хранит функцию и HashMap результатов. new(f); get(&mut self, x) → u64 вызывает f только при первом запросе значения; hits() → u32 — сколько раз ответ взят из кеша. Драйвер считает вызовы f сам.', 'use std::collections::HashMap;

struct Memo<F: Fn(u64) -> u64> {
    f: F,
    cache: HashMap<u64, u64>,
    hits: u32,
}

impl<F: Fn(u64) -> u64> Memo<F> {
    fn new(f: F) -> Memo<F> {
        todo!()
    }
    fn get(&mut self, x: u64) -> u64 {
        todo!()
    }
    fn hits(&self) -> u32 {
        todo!()
    }
}
', 'Вызов поля-замыкания пишут в скобках: (self.f)(x), иначе раст ищет метод f.', '{"driver": "use std::cell::Cell;\n\nfn main() {\n    let calls = Cell::new(0);\n    let mut m = Memo::new(|x| {\n        calls.set(calls.get() + 1);\n        x * x\n    });\n    println!(\"{} {} {}\", m.get(4), m.get(4), m.get(5));\n    println!(\"{} {}\", m.get(4), m.get(5));\n    println!(\"calls={} hits={}\", calls.get(), m.hits());\n}\n", "expected": ["16 16 25", "16 25", "calls=2 hits=3"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-lazy-calls', 9, 'rust', 'Ленивость: считаем вызовы', 'lazy_calls() → (usize, usize): создайте итератор (0..100).map(g), где g увеличивает внешний счётчик и возвращает число × 2. Верните число вызовов g, когда итератор только построен (ничего не запрошено), и после take(3).collect().', 'use std::cell::Cell;

fn lazy_calls() -> (usize, usize) {
    let calls = Cell::new(0usize);
    todo!()
}
', 'Cell позволяет менять значение через общую ссылку: calls.set(calls.get() + 1) внутри замыкания.', '{"driver": "fn main() {\n    println!(\"{:?}\", lazy_calls());\n}\n", "expected": ["(0, 3)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-scan-windows', 10, 'rust', 'Нарастающие суммы и разности', 'prefix_sums(v) → Vec<i32> — нарастающие суммы (scan). diffs(v) → Vec<i32> — разности соседних (windows(2)). running_max(v) → Vec<i32> — максимум на каждом префиксе. is_sorted_asc(v) → bool — через windows.', 'fn prefix_sums(v: &[i32]) -> Vec<i32> {
    todo!()
}

fn diffs(v: &[i32]) -> Vec<i32> {
    todo!()
}

fn running_max(v: &[i32]) -> Vec<i32> {
    todo!()
}

fn is_sorted_asc(v: &[i32]) -> bool {
    todo!()
}
', 'scan(начальное_состояние, |состояние, &x| { …; Some(значение) }); windows(2) даёт срезы по два соседних элемента.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\"fo\", \"r \")).count();\n    println!(\"{:?}\", prefix_sums(&[1, 2, 3, 4]));\n    println!(\"{:?}\", diffs(&[1, 4, 9, 16]));\n    println!(\"{:?}\", running_max(&[3, 1, 4, 1, 5, 2]));\n    println!(\"{} {} {}\", is_sorted_asc(&[1, 2, 2, 5]), is_sorted_asc(&[1, 0]), is_sorted_asc(&[]));\n    println!(\"{:?} {:?}\", prefix_sums(&[]), diffs(&[7]));\n    println!(\"loops: {}\", bad0);\n}\n", "expected": ["[1, 3, 6, 10]", "[3, 5, 7]", "[3, 3, 4, 4, 5, 5]", "true false true", "[] []", "loops: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-flat-map', 11, 'rust', 'flat_map: раскрыть вложенное', 'all_chars(words) → String — все символы слов подряд. pairs(n) → Vec<(i32, i32)> — все пары (i, j) с 1 ≤ i < j ≤ n в лексикографическом порядке. unique_letters(words) → String — все различные буквы в алфавитном порядке.', 'fn all_chars(words: &[&str]) -> String {
    todo!()
}

fn pairs(n: i32) -> Vec<(i32, i32)> {
    todo!()
}

fn unique_letters(words: &[&str]) -> String {
    todo!()
}
', 'Во внутреннем замыкании move |j| (i, j) забирает i; без move i останется ссылкой на внешнюю переменную.', '{"driver": "fn main() {\n    println!(\"{}\", all_chars(&[\"ab\", \"\", \"cde\"]));\n    println!(\"{:?}\", pairs(4));\n    println!(\"{:?}\", pairs(1));\n    println!(\"{}\", unique_letters(&[\"banana\", \"bandana\"]));\n    println!(\"{}\", unique_letters(&[]).len());\n}\n", "expected": ["abcde", "[(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]", "[]", "abdn", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-zip-dot', 12, 'rust', 'zip: скалярное произведение и пары', 'dot(a, b) → i64 — скалярное произведение (до длины короче). pairwise_max(a, b) → Vec<i32> — максимум в каждой позиции. unzip_sum(pairs) → (i32, i32) — суммы первых и вторых элементов (unzip).', 'fn dot(a: &[i32], b: &[i32]) -> i64 {
    todo!()
}

fn pairwise_max(a: &[i32], b: &[i32]) -> Vec<i32> {
    todo!()
}

fn unzip_sum(pairs: &[(i32, i32)]) -> (i32, i32) {
    todo!()
}
', 'zip остановится на более коротком; произведение считайте в i64, чтобы не переполнить i32.', '{"driver": "fn main() {\n    println!(\"{} {}\", dot(&[1, 2, 3], &[4, 5, 6]), dot(&[1, 2], &[10]));\n    println!(\"{}\", dot(&[i32::MAX, i32::MAX], &[2, 2]));\n    println!(\"{:?}\", pairwise_max(&[1, 9, 3], &[4, 2, 8, 100]));\n    println!(\"{:?}\", unzip_sum(&[(1, 10), (2, 20), (3, 30)]));\n    println!(\"{:?}\", unzip_sum(&[]));\n}\n", "expected": ["32 10", "8589934588", "[4, 9, 8]", "(6, 60)", "(0, 0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-chunks-windows', 13, 'rust', 'chunks и windows', 'chunk_sums(v, k) → Vec<i32> — суммы подряд идущих кусков по k (последний может быть короче). moving_average(v, k) → Vec<f64> — среднее каждого окна из k элементов. peaks(v) → Vec<usize> — индексы пиков: элементов строго больше обоих соседей.', 'fn chunk_sums(v: &[i32], k: usize) -> Vec<i32> {
    todo!()
}

fn moving_average(v: &[i32], k: usize) -> Vec<f64> {
    todo!()
}

fn peaks(v: &[i32]) -> Vec<usize> {
    todo!()
}
', 'У windows(3) индекс пика на единицу больше номера окна: .map(|(i, _)| i + 1).', '{"driver": "fn main() {\n    println!(\"{:?}\", chunk_sums(&[1, 2, 3, 4, 5, 6, 7], 3));\n    println!(\"{:?}\", moving_average(&[1, 2, 3, 4, 5], 2));\n    println!(\"{:?}\", moving_average(&[10, 20], 3));\n    println!(\"{:?}\", peaks(&[1, 3, 2, 5, 5, 4, 6, 1]));\n    println!(\"{:?}\", peaks(&[1, 2]));\n}\n", "expected": ["[6, 15, 7]", "[1.5, 2.5, 3.5, 4.5]", "[]", "[1, 6]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-partition-runs', 14, 'rust', 'Разбиения и серии', 'partition_parity(v) → (Vec<i32>, Vec<i32>) — чётные и нечётные. run_lengths(v) → Vec<(i32, usize)> — серии одинаковых подряд идущих значений. split_runs(v) → Vec<Vec<i32>> — те же серии как подмассивы.', 'fn partition_parity(v: &[i32]) -> (Vec<i32>, Vec<i32>) {
    todo!()
}

fn run_lengths(v: &[i32]) -> Vec<(i32, usize)> {
    todo!()
}

fn split_runs(v: &[i32]) -> Vec<Vec<i32>> {
    todo!()
}
', 'В fold накопитель — вектор пар; последнюю пару можно изменить через last_mut().', '{"driver": "fn main() {\n    println!(\"{:?}\", partition_parity(&[1, 2, 3, 4, 5, 6]));\n    println!(\"{:?}\", run_lengths(&[1, 1, 2, 2, 2, 1, 3]));\n    println!(\"{:?}\", split_runs(&[5, 5, 7, 5]));\n    println!(\"{:?} {:?}\", run_lengths(&[]), split_runs(&[]));\n}\n", "expected": ["([2, 4, 6], [1, 3, 5])", "[(1, 2), (2, 3), (1, 1), (3, 1)]", "[[5, 5], [7], [5]]", "[] []"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-find-any', 15, 'rust', 'Поиск: any, all, find, position', 'all_distinct(v) → bool; first_negative_index(v) → Option<usize>; first_number(words: &[&str]) → Option<i64> — первое слово, которое парсится как число (find_map); position_of_max(v) → Option<usize> — индекс первого максимума.', 'fn all_distinct(v: &[i32]) -> bool {
    todo!()
}

fn first_negative_index(v: &[i32]) -> Option<usize> {
    todo!()
}

fn first_number(words: &[&str]) -> Option<i64> {
    todo!()
}

fn position_of_max(v: &[i32]) -> Option<usize> {
    todo!()
}
', 'find_map объединяет поиск и преобразование: возвращает первое Some.', '{"driver": "fn main() {\n    println!(\"{} {} {}\", all_distinct(&[3, 1, 2]), all_distinct(&[1, 2, 1]), all_distinct(&[]));\n    println!(\"{:?} {:?}\", first_negative_index(&[4, 0, -2, -5]), first_negative_index(&[1, 2]));\n    println!(\"{:?} {:?}\", first_number(&[\"abc\", \"x1\", \"42\", \"7\"]), first_number(&[\"a\", \"b\"]));\n    println!(\"{:?} {:?}\", position_of_max(&[2, 9, 1, 9]), position_of_max(&[]));\n}\n", "expected": ["true false true", "Some(2) None", "Some(42) None", "Some(1) None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-min-max-by', 16, 'rust', 'min_by, max_by_key, partial_cmp', 'longest_word(words) → Option<&str> — первое самое длинное. closest_to(v: &[f64], target) → Option<f64> — ближайшее к target значение (при равенстве — первое). youngest(people: &[(&str, u32)]) → Option<&str> — имя самого молодого (первого).', 'fn longest_word<''a>(words: &[&''a str]) -> Option<&''a str> {
    todo!()
}

fn closest_to(v: &[f64], target: f64) -> Option<f64> {
    todo!()
}

fn youngest<''a>(people: &[(&''a str, u32)]) -> Option<&''a str> {
    todo!()
}
', 'max_by_key при равенстве возвращает ПОСЛЕДНИЙ, min_by_key — первый: для «первого самого длинного» удобнее fold.', '{"driver": "fn main() {\n    println!(\"{:?}\", longest_word(&[\"aa\", \"bbb\", \"ccc\", \"d\"]));\n    println!(\"{:?}\", longest_word(&[]));\n    println!(\"{:?} {:?}\", closest_to(&[1.0, 4.5, 3.9, 10.0], 4.0), closest_to(&[], 1.0));\n    println!(\"{:?}\", closest_to(&[2.0, 4.0], 3.0));\n    println!(\"{:?}\", youngest(&[(\"ann\", 31), (\"bob\", 22), (\"cat\", 22)]));\n}\n", "expected": ["Some(\"bbb\")", "None", "Some(3.9) None", "Some(2.0)", "Some(\"bob\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-fold-counts', 17, 'rust', 'fold: частоты и гистограмма', 'char_counts(s) → BTreeMap<char, usize> — сколько раз встречается каждый символ (через fold). length_histogram(words) → Vec<usize> — количество слов каждой длины, начиная с длины 1 до максимальной (пропущенные длины — нули).', 'use std::collections::BTreeMap;

fn char_counts(s: &str) -> BTreeMap<char, usize> {
    todo!()
}

fn length_histogram(words: &[&str]) -> Vec<usize> {
    todo!()
}
', 'fold(начальный_контейнер, |mut acc, x| { …; acc }): накопитель объявляется mut и возвращается в конце.', '{"driver": "fn main() {\n    println!(\"{:?}\", char_counts(\"hello\"));\n    println!(\"{:?}\", char_counts(\"привет мир\"));\n    println!(\"{:?}\", char_counts(\"\"));\n    println!(\"{:?}\", length_histogram(&[\"a\", \"bb\", \"cc\", \"dddd\", \"e\"]));\n    println!(\"{:?}\", length_histogram(&[]));\n}\n", "expected": ["{''e'': 1, ''h'': 1, ''l'': 2, ''o'': 1}", "{'' '': 1, ''в'': 1, ''е'': 1, ''и'': 2, ''м'': 1, ''п'': 1, ''р'': 2, ''т'': 1}", "{}", "[2, 2, 0, 1]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-collect-result', 18, 'rust', 'collect в Option и Result', 'parse_list(s) → Result<Vec<i32>, ParseIntError> — числа из «1,2,3» (первая ошибка прерывает). all_some(v: &[Option<i32>]) → Option<Vec<i32>> — Some, только если все Some. sum_ok(items: &[&str]) → i32 — сумма разобравшихся чисел, остальные пропускаются.', 'use std::num::ParseIntError;

fn parse_list(s: &str) -> Result<Vec<i32>, ParseIntError> {
    todo!()
}

fn all_some(v: &[Option<i32>]) -> Option<Vec<i32>> {
    todo!()
}

fn sum_ok(items: &[&str]) -> i32 {
    todo!()
}
', 'collect() умеет собирать Result<Vec<_>, _> и Option<Vec<_>> — остановится на первой неудаче.', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_list(\"1, 2,3\"));\n    println!(\"{:?}\", parse_list(\"1,x,3\"));\n    println!(\"{:?}\", parse_list(\"\"));\n    println!(\"{:?}\", all_some(&[Some(1), Some(2)]));\n    println!(\"{:?}\", all_some(&[Some(1), None]));\n    println!(\"{} {}\", sum_ok(&[\"1\", \"x\", \"20\"]), sum_ok(&[]));\n}\n", "expected": ["Ok([1, 2, 3])", "Err(ParseIntError { kind: InvalidDigit })", "Err(ParseIntError { kind: Empty })", "Some([1, 2])", "None", "21 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-collect-maps', 19, 'rust', 'collect в String и HashMap', 'acronym(s) → String — первые буквы слов заглавными. index_by_len(words) → BTreeMap<usize, Vec<&str>> — слова по длине (в порядке появления). to_lookup(pairs: &[(&str, i32)]) → HashMap<&str, i32> — при повторах побеждает последнее значение.', 'use std::collections::{BTreeMap, HashMap};

fn acronym(s: &str) -> String {
    todo!()
}

fn index_by_len<''a>(words: &[&''a str]) -> BTreeMap<usize, Vec<&''a str>> {
    todo!()
}

fn to_lookup<''a>(pairs: &[(&''a str, i32)]) -> HashMap<&''a str, i32> {
    todo!()
}
', 'Итератор пар (K, V) собирается в HashMap, а позже пара с тем же ключом затирает прежнюю.', '{"driver": "fn main() {\n    println!(\"{}\", acronym(\"portable network graphics\"));\n    println!(\"{} {:?}\", acronym(\"  по  умолчанию \"), acronym(\"\"));\n    println!(\"{:?}\", index_by_len(&[\"a\", \"bb\", \"c\", \"dd\", \"eee\"]));\n    let m = to_lookup(&[(\"x\", 1), (\"y\", 2), (\"x\", 3)]);\n    let mut items: Vec<_> = m.iter().collect();\n    items.sort();\n    println!(\"{:?}\", items);\n}\n", "expected": ["PNG", "ПУ \"\"", "{1: [\"a\", \"c\"], 2: [\"bb\", \"dd\"], 3: [\"eee\"]}", "[(\"x\", 3), (\"y\", 2)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-peekable-tokens', 20, 'rust', 'peekable: разбор выражения на токены', 'Token — Num(i64) или Op(char) (+ - * /, скобки ''('' и '')'' тоже Op). tokenize(s) → Result<Vec<Token>, String>: числа из нескольких цифр, пробелы пропускаются; недопустимый символ → Err("bad char X"). Используйте peekable, чтобы дочитать число до конца.', '#[derive(Debug, PartialEq)]
enum Token {
    Num(i64),
    Op(char),
}

fn tokenize(s: &str) -> Result<Vec<Token>, String> {
    todo!()
}
', 'peek() не забирает символ: пока следующий — цифра, копите число и вызывайте next().', '{"driver": "fn main() {\n    println!(\"{:?}\", tokenize(\"12 + 3*(40-5)\"));\n    println!(\"{:?}\", tokenize(\"\"));\n    println!(\"{:?}\", tokenize(\"7 $ 3\"));\n    println!(\"{:?}\", tokenize(\"007\"));\n}\n", "expected": ["Ok([Num(12), Op(''+''), Num(3), Op(''*''), Op(''(''), Num(40), Op(''-''), Num(5), Op('')'')])", "Ok([])", "Err(\"bad char $\")", "Ok([Num(7)])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-rle', 21, 'rust', 'Кодирование серий (RLE)', 'rle(s) → String: «aaabcc» → «a3b1c2» (символ и длина серии). unrle(s) → Option<String> — обратное преобразование; None, если формат неверен (после символа нет цифр). Серии могут быть длиннее 9: «x12».', 'fn rle(s: &str) -> String {
    todo!()
}

fn unrle(s: &str) -> Option<String> {
    todo!()
}
', 'В rle после символа продолжайте читать, пока peek() равен тому же символу; в unrle длину читайте цифрами.', '{"driver": "fn main() {\n    println!(\"{}\", rle(\"aaabcc\"));\n    println!(\"{:?}\", rle(\"\"));\n    println!(\"{}\", rle(\"ppppppppppppq\"));\n    println!(\"{:?}\", unrle(\"a3b1c2\"));\n    println!(\"{:?}\", unrle(\"x12\"));\n    println!(\"{:?} {:?}\", unrle(\"ab\"), unrle(\"3a\"));\n    println!(\"{}\", unrle(&rle(\"привет миииир\")).unwrap());\n}\n", "expected": ["a3b1c2", "\"\"", "p12q1", "Some(\"aaabcc\")", "Some(\"xxxxxxxxxxxx\")", "None None", "привет миииир"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-successors', 22, 'rust', 'successors: ряды по правилу', 'collatz(n) → Vec<u64> — последовательность Коллатца от n до 1 включительно (чётное /2, нечётное 3n+1). powers_of_two_below(limit) → Vec<u64> — 1, 2, 4, … меньше limit. digits(n: u64) → Vec<u8> — цифры числа слева направо (через successors и деление на 10).', 'fn collatz(n: u64) -> Vec<u64> {
    todo!()
}

fn powers_of_two_below(limit: u64) -> Vec<u64> {
    todo!()
}

fn digits(n: u64) -> Vec<u8> {
    todo!()
}
', 'successors(Some(начало), |&x| правило) — когда правило вернёт None, ряд заканчивается.', '{"driver": "fn main() {\n    println!(\"{:?}\", collatz(6));\n    println!(\"{:?}\", collatz(1));\n    println!(\"{}\", collatz(27).len());\n    println!(\"{:?}\", powers_of_two_below(100));\n    println!(\"{}\", powers_of_two_below(u64::MAX).len());\n    println!(\"{:?} {:?}\", digits(9071), digits(0));\n}\n", "expected": ["[6, 3, 10, 5, 16, 8, 4, 2, 1]", "[1]", "112", "[1, 2, 4, 8, 16, 32, 64]", "64", "[9, 0, 7, 1] [0]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-from-fn', 23, 'rust', 'from_fn, repeat и cycle', 'fibs(n) → Vec<u64> — первые n чисел Фибоначчи (std::iter::from_fn с состоянием). round_robin(items, n) → Vec<String> — n элементов по кругу (cycle().take). every_kth(v, k) → Vec<i32> — элементы с индексами 0, k, 2k, … (step_by).', 'fn fibs(n: usize) -> Vec<u64> {
    todo!()
}

fn round_robin(items: &[&str], n: usize) -> Vec<String> {
    todo!()
}

fn every_kth(v: &[i32], k: usize) -> Vec<i32> {
    todo!()
}
', 'В from_fn состояние держит замыкание: объявите его снаружи и перенесите внутрь через move.', '{"driver": "fn main() {\n    println!(\"{:?}\", fibs(10));\n    println!(\"{:?}\", fibs(0));\n    println!(\"{:?}\", round_robin(&[\"a\", \"b\", \"c\"], 7));\n    println!(\"{:?}\", round_robin(&[], 3));\n    println!(\"{:?}\", every_kth(&[1, 2, 3, 4, 5, 6, 7], 3));\n}\n", "expected": ["[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]", "[]", "[\"a\", \"b\", \"c\", \"a\", \"b\", \"c\", \"a\"]", "[]", "[1, 4, 7]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-between-markers', 24, 'rust', 'skip_while и take_while', 'between(lines: &[&str], start: &str, end: &str) → Vec<&str> — строки между первой строкой start и следующей за ней end (сами маркеры не входят; если start нет — пусто; если end нет — до конца). last_n<T: Clone>(v: &[T], n) → Vec<T> — последние n элементов в исходном порядке (через rev и take).', 'fn between<''a>(lines: &[&''a str], start: &str, end: &str) -> Vec<&''a str> {
    todo!()
}

fn last_n<T: Clone>(v: &[T], n: usize) -> Vec<T> {
    todo!()
}
', 'skip_while пропускает до маркера включительно не пропуская его самого — поэтому после него нужен skip(1).', '{"driver": "fn main() {\n    let log = [\"x\", \"BEGIN\", \"a\", \"b\", \"END\", \"c\", \"BEGIN\"];\n    println!(\"{:?}\", between(&log, \"BEGIN\", \"END\"));\n    println!(\"{:?}\", between(&log, \"NONE\", \"END\"));\n    println!(\"{:?}\", between(&[\"BEGIN\", \"q\"], \"BEGIN\", \"END\"));\n    println!(\"{:?} {:?}\", last_n(&[1, 2, 3, 4, 5], 2), last_n(&[1, 2], 5));\n    println!(\"{:?}\", last_n::<i32>(&[], 3));\n}\n", "expected": ["[\"a\", \"b\"]", "[]", "[\"q\"]", "[4, 5] [1, 2]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-event-bus', 25, 'rust', 'Обработчики: Vec<Box<dyn FnMut>>', 'Bus хранит обработчики Box<dyn FnMut(&str) → String>. on(&mut self, h) добавляет обработчик; emit(&mut self, event: &str) → Vec<String> вызывает все по порядку и собирает их ответы. Обработчики могут иметь своё изменяемое состояние (счётчик, накопитель).', 'struct Bus {
    handlers: Vec<Box<dyn FnMut(&str) -> String>>,
}

impl Bus {
    fn new() -> Bus {
        todo!()
    }
    fn on(&mut self, h: impl FnMut(&str) -> String + ''static) {
        todo!()
    }
    fn emit(&mut self, event: &str) -> Vec<String> {
        todo!()
    }
}
', 'Box::new(h) превращает замыкание в Box<dyn FnMut>; вызывать через iter_mut(), потому что состояние меняется.', '{"driver": "fn main() {\n    let mut bus = Bus::new();\n    let mut n = 0;\n    bus.on(move |e| {\n        n += 1;\n        format!(\"#{n} {e}\")\n    });\n    bus.on(|e| e.to_uppercase());\n    let mut seen: Vec<String> = Vec::new();\n    bus.on(move |e| {\n        seen.push(e.to_string());\n        seen.join(\"+\")\n    });\n    println!(\"{:?}\", bus.emit(\"start\"));\n    println!(\"{:?}\", bus.emit(\"stop\"));\n    println!(\"{:?}\", Bus::new().emit(\"nobody\"));\n}\n", "expected": ["[\"#1 start\", \"START\", \"start\"]", "[\"#2 stop\", \"STOP\", \"start+stop\"]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-fn-table', 26, 'rust', 'Таблица функций: fn-указатели', 'apply_all(fs: &[fn(f64) → f64], x) → Vec<f64> — результаты всех функций. op_for(name: &str) → Option<fn(f64, f64) → f64> — «add», «sub», «mul», «div» (деление обычное, a / b), иначе None. calc(expr: &str) → Option<f64>: «3 add 4» → 7 (число, имя операции, число); любая ошибка формата → None.', 'fn apply_all(fs: &[fn(f64) -> f64], x: f64) -> Vec<f64> {
    todo!()
}

fn op_for(name: &str) -> Option<fn(f64, f64) -> f64> {
    todo!()
}

fn calc(expr: &str) -> Option<f64> {
    todo!()
}
', 'Указатель fn получается из имени функции: Some(add); замыкание без захвата тоже приводится к fn.', '{"driver": "fn main() {\n    let fs: [fn(f64) -> f64; 3] = [f64::sqrt, f64::abs, |x| x * 10.0];\n    println!(\"{:?}\", apply_all(&fs, 16.0));\n    println!(\"{:?}\", apply_all(&[], 1.0));\n    println!(\"{:?} {:?}\", calc(\"3 add 4\"), calc(\"10 div 4\"));\n    println!(\"{:?} {:?} {:?}\", calc(\"2 pow 3\"), calc(\"x add 1\"), calc(\"1 add\"));\n    println!(\"{}\", std::mem::size_of::<fn(f64) -> f64>());\n}\n", "expected": ["[4.0, 16.0, 160.0]", "[]", "Some(7.0) Some(2.5)", "None None None", "8"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-boxed-predicates', 27, 'rust', 'Комбинаторы предикатов: Box<dyn Fn>', 'in_range(lo, hi) → Box<dyn Fn(i32) → bool>; not(p) → Box<dyn Fn(i32) → bool>; all_of(ps: Vec<Box<dyn Fn(i32) → bool>>) → Box<dyn Fn(i32) → bool> — истина, если все предикаты истинны; any_of — если хотя бы один. Замыкания владеют захваченными значениями.', 'fn in_range(lo: i32, hi: i32) -> Box<dyn Fn(i32) -> bool> {
    todo!()
}

fn not(p: Box<dyn Fn(i32) -> bool>) -> Box<dyn Fn(i32) -> bool> {
    todo!()
}

fn all_of(ps: Vec<Box<dyn Fn(i32) -> bool>>) -> Box<dyn Fn(i32) -> bool> {
    todo!()
}

fn any_of(ps: Vec<Box<dyn Fn(i32) -> bool>>) -> Box<dyn Fn(i32) -> bool> {
    todo!()
}
', 'Каждый комбинатор возвращает Box::new(move |x| …): move забирает предикаты внутрь замыкания.', '{"driver": "fn main() {\n    let teen = in_range(13, 19);\n    println!(\"{} {}\", teen(15), teen(20));\n    let not_teen = not(in_range(13, 19));\n    println!(\"{} {}\", not_teen(15), not_teen(20));\n    let both = all_of(vec![in_range(0, 100), not(in_range(40, 60))]);\n    println!(\"{} {} {}\", both(10), both(50), both(200));\n    let either = any_of(vec![in_range(0, 5), in_range(100, 105)]);\n    println!(\"{} {} {}\", either(3), either(50), either(101));\n    println!(\"{} {}\", all_of(vec![])(1), any_of(vec![])(1));\n}\n", "expected": ["true false", "false true", "true false false", "true false true", "true false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-log-summary', 28, 'rust', 'Конвейер без циклов: сводка журнала', 'summarize(log: &str) → Vec<(String, usize)>: строки вида «LEVEL текст», пустые и без пробела пропускаются; результат — уровни с числом строк, по убыванию числа, при равенстве по алфавиту. Слово for в коде использовать нельзя — только адаптеры и потребители.', 'fn summarize(log: &str) -> Vec<(String, usize)> {
    todo!()
}
', 'lines().filter_map(...) отбросит строки без пробела; подсчёт — fold с HashMap, затем сортировка.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\"fo\", \"r \")).count();\n    let log = \"INFO started\\nWARN disk 91%\\n\\nINFO ready\\nERROR boom\\nbare\\nINFO x\\nWARN y\";\n    println!(\"{:?}\", summarize(log));\n    println!(\"{:?}\", summarize(\"\"));\n    println!(\"loops: {}\", bad0);\n}\n", "expected": ["[(\"INFO\", 3), (\"WARN\", 2), (\"ERROR\", 1)]", "[]", "loops: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 20, 'r20-closure-sizes', 29, 'rust', 'Размер замыкания = размер захваченного', 'closure_sizes() → [usize; 4]: создайте четыре замыкания и верните size_of_val каждого: (1) ничего не захватывает; (2) move || n + 1 с захватом i32 n; (3) || s.len() — без move, берёт ссылку на String s; (4) move-замыкание, владеющее клоном строки s. Замыкание — это структура с захваченными значениями.', 'fn closure_sizes() -> [usize; 4] {
    let n = 7i32;
    let s = String::from("hi");
    todo!()
}
', 'size_of_val(&замыкание); ссылка занимает 8 байт, String — 24, i32 — 4, пустое замыкание — 0.', '{"driver": "fn main() {\n    println!(\"{:?}\", closure_sizes());\n}\n", "expected": ["[0, 4, 8, 24]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-longest', 0, 'rust', 'Метки времени жизни: longest и пары', 'longest<''a>(a, b) → &''a str — более длинная по числу символов (при равенстве первая). first_two<''a>(s) → (&''a str, &''a str) — первые два слова строки (пустая строка вместо отсутствующего). shorter_of<''a>(words: &[&''a str]) → Option<&''a str> — самое короткое слово (первое при равенстве).', 'fn longest<''a>(a: &''a str, b: &''a str) -> &''a str {
    todo!()
}

fn first_two<''a>(s: &''a str) -> (&''a str, &''a str) {
    todo!()
}

fn shorter_of<''a>(words: &[&''a str]) -> Option<&''a str> {
    todo!()
}
', 'Метка ''a на всех ссылках говорит: результат живёт не дольше обоих аргументов; в shorter_of слова несут ''a внутри среза.', '{"driver": "fn main() {\n    println!(\"{} {}\", longest(\"привет\", \"hello\"), longest(\"ab\", \"cd\"));\n    println!(\"{:?} {:?} {:?}\", first_two(\"  one two three\"), first_two(\"solo\"), first_two(\"\"));\n    println!(\"{:?} {:?}\", shorter_of(&[\"pear\", \"fig\", \"kiwi\", \"fog\"]), shorter_of(&[]));\n}\n", "expected": ["привет ab", "(\"one\", \"two\") (\"solo\", \"\") (\"\", \"\")", "Some(\"fig\") None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-two-lifetimes', 1, 'rust', 'Две независимые метки', 'pick_first<''a, ''b>(a: &''a str, _b: &''b str) → &''a str всегда возвращает a. В драйвере вторая строка умирает раньше результата — это допустимо только с ДВУМЯ метками. Реализуйте также between<''a, ''b>(text: &''a str, left: &''b str, right: &''b str) → Option<&''a str> — часть text между первым left и следующим right.', 'fn pick_first<''a, ''b>(a: &''a str, _b: &''b str) -> &''a str {
    todo!()
}

fn between<''a, ''b>(text: &''a str, left: &''b str, right: &''b str) -> Option<&''a str> {
    todo!()
}
', 'Каждой ссылке — своя метка: результат привязан только к ''a, а ''b может закончиться раньше.', '{"driver": "fn main() {\n    let a = String::from(\"долгоживущая\");\n    let r;\n    {\n        let b = String::from(\"короткая\");\n        r = pick_first(&a, &b);\n    }\n    println!(\"{}\", r);\n    let text = String::from(\"x=[alpha]; y=[beta]\");\n    let found;\n    {\n        let (l, rr) = (String::from(\"[\"), String::from(\"]\"));\n        found = between(&text, &l, &rr);\n    }\n    println!(\"{:?}\", found);\n    println!(\"{:?} {:?}\", between(\"no brackets\", \"[\", \"]\"), between(\"[open\", \"[\", \"]\"));\n}\n", "expected": ["долгоживущая", "Some(\"alpha\")", "None None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-split-kv', 2, 'rust', 'Срезы без копирования: key=value', 'split_kv<''a>(line: &''a str) → Option<(&''a str, &''a str)> — «ключ=значение»: ключ и значение без пробелов по краям; None, если нет «=» или ключ пустой. parse_lines<''a>(text: &''a str) → Vec<(&''a str, &''a str)> — все корректные строки. Результат — срезы исходного текста, копий нет.', 'fn split_kv<''a>(line: &''a str) -> Option<(&''a str, &''a str)> {
    todo!()
}

fn parse_lines<''a>(text: &''a str) -> Vec<(&''a str, &''a str)> {
    todo!()
}
', 'trim() возвращает срез той же строки — копии не создаются; filter_map(split_kv) подходит, потому что split_kv принимает &str.', '{"driver": "fn main() {\n    println!(\"{:?} {:?} {:?}\", split_kv(\" a = 1 \"), split_kv(\"=x\"), split_kv(\"novalue\"));\n    let text = String::from(\"host = example.org\\nbad line\\nport=8080\\n=oops\\nmode =\");\n    let kv = parse_lines(&text);\n    println!(\"{:?}\", kv);\n    let (k, _) = kv[0];\n    let off = k.as_ptr() as usize - text.as_ptr() as usize;\n    println!(\"указывает в исходный текст: {}\", off < text.len());\n}\n", "expected": ["Some((\"a\", \"1\")) None None", "[(\"host\", \"example.org\"), (\"port\", \"8080\"), (\"mode\", \"\")]", "указывает в исходный текст: true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-tokens-iterator', 3, 'rust', 'Итератор срезов: Tokens<''a>', 'Tokens<''a> хранит остаток текста и выдаёт слова (непробельные куски) как &''a str — без копирования. Реализуйте Tokens::new(text) и Iterator<Item = &''a str>. Слова должны быть срезами исходной строки (тот же буфер).', 'struct Tokens<''a> {
    rest: &''a str,
}

impl<''a> Tokens<''a> {
    fn new(text: &''a str) -> Tokens<''a> {
        todo!()
    }
}

impl<''a> Iterator for Tokens<''a> {
    type Item = &''a str;
    fn next(&mut self) -> Option<&''a str> {
        todo!()
    }
}
', 'split_at(end) делит срез на слово и остаток — оба с тем же временем жизни ''a.', '{"driver": "fn main() {\n    let text = String::from(\"  привет  мир\\tи\\nвсе \");\n    let words: Vec<&str> = Tokens::new(&text).collect();\n    println!(\"{:?}\", words);\n    let inside = words.iter().all(|w| {\n        let p = w.as_ptr() as usize;\n        p >= text.as_ptr() as usize && p + w.len() <= text.as_ptr() as usize + text.len()\n    });\n    println!(\"{}\", inside);\n    println!(\"{}\", Tokens::new(\"a b c d\").count());\n    println!(\"{:?}\", Tokens::new(\"   \").next());\n    println!(\"{:?}\", Tokens::new(\"x\").map(str::len).sum::<usize>());\n}\n", "expected": ["[\"привет\", \"мир\", \"и\", \"все\"]", "true", "4", "None", "1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-fix-capture', 4, 'rust', 'Исправьте: итератор захватывает ссылку', 'evens_of возвращает итератор по чётным числам вектора, но компилятор жалуется: скрытый тип захватывает время жизни ссылки, которого нет в ограничениях. Допишите в сигнатуру метку, связывающую итератор с аргументом.', 'fn evens_of(v: &Vec<i32>) -> impl Iterator<Item = i32> {
    v.iter().copied().filter(|x| x % 2 == 0)
}
', '+ ''_ означает: итератор живёт не дольше заимствованного аргумента.', '{"driver": "fn main() {\n    let v = vec![1, 2, 3, 4, 5, 6];\n    println!(\"{:?}\", evens_of(&v).collect::<Vec<_>>());\n    println!(\"{}\", evens_of(&v).sum::<i32>());\n    println!(\"{}\", evens_of(&Vec::new()).count());\n}\n", "expected": ["[2, 4, 6]", "12", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-static-table', 5, 'rust', '''static: таблицы и константы', 'static NAMES: [&str; 4] = ["север", "восток", "юг", "запад"]. direction_name(i: usize) → &''static str (индекс по кругу), direction_index(name: &str) → Option<usize>, turn(from: &str, steps: i32) → Option<&''static str> — повернуть на steps четвертей (может быть отрицательным). const QUARTER: i32 = 90.', 'static NAMES: [&str; 4] = ["север", "восток", "юг", "запад"];
const QUARTER: i32 = 90;

fn direction_name(i: usize) -> &''static str {
    todo!()
}

fn direction_index(name: &str) -> Option<usize> {
    todo!()
}

fn turn(from: &str, steps: i32) -> Option<&''static str> {
    todo!()
}
', 'rem_euclid(4) даёт неотрицательный остаток даже для отрицательных поворотов.', '{"driver": "fn main() {\n    println!(\"{} {} {}\", direction_name(0), direction_name(5), direction_name(11));\n    println!(\"{:?} {:?}\", direction_index(\"юг\"), direction_index(\"вверх\"));\n    println!(\"{:?} {:?} {:?}\", turn(\"север\", 1), turn(\"север\", -1), turn(\"запад\", 6));\n    println!(\"{:?}\", turn(\"x\", 1));\n    println!(\"{}\", QUARTER * 4);\n}\n", "expected": ["север восток запад", "Some(2) None", "Some(\"восток\") Some(\"запад\") Some(\"восток\")", "None", "360"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-box-list', 6, 'rust', 'Список на Box: длина, сумма, разворот', 'List { Cons(i32, Box<List>), Nil }. len(&List), sum(&List), to_vec(&List), reverse(List) → List (забирает список и переставляет звенья, без новых выделений через clone), from_slice(&[i32]) → List.', 'enum List {
    Cons(i32, Box<List>),
    Nil,
}
use List::{Cons, Nil};

fn from_slice(v: &[i32]) -> List {
    todo!()
}

fn len(l: &List) -> usize {
    todo!()
}

fn sum(l: &List) -> i32 {
    todo!()
}

fn to_vec(l: &List) -> Vec<i32> {
    todo!()
}

fn reverse(l: List) -> List {
    todo!()
}
', 'fold справа налево (rev()) собирает список с головой в начале; reverse переносит каждое звено в новый список.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\".clo\", \"ne()\")).count();\n    let l = from_slice(&[1, 2, 3, 4]);\n    println!(\"{} {} {:?}\", len(&l), sum(&l), to_vec(&l));\n    let r = reverse(l);\n    println!(\"{:?}\", to_vec(&r));\n    println!(\"{:?} {}\", to_vec(&from_slice(&[])), len(&Nil));\n    println!(\"clones: {}\", bad0);\n}\n", "expected": ["4 10 [1, 2, 3, 4]", "[4, 3, 2, 1]", "[] 0", "clones: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-box-tree', 7, 'rust', 'Двоичное дерево поиска на Box', 'Tree { root: Option<Box<Node>> } с методами insert(&mut self, k) (дубликаты игнорируются), contains(&self, k) → bool, height(&self) → usize (пустое — 0), in_order(&self) → Vec<i32>, min(&self) → Option<i32>.', 'struct Node {
    key: i32,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

struct Tree {
    root: Option<Box<Node>>,
}

impl Tree {
    fn new() -> Tree {
        Tree { root: None }
    }
    fn insert(&mut self, k: i32) {
        todo!()
    }
    fn contains(&self, k: i32) -> bool {
        todo!()
    }
    fn height(&self) -> usize {
        todo!()
    }
    fn in_order(&self) -> Vec<i32> {
        todo!()
    }
    fn min(&self) -> Option<i32> {
        todo!()
    }
}
', 'В insert идите вниз по &mut Option<Box<Node>>: пока Some — выбирайте сторону, а на None запишите новый узел.', '{"driver": "fn main() {\n    let mut t = Tree::new();\n    println!(\"{} {:?} {}\", t.height(), t.min(), t.contains(1));\n    for k in [5, 3, 8, 1, 4, 7, 9, 3, 5, 2] {\n        t.insert(k);\n    }\n    println!(\"{:?}\", t.in_order());\n    println!(\"{} {:?} {} {}\", t.height(), t.min(), t.contains(7), t.contains(6));\n    let mut chain = Tree::new();\n    for k in 1..=6 {\n        chain.insert(k);\n    }\n    println!(\"{}\", chain.height());\n}\n", "expected": ["0 None false", "[1, 2, 3, 4, 5, 7, 8, 9]", "4 Some(1) true false", "6"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-box-dyn-state', 8, 'rust', 'Состояния через Box<dyn State>', 'Трейт State: name(&self) → &''static str и next(self: Box<Self>, event: &str) → Box<dyn State>. Реализуйте Idle → ("start") Running → ("pause") Paused → ("resume") Running; из Running по "stop" → Idle; Paused по "stop" → Idle; неизвестное событие оставляет состояние. run(events: &[&str]) → Vec<&''static str> — имена состояний после каждого события.', 'trait State {
    fn name(&self) -> &''static str;
    fn next(self: Box<Self>, event: &str) -> Box<dyn State>;
}

struct Idle;
struct Running;
struct Paused;

// impl State для трёх типов

fn run(events: &[&str]) -> Vec<&''static str> {
    todo!()
}
', 'self: Box<Self> позволяет забрать и вернуть себя же (_ => self) или заменить другим состоянием.', '{"driver": "fn main() {\n    println!(\"{:?}\", run(&[\"start\", \"pause\", \"resume\", \"stop\", \"stop\"]));\n    println!(\"{:?}\", run(&[\"pause\", \"start\", \"bogus\", \"pause\", \"stop\"]));\n    println!(\"{:?}\", run(&[]));\n    println!(\"{}\", std::mem::size_of::<Box<dyn State>>());\n}\n", "expected": ["[\"running\", \"paused\", \"running\", \"idle\", \"idle\"]", "[\"idle\", \"running\", \"running\", \"paused\", \"idle\"]", "[]", "16"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-box-sizes', 9, 'rust', 'Размеры указателей и Box', 'sizes() → [usize; 8]: size_of для &u8, Box<u8>, Box<[u8; 100]>, &[u8], Box<dyn Fn()>, Option<Box<u8>>, Option<&u8>, Rc<[u8; 100]> — в таком порядке. Какие из них одно слово, а какие два?', 'use std::rc::Rc;

fn sizes() -> [usize; 8] {
    todo!()
}
', 'Срез и dyn хранят дополнительное слово; массив известной длины — обычный указатель; Option над указателем не толще указателя.', '{"driver": "fn main() {\n    println!(\"{:?}\", sizes());\n}\n", "expected": ["[8, 8, 8, 16, 16, 8, 8, 8]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-mybox-deref', 10, 'rust', 'Свой умный указатель: Deref', 'MyBox<T>(T) с new(x). Реализуйте Deref (Target = T) и DerefMut. После этого hello(&MyBox<String>) принимает &str благодаря приведению по разыменованию, а *b даёт внутреннее значение. shout(b: &MyBox<String>) → String вызывает метод строки напрямую.', 'use std::ops::{Deref, DerefMut};

struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        todo!()
    }
}

// impl Deref и DerefMut для MyBox<T>

fn hello(name: &str) -> String {
    format!("Привет, {name}!")
}

fn shout(b: &MyBox<String>) -> String {
    todo!()
}
', 'deref возвращает &self.0; DerefMut — &mut self.0. Приведение &MyBox<String> → &String → &str делает компилятор.', '{"driver": "fn main() {\n    let b = MyBox::new(String::from(\"мир\"));\n    println!(\"{}\", hello(&b));\n    println!(\"{} {}\", shout(&b), b.len());\n    let mut n = MyBox::new(5);\n    *n += 10;\n    println!(\"{}\", *n);\n    let mut s = MyBox::new(String::from(\"a\"));\n    s.push_str(\"bc\");\n    println!(\"{}\", *s);\n}\n", "expected": ["Привет, мир!", "МИР 6", "15", "abc"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-deref-slice', 11, 'rust', 'Deref к срезу: Sorted', 'Sorted хранит Vec<i32> в отсортированном виде. new(v) сортирует; insert(&mut self, x) вставляет на нужное место (бинарный поиск); Deref<Target = [i32]> даёт len(), iter(), first(), contains() и срезы без повторения методов.', 'use std::ops::Deref;

struct Sorted(Vec<i32>);

impl Sorted {
    fn new(mut v: Vec<i32>) -> Sorted {
        todo!()
    }
    fn insert(&mut self, x: i32) {
        todo!()
    }
}

// impl Deref for Sorted { Target = [i32] }
', 'Target = [i32], deref возвращает &self.0 — вектор автоматически превращается в срез.', '{"driver": "fn main() {\n    let mut s = Sorted::new(vec![5, 1, 4]);\n    s.insert(3);\n    s.insert(9);\n    s.insert(0);\n    println!(\"{} {:?} {:?}\", s.len(), s.first(), s.last());\n    println!(\"{:?}\", s.iter().collect::<Vec<_>>());\n    println!(\"{} {}\", s.contains(&4), s.contains(&7));\n    println!(\"{:?} {:?}\", &s[1..3], s.binary_search(&9));\n}\n", "expected": ["6 Some(0) Some(9)", "[0, 1, 3, 4, 5, 9]", "true false", "[1, 3] Ok(5)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-drop-order', 12, 'rust', 'Порядок Drop: журнал', 'Guard(name, log) при уничтожении дописывает в общий журнал «drop name». Реализуйте Drop. scenario(log) создаёт Guard a, b, c в одном блоке, затем вложенный блок с d, затем явно drop(b) и в конце возвращает журнал. Проверьте порядок: переменные умирают в обратном порядке объявления.', 'use std::cell::RefCell;
use std::rc::Rc;

struct Guard {
    name: &''static str,
    log: Rc<RefCell<Vec<String>>>,
}

// impl Drop for Guard

fn scenario() -> Vec<String> {
    let log = Rc::new(RefCell::new(Vec::new()));
    todo!()
}
', 'Журнал общий: Rc<RefCell<Vec<String>>>; в drop пишем через log.borrow_mut().push(...).', '{"driver": "fn main() {\n    for line in scenario() {\n        println!(\"{line}\");\n    }\n}\n", "expected": ["inner", "drop d", "drop b", "end of block", "drop c", "drop a"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-forget-and-moves', 13, 'rust', 'drop, forget и перемещение', 'Guard(&''static str) печатает «drop <имя>» при уничтожении, consume(g) печатает «consume». Напишите trace(): создайте Guard a, b, c; передайте b в consume (Guard умрёт внутри); затем напечатайте «mid»; отдайте c в std::mem::forget (деструктор не вызывается); напечатайте «end». Что будет с a?', 'struct Guard(&''static str);

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn consume(_g: Guard) {
    println!("consume");
}

fn trace() {
    todo!()
}
', 'consume(b) забирает b: drop b сработает на выходе из consume; forget(c) не запускает drop; a умирает на скобке.', '{"driver": "fn main() {\n    trace();\n}\n", "expected": ["consume", "drop b", "mid", "end", "drop a"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-raii-transaction', 14, 'rust', 'RAII: транзакция откатывается сама', 'Tx<''a> заимствует &''a mut Vec<i32> («базу»). begin(db) запоминает исходный размер; push(&mut self, x) добавляет число; commit(self) фиксирует; если Tx уничтожена без commit, Drop откатывает базу к исходной длине. Так «изменения» не просочатся при ошибке или раннем выходе.', 'struct Tx<''a> {
    db: &''a mut Vec<i32>,
    start_len: usize,
    committed: bool,
}

impl<''a> Tx<''a> {
    fn begin(db: &''a mut Vec<i32>) -> Tx<''a> {
        todo!()
    }
    fn push(&mut self, x: i32) {
        todo!()
    }
    fn commit(mut self) {
        todo!()
    }
}

// impl Drop for Tx
', 'commit(mut self) выставляет флаг и сам Tx умирает на выходе: Drop видит committed = true и ничего не откатывает.', '{"driver": "fn main() {\n    let mut db = vec![1, 2];\n    {\n        let mut tx = Tx::begin(&mut db);\n        tx.push(3);\n        tx.push(4);\n        tx.commit();\n    }\n    println!(\"{:?}\", db);\n    {\n        let mut tx = Tx::begin(&mut db);\n        tx.push(99);\n        tx.push(100);\n    }\n    println!(\"{:?}\", db);\n    fn risky(db: &mut Vec<i32>, fail: bool) -> Result<(), String> {\n        let mut tx = Tx::begin(db);\n        tx.push(7);\n        if fail {\n            return Err(\"boom\".into());\n        }\n        tx.commit();\n        Ok(())\n    }\n    println!(\"{:?} {:?}\", risky(&mut db, true), db);\n    println!(\"{:?} {:?}\", risky(&mut db, false), db);\n}\n", "expected": ["[1, 2, 3, 4]", "[1, 2, 3, 4]", "Err(\"boom\") [1, 2, 3, 4]", "Ok(()) [1, 2, 3, 4, 7]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-rc-counts', 15, 'rust', 'Rc: следим за счётчиком', 'counts() → Vec<usize>: создайте Rc<String>, запишите strong_count; клонируйте дважды — снова запишите; в вложенном блоке сделайте ещё клон и запишите; после блока и после drop одного клона — запишите. Всего шесть чисел.', 'use std::rc::Rc;

fn counts() -> Vec<usize> {
    let a = Rc::new(String::from("данные"));
    let mut out = vec![Rc::strong_count(&a)];
    todo!()
}
', 'strong_count после каждого действия: 1, 3, 4, 3, 2, 1 — клон увеличивает, выход из блока и drop уменьшают.', '{"driver": "fn main() {\n    println!(\"{:?}\", counts());\n}\n", "expected": ["[1, 3, 4, 3, 2, 1]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-shared-account', 16, 'rust', 'Rc<RefCell<Account>>: общий счёт', 'Account { balance: i64 }. Два владельца делят один счёт через Rc<RefCell<Account>>. deposit(acc, n) и withdraw(acc, n) → Result<(), String> «недостаточно средств: нужно N, есть M»; transfer(from, to, n) → Result<(), String> переводит между двумя счетами (если from и to — один и тот же счёт, перевод ничего не меняет).', 'use std::cell::RefCell;
use std::rc::Rc;

struct Account {
    balance: i64,
}

type Shared = Rc<RefCell<Account>>;

fn deposit(acc: &Shared, n: i64) {
    todo!()
}

fn withdraw(acc: &Shared, n: i64) -> Result<(), String> {
    todo!()
}

fn transfer(from: &Shared, to: &Shared, n: i64) -> Result<(), String> {
    todo!()
}
', 'Если from и to — один счёт, второй borrow_mut вызвал бы панику: проверьте Rc::ptr_eq заранее.', '{"driver": "fn main() {\n    let a: Shared = Rc::new(RefCell::new(Account { balance: 100 }));\n    let a2 = Rc::clone(&a);\n    let b: Shared = Rc::new(RefCell::new(Account { balance: 5 }));\n    deposit(&a2, 50);\n    println!(\"{}\", a.borrow().balance);\n    println!(\"{:?}\", withdraw(&a, 500));\n    println!(\"{:?} {} {}\", transfer(&a, &b, 120), a.borrow().balance, b.borrow().balance);\n    println!(\"{:?} {}\", transfer(&a, &a2, 30), a.borrow().balance);\n    println!(\"{:?}\", transfer(&b, &a, 1000));\n    println!(\"{}\", Rc::strong_count(&a));\n}\n", "expected": ["150", "Err(\"недостаточно средств: нужно 500, есть 150\")", "Ok(()) 30 125", "Ok(()) 30", "Err(\"недостаточно средств: нужно 1000, есть 125\")", "2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-rc-diamond', 17, 'rust', 'Общие узлы: Rc в графе без циклов', 'Node { val: i32, kids: Vec<Rc<Node>> }. total(&Node) → i32 — сумма по всем путям (общий узел считается каждый раз), unique_total(&Node) → i32 — каждый узел один раз (множество адресов *const Node). refs(&Rc<Node>) → usize — strong_count.', 'use std::collections::HashSet;
use std::rc::Rc;

struct Node {
    val: i32,
    kids: Vec<Rc<Node>>,
}

fn total(n: &Node) -> i32 {
    todo!()
}

fn unique_total(n: &Node) -> i32 {
    todo!()
}

fn refs(n: &Rc<Node>) -> usize {
    todo!()
}
', 'Адрес узла — n as *const Node; множество seen не даёт посетить общий узел дважды.', '{"driver": "fn main() {\n    let shared = Rc::new(Node { val: 10, kids: vec![] });\n    let left = Rc::new(Node { val: 1, kids: vec![Rc::clone(&shared)] });\n    let right = Rc::new(Node { val: 2, kids: vec![Rc::clone(&shared)] });\n    let root = Node { val: 100, kids: vec![left, right] };\n    println!(\"{} {}\", total(&root), unique_total(&root));\n    println!(\"{}\", refs(&shared));\n    drop(root);\n    println!(\"{}\", refs(&shared));\n}\n", "expected": ["123 113", "3", "1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-refcell-try', 18, 'rust', 'RefCell: try_borrow без паники', 'probe() → Vec<bool>: создайте RefCell<i32>; запишите результаты is_ok() такой последовательности: try_borrow_mut() на свободной ячейке; try_borrow() при живом изменяемом заимствовании; try_borrow_mut() при живом разделяемом; try_borrow() при двух разделяемых; try_borrow_mut() после освобождения всего.', 'use std::cell::RefCell;

fn probe() -> Vec<bool> {
    let c = RefCell::new(0);
    let mut out = Vec::new();
    todo!()
}
', 'Живой Ref или RefMut — это переменная в области видимости; блоки { … } освобождают заимствование.', '{"driver": "fn main() {\n    println!(\"{:?}\", probe());\n}\n", "expected": ["[true, false, false, true, true]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-cell-counter', 19, 'rust', 'Cell: счётчик через &self', 'Stats хранит hits: Cell<u32> и last: Cell<Option<i32>>. touch(&self, x) увеличивает hits и запоминает x в last; hits() и last() возвращают значения. Все методы принимают &self — изменение внутри общей ссылки (внутренняя изменяемость без RefCell).', 'use std::cell::Cell;

struct Stats {
    hits: Cell<u32>,
    last: Cell<Option<i32>>,
}

impl Stats {
    fn new() -> Stats {
        todo!()
    }
    fn touch(&self, x: i32) {
        todo!()
    }
    fn hits(&self) -> u32 {
        todo!()
    }
    fn last(&self) -> Option<i32> {
        todo!()
    }
}
', 'Cell::get/set работают с копируемыми значениями без выдачи ссылок — поэтому им не нужны проверки при запуске.', '{"driver": "fn main() {\n    let s = Stats::new();\n    let r1 = &s;\n    let r2 = &s;\n    r1.touch(5);\n    r2.touch(7);\n    r1.touch(-1);\n    println!(\"{} {:?}\", s.hits(), s.last());\n    println!(\"{} {}\", std::mem::size_of::<Cell<u32>>(), std::mem::size_of::<Stats>());\n}\n", "expected": ["3 Some(-1)", "4 12"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-observer-weak', 20, 'rust', 'Наблюдатели на Weak', 'Subject хранит Vec<Weak<RefCell<Vec<String>>>> — «почтовые ящики» наблюдателей. subscribe(&mut self, inbox: &Rc<RefCell<Vec<String>>>) добавляет слабую ссылку; publish(&mut self, msg) → usize кладёт сообщение в живые ящики, удаляет умершие и возвращает число доставленных.', 'use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Subject {
    inboxes: Vec<Weak<RefCell<Vec<String>>>>,
}

impl Subject {
    fn new() -> Subject {
        todo!()
    }
    fn subscribe(&mut self, inbox: &Rc<RefCell<Vec<String>>>) {
        todo!()
    }
    fn publish(&mut self, msg: &str) -> usize {
        todo!()
    }
}
', 'Rc::downgrade(&rc) — слабая ссылка; upgrade() вернёт None, когда владельцев не осталось.', '{"driver": "fn main() {\n    let mut subj = Subject::new();\n    let a = Rc::new(RefCell::new(Vec::new()));\n    let b = Rc::new(RefCell::new(Vec::new()));\n    subj.subscribe(&a);\n    subj.subscribe(&b);\n    println!(\"{}\", subj.publish(\"первое\"));\n    drop(b);\n    println!(\"{}\", subj.publish(\"второе\"));\n    println!(\"{:?}\", a.borrow());\n    println!(\"{} {}\", Rc::strong_count(&a), Rc::weak_count(&a));\n    println!(\"{}\", Subject::new().publish(\"никому\"));\n}\n", "expected": ["2", "1", "[\"первое\", \"второе\"]", "1 1", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-parent-weak', 21, 'rust', 'Дерево с Weak на родителя', 'Node { name: String, parent: RefCell<Weak<Node>>, kids: RefCell<Vec<Rc<Node>>> }. new(name) → Rc<Node>; add_child(parent: &Rc<Node>, child: Rc<Node>) прикрепляет ребёнка и записывает слабую ссылку на родителя; path(n: &Rc<Node>) → String — путь от корня «a/b/c».', 'use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Node {
    name: String,
    parent: RefCell<Weak<Node>>,
    kids: RefCell<Vec<Rc<Node>>>,
}

fn new(name: &str) -> Rc<Node> {
    todo!()
}

fn add_child(parent: &Rc<Node>, child: Rc<Node>) {
    todo!()
}

fn path(n: &Rc<Node>) -> String {
    todo!()
}
', 'Родитель держит детей сильно (kids), а ребёнок родителя — слабо (parent), поэтому цикла нет и после drop(root) корень освобождается.', '{"driver": "fn main() {\n    let root = new(\"usr\");\n    let bin = new(\"bin\");\n    let tool = new(\"cargo\");\n    add_child(&root, Rc::clone(&bin));\n    add_child(&bin, Rc::clone(&tool));\n    println!(\"{} | {} | {}\", path(&root), path(&bin), path(&tool));\n    println!(\"{} {}\", Rc::strong_count(&bin), Rc::weak_count(&bin));\n    println!(\"{} {}\", Rc::strong_count(&root), Rc::weak_count(&root));\n    drop(root);\n    println!(\"{}\", path(&bin));\n}\n", "expected": ["usr | usr/bin | usr/bin/cargo", "2 1", "1 1", "bin"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-cycle-leak', 22, 'rust', 'Цикл Rc: утечка и её устранение', 'cycle_counts() → Vec<usize>: создайте два узла Node { next: RefCell<Option<Rc<Node>>> }; запишите strong_count обоих; замкните их друг на друга и запишите снова; разорвите цикл (take()) и запишите ещё раз. Всего шесть чисел: a, b до; a, b в цикле; a, b после.', 'use std::cell::RefCell;
use std::rc::Rc;

struct Node {
    next: RefCell<Option<Rc<Node>>>,
}

fn cycle_counts() -> Vec<usize> {
    let a = Rc::new(Node { next: RefCell::new(None) });
    let b = Rc::new(Node { next: RefCell::new(None) });
    let mut out = vec![Rc::strong_count(&a), Rc::strong_count(&b)];
    todo!()
}
', 'Пока цикл замкнут, у каждого узла счётчик 2 — после выхода из функции они бы не освободились; take() разрывает связь.', '{"driver": "fn main() {\n    println!(\"{:?}\", cycle_counts());\n}\n", "expected": ["[1, 1, 2, 2, 1, 2]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-arc-basics', 23, 'rust', 'Arc: счётчик, try_unwrap и make_mut', 'arc_demo() → (usize, bool, Vec<i32>, Vec<i32>): создайте Arc<Vec<i32>> из [1, 2, 3]; клонируйте; запишите strong_count; попытка Arc::try_unwrap при двух владельцах (is_err); затем через Arc::make_mut у клона добавьте 4 (копия, потому что владельцев двое) — верните оригинал и изменённый клон.', 'use std::sync::Arc;

fn arc_demo() -> (usize, bool, Vec<i32>, Vec<i32>) {
    let a = Arc::new(vec![1, 2, 3]);
    todo!()
}
', 'try_unwrap возвращает Err, пока есть другие владельцы; make_mut клонирует данные, если Arc не единственный.', '{"driver": "fn main() {\n    println!(\"{:?}\", arc_demo());\n}\n", "expected": ["(2, true, [1, 2, 3], [1, 2, 3, 4])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-cow-normalize', 24, 'rust', 'Cow: копируем только при необходимости', 'normalize(s: &str) → Cow<str>: если в строке есть табы или подряд идущие пробелы, вернуть исправленную копию (табы → пробел, серии пробелов → один); иначе вернуть Cow::Borrowed без копии. is_borrowed(c) → bool — Cow ли заимствован.', 'use std::borrow::Cow;

fn normalize(s: &str) -> Cow<str> {
    todo!()
}

fn is_borrowed(c: &Cow<str>) -> bool {
    todo!()
}
', 'В ветке без правок возвращайте Cow::Borrowed(s) — тот же адрес, без копии.', '{"driver": "fn main() {\n    for s in [\"ok text\", \"a  b\", \"x\\ty\", \"  \", \"\"] {\n        let n = normalize(s);\n        println!(\"{:?} -> {:?} borrowed={}\", s, n, is_borrowed(&n));\n    }\n    let src = \"unchanged\";\n    let n = normalize(src);\n    println!(\"{}\", n.as_ptr() == src.as_ptr());\n}\n", "expected": ["\"ok text\" -> \"ok text\" borrowed=true", "\"a  b\" -> \"a b\" borrowed=false", "\"x\\ty\" -> \"x y\" borrowed=false", "\"  \" -> \" \" borrowed=false", "\"\" -> \"\" borrowed=true", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-mem-replace', 25, 'rust', 'mem::replace, take и swap', 'Machine { state: State, items: Vec<String>, name: String }. finish(&mut self) → State — перевести состояние в Done и вернуть прежнее (mem::replace); drain_items(&mut self) → Vec<String> — забрать все элементы (mem::take); swap_name(&mut self, other: &mut Machine) — поменять имена местами (mem::swap).', 'use std::mem;

#[derive(Debug, PartialEq)]
enum State {
    New,
    Busy(u32),
    Done,
}

struct Machine {
    state: State,
    items: Vec<String>,
    name: String,
}

impl Machine {
    fn finish(&mut self) -> State {
        todo!()
    }
    fn drain_items(&mut self) -> Vec<String> {
        todo!()
    }
    fn swap_name(&mut self, other: &mut Machine) {
        todo!()
    }
}
', 'mem::replace(&mut поле, новое) возвращает старое; mem::take подставляет Default (пустой Vec).', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\".clo\", \"ne()\")).count();\n    let mut a = Machine { state: State::Busy(3), items: vec![\"x\".into(), \"y\".into()], name: \"alpha\".into() };\n    let mut b = Machine { state: State::New, items: vec![], name: \"beta\".into() };\n    println!(\"{:?} {:?}\", a.finish(), a.state);\n    println!(\"{:?} {:?}\", a.drain_items(), a.items);\n    a.swap_name(&mut b);\n    println!(\"{} {}\", a.name, b.name);\n    println!(\"{:?} {:?}\", b.finish(), b.finish());\n    println!(\"clones: {}\", bad0);\n}\n", "expected": ["Busy(3) Done", "[\"x\", \"y\"] []", "beta alpha", "New Done", "clones: 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-intern', 26, 'rust', 'Интернирование строк: Rc<str>', 'Interner хранит HashMap<String, Rc<str>>. intern(&mut self, s: &str) → Rc<str> возвращает один и тот же Rc для равных строк (память выделяется один раз); len(&self) → usize — число различных строк; total_refs(&self) → usize — сумма strong_count по всем записям.', 'use std::collections::HashMap;
use std::rc::Rc;

struct Interner {
    map: HashMap<String, Rc<str>>,
}

impl Interner {
    fn new() -> Interner {
        todo!()
    }
    fn intern(&mut self, s: &str) -> Rc<str> {
        todo!()
    }
    fn len(&self) -> usize {
        todo!()
    }
    fn total_refs(&self) -> usize {
        todo!()
    }
}
', 'Rc<str> — толстый указатель (адрес и длина); Rc::from(&str) копирует байты один раз в блок с счётчиками.', '{"driver": "fn main() {\n    let mut i = Interner::new();\n    let a = i.intern(\"привет\");\n    let b = i.intern(\"мир\");\n    let c = i.intern(\"привет\");\n    println!(\"{} {}\", Rc::ptr_eq(&a, &c), Rc::ptr_eq(&a, &b));\n    println!(\"{} {}\", i.len(), i.total_refs());\n    drop(c);\n    println!(\"{}\", i.total_refs());\n    println!(\"{} {}\", &*a, std::mem::size_of::<Rc<str>>());\n}\n", "expected": ["true false", "2 5", "4", "привет 16"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-arena-tree', 27, 'rust', 'Дерево в арене: индексы вместо указателей', 'Arena { nodes: Vec<Item> } с Item { name, parent: Option<usize>, kids: Vec<usize> }. add(name, parent: Option<usize>) → usize — id нового узла (и запись в kids родителя); depth(id) → usize — число предков; path(id) → String «a/b/c»; leaves(&self) → Vec<&str> — имена узлов без детей в порядке id. Ни Rc, ни RefCell.', 'struct Item {
    name: String,
    parent: Option<usize>,
    kids: Vec<usize>,
}

struct Arena {
    nodes: Vec<Item>,
}

impl Arena {
    fn new() -> Arena {
        todo!()
    }
    fn add(&mut self, name: &str, parent: Option<usize>) -> usize {
        todo!()
    }
    fn depth(&self, id: usize) -> usize {
        todo!()
    }
    fn path(&self, id: usize) -> String {
        todo!()
    }
    fn leaves(&self) -> Vec<&str> {
        todo!()
    }
}
', 'Связи — индексы в одном Vec: добавляя узел, допишите его id в kids родителя.', '{"driver": "fn main() {\n    let mut a = Arena::new();\n    let root = a.add(\"src\", None);\n    let lib = a.add(\"lib\", Some(root));\n    let main = a.add(\"main\", Some(root));\n    let util = a.add(\"util\", Some(lib));\n    println!(\"{} {} {}\", a.depth(root), a.depth(lib), a.depth(util));\n    println!(\"{} | {}\", a.path(util), a.path(main));\n    println!(\"{:?}\", a.leaves());\n    println!(\"{}\", a.nodes[root].kids.len());\n}\n", "expected": ["0 1 2", "src/lib/util | src/main", "[\"main\", \"util\"]", "2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-persistent-list', 28, 'rust', 'Неизменяемый список с общим хвостом', 'type Link = Option<Rc<Node>>; Node { val, next: Link }. push(list: &Link, v) → Link создаёт новую голову, делящую хвост со старым списком; to_vec(&Link); len(&Link); tail_refs(list: &Link) → usize — strong_count головы (сколько списков делят этот хвост).', 'use std::rc::Rc;

struct Node {
    val: i32,
    next: Link,
}
type Link = Option<Rc<Node>>;

fn push(list: &Link, v: i32) -> Link {
    todo!()
}

fn to_vec(list: &Link) -> Vec<i32> {
    todo!()
}

fn len(list: &Link) -> usize {
    todo!()
}

fn tail_refs(list: &Link) -> usize {
    todo!()
}
', 'list.clone() у Option<Rc<…>> копирует лишь указатель и увеличивает счётчик: хвост общий.', '{"driver": "fn main() {\n    let base = push(&push(&None, 3), 2);\n    let a = push(&base, 1);\n    let b = push(&base, 100);\n    println!(\"{:?} {:?} {:?}\", to_vec(&base), to_vec(&a), to_vec(&b));\n    println!(\"{} {}\", len(&a), len(&None));\n    println!(\"{} {}\", tail_refs(&base), tail_refs(&a));\n    drop(a);\n    println!(\"{}\", tail_refs(&base));\n}\n", "expected": ["[2, 3] [1, 2, 3] [100, 2, 3]", "3 0", "3 1", "2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 21, 'r21-dlist-weak', 29, 'rust', 'Двусвязный список: Rc вперёд, Weak назад', 'DList { head: Option<Rc<RefCell<DNode>>>, tail: Option<Rc<RefCell<DNode>>> } с DNode { val, next: Option<Rc<RefCell<DNode>>>, prev: Option<Weak<RefCell<DNode>>> }. push_back(v); push_front(v); pop_back() → Option<i32>; forward() → Vec<i32> (по next); backward() → Vec<i32> (по prev от хвоста).', 'use std::cell::RefCell;
use std::rc::{Rc, Weak};

type Link = Option<Rc<RefCell<DNode>>>;

struct DNode {
    val: i32,
    next: Link,
    prev: Option<Weak<RefCell<DNode>>>,
}

struct DList {
    head: Link,
    tail: Link,
}

impl DList {
    fn new() -> DList {
        DList { head: None, tail: None }
    }
    fn push_back(&mut self, v: i32) {
        todo!()
    }
    fn push_front(&mut self, v: i32) {
        todo!()
    }
    fn pop_back(&mut self) -> Option<i32> {
        todo!()
    }
    fn forward(&self) -> Vec<i32> {
        todo!()
    }
    fn backward(&self) -> Vec<i32> {
        todo!()
    }
}
', 'Вперёд (next) — сильные Rc, назад (prev) — Weak; при pop_back не забудьте обнулить next у нового хвоста.', '{"driver": "fn main() {\n    let mut l = DList::new();\n    println!(\"{:?} {:?}\", l.forward(), l.pop_back());\n    l.push_back(2);\n    l.push_back(3);\n    l.push_front(1);\n    l.push_back(4);\n    println!(\"{:?} {:?}\", l.forward(), l.backward());\n    println!(\"{:?} {:?}\", l.pop_back(), l.pop_back());\n    println!(\"{:?} {:?}\", l.forward(), l.backward());\n    l.pop_back();\n    l.pop_back();\n    println!(\"{:?} {:?} {}\", l.forward(), l.pop_back(), l.head.is_none() && l.tail.is_none());\n}\n", "expected": ["[] None", "[1, 2, 3, 4] [4, 3, 2, 1]", "Some(4) Some(3)", "[1, 2] [2, 1]", "[] None true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-fix-visibility', 0, 'rust', 'Исправьте: приватная функция модуля', 'В модуле bank функции new_account и deposit не помечены pub, и код вне модуля не собирается (E0603). Откройте наружу ровно то, что нужно драйверу: new_account и deposit. Поле balance закрытым оставьте: читать баланс можно только через audit.', 'mod bank {
    pub struct Account {
        balance: i64,
    }

    fn new_account(initial: i64) -> Account {
        Account { balance: initial }
    }

    fn deposit(a: &mut Account, n: i64) {
        a.balance += n;
    }

    pub fn audit(a: &Account) -> String {
        format!("balance={}", a.balance)
    }
}
', 'Слово pub перед fn: new_account и deposit станут видимы снаружи модуля.', '{"driver": "fn main() {\n    let mut a = bank::new_account(10);\n    bank::deposit(&mut a, 5);\n    println!(\"{}\", bank::audit(&a));\n}\n", "expected": ["balance=15"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-fix-field', 1, 'rust', 'Закрытые поля: конструктор и геттеры', 'Поля Rect закрыты, поэтому снаружи структуру не собрать и не прочитать. Напишите new(w, h) → Result<Rect, String> (стороны должны быть > 0, иначе «сторона должна быть положительной»), width(), height(), area() и scale(&self, k: u32) → Rect.', 'mod shapes {
    pub struct Rect {
        w: u32,
        h: u32,
    }

    impl Rect {
        // new, width, height, area, scale
    }
}
', 'Конструктор — единственный способ получить Rect снаружи; поэтому внутри него можно гарантировать w > 0 и h > 0.', '{"driver": "fn main() {\n    let r = shapes::Rect::new(3, 4).unwrap();\n    println!(\"{} {} {}\", r.width(), r.height(), r.area());\n    let big = r.scale(3);\n    println!(\"{}x{} {}\", big.width(), big.height(), big.area());\n    println!(\"{:?}\", shapes::Rect::new(0, 5).err());\n    println!(\"{:?}\", shapes::Rect::new(2, 0).err());\n}\n", "expected": ["3 4 12", "9x12 108", "Some(\"сторона должна быть положительной\")", "Some(\"сторона должна быть положительной\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-fix-use-trait', 2, 'rust', 'Исправьте: трейт не в области видимости', 'Трейт Shout реализован для str в модуле text, но метод shout() в функции loud вызвать нельзя: имя трейта не подключено (E0599). Исправьте одной строкой use.', 'mod text {
    pub trait Shout {
        fn shout(&self) -> String;
    }

    impl Shout for str {
        fn shout(&self) -> String {
            format!("{}!", self.to_uppercase())
        }
    }
}

fn loud(s: &str) -> String {
    s.shout()
}
', 'Методы трейта доступны, только если сам трейт подключён: use text::Shout;', '{"driver": "fn main() {\n    println!(\"{}\", loud(\"привет\"));\n    println!(\"{}\", loud(\"rust\"));\n}\n", "expected": ["ПРИВЕТ!", "RUST!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-reexport', 3, 'rust', 'pub use: плоский публичный интерфейс', 'Типы Circle и Rect лежат глубоко: shapes::circle::Circle и shapes::rect::Rect, а трейт Shape — в shapes::Shape. Сделайте так, чтобы из корня крейта были доступны Circle, Rect и Shape (pub use), а также модуль prelude с теми же тремя именами.', 'mod shapes {
    pub trait Shape {
        fn area(&self) -> f64;
    }

    pub mod circle {
        pub struct Circle(pub f64);
        impl super::Shape for Circle {
            fn area(&self) -> f64 {
                3.0 * self.0 * self.0
            }
        }
    }

    pub mod rect {
        pub struct Rect(pub f64, pub f64);
        impl super::Shape for Rect {
            fn area(&self) -> f64 {
                self.0 * self.1
            }
        }
    }
}

// pub use и mod prelude
', 'В корне: pub use shapes::circle::Circle; и так далее; prelude — модуль с pub use crate::{…}.', '{"driver": "fn main() {\n    let c = Circle(2.0);\n    let r = Rect(3.0, 4.0);\n    println!(\"{} {}\", c.area(), r.area());\n    use prelude::*;\n    let shapes: Vec<Box<dyn Shape>> = vec![Box::new(Circle(1.0)), Box::new(Rect(1.0, 2.0))];\n    println!(\"{}\", shapes.iter().map(|s| s.area()).sum::<f64>());\n}\n", "expected": ["12 12", "5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-paths-super', 4, 'rust', 'Пути: crate, self, super', 'Три вложенных модуля. util::double(x) → x * 2. engine::run(x) → util::double(x) + 1 (путь от корня). engine::fast::run(x) → engine::run(x) через super, а fast::twice(x) → self::step(x) * 2. Реализуйте функции, используя ровно такие пути: crate::, super::, self::.', 'mod util {
    pub fn double(x: i32) -> i32 {
        x * 2
    }
}

mod engine {
    pub fn run(x: i32) -> i32 {
        todo!()
    }

    pub mod fast {
        fn step(x: i32) -> i32 {
            x + 10
        }

        pub fn run(x: i32) -> i32 {
            todo!()
        }

        pub fn twice(x: i32) -> i32 {
            todo!()
        }
    }
}
', 'Три разных начала пути: crate::util::double, super::run, self::step — каждое по разу.', '{"driver": "fn main() {\n    let src = include_str!(\"main.rs\");\n    let bad0 = src.matches(concat!(\"crate\", \"::util\")).count();\n    let bad1 = src.matches(concat!(\"super\", \"::run\")).count();\n    let bad2 = src.matches(concat!(\"self:\", \":step\")).count();\n    println!(\"{} {}\", engine::run(5), engine::fast::run(5));\n    println!(\"{}\", engine::fast::twice(1));\n    println!(\"paths: {} {} {}\", bad0, bad1, bad2);\n}\n", "expected": ["11 11", "22", "paths: 1 1 1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-fmt-write', 5, 'rust', 'use std::fmt::Write для String', 'render_table(rows: &[(&str, i32)]) → String: строки «имя<пробелы до 8>|<число по правому краю в 5>» с переводом строки; в конце строка «итого» с суммой. Формируйте результат через writeln! прямо в String (для этого нужно подключить трейт std::fmt::Write).', 'fn render_table(rows: &[(&str, i32)]) -> String {
    todo!()
}
', 'writeln!(out, "...") доступен у String, только если подключён use std::fmt::Write; результат нужно unwrap() или ?.', '{"driver": "fn main() {\n    print!(\"{}\", render_table(&[(\"хлеб\", 40), (\"молоко\", 95), (\"сыр\", 310)]));\n    print!(\"{}\", render_table(&[]));\n}\n", "expected": ["хлеб    |   40", "молоко  |   95", "сыр     |  310", "итого   |  445", "итого   |    0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-invariant-ctor', 6, 'rust', 'Инвариант в конструкторе: Kelvin', 'В модуле temp тип Kelvin(f64) с закрытым полем. new(k) → Result<Kelvin, String> («ниже абсолютного нуля: K»), from_celsius(c) → Result, kelvin(), celsius(), add(&self, delta: f64) → Result<Kelvin, String> (сумма не должна выйти ниже нуля). Снаружи значения ниже нуля получить невозможно.', 'mod temp {
    pub struct Kelvin(f64);

    impl Kelvin {
        // new, from_celsius, kelvin, celsius, add
    }
}
', 'Все пути создания значения проходят через new: там проверка k >= 0.', '{"driver": "fn main() {\n    let t = temp::Kelvin::from_celsius(25.0).unwrap();\n    println!(\"{:.2} {:.2}\", t.kelvin(), t.celsius());\n    println!(\"{:?}\", temp::Kelvin::new(-1.0).err());\n    println!(\"{:?}\", temp::Kelvin::from_celsius(-300.0).err().map(|e| e.starts_with(\"ниже\")));\n    println!(\"{:?}\", t.add(-400.0).err());\n    println!(\"{:.1}\", t.add(10.0).unwrap().kelvin());\n}\n", "expected": ["298.15 25.00", "Some(\"ниже абсолютного нуля: -1\")", "Some(true)", "Some(\"ниже абсолютного нуля: -101.85000000000002\")", "308.1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-builder', 7, 'rust', 'Строитель с проверкой в build()', 'Config { host, port, tls, timeout_ms }. ConfigBuilder::new(host) с умолчаниями (port 80, tls false, timeout 1000); методы port(self, p), tls(self, on), timeout_ms(self, t) возвращают Self; build(self) → Result<Config, String>: «пустой хост», «порт 0», «таймаут больше 60000»; при tls = true и порте 80 порт автоматически становится 443.', '#[derive(Debug, PartialEq)]
struct Config {
    host: String,
    port: u16,
    tls: bool,
    timeout_ms: u32,
}

struct ConfigBuilder {
    host: String,
    port: u16,
    tls: bool,
    timeout_ms: u32,
}

impl ConfigBuilder {
    fn new(host: &str) -> ConfigBuilder {
        todo!()
    }
    fn port(mut self, p: u16) -> ConfigBuilder {
        todo!()
    }
    fn tls(mut self, on: bool) -> ConfigBuilder {
        todo!()
    }
    fn timeout_ms(mut self, t: u32) -> ConfigBuilder {
        todo!()
    }
    fn build(self) -> Result<Config, String> {
        todo!()
    }
}
', 'Методы-настройки возвращают self, а все проверки собраны в build.', '{"driver": "fn main() {\n    println!(\"{:?}\", ConfigBuilder::new(\"example.org\").build());\n    println!(\"{:?}\", ConfigBuilder::new(\"a.b\").tls(true).build());\n    println!(\"{:?}\", ConfigBuilder::new(\"a.b\").tls(true).port(8443).timeout_ms(250).build());\n    println!(\"{:?}\", ConfigBuilder::new(\" \").build());\n    println!(\"{:?}\", ConfigBuilder::new(\"x\").port(0).build());\n    println!(\"{:?}\", ConfigBuilder::new(\"x\").timeout_ms(70000).build());\n}\n", "expected": ["Ok(Config { host: \"example.org\", port: 80, tls: false, timeout_ms: 1000 })", "Ok(Config { host: \"a.b\", port: 443, tls: true, timeout_ms: 1000 })", "Ok(Config { host: \"a.b\", port: 8443, tls: true, timeout_ms: 250 })", "Err(\"пустой хост\")", "Err(\"порт 0\")", "Err(\"таймаут больше 60000\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-default-config', 8, 'rust', 'Default и обновление структуры', 'Config { name, retries, verbose, ratio, tags }. Реализуйте Default вручную: name «app», retries 3, verbose false, ratio 0.5, tags пусто. overridden(base, retries: Option<u32>, verbose: Option<bool>) → Config — подставить заданные значения поверх base (None — оставить как было).', '#[derive(Debug, Clone, PartialEq)]
struct Config {
    name: String,
    retries: u32,
    verbose: bool,
    ratio: f64,
    tags: Vec<String>,
}

// impl Default for Config

fn overridden(base: Config, retries: Option<u32>, verbose: Option<bool>) -> Config {
    todo!()
}
', 'Config { retries: …, verbose: …, ..base } — остальные поля берутся из base (в том числе строка и вектор — они переезжают).', '{"driver": "fn main() {\n    let d = Config::default();\n    println!(\"{:?}\", d);\n    println!(\"{:?}\", overridden(d.clone(), Some(10), None));\n    println!(\"{:?}\", overridden(d.clone(), None, Some(true)).verbose);\n    let custom = Config { name: \"svc\".into(), tags: vec![\"x\".into()], ..Default::default() };\n    println!(\"{:?}\", custom);\n    println!(\"{}\", overridden(custom.clone(), None, None) == custom);\n}\n", "expected": ["Config { name: \"app\", retries: 3, verbose: false, ratio: 0.5, tags: [] }", "Config { name: \"app\", retries: 10, verbose: false, ratio: 0.5, tags: [] }", "true", "Config { name: \"svc\", retries: 3, verbose: false, ratio: 0.5, tags: [\"x\"] }", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-fromstr-version', 9, 'rust', 'Version: разбор, порядок, вывод', 'Version { major, minor, patch } (u32). Реализуйте FromStr для «1.2.3» (ровно три числа, иначе Err со словом «формат»; нечисло → Err «число: <часть>»), Display «1.2.3» и порядок (derive Ord по полям major, minor, patch). Тогда sort() и max() работают.', 'use std::fmt;
use std::str::FromStr;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
struct Version {
    major: u32,
    minor: u32,
    patch: u32,
}

// impl FromStr и Display
', 'split(''.'') и проверка длины; числа разбирайте замыканием с map_err и оператором ?.', '{"driver": "fn main() {\n    let mut v: Vec<Version> = [\"1.10.0\", \"1.2.9\", \"0.9.9\", \"1.2.10\"].iter().map(|s| s.parse().unwrap()).collect();\n    v.sort();\n    println!(\"{}\", v.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(\" < \"));\n    println!(\"{}\", v.iter().max().unwrap());\n    println!(\"{:?}\", \"1.2\".parse::<Version>());\n    println!(\"{:?}\", \"1.x.3\".parse::<Version>());\n    println!(\"{:?}\", \"1.2.3.4\".parse::<Version>().is_err());\n}\n", "expected": ["0.9.9 < 1.2.9 < 1.2.10 < 1.10.0", "1.10.0", "Err(\"формат: ожидалось X.Y.Z, получено \\\"1.2\\\"\")", "Err(\"число: x\")", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-semver-req', 10, 'rust', 'Требования версий: ^, ~, =, >=', 'Req::parse(s) → Option<Req> и matches(&self, v: &Version) → bool. «^1.2.3»: ≥1.2.3 и <2.0.0 (для 0.x: «^0.2.3» — <0.3.0, «^0.0.3» — только 0.0.3); «~1.2.3»: ≥1.2.3 и <1.3.0; «=1.2.3» — точно; «>=1.2.3»; «*» — любая. Version и разбор версии уже готовы.', '#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
struct Version {
    major: u32,
    minor: u32,
    patch: u32,
}

fn v(s: &str) -> Option<Version> {
    let mut it = s.split(''.'').map(|p| p.parse::<u32>().ok());
    let (a, b, c) = (it.next()??, it.next()??, it.next()??);
    if it.next().is_some() {
        return None;
    }
    Some(Version { major: a, minor: b, patch: c })
}

enum Req {
    Any,
    Exact(Version),
    AtLeast(Version),
    Caret(Version),
    Tilde(Version),
}

impl Req {
    fn parse(s: &str) -> Option<Req> {
        todo!()
    }
    fn matches(&self, ver: &Version) -> bool {
        todo!()
    }
}
', 'Для каретки три случая: major > 0 — совпадает major; иначе minor > 0 — совпадают 0 и minor; иначе — только точная.', '{"driver": "fn main() {\n    let vers: Vec<Version> = [\"0.0.3\", \"0.2.3\", \"0.2.9\", \"0.3.0\", \"1.2.2\", \"1.2.3\", \"1.9.0\", \"2.0.0\"].iter().map(|s| v(s).unwrap()).collect();\n    for r in [\"^1.2.3\", \"^0.2.3\", \"^0.0.3\", \"~1.2.3\", \"=1.2.3\", \">=1.2.3\", \"*\"] {\n        let req = Req::parse(r).unwrap();\n        let ok: Vec<String> = vers.iter().filter(|x| req.matches(x)).map(|x| format!(\"{}.{}.{}\", x.major, x.minor, x.patch)).collect();\n        println!(\"{r}: {}\", ok.join(\" \"));\n    }\n    println!(\"{} {}\", Req::parse(\"^x\").is_none(), Req::parse(\"1.2.3\").is_none());\n}\n", "expected": ["^1.2.3: 1.2.3 1.9.0", "^0.2.3: 0.2.3 0.2.9", "^0.0.3: 0.0.3", "~1.2.3: 1.2.3", "=1.2.3: 1.2.3", ">=1.2.3: 1.2.3 1.9.0 2.0.0", "*: 0.0.3 0.2.3 0.2.9 0.3.0 1.2.2 1.2.3 1.9.0 2.0.0", "true true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-semver-bump', 11, 'rust', 'Повышение версии и совместимость', 'bump(v: Version, kind: &str) → Option<Version>: «major» (minor и patch → 0), «minor» (patch → 0), «patch»; другое слово — None. breaking(old, new) → bool: true, если major вырос, либо major = 0 и вырос minor. sort_desc(Vec<Version>) → Vec<Version> — от новых к старым.', '#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
struct Version {
    major: u32,
    minor: u32,
    patch: u32,
}

fn bump(v: Version, kind: &str) -> Option<Version> {
    todo!()
}

fn breaking(old: Version, new: Version) -> bool {
    todo!()
}

fn sort_desc(mut v: Vec<Version>) -> Vec<Version> {
    todo!()
}
', 'Структурное обновление Version { patch: …, ..v } меняет только указанные поля.', '{"driver": "fn main() {\n    let v = |a, b, c| Version { major: a, minor: b, patch: c };\n    println!(\"{:?}\", bump(v(1, 2, 3), \"major\"));\n    println!(\"{:?}\", bump(v(1, 2, 3), \"minor\"));\n    println!(\"{:?}\", bump(v(1, 2, 3), \"patch\"));\n    println!(\"{:?}\", bump(v(1, 2, 3), \"huge\"));\n    println!(\"{} {} {}\", breaking(v(1, 5, 0), v(2, 0, 0)), breaking(v(0, 2, 0), v(0, 3, 0)), breaking(v(1, 2, 0), v(1, 9, 9)));\n    println!(\"{:?}\", sort_desc(vec![v(1, 0, 0), v(0, 9, 9), v(1, 0, 1)]));\n}\n", "expected": ["Some(Version { major: 2, minor: 0, patch: 0 })", "Some(Version { major: 1, minor: 3, patch: 0 })", "Some(Version { major: 1, minor: 2, patch: 4 })", "None", "true true false", "[Version { major: 1, minor: 0, patch: 1 }, Version { major: 1, minor: 0, patch: 0 }, Version { major: 0, minor: 9, patch: 9 }]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-cargo-toml-parse', 12, 'rust', 'Разбор Cargo.toml', 'parse_manifest(text) → Result<Manifest, String>. Manifest { name, version, deps: BTreeMap<String, String> }. Секции [package] (name, version — в кавычках) и [dependencies] («имя = "версия"» или «имя = { version = "версия", … }»). Комментарии «#» и пустые строки пропускать; другие секции игнорировать. Нет name или version → Err("нет name") / Err("нет version").', 'use std::collections::BTreeMap;

#[derive(Debug, PartialEq)]
struct Manifest {
    name: String,
    version: String,
    deps: BTreeMap<String, String>,
}

fn parse_manifest(text: &str) -> Result<Manifest, String> {
    todo!()
}
', 'Запоминайте текущую секцию в переменной; значение в кавычках — через strip_prefix(''"'') и strip_suffix(''"'').', '{"driver": "fn main() {\n    let t = \"# мой проект\\n[package]\\nname = \\\"hello\\\"\\nversion = \\\"0.3.1\\\"\\nedition = \\\"2021\\\"\\n\\n[dependencies]\\nserde = \\\"1.0\\\"\\nrand = { version = \\\"0.8\\\", features = [\\\"small_rng\\\"] }\\n\\n[dev-dependencies]\\ntempfile = \\\"3\\\"\\n\";\n    println!(\"{:?}\", parse_manifest(t));\n    println!(\"{:?}\", parse_manifest(\"[package]\\nversion = \\\"1.0.0\\\"\\n\"));\n    println!(\"{:?}\", parse_manifest(\"[package]\\nname = \\\"x\\\"\\n\"));\n    println!(\"{:?}\", parse_manifest(\"[package]\\nname = \\\"x\\\"\\nversion = \\\"0.1.0\\\"\\n\").map(|m| m.deps.len()));\n}\n", "expected": ["Ok(Manifest { name: \"hello\", version: \"0.3.1\", deps: {\"rand\": \"0.8\", \"serde\": \"1.0\"} })", "Err(\"нет name\")", "Err(\"нет version\")", "Ok(0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-dep-graph', 13, 'rust', 'Порядок сборки крейтов', 'build_order(deps: &[(&str, &[&str])]) → Result<Vec<String>, String>: каждая пара — крейт и его зависимости. Сначала собираются зависимости; из готовых к сборке крейтов берите по алфавиту. Зависимость, которой нет в списке, считается внешней и игнорируется. Цикл → Err("цикл: a b c") с оставшимися крейтами по алфавиту.', 'fn build_order(deps: &[(&str, &[&str])]) -> Result<Vec<String>, String> {
    todo!()
}
', 'Ключи BTreeMap идут по алфавиту — первый крейт без оставшихся зависимостей и есть следующий.', '{"driver": "fn main() {\n    println!(\"{:?}\", build_order(&[(\"app\", &[\"net\", \"log\"]), (\"net\", &[\"log\", \"libc\"]), (\"log\", &[]), (\"tools\", &[\"log\"])]));\n    println!(\"{:?}\", build_order(&[(\"a\", &[\"b\"]), (\"b\", &[\"c\"]), (\"c\", &[\"a\"]), (\"d\", &[])]));\n    println!(\"{:?}\", build_order(&[]));\n    println!(\"{:?}\", build_order(&[(\"z\", &[]), (\"a\", &[])]));\n}\n", "expected": ["Ok([\"log\", \"net\", \"app\", \"tools\"])", "Err(\"цикл: a b c\")", "Ok([])", "Ok([\"a\", \"z\"])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-features-closure', 14, 'rust', 'Features: замыкание включённых', 'resolve(features: &[(&str, &[&str])], requested: &[&str]) → Result<Vec<String>, String>. Каждый feature включает другие. Результат — все включённые features по алфавиту (включая вложенные); «default» включается всегда, если он описан. Неизвестное имя в requested или в зависимости → Err("нет feature X").', 'fn resolve(features: &[(&str, &[&str])], requested: &[&str]) -> Result<Vec<String>, String> {
    todo!()
}
', 'Обход со стеком и множеством уже включённых; на неизвестное имя возвращайте ошибку сразу.', '{"driver": "fn main() {\n    let f: [(&str, &[&str]); 5] = [(\"default\", &[\"json\"]), (\"json\", &[\"alloc\"]), (\"alloc\", &[]), (\"tls\", &[\"alloc\", \"net\"]), (\"net\", &[])];\n    println!(\"{:?}\", resolve(&f, &[]));\n    println!(\"{:?}\", resolve(&f, &[\"tls\"]));\n    println!(\"{:?}\", resolve(&f, &[\"ghost\"]));\n    println!(\"{:?}\", resolve(&[(\"a\", &[\"zzz\"])], &[\"a\"]));\n    println!(\"{:?}\", resolve(&[], &[]));\n}\n", "expected": ["Ok([\"alloc\", \"default\", \"json\"])", "Ok([\"alloc\", \"default\", \"json\", \"net\", \"tls\"])", "Err(\"нет feature ghost\")", "Err(\"нет feature zzz\")", "Ok([])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-lockfile-diff', 15, 'rust', 'Сравнение Cargo.lock', 'diff(old, new: &[(&str, &str)]) → Vec<String> — пары (крейт, версия). По алфавиту крейтов: «+ имя версия» — появился; «- имя версия» — исчез; «~ имя старая -> новая» — версия изменилась. Неизменившиеся не выводить.', 'fn diff(old: &[(&str, &str)], new: &[(&str, &str)]) -> Vec<String> {
    todo!()
}
', 'Объедините имена двух списков в BTreeSet — получите алфавитный порядок; затем match по паре Option.', '{"driver": "fn main() {\n    let old = [(\"serde\", \"1.0.1\"), (\"rand\", \"0.8.0\"), (\"log\", \"0.4.1\")];\n    let new = [(\"serde\", \"1.0.9\"), (\"log\", \"0.4.1\"), (\"tokio\", \"1.2.0\")];\n    for l in diff(&old, &new) {\n        println!(\"{l}\");\n    }\n    println!(\"{:?}\", diff(&new, &new));\n    println!(\"{:?}\", diff(&[], &[(\"a\", \"1\")]));\n}\n", "expected": ["- rand 0.8.0", "~ serde 1.0.1 -> 1.0.9", "+ tokio 1.2.0", "[]", "[\"+ a 1\"]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-cfg-info', 16, 'rust', 'cfg!: что известно при сборке', 'build_info() → String вида «mode=<debug|release> os=<linux|other> ptr=<32|64> endian=<little|big> unix=<yes|no>». Используйте макрос cfg! (debug_assertions, target_os = "linux", target_pointer_width, target_endian, unix). Проверка собрана с оптимизацией.', 'fn build_info() -> String {
    todo!()
}
', 'cfg!(условие) — обычное булево выражение, вычисляемое при сборке; пары вида target_os = "linux".', '{"driver": "fn main() {\n    println!(\"{}\", build_info());\n    println!(\"{}\", std::mem::size_of::<usize>() * 8);\n}\n", "expected": ["mode=release os=linux ptr=64 endian=little unix=yes", "64"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-atomic-oncelock', 17, 'rust', 'Глобальное состояние: AtomicUsize и OnceLock', 'static NEXT: AtomicUsize — next_id() выдаёт 1, 2, 3, … (fetch_add), reset_ids() обнуляет, peek_id() показывает следующий без выдачи. static NAME: OnceLock<String> — init_name(s) → bool: true, если это первая инициализация; name() → Option<&''static str>.', 'use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::OnceLock;

static NEXT: AtomicUsize = AtomicUsize::new(1);
static NAME: OnceLock<String> = OnceLock::new();

fn next_id() -> usize {
    todo!()
}

fn peek_id() -> usize {
    todo!()
}

fn reset_ids() {
    todo!()
}

fn init_name(s: &str) -> bool {
    todo!()
}

fn name() -> Option<&''static str> {
    todo!()
}
', 'fetch_add возвращает прежнее значение; OnceLock::set возвращает Err, если значение уже задано.', '{"driver": "fn main() {\n    println!(\"{} {} {}\", next_id(), next_id(), next_id());\n    println!(\"{}\", peek_id());\n    reset_ids();\n    println!(\"{} {}\", next_id(), peek_id());\n    println!(\"{:?}\", name());\n    println!(\"{} {}\", init_name(\"первое\"), init_name(\"второе\"));\n    println!(\"{:?}\", name());\n}\n", "expected": ["1 2 3", "4", "1 2", "None", "true false", "Some(\"первое\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-const-fn', 18, 'rust', 'const fn: таблицы при сборке', 'const fn fact(n: u32) → u64 (цикл while внутри const fn разрешён). const FACTS: [u64; 11] — факториалы 0..=10, заполненные при сборке через const-блок. const fn gcd(a, b) → u64 (Евклид). const fn is_pow2(x: u32) → bool. Таблица и функции вычисляются компилятором.', 'const fn fact(n: u32) -> u64 {
    todo!()
}

const fn gcd(a: u64, b: u64) -> u64 {
    todo!()
}

const fn is_pow2(x: u32) -> bool {
    todo!()
}

// const FACTS: [u64; 11] = ...
', 'В const fn нет for и замыканий — только while, let mut и арифметика; таблицу заполняет блок-константа.', '{"driver": "const G: u64 = gcd(84, 36);\nconst P: bool = is_pow2(1024);\n\nfn main() {\n    println!(\"{:?}\", FACTS);\n    println!(\"{} {}\", G, P);\n    println!(\"{} {}\", is_pow2(0), is_pow2(96));\n    println!(\"{}\", gcd(17, 5));\n    let a = [0u8; FACTS.len()];\n    println!(\"{}\", a.len());\n}\n", "expected": ["[1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]", "12 true", "false false", "1", "11"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-doc-extractor', 19, 'rust', 'Мини-rustdoc: извлечь документацию', 'extract_docs(src: &str) → Vec<(String, String)>: для каждой функции (fn имя(… или pub fn имя(…) собрать текст идущих перед ней строк «///» (без «///» и пробела после, склеенных через пробел). Функции без документации пропускать. Порядок — как в исходнике.', 'fn extract_docs(src: &str) -> Vec<(String, String)> {
    todo!()
}
', 'Копите строки /// в вектор; на строке с fn — сохраните и очистите; атрибут #[...] между документацией и функцией её не сбрасывает.', '{"driver": "fn main() {\n    let src = \"/// Складывает.\\n/// Два числа.\\npub fn add(a: i32, b: i32) -> i32 { a + b }\\n\\nfn hidden() {}\\n\\n/// Печатает.\\n#[inline]\\nfn show() {}\\n\\n/// Висит в воздухе\\nstruct S;\\nfn after() {}\\n\";\n    for (n, d) in extract_docs(src) {\n        println!(\"{n}: {d}\");\n    }\n    println!(\"{}\", extract_docs(\"fn a() {}\").len());\n}\n", "expected": ["add: Складывает. Два числа.", "show: Печатает.", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-mini-test-runner', 20, 'rust', 'Мини-раннер тестов', 'type TestFn = fn() → Result<(), String>. run_tests(tests: &[(&str, TestFn)]) → (usize, usize, Vec<String>): число прошедших, число упавших и строки отчёта «test <имя> ... ok» / «test <имя> ... FAILED: <сообщение>». Паника внутри теста — тоже провал: «FAILED: panicked» (ловите через std::panic::catch_unwind). Раннер не должен падать сам.', 'type TestFn = fn() -> Result<(), String>;

fn run_tests(tests: &[(&str, TestFn)]) -> (usize, usize, Vec<String>) {
    todo!()
}
', 'catch_unwind(*t) возвращает Result<Result<(), String>, Box<dyn Any + Send>>: три случая — ok, Err и паника.', '{"driver": "fn good() -> Result<(), String> {\n    Ok(())\n}\nfn bad() -> Result<(), String> {\n    Err(\"1 != 2\".to_string())\n}\nfn boom() -> Result<(), String> {\n    let v: Vec<i32> = vec![];\n    let _ = v[3];\n    Ok(())\n}\n\nfn main() {\n    std::panic::set_hook(Box::new(|_| {}));\n    let (p, f, rep) = run_tests(&[(\"good\", good), (\"bad\", bad), (\"boom\", boom), (\"good2\", good)]);\n    for l in &rep {\n        println!(\"{l}\");\n    }\n    println!(\"{p} passed, {f} failed\");\n    println!(\"{:?}\", run_tests(&[]));\n}\n", "expected": ["test good ... ok", "test bad ... FAILED: 1 != 2", "test boom ... FAILED: panicked", "test good2 ... ok", "2 passed, 2 failed", "(0, 0, [])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-assert-helpers', 21, 'rust', 'Свои проверки, возвращающие Result', 'check_eq<T: PartialEq + Debug>(left, right) → Result<(), String> «left: <l:?>, right: <r:?>» при неравенстве. check_close(a, b, eps) → Result<(), String> «|a-b| = <d> > <eps>». check_sorted<T: PartialOrd + Debug>(v) → Result<(), String> «не отсортировано на позиции <i>: <a:?> > <b:?>» (индекс первого нарушения пары). Все проверки — функции, не паникуют.', 'use std::fmt::Debug;

fn check_eq<T: PartialEq + Debug>(left: T, right: T) -> Result<(), String> {
    todo!()
}

fn check_close(a: f64, b: f64, eps: f64) -> Result<(), String> {
    todo!()
}

fn check_sorted<T: PartialOrd + Debug>(v: &[T]) -> Result<(), String> {
    todo!()
}
', 'Сообщение собирайте format!-ом с {:?}; пара окон windows(2) даёт индекс первого нарушения.', '{"driver": "fn main() {\n    println!(\"{:?}\", check_eq(2 + 2, 4));\n    println!(\"{:?}\", check_eq(\"a\", \"b\"));\n    println!(\"{:?}\", check_eq(vec![1, 2], vec![1, 3]));\n    println!(\"{:?} {:?}\", check_close(0.1 + 0.2, 0.3, 1e-9), check_close(1.0, 1.5, 0.1));\n    println!(\"{:?} {:?}\", check_sorted(&[1, 2, 2, 5]), check_sorted(&[1, 3, 2, 4]));\n    println!(\"{:?}\", check_sorted::<i32>(&[]));\n}\n", "expected": ["Ok(())", "Err(\"left: \\\"a\\\", right: \\\"b\\\"\")", "Err(\"left: [1, 2], right: [1, 3]\")", "Ok(()) Err(\"|a-b| = 0.5 > 0.1\")", "Ok(()) Err(\"не отсортировано на позиции 1: 3 > 2\")", "Ok(())"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-write-tests-abs', 22, 'rust', 'Напишите тесты: abs и её мутанты', 'Вам нужно написать failures_abs(f: &dyn Fn(i32) → i32) → usize — набор проверок для функции абсолютного значения: вернуть число не прошедших проверок. Драйвер запускает ваш набор на верной реализации (должно быть 0 провалов) и на пяти сломанных — каждая обязана быть поймана хотя бы одним провалом.', 'fn failures_abs(f: &dyn Fn(i32) -> i32) -> usize {
    let mut fails = 0;
    // добавляйте проверки: if f(вход) != ожидаемое { fails += 1; }
    fails
}
', 'Проверьте ноль, плюс и минус единицу, обычные числа обоих знаков и очень большие по модулю — каждый мутант ломается на своей границе.', '{"driver": "fn main() {\n    let good = |x: i32| x.wrapping_abs();\n    println!(\"good: {}\", failures_abs(&good));\n    let m1 = |x: i32| x;\n    let m2 = |x: i32| if x < 0 { x } else { -x };\n    let m3 = |x: i32| if x < -1 { -x } else { x };\n    let m4 = |x: i32| if x == 0 { 1 } else { x.abs() };\n    let m5 = |x: i32| x.abs().min(1000);\n    let names = [\"identity\", \"negate\", \"minus-one\", \"zero\", \"clamp\"];\n    let ms: [&dyn Fn(i32) -> i32; 5] = [&m1, &m2, &m3, &m4, &m5];\n    for (n, m) in names.iter().zip(ms.iter()) {\n        let f = failures_abs(*m);\n        println!(\"{n}: {}\", if f > 0 { \"caught\" } else { \"SURVIVED\" });\n    }\n}\n", "expected": ["good: 0", "identity: caught", "negate: caught", "minus-one: caught", "zero: caught", "clamp: caught"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-write-tests-leap', 23, 'rust', 'Напишите тесты: високосный год', 'failures_leap(f: &dyn Fn(i32) → bool) → usize — проверки is_leap_year. Верная реализация: делится на 4, кроме кратных 100, кроме кратных 400. Драйвер проверяет, что на верной реализации провалов 0, а все четыре мутанта пойманы.', 'fn failures_leap(f: &dyn Fn(i32) -> bool) -> usize {
    let mut fails = 0;
    // if f(год) != ожидаемое { fails += 1; }
    fails
}
', 'Нужны годы разных видов: обычный високосный, обычный невисокосный, кратный 100, кратный 400 и кратный 200, но не 400.', '{"driver": "fn main() {\n    let good = |y: i32| (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;\n    println!(\"good: {}\", failures_leap(&good));\n    let m1 = |y: i32| y % 4 == 0;\n    let m2 = |y: i32| y % 4 == 0 && y % 100 != 0;\n    let m3 = |y: i32| y % 4 == 0 && (y % 100 != 0 || y % 200 == 0);\n    let m4 = |y: i32| (y % 4 == 0 && y % 100 != 0) || y % 100 == 0;\n    let ms: [&dyn Fn(i32) -> bool; 4] = [&m1, &m2, &m3, &m4];\n    let names = [\"only-4\", \"no-400\", \"200-rule\", \"100-always\"];\n    for (n, m) in names.iter().zip(ms.iter()) {\n        println!(\"{n}: {}\", if failures_leap(*m) > 0 { \"caught\" } else { \"SURVIVED\" });\n    }\n}\n", "expected": ["good: 0", "only-4: caught", "no-400: caught", "200-rule: caught", "100-always: caught"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-write-tests-clamp', 24, 'rust', 'Напишите тесты: clamp(x, lo, hi)', 'failures_clamp(f: &dyn Fn(i32, i32, i32) → i32) → usize — проверки clamp(x, lo, hi) = x, обрезанный в [lo, hi] (считайте lo ≤ hi). Верная реализация даёт 0 провалов; четыре мутанта обязаны быть пойманы.', 'fn failures_clamp(f: &dyn Fn(i32, i32, i32) -> i32) -> usize {
    let mut fails = 0;
    // if f(x, lo, hi) != ожидаемое { fails += 1; }
    fails
}
', 'Проверяйте внутри диапазона, ровно на обеих границах, за каждой границей, вырожденный диапазон lo = hi и отрицательные границы.', '{"driver": "fn main() {\n    let good = |x: i32, lo: i32, hi: i32| x.max(lo).min(hi);\n    println!(\"good: {}\", failures_clamp(&good));\n    let m1 = |x: i32, lo: i32, _hi: i32| x.max(lo);\n    let m2 = |x: i32, _lo: i32, hi: i32| x.min(hi);\n    let m3 = |x: i32, lo: i32, hi: i32| if x < lo { lo } else if x > hi { hi - 1 } else { x };\n    let m4 = |x: i32, lo: i32, hi: i32| if x <= lo { lo + 1 } else if x > hi { hi } else { x };\n    let ms: [&dyn Fn(i32, i32, i32) -> i32; 4] = [&m1, &m2, &m3, &m4];\n    let names = [\"no-upper\", \"no-lower\", \"off-by-one-hi\", \"off-by-one-lo\"];\n    for (n, m) in names.iter().zip(ms.iter()) {\n        println!(\"{n}: {}\", if failures_clamp(*m) > 0 { \"caught\" } else { \"SURVIVED\" });\n    }\n}\n", "expected": ["good: 0", "no-upper: caught", "no-lower: caught", "off-by-one-hi: caught", "off-by-one-lo: caught"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-write-tests-stack', 25, 'rust', 'Напишите тесты: реализации стека', 'Трейт StackLike: new() → Self, push(&mut self, i32), pop(&mut self) → Option<i32>, peek(&self) → Option<i32>, len(&self) → usize. Напишите failures<S: StackLike>() → usize: проверки любой реализации. Драйвер даёт верный стек и три сломанных (очередь вместо стека; pop не уменьшает длину; peek снимает элемент) — все должны быть пойманы.', 'trait StackLike {
    fn new() -> Self;
    fn push(&mut self, x: i32);
    fn pop(&mut self) -> Option<i32>;
    fn peek(&self) -> Option<i32>;
    fn len(&self) -> usize;
}

fn failures<S: StackLike>() -> usize {
    let mut fails = 0;
    // let mut s = S::new(); ... if условие_нарушено { fails += 1; }
    fails
}
', 'Проверяйте порядок LIFO на нескольких элементах, длину после каждой операции, пустой стек и то, что peek ничего не удаляет.', '{"driver": "struct Good(Vec<i32>);\nimpl StackLike for Good {\n    fn new() -> Good { Good(vec![]) }\n    fn push(&mut self, x: i32) { self.0.push(x) }\n    fn pop(&mut self) -> Option<i32> { self.0.pop() }\n    fn peek(&self) -> Option<i32> { self.0.last().copied() }\n    fn len(&self) -> usize { self.0.len() }\n}\nstruct Fifo(Vec<i32>);\nimpl StackLike for Fifo {\n    fn new() -> Fifo { Fifo(vec![]) }\n    fn push(&mut self, x: i32) { self.0.push(x) }\n    fn pop(&mut self) -> Option<i32> { if self.0.is_empty() { None } else { Some(self.0.remove(0)) } }\n    fn peek(&self) -> Option<i32> { self.0.first().copied() }\n    fn len(&self) -> usize { self.0.len() }\n}\nstruct NoShrink(Vec<i32>, usize);\nimpl StackLike for NoShrink {\n    fn new() -> NoShrink { NoShrink(vec![], 0) }\n    fn push(&mut self, x: i32) { self.0.push(x); self.1 += 1 }\n    fn pop(&mut self) -> Option<i32> { self.0.pop() }\n    fn peek(&self) -> Option<i32> { self.0.last().copied() }\n    fn len(&self) -> usize { self.1 }\n}\nstruct PeekPops(Vec<i32>);\nimpl StackLike for PeekPops {\n    fn new() -> PeekPops { PeekPops(vec![]) }\n    fn push(&mut self, x: i32) { self.0.push(x) }\n    fn pop(&mut self) -> Option<i32> { self.0.pop() }\n    fn peek(&self) -> Option<i32> { self.0.last().copied().map(|x| x + 0) }\n    fn len(&self) -> usize { if self.0.len() > 2 { self.0.len() - 1 } else { self.0.len() } }\n}\n\nfn main() {\n    println!(\"good: {}\", failures::<Good>());\n    for (n, f) in [(\"fifo\", failures::<Fifo>()), (\"no-shrink\", failures::<NoShrink>()), (\"len-bug\", failures::<PeekPops>())] {\n        println!(\"{n}: {}\", if f > 0 { \"caught\" } else { \"SURVIVED\" });\n    }\n}\n", "expected": ["good: 0", "fifo: caught", "no-shrink: caught", "len-bug: caught"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-parse-duration', 26, 'rust', 'Разбор «1h30m15s»: таблица случаев', 'parse_duration(s) → Option<u64> — секунды: единицы h (3600), m (60), s (1), каждая не более одного раза и в порядке h, m, s; число без знака, не пустое. «90s» → 90, «1h30m15s» → 5415, «2h» → 7200. Пустая строка, число без единицы, неизвестная единица, повтор или неправильный порядок → None.', 'fn parse_duration(s: &str) -> Option<u64> {
    todo!()
}
', 'Копите цифры в строке; встретили букву — переводите накопленное число в секунды и проверяйте порядок единиц.', '{"driver": "fn main() {\n    let cases = [\"1h30m15s\", \"90s\", \"2h\", \"45m\", \"0s\", \"\", \"15\", \"h\", \"1x\", \"1m1h\", \"1h1h\", \"12m3\", \"5s5s\", \"003m\"];\n    for c in cases {\n        println!(\"{:>10} -> {:?}\", format!(\"{:?}\", c), parse_duration(c));\n    }\n}\n", "expected": ["\"1h30m15s\" -> Some(5415)", "     \"90s\" -> Some(90)", "      \"2h\" -> Some(7200)", "     \"45m\" -> Some(2700)", "      \"0s\" -> Some(0)", "        \"\" -> None", "      \"15\" -> None", "       \"h\" -> None", "      \"1x\" -> None", "    \"1m1h\" -> None", "    \"1h1h\" -> None", "    \"12m3\" -> None", "    \"5s5s\" -> None", "    \"003m\" -> Some(180)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-error-api', 27, 'rust', 'Ошибки библиотеки: enum, Display, Error, From', 'ConfigError: Missing(String) — нет ключа, BadNumber { key: String, source: ParseIntError }. Реализуйте Display («нет ключа X» / «ключ X: неверное число»), std::error::Error с методом source (для BadNumber — причина, для Missing — None). load(text) → Result<Settings, ConfigError>: строки «ключ=значение»; обязательны port и workers (числа u16 и u8).', 'use std::error::Error;
use std::fmt;
use std::num::ParseIntError;

#[derive(Debug)]
enum ConfigError {
    Missing(String),
    BadNumber { key: String, source: ParseIntError },
}

#[derive(Debug, PartialEq)]
struct Settings {
    port: u16,
    workers: u8,
}

// impl Display и Error для ConfigError

fn load(text: &str) -> Result<Settings, ConfigError> {
    todo!()
}
', 'source() возвращает Some(source) как &dyn Error; для u16 и u8 число 70000 и 256 — это уже ошибка разбора.', '{"driver": "fn main() {\n    println!(\"{:?}\", load(\"port = 8080\\nworkers=4\"));\n    for t in [\"workers=4\", \"port=80\", \"port=70000\\nworkers=1\", \"port=1\\nworkers=abc\"] {\n        match load(t) {\n            Ok(s) => println!(\"ok {:?}\", s),\n            Err(e) => println!(\"{} | причина: {:?}\", e, e.source().map(|s| s.to_string())),\n        }\n    }\n}\n", "expected": ["Ok(Settings { port: 8080, workers: 4 })", "нет ключа port | причина: None", "нет ключа workers | причина: None", "ключ port: неверное число | причина: Some(\"number too large to fit in target type\")", "ключ workers: неверное число | причина: Some(\"invalid digit found in string\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-module-tree', 28, 'rust', 'Дерево модулей из путей', 'render_tree(paths: &[&str]) → String: пути вида «net::tcp::connect» собираются в дерево; каждый уровень — на отдельной строке с отступом в два пробела на глубину, дети по алфавиту, повторы объединяются. Пустой список — пустая строка.', 'fn render_tree(paths: &[&str]) -> String {
    todo!()
}
', 'Дерево — вложенные BTreeMap (или узел с BTreeMap детей); entry(...).or_default() создаёт недостающие уровни.', '{"driver": "fn main() {\n    print!(\"{}\", render_tree(&[\"net::tcp::connect\", \"net::udp\", \"db::query\", \"net::tcp::listen\", \"net::tcp::connect\", \"app\"]));\n    println!(\"[{}]\", render_tree(&[]));\n}\n", "expected": ["app", "db", "  query", "net", "  tcp", "    connect", "    listen", "  udp", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 22, 'r22-public-surface', 29, 'rust', 'Публичная поверхность: что видно снаружи', 'Элемент описан путём и видимостью каждого сегмента: Item { path: &str (через ::), vis: Vec<Vis> } с Vis ∈ {Private, Crate, Pub} (длины равны). surface(items) → (Vec<String>, Vec<String>): первое — элементы, видимые другим крейтам (все сегменты Pub), второе — только внутри крейта (нет Private, но есть Crate). Оба списка по алфавиту.', '#[derive(Clone, Copy, PartialEq)]
enum Vis {
    Private,
    Crate,
    Pub,
}

struct Item {
    path: &''static str,
    vis: Vec<Vis>,
}

fn surface(items: &[Item]) -> (Vec<String>, Vec<String>) {
    todo!()
}
', 'Элемент виден снаружи, только если открыты все сегменты пути: достаточно одного закрытого родителя, чтобы спрятать потомка.', '{"driver": "fn main() {\n    use Vis::*;\n    let items = vec![\n        Item { path: \"net::connect\", vis: vec![Pub, Pub] },\n        Item { path: \"net::tcp::listen\", vis: vec![Pub, Crate, Pub] },\n        Item { path: \"net::tcp::raw\", vis: vec![Pub, Pub, Private] },\n        Item { path: \"db::query\", vis: vec![Pub, Pub] },\n        Item { path: \"util::hash\", vis: vec![Crate, Pub] },\n        Item { path: \"secret::key\", vis: vec![Private, Pub] },\n    ];\n    let (p, c) = surface(&items);\n    println!(\"{:?}\", p);\n    println!(\"{:?}\", c);\n    println!(\"{:?}\", surface(&[]));\n}\n", "expected": ["[\"db::query\", \"net::connect\"]", "[\"net::tcp::listen\", \"util::hash\"]", "([], [])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-par-sum', 0, 'rust', 'Параллельная сумма: scope и chunks', 'par_sum(v: &[i64], parts: usize) → i64: разрежьте срез на parts кусков (последний может быть короче; parts ≥ 1), в thread::scope запустите по потоку на кусок, каждый считает свою сумму, затем сложите результаты. Данные не копируются: потоки берут ссылки на куски.', 'use std::thread;

fn par_sum(v: &[i64], parts: usize) -> i64 {
    todo!()
}
', 'chunks(size) даёт срезы; s.spawn(move || …) в scope может брать срез напрямую; h.join().unwrap() возвращает сумму куска.', '{"driver": "fn main() {\n    let v: Vec<i64> = (1..=100_000).collect();\n    println!(\"{}\", par_sum(&v, 4));\n    println!(\"{}\", par_sum(&v, 7));\n    println!(\"{}\", par_sum(&v[..10], 100));\n    println!(\"{}\", par_sum(&[], 3));\n    println!(\"{}\", par_sum(&[5], 1));\n}\n", "expected": ["5000050000", "5000050000", "55", "0", "5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-spawn-join-results', 1, 'rust', 'spawn и join: результаты по порядку', 'squares_in_threads(n) → Vec<u64>: для каждого i от 1 до n запустите поток, который возвращает i², и соберите результаты В ПОРЯДКЕ i (дождитесь потоков по очереди через JoinHandle). word_lengths(words: Vec<String>) → Vec<usize> — каждое слово обрабатывается в своём потоке (слова переезжают в потоки).', 'use std::thread;

fn squares_in_threads(n: u64) -> Vec<u64> {
    todo!()
}

fn word_lengths(words: Vec<String>) -> Vec<usize> {
    todo!()
}
', 'Сначала запустите ВСЕ потоки (collect в вектор хэндлов), только потом join: иначе потоки пойдут по очереди.', '{"driver": "fn main() {\n    println!(\"{:?}\", squares_in_threads(8));\n    println!(\"{:?}\", squares_in_threads(0));\n    println!(\"{:?}\", word_lengths(vec![\"привет\".into(), \"мир\".into(), \"\".into(), \"rust\".into()]));\n}\n", "expected": ["[1, 4, 9, 16, 25, 36, 49, 64]", "[]", "[6, 3, 0, 4]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-fix-move', 2, 'rust', 'Исправьте: замыкание заимствует локальное', 'sum_in_thread запускает поток, который суммирует вектор, но замыкание берёт v по ссылке, а поток может пережить функцию (E0373). Исправьте одним словом.', 'use std::thread;

fn sum_in_thread(v: Vec<i32>) -> i32 {
    let h = thread::spawn(|| v.iter().sum::<i32>());
    h.join().unwrap()
}
', 'move передаст вектор потоку целиком.', '{"driver": "fn main() {\n    println!(\"{}\", sum_in_thread(vec![1, 2, 3, 4]));\n    println!(\"{}\", sum_in_thread(vec![]));\n}\n", "expected": ["10", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-fix-rc', 3, 'rust', 'Исправьте: Rc не Send', 'len_in_thread оборачивает строку в Rc и отправляет в поток — компилятор не пускает (Rc не реализует Send). Замените Rc на Arc, остальное оставьте.', 'use std::rc::Rc;
use std::thread;

fn len_in_thread(s: &str) -> usize {
    let shared = Rc::new(s.to_string());
    let for_thread = Rc::clone(&shared);
    let h = thread::spawn(move || for_thread.len());
    let n = h.join().unwrap();
    n + Rc::strong_count(&shared) - 1
}
', 'Arc имеет те же методы new, clone и strong_count — подставьте его вместо Rc и подключите std::sync::Arc.', '{"driver": "fn main() {\n    println!(\"{}\", len_in_thread(\"привет\"));\n    println!(\"{}\", len_in_thread(\"\"));\n}\n", "expected": ["12", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-counter-mutex', 4, 'rust', 'Общий счётчик: Arc<Mutex<u64>>', 'count_parallel(threads: usize, per_thread: u64) → u64: запустите threads потоков, каждый увеличивает общий счётчик (Arc<Mutex<u64>>) per_thread раз по единице; верните итог. contended(threads, per_thread) → u64 — то же, но каждый поток сначала считает локально и один раз прибавляет к общему.', 'use std::sync::{Arc, Mutex};
use std::thread;

fn count_parallel(threads: usize, per_thread: u64) -> u64 {
    todo!()
}

fn contended(threads: usize, per_thread: u64) -> u64 {
    todo!()
}
', 'Каждому потоку — свой клон Arc; замок берётся на одну операцию: *c.lock().unwrap() += 1.', '{"driver": "fn main() {\n    println!(\"{} {}\", count_parallel(8, 10_000), contended(8, 10_000));\n    println!(\"{} {}\", count_parallel(1, 5), contended(3, 0));\n    println!(\"{}\", count_parallel(0, 100));\n}\n", "expected": ["80000 80000", "5 0", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-bank-transfers', 5, 'rust', 'Переводы без взаимных блокировок', 'transfer_all(accounts: &[Arc<Mutex<i64>>], transfers: &[(usize, usize, i64)]) → Vec<i64>: каждый перевод (from, to, сумма) выполняется в своём потоке одновременно с остальными. Чтобы не получить deadlock, всегда захватывайте счета в порядке возрастания номера. from == to — ничего не делать. Верните итоговые балансы (отрицательные допустимы).', 'use std::sync::{Arc, Mutex};
use std::thread;

fn transfer_all(accounts: &[Arc<Mutex<i64>>], transfers: &[(usize, usize, i64)]) -> Vec<i64> {
    todo!()
}
', 'Всегда блокируйте сначала счёт с меньшим номером: так цикл ожидания невозможен.', '{"driver": "fn main() {\n    let accs: Vec<Arc<Mutex<i64>>> = (0..4).map(|_| Arc::new(Mutex::new(100))).collect();\n    let mut transfers = Vec::new();\n    for i in 0..200usize {\n        transfers.push((i % 4, (i * 3 + 1) % 4, (i as i64 % 7) + 1));\n    }\n    let res = transfer_all(&accs, &transfers);\n    println!(\"{:?} total={}\", res, res.iter().sum::<i64>());\n    let expected: Vec<i64> = {\n        let mut e = vec![100i64; 4];\n        for &(f, t, a) in &transfers {\n            if f != t {\n                e[f] -= a;\n                e[t] += a;\n            }\n        }\n        e\n    };\n    println!(\"{}\", res == expected);\n    println!(\"{:?}\", transfer_all(&[], &[]));\n}\n", "expected": ["[101, 99, 101, 99] total=400", "true", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-rwlock-cache', 6, 'rust', 'Кеш на RwLock', 'Cache хранит RwLock<HashMap<u64, u64>> и AtomicUsize числа реальных вычислений. get(&self, x, f: fn(u64) → u64) → u64: читает под read-замком; если нет — берёт write-замок, проверяет ещё раз и вычисляет (вычисление считается). computations(&self) → usize. Из нескольких потоков одно значение должно вычисляться ровно один раз.', 'use std::collections::HashMap;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::RwLock;

struct Cache {
    map: RwLock<HashMap<u64, u64>>,
    computed: AtomicUsize,
}

impl Cache {
    fn new() -> Cache {
        todo!()
    }
    fn get(&self, x: u64, f: fn(u64) -> u64) -> u64 {
        todo!()
    }
    fn computations(&self) -> usize {
        todo!()
    }
}
', 'После получения write-замка проверьте ключ ещё раз: пока вы ждали, другой поток мог его вычислить.', '{"driver": "use std::sync::Arc;\nuse std::thread;\n\nfn slow_square(x: u64) -> u64 {\n    x * x\n}\n\nfn main() {\n    let c = Arc::new(Cache::new());\n    let hs: Vec<_> = (0..8)\n        .map(|t| {\n            let c = Arc::clone(&c);\n            thread::spawn(move || (0..50u64).map(|i| c.get((i + t) % 10, slow_square)).sum::<u64>())\n        })\n        .collect();\n    let total: u64 = hs.into_iter().map(|h| h.join().unwrap()).sum();\n    println!(\"{} {}\", total, c.computations());\n    println!(\"{}\", c.get(3, slow_square));\n    println!(\"{}\", c.computations());\n}\n", "expected": ["11400 10", "9", "10"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-word-count-par', 7, 'rust', 'Параллельный подсчёт слов', 'word_count_par(text: &str, parts: usize) → BTreeMap<String, usize>: разделите строки текста между parts потоками (по порядку блоками), каждый считает слова (в нижнем регистре, слова — буквы и цифры) в своём HashMap, затем слейте результаты. Результат не должен зависеть от parts.', 'use std::collections::BTreeMap;

fn word_count_par(text: &str, parts: usize) -> BTreeMap<String, usize> {
    todo!()
}
', 'Каждый поток возвращает свой HashMap; общий результат собирается уже в главном потоке — без блокировок.', '{"driver": "fn main() {\n    let text = \"the quick brown fox\\njumps over the lazy dog\\nThe DOG barks, the fox runs\\n\\nfox fox\";\n    let a = word_count_par(text, 1);\n    let b = word_count_par(text, 3);\n    let c = word_count_par(text, 10);\n    println!(\"{:?}\", a);\n    println!(\"{}\", a == b && b == c);\n    println!(\"{:?}\", word_count_par(\"\", 4));\n    println!(\"{:?}\", word_count_par(\"Привет, привет! мир\", 2));\n}\n", "expected": ["{\"barks\": 1, \"brown\": 1, \"dog\": 2, \"fox\": 4, \"jumps\": 1, \"lazy\": 1, \"over\": 1, \"quick\": 1, \"runs\": 1, \"the\": 4}", "true", "{}", "{\"мир\": 1, \"привет\": 2}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-par-map', 8, 'rust', 'par_map: параллельное преобразование', 'par_map<T, U, F>(v: &[T], parts: usize, f: F) → Vec<U> where T: Sync, U: Send, F: Fn(&T) → U + Sync: применить f ко всем элементам, разбив срез на parts кусков по потокам; результат в исходном порядке.', 'use std::thread;

fn par_map<T, U, F>(v: &[T], parts: usize, f: F) -> Vec<U>
where
    T: Sync,
    U: Send,
    F: Fn(&T) -> U + Sync,
{
    todo!()
}
', 'Замыкание f вызывается из нескольких потоков по общей ссылке: поэтому F: Sync; берите &f и копируйте ссылку в потоки.', '{"driver": "fn main() {\n    let v: Vec<u64> = (1..=20).collect();\n    println!(\"{:?}\", par_map(&v, 3, |x| x * x));\n    println!(\"{:?}\", par_map(&[\"a\", \"bb\", \"ccc\"], 2, |s| s.len()));\n    println!(\"{:?}\", par_map(&[] as &[i32], 4, |x| x + 1));\n    let words = vec![String::from(\"раз\"), String::from(\"два\"), String::from(\"три\")];\n    println!(\"{:?}\", par_map(&words, 3, |w| w.to_uppercase()));\n    let k = 10;\n    println!(\"{:?}\", par_map(&[1, 2, 3], 2, |x| x * k));\n}\n", "expected": ["[1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400]", "[1, 2, 3]", "[]", "[\"РАЗ\", \"ДВА\", \"ТРИ\"]", "[10, 20, 30]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-pipeline-channels', 9, 'rust', 'Конвейер из потоков и каналов', 'pipeline(n: u64) → Vec<u64>: три стадии в трёх потоках, соединённые каналами mpsc: (1) генератор шлёт числа 1..=n; (2) возводит в квадрат; (3) фильтр оставляет квадраты, делящиеся на 3. Главный поток собирает результат (порядок сохраняется).', 'use std::sync::mpsc;
use std::thread;

fn pipeline(n: u64) -> Vec<u64> {
    todo!()
}
', 'Каждая стадия владеет своим tx; когда стадия закончилась, её tx закрывается — следующая стадия выходит из цикла по rx.', '{"driver": "fn main() {\n    println!(\"{:?}\", pipeline(12));\n    println!(\"{:?}\", pipeline(0));\n    println!(\"{}\", pipeline(1000).len());\n}\n", "expected": ["[9, 36, 81, 144]", "[]", "333"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-fan-in', 10, 'rust', 'Несколько производителей, один получатель', 'fan_in(producers: usize, items: usize) → Vec<(usize, usize)>: запустите producers потоков; поток p шлёт в общий канал пары (p, 0), (p, 1), …, (p, items-1). Главный поток собирает ВСЕ сообщения и возвращает их отсортированными. Для этого клонируйте отправителя и не забудьте закрыть исходного.', 'use std::sync::mpsc;
use std::thread;

fn fan_in(producers: usize, items: usize) -> Vec<(usize, usize)> {
    todo!()
}
', 'drop(tx) в главном потоке закрывает исходный отправитель: иначе rx.iter() никогда не закончится.', '{"driver": "fn main() {\n    println!(\"{:?}\", fan_in(3, 2));\n    println!(\"{}\", fan_in(10, 100).len());\n    println!(\"{:?}\", fan_in(0, 5));\n    println!(\"{:?}\", fan_in(2, 0));\n}\n", "expected": ["[(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]", "1000", "[]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-ping-pong', 11, 'rust', 'Пинг-понг через два канала', 'ping_pong(rounds: u32) → Vec<String>: два потока обмениваются сообщениями через два канала: «ping» от первого второму, «pong» обратно, rounds раз. Каждый поток записывает в общий журнал (отдельный канал или значение, возвращаемое из join) события в порядке «ping 1», «pong 1», «ping 2», …', 'use std::sync::mpsc;
use std::thread;

fn ping_pong(rounds: u32) -> Vec<String> {
    todo!()
}
', 'Пинг ждёт ответа recv() после каждого send(): так события выстраиваются строго по очереди.', '{"driver": "fn main() {\n    println!(\"{:?}\", ping_pong(3));\n    println!(\"{:?}\", ping_pong(0));\n    println!(\"{}\", ping_pong(500).len());\n}\n", "expected": ["[\"ping 1\", \"pong 1\", \"ping 2\", \"pong 2\", \"ping 3\", \"pong 3\"]", "[]", "1000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-sync-channel', 12, 'rust', 'Ограниченный канал: давление назад', 'bounded_sum(items: u64, capacity: usize) → (u64, bool): производитель в потоке шлёт числа 1..=items в sync_channel(capacity); потребитель в главном потоке суммирует. Второе значение — истина, если потребитель получил числа строго по порядку 1, 2, 3, …', 'use std::sync::mpsc;
use std::thread;

fn bounded_sum(items: u64, capacity: usize) -> (u64, bool) {
    todo!()
}
', 'sync_channel(0) — «рандеву»: send ждёт, пока получатель не заберёт значение.', '{"driver": "fn main() {\n    println!(\"{:?}\", bounded_sum(10, 2));\n    println!(\"{:?}\", bounded_sum(10_000, 1));\n    println!(\"{:?}\", bounded_sum(100, 0));\n    println!(\"{:?}\", bounded_sum(0, 4));\n}\n", "expected": ["(55, true)", "(50005000, true)", "(5050, true)", "(0, true)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-condvar-queue', 13, 'rust', 'Ограниченная очередь на Mutex и Condvar', 'BoundedQueue<T> { Mutex<VecDeque<T>>, Condvar not_empty, Condvar not_full, capacity }: push(&self, x) ждёт, пока есть место; pop(&self) → T ждёт, пока появится элемент. Проверка: производители и потребители в разных потоках, сумма всех элементов совпадает.', 'use std::collections::VecDeque;
use std::sync::{Condvar, Mutex};

struct BoundedQueue<T> {
    items: Mutex<VecDeque<T>>,
    not_empty: Condvar,
    not_full: Condvar,
    capacity: usize,
}

impl<T> BoundedQueue<T> {
    fn new(capacity: usize) -> BoundedQueue<T> {
        todo!()
    }
    fn push(&self, x: T) {
        todo!()
    }
    fn pop(&self) -> T {
        todo!()
    }
}
', 'Ожидание условия — всегда в цикле while: после пробуждения условие нужно проверить ещё раз.', '{"driver": "use std::sync::Arc;\nuse std::thread;\n\nfn main() {\n    let q = Arc::new(BoundedQueue::new(3));\n    let producers: Vec<_> = (0..4u64)\n        .map(|p| {\n            let q = Arc::clone(&q);\n            thread::spawn(move || {\n                for i in 0..50 {\n                    q.push(p * 1000 + i);\n                }\n            })\n        })\n        .collect();\n    let consumers: Vec<_> = (0..2)\n        .map(|_| {\n            let q = Arc::clone(&q);\n            thread::spawn(move || (0..100).map(|_| q.pop()).sum::<u64>())\n        })\n        .collect();\n    for p in producers {\n        p.join().unwrap();\n    }\n    let total: u64 = consumers.into_iter().map(|c| c.join().unwrap()).sum();\n    let expected: u64 = (0..4u64).map(|p| (0..50).map(|i| p * 1000 + i).sum::<u64>()).sum();\n    println!(\"{} {}\", total, total == expected);\n    let single: BoundedQueue<i32> = BoundedQueue::new(1);\n    single.push(7);\n    println!(\"{}\", single.pop());\n}\n", "expected": ["304900 true", "7"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-barrier-phases', 14, 'rust', 'Barrier: две фазы', 'phases(n: usize) → Vec<u64>: n потоков; в фазе 1 поток i записывает в общий вектор слот i значение (i+1)²; после Barrier в фазе 2 каждый поток читает сумму всех слотов и возвращает её. Благодаря барьеру все n результатов одинаковы.', 'use std::sync::{Arc, Barrier, Mutex};
use std::thread;

fn phases(n: usize) -> Vec<u64> {
    todo!()
}
', 'barrier.wait() блокирует поток, пока не придут все n; только после него безопасно читать чужие слоты.', '{"driver": "fn main() {\n    println!(\"{:?}\", phases(4));\n    println!(\"{:?}\", phases(1));\n    let r = phases(12);\n    println!(\"{} {}\", r.len(), r.iter().all(|&x| x == r[0]));\n    println!(\"{:?}\", phases(0));\n}\n", "expected": ["[30, 30, 30, 30]", "[1]", "12 true", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-atomic-counter', 15, 'rust', 'Атомики: fetch_add и fetch_max', 'atomic_stats(threads: usize, per_thread: usize) → (usize, usize, usize). Поток с номером id (0..threads): per_thread раз увеличивает общий счётчик hits (fetch_add); записывает свой id в biggest через fetch_max; пытается занять флаг first через compare_exchange(0, id + 1) — это удаётся ровно одному потоку. Верните (hits, наибольший id, число потоков, занявших флаг).', 'use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::thread;

fn atomic_stats(threads: usize, per_thread: usize) -> (usize, usize, usize) {
    todo!()
}
', 'compare_exchange(0, id+1, …) удаётся ровно одному потоку — победитель один независимо от порядка запуска.', '{"driver": "fn main() {\n    println!(\"{:?}\", atomic_stats(8, 10_000));\n    println!(\"{:?}\", atomic_stats(1, 3));\n    println!(\"{:?}\", atomic_stats(16, 0));\n    println!(\"{:?}\", atomic_stats(0, 5));\n}\n", "expected": ["(80000, 7, 1)", "(3, 0, 1)", "(0, 15, 1)", "(0, 0, 0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-spinlock', 16, 'rust', 'Спинлок на AtomicBool', 'SpinLock { locked: AtomicBool }: lock(&self) крутится, пока compare_exchange(false, true, Acquire, Relaxed) не удастся (std::hint::spin_loop() в цикле); unlock(&self) пишет false (Release). Драйвер проверяет, что внутри критической секции одновременно находится не больше одного потока.', 'use std::sync::atomic::{AtomicBool, Ordering};

struct SpinLock {
    locked: AtomicBool,
}

impl SpinLock {
    fn new() -> SpinLock {
        todo!()
    }
    fn lock(&self) {
        todo!()
    }
    fn unlock(&self) {
        todo!()
    }
}
', 'Успешный compare_exchange(false, true) означает «я взял замок»; Acquire при взятии и Release при отпускании связывают секции.', '{"driver": "use std::sync::atomic::{AtomicUsize, Ordering};\nuse std::sync::Arc;\nuse std::thread;\n\nfn main() {\n    let lock = Arc::new(SpinLock::new());\n    let inside = Arc::new(AtomicUsize::new(0));\n    let max_inside = Arc::new(AtomicUsize::new(0));\n    let entries = Arc::new(AtomicUsize::new(0));\n    let hs: Vec<_> = (0..4)\n        .map(|_| {\n            let (lock, inside, max_inside, entries) = (lock.clone(), inside.clone(), max_inside.clone(), entries.clone());\n            thread::spawn(move || {\n                for _ in 0..2000 {\n                    lock.lock();\n                    let now = inside.fetch_add(1, Ordering::SeqCst) + 1;\n                    max_inside.fetch_max(now, Ordering::SeqCst);\n                    entries.fetch_add(1, Ordering::SeqCst);\n                    inside.fetch_sub(1, Ordering::SeqCst);\n                    lock.unlock();\n                }\n            })\n        })\n        .collect();\n    for h in hs {\n        h.join().unwrap();\n    }\n    println!(\"max_inside={} entries={}\", max_inside.load(Ordering::SeqCst), entries.load(Ordering::SeqCst));\n}\n", "expected": ["max_inside=1 entries=8000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-once-flag', 17, 'rust', 'Выполнить ровно один раз', 'Once { done: AtomicBool }: run(&self, f: impl FnOnce()) → bool: выполняет f только если никто ещё не начал (compare_exchange на флаге); возвращает true тому, кто выполнил. Драйвер запускает 16 потоков: f должна сработать ровно один раз.', 'use std::sync::atomic::{AtomicBool, Ordering};

struct Once {
    done: AtomicBool,
}

impl Once {
    fn new() -> Once {
        todo!()
    }
    fn run(&self, f: impl FnOnce()) -> bool {
        todo!()
    }
}
', 'Только один compare_exchange(false, true) окажется успешным — он и вызывает f.', '{"driver": "use std::sync::atomic::{AtomicUsize, Ordering};\nuse std::sync::Arc;\nuse std::thread;\n\nfn main() {\n    let once = Arc::new(Once::new());\n    let calls = Arc::new(AtomicUsize::new(0));\n    let winners = Arc::new(AtomicUsize::new(0));\n    let hs: Vec<_> = (0..16)\n        .map(|_| {\n            let (once, calls, winners) = (once.clone(), calls.clone(), winners.clone());\n            thread::spawn(move || {\n                if once.run(|| {\n                    calls.fetch_add(1, Ordering::SeqCst);\n                }) {\n                    winners.fetch_add(1, Ordering::SeqCst);\n                }\n            })\n        })\n        .collect();\n    for h in hs {\n        h.join().unwrap();\n    }\n    println!(\"calls={} winners={}\", calls.load(Ordering::SeqCst), winners.load(Ordering::SeqCst));\n    println!(\"{}\", once.run(|| {}));\n}\n", "expected": ["calls=1 winners=1", "false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-thread-pool', 18, 'rust', 'Свой пул потоков', 'ThreadPool::new(n) запускает n рабочих; execute(&self, job: impl FnOnce() + Send + ''static) кладёт задачу в канал; shutdown(self) закрывает канал и дожидается рабочих (все поставленные задачи выполнены). Рабочие достают задачи из общего Arc<Mutex<Receiver<Job>>>.', 'use std::sync::mpsc;
use std::sync::{Arc, Mutex};
use std::thread::{self, JoinHandle};

type Job = Box<dyn FnOnce() + Send + ''static>;

struct ThreadPool {
    workers: Vec<JoinHandle<()>>,
    sender: Option<mpsc::Sender<Job>>,
}

impl ThreadPool {
    fn new(n: usize) -> ThreadPool {
        todo!()
    }
    fn execute(&self, job: impl FnOnce() + Send + ''static) {
        todo!()
    }
    fn shutdown(mut self) {
        todo!()
    }
}
', 'Рабочий: loop { let job = rx.lock().unwrap().recv(); … } — замок держится только на время recv; закрытый канал → Err → выходим.', '{"driver": "use std::sync::atomic::{AtomicU64, Ordering};\nuse std::sync::Arc;\n\nfn main() {\n    let pool = ThreadPool::new(4);\n    let total = Arc::new(AtomicU64::new(0));\n    for i in 1..=100u64 {\n        let total = Arc::clone(&total);\n        pool.execute(move || {\n            total.fetch_add(i * i, Ordering::SeqCst);\n        });\n    }\n    pool.shutdown();\n    println!(\"{}\", total.load(Ordering::SeqCst));\n    let empty = ThreadPool::new(2);\n    empty.shutdown();\n    println!(\"ok\");\n}\n", "expected": ["338350", "ok"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-par-double', 19, 'rust', 'chunks_mut: изменить на месте параллельно', 'par_scale(v: &mut [i64], k: i64, parts: usize): умножьте каждый элемент на k, разделив срез на parts непересекающихся изменяемых кусков (chunks_mut) и запустив поток на каждый. par_prefix_marks(v: &mut [i64]) — каждый элемент заменить на его индекс × значение (потоки получают смещение куска).', 'use std::thread;

fn par_scale(v: &mut [i64], k: i64, parts: usize) {
    todo!()
}

fn par_prefix_marks(v: &mut [i64]) {
    todo!()
}
', 'chunks_mut даёт непересекающиеся &mut [T]: каждый кусок можно отдать своему потоку без блокировок.', '{"driver": "fn main() {\n    let mut v: Vec<i64> = (1..=10).collect();\n    par_scale(&mut v, 3, 4);\n    println!(\"{:?}\", v);\n    let mut w = vec![5; 10];\n    par_prefix_marks(&mut w);\n    println!(\"{:?}\", w);\n    let mut e: Vec<i64> = vec![];\n    par_scale(&mut e, 2, 3);\n    println!(\"{:?}\", e);\n}\n", "expected": ["[3, 6, 9, 12, 15, 18, 21, 24, 27, 30]", "[0, 5, 10, 15, 20, 25, 30, 35, 40, 45]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-sieve-par', 20, 'rust', 'Простые числа: сегменты по потокам', 'count_primes(n: u64, parts: usize) → usize: сколько простых меньше n. Диапазон 2..n делится на parts сегментов; каждый поток проверяет числа своего сегмента пробным делением. Результат не зависит от parts. Для n до 200 000 работа должна уложиться в лимит.', 'use std::thread;

fn count_primes(n: u64, parts: usize) -> usize {
    todo!()
}
', 'Сегмент [lo, hi): lo = 2 + p·size, hi = min(lo + size, n); поток возвращает количество простых в нём.', '{"driver": "fn main() {\n    println!(\"{} {} {}\", count_primes(100, 1), count_primes(100, 4), count_primes(100, 9));\n    println!(\"{} {}\", count_primes(2, 3), count_primes(3, 5));\n    println!(\"{}\", count_primes(200_000, 8));\n}\n", "expected": ["25 25 25", "0 1", "17984"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-matrix-rows', 21, 'rust', 'Матрица: строки по потокам', 'matmul(a: &[Vec<i64>], b: &[Vec<i64>]) → Vec<Vec<i64>>: произведение матриц (размеры согласованы). Каждая строка результата вычисляется в отдельном потоке внутри scope; результат должен совпасть с последовательным вычислением.', 'use std::thread;

fn matmul(a: &[Vec<i64>], b: &[Vec<i64>]) -> Vec<Vec<i64>> {
    todo!()
}
', 'Каждая строка результата зависит только от строки a и всей b — потоки не пересекаются; b берётся по общей ссылке.', '{"driver": "fn main() {\n    let a = vec![vec![1, 2, 3], vec![4, 5, 6]];\n    let b = vec![vec![7, 8], vec![9, 10], vec![11, 12]];\n    println!(\"{:?}\", matmul(&a, &b));\n    let n = 60;\n    let big: Vec<Vec<i64>> = (0..n).map(|i| (0..n).map(|j| ((i * 7 + j * 3) % 10) as i64).collect()).collect();\n    let r = matmul(&big, &big);\n    let mut seq = vec![vec![0i64; n]; n];\n    for i in 0..n {\n        for j in 0..n {\n            for k in 0..n {\n                seq[i][j] += big[i][k] * big[k][j];\n            }\n        }\n    }\n    println!(\"{} {}\", r == seq, r[5][7]);\n    println!(\"{:?}\", matmul(&[], &[]));\n}\n", "expected": ["[[58, 64], [139, 154]]", "true 1350", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-merge-sort-par', 22, 'rust', 'Параллельная сортировка слиянием', 'par_sort(v: Vec<i64>) → Vec<i64>: сортировка слиянием; половины сортируются в разных потоках (thread::scope), пока длина больше 1000, ниже — обычная sort. Результат совпадает с v.sort().', 'fn par_sort(v: Vec<i64>) -> Vec<i64> {
    todo!()
}
', 'Поток получает правую половину целиком (split_off), левая сортируется в текущем потоке; потом merge двух отсортированных векторов.', '{"driver": "fn main() {\n    let mut x: u64 = 12345;\n    let v: Vec<i64> = (0..50_000)\n        .map(|_| {\n            x = x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n            ((x >> 33) % 100_000) as i64 - 50_000\n        })\n        .collect();\n    let mut want = v.clone();\n    want.sort();\n    let got = par_sort(v);\n    println!(\"{} {} {}\", got == want, got[0], got[got.len() - 1]);\n    println!(\"{:?} {:?}\", par_sort(vec![]), par_sort(vec![3, 1, 2]));\n}\n", "expected": ["true -49999 49999", "[] [1, 2, 3]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-histogram-par', 23, 'rust', 'Гистограмма: у каждого потока своя копия', 'histogram(data: &[u8], parts: usize) → [usize; 16]: частота значений data[i] % 16. Каждый поток заполняет СВОЙ массив [usize; 16] по своему куску, затем массивы складываются. Никаких общих счётчиков внутри цикла.', 'use std::thread;

fn histogram(data: &[u8], parts: usize) -> [usize; 16] {
    todo!()
}
', 'Массив [usize; 16] — копируемый тип, его удобно вернуть из потока; суммируйте поэлементно.', '{"driver": "fn main() {\n    let data: Vec<u8> = (0..100_000u32).map(|i| (i.wrapping_mul(2654435761) >> 24) as u8).collect();\n    let h1 = histogram(&data, 1);\n    let h8 = histogram(&data, 8);\n    println!(\"{}\", h1 == h8);\n    println!(\"{} {:?}\", h1.iter().sum::<usize>(), &h1[..4]);\n    println!(\"{:?}\", histogram(&[], 3));\n    println!(\"{:?}\", histogram(&[1, 17, 33, 2], 2));\n}\n", "expected": ["true", "100000 [6246, 6250, 6251, 6247]", "[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]", "[0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-poison-recovery', 24, 'rust', 'Отравленный мьютекс', 'poison_demo() → (bool, i32, bool): создайте Arc<Mutex<i32>> со значением 10; поток берёт замок, делает +5 и паникует; затем: (1) is_poisoned() замка, (2) значение, полученное через lock().unwrap_or_else(|e| e.into_inner()), (3) удастся ли после clear_poison() обычный lock().is_ok().', 'use std::sync::{Arc, Mutex};
use std::thread;

fn poison_demo() -> (bool, i32, bool) {
    todo!()
}
', 'PoisonError::into_inner отдаёт охранника даже у отравленного мьютекса; clear_poison снимает пометку.', '{"driver": "fn main() {\n    std::panic::set_hook(Box::new(|_| {}));\n    println!(\"{:?}\", poison_demo());\n}\n", "expected": ["(true, 15, true)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-try-lock', 25, 'rust', 'try_lock: без ожидания', 'try_lock_demo() → Vec<bool>: замок Mutex<i32>. Запишите is_ok() последовательности: try_lock() на свободном; на занятом (охранник жив в этом же потоке) — в другом потоке через scope; в этом потоке после отпускания; затем RwLock: try_write() при живом читателе; try_read() при живом читателе.', 'use std::sync::{Mutex, RwLock};
use std::thread;

fn try_lock_demo() -> Vec<bool> {
    todo!()
}
', 'try_lock возвращает Err(WouldBlock), если замок занят; живой охранник — это переменная, не вызов-выражение.', '{"driver": "fn main() {\n    println!(\"{:?}\", try_lock_demo());\n}\n", "expected": ["[true, false, true, false, true]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-cancel-flag', 26, 'rust', 'Отмена потока флагом', 'cancel_demo() → (bool, bool): worker в цикле увеличивает общий AtomicU64 и проверяет Arc<AtomicBool> «stop». Главный поток дожидается, пока счётчик станет ≥ 1000, ставит stop, join-ит рабочего. Верните (поток завершился, счётчик на момент join ≥ 1000).', 'use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::Arc;
use std::thread;

fn cancel_demo() -> (bool, bool) {
    todo!()
}
', 'Флаг отмены — AtomicBool в Arc: рабочий читает его в цикле, главный потом выставляет true.', '{"driver": "fn main() {\n    println!(\"{:?}\", cancel_demo());\n    println!(\"{:?}\", cancel_demo());\n}\n", "expected": ["(true, true)", "(true, true)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-send-bounds', 27, 'rust', 'Границы Send и ''static', 'run_in_thread<R, F>(f: F) → R запускает замыкание в новом потоке и возвращает результат (join). Напишите правильные ограничения: F: FnOnce() → R + Send + ''static, R: Send + ''static. run_all<R, F>(jobs: Vec<F>) → Vec<R> запускает все параллельно и возвращает результаты по порядку.', 'use std::thread;

fn run_in_thread<R, F>(f: F) -> R {
    todo!()
}

fn run_all<R, F>(jobs: Vec<F>) -> Vec<R> {
    todo!()
}
', 'thread::spawn требует Send + ''static от замыкания и Send + ''static от результата — повторите эти границы в where.', '{"driver": "fn main() {\n    println!(\"{}\", run_in_thread(|| 6 * 7));\n    let s = String::from(\"владение\");\n    println!(\"{}\", run_in_thread(move || s.to_uppercase()));\n    println!(\"{:?}\", run_all((1..=5).map(|i| move || i * i).collect()));\n    let v = vec![1, 2, 3];\n    println!(\"{:?}\", run_all(vec![move || v.iter().sum::<i32>()]));\n    println!(\"{:?}\", run_all(Vec::<fn() -> u8>::new()));\n}\n", "expected": ["42", "ВЛАДЕНИЕ", "[1, 4, 9, 16, 25]", "[6]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-named-threads', 28, 'rust', 'Именованные потоки и thread_local', 'named_work(n: usize) → Vec<(String, u32)>: запустите n потоков через thread::Builder с именами «worker-0», «worker-1», …; в каждом thread_local-счётчик (Cell<u32>) увеличивается (i+1) раз; поток возвращает (своё имя через thread::current().name(), значение локального счётчика). Результаты — по порядку запуска.', 'use std::cell::Cell;
use std::thread;

thread_local! {
    static LOCAL: Cell<u32> = Cell::new(0);
}

fn named_work(n: usize) -> Vec<(String, u32)> {
    todo!()
}
', 'thread_local даёт каждому потоку собственную копию: изменения в рабочих не видны главному потоку.', '{"driver": "fn main() {\n    println!(\"{:?}\", named_work(4));\n    LOCAL.with(|c| c.set(100));\n    println!(\"{:?}\", named_work(2));\n    println!(\"{}\", LOCAL.with(|c| c.get()));\n}\n", "expected": ["[(\"worker-0\", 1), (\"worker-1\", 2), (\"worker-2\", 3), (\"worker-3\", 4)]", "[(\"worker-0\", 1), (\"worker-1\", 2)]", "100"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 23, 'r23-dining-philosophers', 29, 'rust', 'Обедающие философы', 'philosophers(n: usize, meals: usize) → Vec<usize>: n философов за круглым столом, n вилок (Mutex<()>). Философ i берёт вилки i и (i+1)%n — НО всегда сначала с меньшим номером, чтобы не было deadlock. Каждый «ест» meals раз (увеличивает свой счётчик). Верните число приёмов пищи каждого.', 'use std::sync::{Arc, Mutex};
use std::thread;

fn philosophers(n: usize, meals: usize) -> Vec<usize> {
    todo!()
}
', 'Сначала вилка с меньшим номером — все философы выстраивают захват в одном порядке, цикла ожидания нет; при n = 1 обе вилки совпадают.', '{"driver": "fn main() {\n    println!(\"{:?}\", philosophers(5, 100));\n    println!(\"{:?}\", philosophers(2, 3));\n    println!(\"{:?}\", philosophers(1, 4));\n    println!(\"{:?}\", philosophers(0, 5));\n}\n", "expected": ["[100, 100, 100, 100, 100]", "[3, 3]", "[4]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-opt-map', 0, 'rust', 'Option::map', 'Напишите double_opt(x: Option<i32>) -> Option<i32>: удвоить значение внутри, None оставить None (без match).', 'fn double_opt(x: Option<i32>) -> Option<i32> {
    todo!()
}
', 'x.map(|v| v * 2)', '{"driver": "fn main() {\n    println!(\"{:?} {:?}\", double_opt(Some(4)), double_opt(None));\n}\n", "expected": ["Some(8) None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-opt-and-then', 1, 'rust', 'and_then', 'Напишите safe_half(x: Option<i32>) -> Option<i32>: половина числа, если оно чётное, иначе None; для None — None. Используйте and_then.', 'fn safe_half(x: Option<i32>) -> Option<i32> {
    todo!()
}
', 'and_then принимает функцию, возвращающую Option.', '{"driver": "fn main() {\n    println!(\"{:?} {:?} {:?}\", safe_half(Some(10)), safe_half(Some(7)), safe_half(None));\n}\n", "expected": ["Some(5) None None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-opt-filter', 2, 'rust', 'filter', 'Напишите positive(x: Option<i32>) -> Option<i32>: оставить значение, только если оно > 0.', 'fn positive(x: Option<i32>) -> Option<i32> {
    todo!()
}
', 'x.filter(|v| *v > 0)', '{"driver": "fn main() {\n    println!(\"{:?} {:?} {:?} {:?}\", positive(Some(5)), positive(Some(-1)), positive(Some(0)), positive(None));\n}\n", "expected": ["Some(5) None None None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-opt-or', 3, 'rust', 'unwrap_or_else', 'Напишите name_or_default(n: Option<&str>) -> String: имя, либо «аноним#» + длина слова «аноним» (так вычисляется лениво) — без match и if.', 'fn name_or_default(n: Option<&str>) -> String {
    todo!()
}
', 'map + unwrap_or_else(|| …)', '{"driver": "fn main() {\n    println!(\"{}\", name_or_default(Some(\"Аня\")));\n    println!(\"{}\", name_or_default(None));\n}\n", "expected": ["Аня", "аноним#6"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-opt-ok-or', 4, 'rust', 'ok_or', 'Напишите first_or_err(v: &[i32]) -> Result<i32, String>: первый элемент или Err("пусто") (first, copied, ok_or).', 'fn first_or_err(v: &[i32]) -> Result<i32, String> {
    todo!()
}
', 'v.first().copied().ok_or(…)', '{"driver": "fn main() {\n    println!(\"{:?} {:?}\", first_or_err(&[7, 8]), first_or_err(&[]));\n}\n", "expected": ["Ok(7) Err(\"пусто\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-opt-zip', 5, 'rust', 'Option::zip', 'Напишите both(a: Option<i32>, b: Option<i32>) -> Option<(i32, i32)>: пара, если оба Some, иначе None (метод zip).', 'fn both(a: Option<i32>, b: Option<i32>) -> Option<(i32, i32)> {
    todo!()
}
', 'a.zip(b)', '{"driver": "fn main() {\n    println!(\"{:?} {:?} {:?}\", both(Some(1), Some(2)), both(Some(1), None), both(None, None));\n}\n", "expected": ["Some((1, 2)) None None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-opt-take', 6, 'rust', 'Option::take', 'Напишите pop_front(slot: &mut Option<String>) -> Option<String>: вынуть значение из слота, оставив None (метод take).', 'fn pop_front(slot: &mut Option<String>) -> Option<String> {
    todo!()
}
', 'take() оставляет None.', '{"driver": "fn main() {\n    let mut s = Some(String::from(\"a\"));\n    println!(\"{:?}\", pop_front(&mut s));\n    println!(\"{:?}\", s);\n    println!(\"{:?}\", pop_front(&mut s));\n}\n", "expected": ["Some(\"a\")", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-res-map-err', 7, 'rust', 'map_err', 'Напишите parse_pos(s: &str) -> Result<u32, String>: разобрать неотрицательное число, при ошибке — Err с текстом «плохое число: <s>» (map_err).', 'fn parse_pos(s: &str) -> Result<u32, String> {
    todo!()
}
', 'map_err превращает тип ошибки.', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_pos(\"42\"));\n    println!(\"{:?}\", parse_pos(\"-3\"));\n    println!(\"{:?}\", parse_pos(\"x\"));\n}\n", "expected": ["Ok(42)", "Err(\"плохое число: -3\")", "Err(\"плохое число: x\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-res-and-then', 8, 'rust', 'Result::and_then', 'Напишите parse_and_sqrt(s: &str) -> Result<f64, String>: разобрать f64 (ошибка «не число») и взять корень (ошибка «отрицательное» при < 0). Цепочка and_then.', 'fn parse_and_sqrt(s: &str) -> Result<f64, String> {
    todo!()
}
', 'map_err, затем and_then.', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_and_sqrt(\"16\"));\n    println!(\"{:?}\", parse_and_sqrt(\"-4\"));\n    println!(\"{:?}\", parse_and_sqrt(\"abc\"));\n}\n", "expected": ["Ok(4.0)", "Err(\"отрицательное\")", "Err(\"не число\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-res-ok', 9, 'rust', 'Result → Option', 'Напишите numbers(items: &[&str]) -> Vec<i32>: разберите все строки в i32 и оставьте только удавшиеся (filter_map с ok()).', 'fn numbers(items: &[&str]) -> Vec<i32> {
    todo!()
}
', 'filter_map(|s| s.parse().ok())', '{"driver": "fn main() {\n    println!(\"{:?}\", numbers(&[\"1\", \"x\", \"3\", \"\", \"-5\"]));\n}\n", "expected": ["[1, 3, -5]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-res-collect', 10, 'rust', 'collect в Result', 'Напишите all_numbers(items: &[&str]) -> Result<Vec<i32>, String>: все строки в числа или Err(<первая плохая строка>). Подсказка: collect умеет собирать Result<Vec<_>, _>.', 'fn all_numbers(items: &[&str]) -> Result<Vec<i32>, String> {
    todo!()
}
', 'iter().map(…).collect::<Result<Vec<_>, _>>()', '{"driver": "fn main() {\n    println!(\"{:?}\", all_numbers(&[\"1\", \"2\", \"3\"]));\n    println!(\"{:?}\", all_numbers(&[\"1\", \"x\", \"y\"]));\n    println!(\"{:?}\", all_numbers(&[]));\n}\n", "expected": ["Ok([1, 2, 3])", "Err(\"x\")", "Ok([])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-res-unwrap-default', 11, 'rust', 'unwrap_or_default', 'Напишите to_i32(s: &str) -> i32: число из строки или 0 (parse + unwrap_or_default).', 'fn to_i32(s: &str) -> i32 {
    todo!()
}
', 'unwrap_or_default берёт 0 из типа.', '{"driver": "fn main() {\n    println!(\"{} {} {}\", to_i32(\"12\"), to_i32(\"x\"), to_i32(\"\"));\n}\n", "expected": ["12 0 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-mem-swap', 12, 'rust', 'mem::swap', 'Напишите swap_values(a: &mut i32, b: &mut i32): поменять значения местами функцией std::mem::swap.', 'fn swap_values(a: &mut i32, b: &mut i32) {
    todo!()
}
', 'std::mem::swap(a, b) принимает две изменяемые ссылки.', '{"driver": "fn main() {\n    let (mut x, mut y) = (1, 2);\n    swap_values(&mut x, &mut y);\n    println!(\"{} {}\", x, y);\n}\n", "expected": ["2 1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-vec-swap', 13, 'rust', 'Vec::swap', 'Напишите swap_items(v: &mut Vec<i32>, a: usize, b: usize): поменять местами элементы с индексами a и b (метод v.swap).', 'fn swap_items(v: &mut Vec<i32>, a: usize, b: usize) {
    todo!()
}
', 'v.swap(a, b) — безопасный обмен двух элементов.', '{"driver": "fn main() {\n    let mut v = vec![1, 2, 3, 4];\n    swap_items(&mut v, 0, 3);\n    println!(\"{:?}\", v);\n}\n", "expected": ["[4, 2, 3, 1]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-mem-replace', 14, 'rust', 'mem::replace', 'Напишите set_name(name: &mut String, new: &str) -> String: заменить значение и вернуть старое (mem::replace).', 'fn set_name(name: &mut String, new: &str) -> String {
    todo!()
}
', 'std::mem::replace(name, new.to_string())', '{"driver": "fn main() {\n    let mut n = String::from(\"Аня\");\n    let old = set_name(&mut n, \"Боря\");\n    println!(\"{} {}\", old, n);\n}\n", "expected": ["Аня Боря"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-mem-take', 15, 'rust', 'mem::take', 'Напишите drain_all(v: &mut Vec<String>) -> Vec<String>: вернуть все элементы и оставить вектор пустым (mem::take).', 'fn drain_all(v: &mut Vec<String>) -> Vec<String> {
    todo!()
}
', 'std::mem::take(v)', '{"driver": "fn main() {\n    let mut v = vec![String::from(\"a\"), String::from(\"b\")];\n    let got = drain_all(&mut v);\n    println!(\"{:?} {:?}\", got, v);\n}\n", "expected": ["[\"a\", \"b\"] []"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-cmp-then', 16, 'rust', 'Сравнение по нескольким полям', 'Напишите sort_people(v: &mut Vec<(String, u32)>): отсортировать пары (имя, возраст) по возрасту по убыванию, при равных — по имени по возрастанию (cmp и then).', 'fn sort_people(v: &mut Vec<(String, u32)>) {
    todo!()
}
', 'b.1.cmp(&a.1).then(a.0.cmp(&b.0))', '{"driver": "fn main() {\n    let mut v = vec![(String::from(\"Боря\"), 30), (String::from(\"Аня\"), 30), (String::from(\"Вера\"), 25)];\n    sort_people(&mut v);\n    println!(\"{:?}\", v);\n}\n", "expected": ["[(\"Аня\", 30), (\"Боря\", 30), (\"Вера\", 25)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-cmp-reverse', 17, 'rust', 'Reverse', 'Напишите top_three(v: &[i32]) -> Vec<i32>: три наибольших по убыванию (sort_by_key с Reverse; если элементов меньше трёх — все).', 'fn top_three(v: &[i32]) -> Vec<i32> {
    todo!()
}
', 'sort_by_key(|x| Reverse(*x))', '{"driver": "fn main() {\n    println!(\"{:?}\", top_three(&[5, 1, 9, 3, 7, 7]));\n    println!(\"{:?}\", top_three(&[2]));\n}\n", "expected": ["[9, 7, 7]", "[2]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-cmp-clamp', 18, 'rust', 'clamp', 'Напишите normalize(v: &[f64]) -> Vec<f64>: ограничить каждое число диапазоном [0.0, 1.0] (метод clamp).', 'fn normalize(v: &[f64]) -> Vec<f64> {
    todo!()
}
', 'x.clamp(0.0, 1.0)', '{"driver": "fn main() {\n    println!(\"{:?}\", normalize(&[-0.5, 0.25, 1.5, 1.0]));\n}\n", "expected": ["[0.0, 0.25, 1.0, 1.0]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-cmp-total', 19, 'rust', 'Сортировка дробных', 'Напишите sort_floats(v: &mut Vec<f64>): по возрастанию, с NaN в конце (метод total_cmp).', 'fn sort_floats(v: &mut Vec<f64>) {
    todo!()
}
', 'a.total_cmp(b) задаёт полный порядок.', '{"driver": "fn main() {\n    let mut v = vec![3.5, f64::NAN, -1.0, 2.0, 0.0];\n    sort_floats(&mut v);\n    println!(\"{:?}\", v);\n}\n", "expected": ["[-1.0, 0.0, 2.0, 3.5, NaN]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-conv-from', 20, 'rust', 'From и Into', 'Структура Rgb(u8, u8, u8) объявлена. Реализуйте From<(u8, u8, u8)> for Rgb и From<u32> for Rgb (значение 0xRRGGBB), чтобы работали Rgb::from(…) и .into().', 'struct Rgb(u8, u8, u8);

impl From<(u8, u8, u8)> for Rgb {
    fn from(t: (u8, u8, u8)) -> Rgb {
        todo!()
    }
}

impl From<u32> for Rgb {
    fn from(x: u32) -> Rgb {
        todo!()
    }
}
', 'Сдвиги >> 16 и >> 8, приведение к u8 отрезает старшие биты.', '{"driver": "fn main() {\n    let a = Rgb::from((1, 2, 3));\n    let b: Rgb = 0xFF8000.into();\n    println!(\"{} {} {}\", a.0, a.1, a.2);\n    println!(\"{} {} {}\", b.0, b.1, b.2);\n}\n", "expected": ["1 2 3", "255 128 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-conv-fromstr', 21, 'rust', 'FromStr', 'Реализуйте FromStr для Point { x: i32, y: i32 }: разбор строки вида «3,-4» (Err(String), если не два числа через запятую). Тогда работает "3,-4".parse::<Point>().', 'use std::str::FromStr;

#[derive(Debug, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

impl FromStr for Point {
    type Err = String;
    fn from_str(s: &str) -> Result<Point, String> {
        todo!()
    }
}
', 'split_once('','') и parse; ? для ошибок.', '{"driver": "fn main() {\n    println!(\"{:?}\", \"3,-4\".parse::<Point>());\n    println!(\"{:?}\", \" 1 , 2 \".parse::<Point>());\n    println!(\"{:?}\", \"1;2\".parse::<Point>());\n    println!(\"{:?}\", \"a,2\".parse::<Point>());\n}\n", "expected": ["Ok(Point { x: 3, y: -4 })", "Ok(Point { x: 1, y: 2 })", "Err(\"нет запятой\")", "Err(\"плохой x\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-conv-asref', 22, 'rust', 'AsRef<str>', 'Напишите shout(s: impl AsRef<str>) -> String: строка в верхнем регистре с «!» на конце. Функция должна принимать и &str, и String.', 'fn shout(s: impl AsRef<str>) -> String {
    todo!()
}
', 's.as_ref() — получить &str из любой формы.', '{"driver": "fn main() {\n    println!(\"{}\", shout(\"привет\"));\n    println!(\"{}\", shout(String::from(\"rust\")));\n}\n", "expected": ["ПРИВЕТ!", "RUST!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-conv-tryfrom', 23, 'rust', 'TryFrom', 'Напишите to_byte(n: i32) -> Option<u8>: n как u8, если помещается (0..=255), иначе None. Используйте u8::try_from(n).ok().', 'fn to_byte(n: i32) -> Option<u8> {
    todo!()
}
', 'try_from возвращает Result; ok() превращает в Option.', '{"driver": "fn main() {\n    println!(\"{:?} {:?} {:?} {:?}\", to_byte(200), to_byte(256), to_byte(-1), to_byte(0));\n}\n", "expected": ["Some(200) None None Some(0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-iter-successors', 24, 'rust', 'successors', 'Напишите powers_of_two(limit: u64) -> Vec<u64>: степени двойки 1, 2, 4, … не больше limit (iter::successors + take_while).', 'fn powers_of_two(limit: u64) -> Vec<u64> {
    todo!()
}
', 'successors(Some(1), |&x| x.checked_mul(2)) — останавливается при переполнении.', '{"driver": "fn main() {\n    println!(\"{:?}\", powers_of_two(100));\n    println!(\"{:?}\", powers_of_two(0));\n    println!(\"{}\", powers_of_two(u64::MAX).len());\n}\n", "expected": ["[1, 2, 4, 8, 16, 32, 64]", "[]", "64"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-iter-from-fn', 25, 'rust', 'from_fn', 'Напишите collatz(n: u64) -> Vec<u64>: последовательность Коллатца из n до 1 включительно (iter::from_fn с состоянием в замыкании).', 'fn collatz(n: u64) -> Vec<u64> {
    todo!()
}
', 'Состояние хранится в Option<u64> внутри замыкания.', '{"driver": "fn main() {\n    println!(\"{:?}\", collatz(6));\n    println!(\"{:?}\", collatz(1));\n    println!(\"{}\", collatz(27).len());\n}\n", "expected": ["[6, 3, 10, 5, 16, 8, 4, 2, 1]", "[1]", "112"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-iter-chain-zip', 26, 'rust', 'chain и zip', 'Напишите interleave(a: &[i32], b: &[i32]) -> Vec<i32>: чередование элементов a и b (a0, b0, a1, b1, …), хвост более длинного добавляется в конец.', 'fn interleave(a: &[i32], b: &[i32]) -> Vec<i32> {
    todo!()
}
', 'min длин, цикл по общей части и хвост.', '{"driver": "fn main() {\n    println!(\"{:?}\", interleave(&[1, 2, 3], &[10, 20]));\n    println!(\"{:?}\", interleave(&[], &[5]));\n    println!(\"{:?}\", interleave(&[1], &[2]));\n}\n", "expected": ["[1, 10, 2, 20, 3]", "[5]", "[1, 2]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-iter-cycle', 27, 'rust', 'cycle', 'Напишите repeat_to(v: &[i32], n: usize) -> Vec<i32>: первые n элементов бесконечного повторения v (cycle + take); для пустого v — пустой вектор.', 'fn repeat_to(v: &[i32], n: usize) -> Vec<i32> {
    todo!()
}
', 'cycle() на пустом срезе даёт пустой итератор.', '{"driver": "fn main() {\n    println!(\"{:?}\", repeat_to(&[1, 2, 3], 7));\n    println!(\"{:?}\", repeat_to(&[], 4));\n}\n", "expected": ["[1, 2, 3, 1, 2, 3, 1]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-iter-fold', 28, 'rust', 'fold', 'Напишите digits_to_num(d: &[u8]) -> u64: число из цифр (d = [1, 2, 3] → 123) через fold.', 'fn digits_to_num(d: &[u8]) -> u64 {
    todo!()
}
', 'acc * 10 + цифра.', '{"driver": "fn main() {\n    println!(\"{}\", digits_to_num(&[1, 2, 3]));\n    println!(\"{}\", digits_to_num(&[]));\n    println!(\"{}\", digits_to_num(&[9, 9, 9, 9, 9, 9, 9, 9, 9, 9]));\n}\n", "expected": ["123", "0", "9999999999"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 24, 'r24-iter-minmax', 29, 'rust', 'min_by_key и max_by', 'Напишите shortest_longest(words: &[&str]) -> Option<(String, String)>: самое короткое и самое длинное слова (по числу символов; при равенстве — первое для короткого и последнее для длинного, как делают min_by_key и max_by_key). Для пустого — None.', 'fn shortest_longest(words: &[&str]) -> Option<(String, String)> {
    todo!()
}
', 'min_by_key и max_by_key.', '{"driver": "fn main() {\n    println!(\"{:?}\", shortest_longest(&[\"aa\", \"b\", \"cc\", \"ddd\", \"eee\"]));\n    println!(\"{:?}\", shortest_longest(&[]));\n}\n", "expected": ["Some((\"b\", \"eee\"))", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-swap-remove', 0, 'rust', 'swap_remove', 'Напишите remove_all_even(v: &mut Vec<i32>): удалить все чётные числа за линейное время без сохранения порядка, с помощью swap_remove. (Проверка — по сумме и количеству оставшихся.)', 'fn remove_all_even(v: &mut Vec<i32>) {
    todo!()
}
', 'Не увеличивайте i после swap_remove — на месте уже новый элемент.', '{"driver": "fn main() {\n    let mut v: Vec<i32> = (1..=10).collect();\n    remove_all_even(&mut v);\n    v.sort();\n    println!(\"{:?}\", v);\n    let mut big: Vec<i32> = (0..400000).collect();\n    remove_all_even(&mut big);\n    println!(\"{} {}\", big.len(), big.iter().map(|&x| x as i64).sum::<i64>());\n}\n", "expected": ["[1, 3, 5, 7, 9]", "200000 40000000000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-split-off', 1, 'rust', 'split_off', 'Напишите split_at_value(v: &mut Vec<i32>, x: i32) -> Vec<i32>: отрежьте от v хвост начиная с первого элемента, равного x (если x нет — вернуть пустой вектор), и верните его.', 'fn split_at_value(v: &mut Vec<i32>, x: i32) -> Vec<i32> {
    todo!()
}
', 'v.split_off(i) оставляет в v первые i элементов.', '{"driver": "fn main() {\n    let mut v = vec![1, 2, 3, 4, 5];\n    let t = split_at_value(&mut v, 3);\n    println!(\"{:?} {:?}\", v, t);\n    let t2 = split_at_value(&mut v, 9);\n    println!(\"{:?} {:?}\", v, t2);\n}\n", "expected": ["[1, 2] [3, 4, 5]", "[1, 2] []"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-dedup-by-key', 2, 'rust', 'dedup_by_key', 'Напишите unique_by_len(words: &mut Vec<String>): оставить только первое слово из каждой подряд идущей группы слов одной длины в символах (dedup_by_key).', 'fn unique_by_len(words: &mut Vec<String>) {
    todo!()
}
', 'dedup_by_key убирает соседние элементы с одинаковым ключом.', '{"driver": "fn main() {\n    let mut w: Vec<String> = [\"aa\", \"bb\", \"ccc\", \"d\", \"e\", \"ff\"].iter().map(|s| s.to_string()).collect();\n    unique_by_len(&mut w);\n    println!(\"{:?}\", w);\n}\n", "expected": ["[\"aa\", \"ccc\", \"d\", \"ff\"]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-drain-filter', 3, 'rust', 'Вынуть по условию', 'Напишите take_evens(v: &mut Vec<i32>) -> Vec<i32>: вернуть все чётные (в исходном порядке) и удалить их из v. Используйте retain и накопление в отдельный вектор.', 'fn take_evens(v: &mut Vec<i32>) -> Vec<i32> {
    todo!()
}
', 'retain вызывает замыкание по порядку — в нём можно копить.', '{"driver": "fn main() {\n    let mut v = vec![1, 2, 3, 4, 5, 6];\n    let e = take_evens(&mut v);\n    println!(\"{:?} {:?}\", e, v);\n}\n", "expected": ["[2, 4, 6] [1, 3, 5]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-rotate', 4, 'rust', 'Поворот среза', 'Напишите rotate(v: &mut [i32], k: usize): циклический сдвиг вправо на k позиций на месте (rotate_right, k может быть больше длины).', 'fn rotate(v: &mut [i32], k: usize) {
    todo!()
}
', 'rotate_right паникует при k > len, поэтому берите k % len.', '{"driver": "fn main() {\n    let mut v = [1, 2, 3, 4, 5];\n    rotate(&mut v, 2);\n    println!(\"{:?}\", v);\n    rotate(&mut v, 12);\n    println!(\"{:?}\", v);\n    let mut e: [i32; 0] = [];\n    rotate(&mut e, 3);\n}\n", "expected": ["[4, 5, 1, 2, 3]", "[2, 3, 4, 5, 1]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-windows-max', 5, 'rust', 'Максимум в окне', 'Напишите window_max(v: &[i32], k: usize) -> Vec<i32>: максимум в каждом окне из k подряд идущих элементов (k > 0; если k > len — пустой). За линейное время (VecDeque хранит индексы кандидатов), на 200000 элементов.', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn window_max(v: &[i32], k: usize) -> Vec<i32> {
    todo!()
}
', 'Очередь убывающих значений: хвост выбрасываем, если он не больше нового.', '{"driver": "fn main() {\n    println!(\"{:?}\", window_max(&[1, 3, -1, -3, 5, 3, 6, 7], 3));\n    println!(\"{:?}\", window_max(&[4], 1));\n    println!(\"{:?}\", window_max(&[1, 2], 5));\n    let big: Vec<i32> = (0..200000i64).map(|x| ((x * 7919) % 10007) as i32).collect();\n    let r = window_max(&big, 1000);\n    println!(\"{} {}\", r.len(), r.iter().map(|&x| x as i64).sum::<i64>());\n}\n", "expected": ["[3, 3, 5, 5, 6, 7]", "[4]", "[]", "199001 1990276864"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-josephus-deque', 6, 'rust', 'Считалка на колоде', 'Напишите last_standing(names: &[&str], k: usize) -> String: по кругу выбывает каждый k-й, вернуть имя последнего. Используйте VecDeque и rotate_left.', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn last_standing(names: &[&str], k: usize) -> String {
    todo!()
}
', 'q.rotate_left(k - 1), затем pop_front.', '{"driver": "fn main() {\n    println!(\"{}\", last_standing(&[\"А\", \"Б\", \"В\", \"Г\", \"Д\"], 2));\n    println!(\"{}\", last_standing(&[\"Один\"], 7));\n    println!(\"{}\", last_standing(&[\"А\", \"Б\", \"В\"], 3));\n}\n", "expected": ["В", "Один", "Б"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-round-robin', 7, 'rust', 'Круговой планировщик', 'Напишите round_robin(tasks: &[(&str, u32)], quantum: u32) -> Vec<String>: каждой задаче по очереди выделяют quantum единиц; порядок завершения (имена) вернуть списком. VecDeque.', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn round_robin(tasks: &[(&str, u32)], quantum: u32) -> Vec<String> {
    todo!()
}
', 'Не закончила — в конец очереди с остатком.', '{"driver": "fn main() {\n    println!(\"{:?}\", round_robin(&[(\"a\", 5), (\"b\", 2), (\"c\", 7)], 3));\n    println!(\"{:?}\", round_robin(&[], 3));\n}\n", "expected": ["[\"b\", \"a\", \"c\"]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-hash-two-sets', 8, 'rust', 'Общие элементы', 'Напишите common_sorted(a: &[i32], b: &[i32]) -> Vec<i32>: пересечение a и b без повторов по возрастанию (HashSet).', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn common_sorted(a: &[i32], b: &[i32]) -> Vec<i32> {
    todo!()
}
', 'Два множества и intersection.', '{"driver": "fn main() {\n    println!(\"{:?}\", common_sorted(&[1, 2, 2, 3, 4], &[2, 4, 4, 6]));\n    println!(\"{:?}\", common_sorted(&[], &[1]));\n}\n", "expected": ["[2, 4]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-subset', 9, 'rust', 'Подмножество', 'Напишите can_make(note: &str, magazine: &str) -> bool: хватит ли букв из magazine, чтобы вырезать note (каждая буква один раз; сравнивать как есть, пробелы игнорировать). HashMap счётчиков.', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn can_make(note: &str, magazine: &str) -> bool {
    todo!()
}
', 'Счётчики букв магазина уменьшаются при вырезании.', '{"driver": "fn main() {\n    println!(\"{}\", can_make(\"aab\", \"baa x\"));\n    println!(\"{}\", can_make(\"aaa\", \"aab\"));\n    println!(\"{}\", can_make(\"\", \"\"));\n}\n", "expected": ["true", "false", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-btree-ranks', 10, 'rust', 'Ранги по возрастанию', 'Напишите ranks(v: &[i32]) -> Vec<usize>: для каждого элемента — его номер (с 0) среди различных значений по возрастанию (сжатие координат): [10, 5, 10, 7] → [2, 0, 2, 1]. Используйте BTreeSet.', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn ranks(v: &[i32]) -> Vec<usize> {
    todo!()
}
', 'BTreeSet даёт отсортированные уникальные значения; binary_search — номер.', '{"driver": "fn main() {\n    println!(\"{:?}\", ranks(&[10, 5, 10, 7]));\n    println!(\"{:?}\", ranks(&[]));\n    println!(\"{:?}\", ranks(&[3, 3, 3]));\n}\n", "expected": ["[2, 0, 2, 1]", "[]", "[0, 0, 0]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-btree-range', 11, 'rust', 'Ближайшие значения', 'Напишите nearest(sorted: &BTreeSet<i32>, x: i32) -> (Option<i32>, Option<i32>): наибольшее значение не больше x и наименьшее не меньше x (методы range).', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn nearest(sorted: &BTreeSet<i32>, x: i32) -> (Option<i32>, Option<i32>) {
    todo!()
}
', 'range(..=x).next_back() и range(x..).next()', '{"driver": "fn main() {\n    let s: BTreeSet<i32> = [10, 20, 30, 40].into_iter().collect();\n    println!(\"{:?}\", nearest(&s, 25));\n    println!(\"{:?}\", nearest(&s, 5));\n    println!(\"{:?}\", nearest(&s, 50));\n    println!(\"{:?}\", nearest(&s, 30));\n}\n", "expected": ["(Some(20), Some(30))", "(None, Some(10))", "(Some(40), None)", "(Some(30), Some(30))"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-btree-intervals', 12, 'rust', 'События по порядку', 'Напишите timeline(events: &[(u32, &str)]) -> Vec<String>: события (время, название) выведите в порядке времени; при одинаковом времени названия через «/» в порядке добавления. Строки вида «5: a/b». BTreeMap.', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn timeline(events: &[(u32, &str)]) -> Vec<String> {
    todo!()
}
', 'entry(t).or_default().push(n); BTreeMap обходит по возрастанию.', '{"driver": "fn main() {\n    for l in timeline(&[(5, \"a\"), (2, \"b\"), (5, \"c\"), (9, \"d\")]) {\n        println!(\"{}\", l);\n    }\n}\n", "expected": ["2: b", "5: a/c", "9: d"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-btree-pop', 13, 'rust', 'Приоритетные задачи', 'Напишите process(tasks: &[(u32, &str)]) -> Vec<String>: задачи (приоритет, имя) выполняются от наименьшего приоритета (число) к наибольшему; при равных — в порядке добавления. Используйте BTreeMap<u32, VecDeque<String>> и pop_first.', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn process(tasks: &[(u32, &str)]) -> Vec<String> {
    todo!()
}
', 'pop_first даёт пару с наименьшим ключом.', '{"driver": "fn main() {\n    println!(\"{:?}\", process(&[(3, \"c\"), (1, \"a\"), (3, \"d\"), (2, \"b\"), (1, \"e\")]));\n    println!(\"{:?}\", process(&[]));\n}\n", "expected": ["[\"a\", \"e\", \"b\", \"c\", \"d\"]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-heap-topk', 14, 'rust', 'Топ-k кучей', 'Напишите top_k(v: &[i32], k: usize) -> Vec<i32>: k наибольших по убыванию, используя кучу-минимум размера k (BinaryHeap<Reverse<i32>>) — для 300000 элементов и k = 5.', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn top_k(v: &[i32], k: usize) -> Vec<i32> {
    todo!()
}
', 'Если в куче больше k — удаляем наименьшее.', '{"driver": "fn main() {\n    println!(\"{:?}\", top_k(&[5, 1, 9, 3, 7, 7], 3));\n    println!(\"{:?}\", top_k(&[2], 5));\n    println!(\"{:?}\", top_k(&[2], 0));\n    let big: Vec<i32> = (0..300000i64).map(|x| ((x * 7919) % 100003) as i32).collect();\n    println!(\"{:?}\", top_k(&big, 5));\n}\n", "expected": ["[9, 7, 7]", "[2]", "[]", "[100002, 100002, 100002, 100001, 100001]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-heap-merge', 15, 'rust', 'Слияние k списков', 'Напишите merge_k(lists: &[Vec<i32>]) -> Vec<i32>: слить отсортированные списки в один отсортированный, используя BinaryHeap<Reverse<(i32, usize, usize)>> (значение, номер списка, индекс).', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn merge_k(lists: &[Vec<i32>]) -> Vec<i32> {
    todo!()
}
', 'В куче всегда по одному кандидату из каждого списка.', '{"driver": "fn main() {\n    println!(\"{:?}\", merge_k(&[vec![1, 4, 7], vec![2, 5], vec![], vec![3, 6, 9]]));\n    println!(\"{:?}\", merge_k(&[]));\n}\n", "expected": ["[1, 2, 3, 4, 5, 6, 7, 9]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-heap-median', 16, 'rust', 'Бегущая медиана', 'Напишите running_median(v: &[i32]) -> Vec<f64>: после каждого элемента — медиана всех прочитанных (две кучи: нижняя — максимум, верхняя — минимум).', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn running_median(v: &[i32]) -> Vec<f64> {
    todo!()
}
', 'Размеры куч отличаются не больше чем на один.', '{"driver": "fn main() {\n    println!(\"{:?}\", running_median(&[5, 15, 1, 3]));\n    println!(\"{:?}\", running_median(&[2]));\n    println!(\"{:?}\", running_median(&[]));\n}\n", "expected": ["[5.0, 10.0, 5.0, 4.0]", "[2.0]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-dijkstra', 17, 'rust', 'Дейкстра на куче', 'Напишите dijkstra(n: usize, edges: &[(usize, usize, u32)], src: usize) -> Vec<Option<u32>>: кратчайшие расстояния от src в ориентированном графе из n вершин; недостижимые — None. Куча-минимум; граф на 20000 вершин.', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn dijkstra(n: usize, edges: &[(usize, usize, u32)], src: usize) -> Vec<Option<u32>> {
    todo!()
}
', 'Пропускайте устаревшие записи в куче: d > dist[u].', '{"driver": "fn main() {\n    println!(\"{:?}\", dijkstra(5, &[(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5)], 0));\n    let n = 20000;\n    let edges: Vec<(usize, usize, u32)> = (0..n - 1).map(|i| (i, i + 1, 1)).chain((0..n - 2).map(|i| (i, i + 2, 3))).collect();\n    let d = dijkstra(n, &edges, 0);\n    println!(\"{:?} {:?}\", d[n - 1], d[1]);\n}\n", "expected": ["[Some(0), Some(3), Some(1), Some(4), None]", "Some(19999) Some(1)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-deque-palindrome', 18, 'rust', 'Палиндром колодой', 'Напишите is_pal(s: &str) -> bool: палиндром ли строка (только буквы и цифры, без учёта регистра), сравнивая символы с обоих концов VecDeque.', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn is_pal(s: &str) -> bool {
    todo!()
}
', 'pop_front и pop_back сравниваем парами.', '{"driver": "fn main() {\n    println!(\"{}\", is_pal(\"А роза упала на лапу Азора\"));\n    println!(\"{}\", is_pal(\"Rust\"));\n    println!(\"{}\", is_pal(\"\"));\n    println!(\"{}\", is_pal(\"A man, a plan, a canal: Panama\"));\n}\n", "expected": ["true", "false", "true", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-lru', 19, 'rust', 'Мини-LRU', 'Структура Lru { cap: usize, order: VecDeque<String>, map: HashMap<String, i32> }. Реализуйте new(cap), get(&mut self, k: &str) -> Option<i32> (обращение делает ключ самым свежим) и put(&mut self, k: &str, v: i32) (обновление ключа тоже делает его свежим; при переполнении удаляется самый старый).', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

struct Lru {
    cap: usize,
    order: VecDeque<String>,
    map: HashMap<String, i32>,
}

impl Lru {
    fn new(cap: usize) -> Lru {
        todo!()
    }
    fn touch(&mut self, k: &str) {
        todo!()
    }
    fn get(&mut self, k: &str) -> Option<i32> {
        todo!()
    }
    fn put(&mut self, k: &str, v: i32) {
        todo!()
    }
}
', 'touch переносит ключ в конец порядка; самый старый — в начале.', '{"driver": "fn main() {\n    let mut c = Lru::new(2);\n    c.put(\"a\", 1);\n    c.put(\"b\", 2);\n    println!(\"{:?}\", c.get(\"a\"));\n    c.put(\"c\", 3);\n    println!(\"{:?} {:?} {:?}\", c.get(\"a\"), c.get(\"b\"), c.get(\"c\"));\n}\n", "expected": ["Some(1)", "Some(1) None Some(3)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-hash-pair-sum', 20, 'rust', 'Пары с суммой', 'Напишите count_pairs(v: &[i32], target: i32) -> usize: сколько пар индексов i < j имеют v[i] + v[j] = target (HashMap частот, один проход) — на 200000 элементов.', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn count_pairs(v: &[i32], target: i32) -> usize {
    todo!()
}
', 'Перед добавлением x в карту ищем его пару.', '{"driver": "fn main() {\n    println!(\"{}\", count_pairs(&[1, 5, 7, -1, 5], 6));\n    println!(\"{}\", count_pairs(&[1, 1, 1], 2));\n    println!(\"{}\", count_pairs(&[], 0));\n    let big: Vec<i32> = (0..200000).map(|x| x % 1000).collect();\n    println!(\"{}\", count_pairs(&big, 999));\n}\n", "expected": ["3", "3", "0", "20000000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-lcp', 21, 'rust', 'Общий префикс', 'Напишите group_by_first(words: &[&str]) -> BTreeMap<char, Vec<String>>: слова по первой букве (в нижнем регистре); пустые строки пропускаются; внутри групп — по возрастанию.', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn group_by_first(words: &[&str]) -> BTreeMap<char, Vec<String>> {
    todo!()
}
', 'entry(буква).or_default().push(…); потом sort.', '{"driver": "fn main() {\n    println!(\"{:?}\", group_by_first(&[\"яблоко\", \"Арбуз\", \"ананас\", \"\", \"Ёж\", \"ежевика\"]));\n}\n", "expected": ["{''а'': [\"Арбуз\", \"ананас\"], ''е'': [\"ежевика\"], ''я'': [\"яблоко\"], ''ё'': [\"Ёж\"]}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-histogram-top', 22, 'rust', 'Самые частые', 'Напишите most_common(v: &[i32]) -> Option<i32>: самое частое значение; при равенстве — наименьшее. Для пустого — None. HashMap и один проход по карте.', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn most_common(v: &[i32]) -> Option<i32> {
    todo!()
}
', 'max_by с тем же сравнением по ключу в обратном порядке.', '{"driver": "fn main() {\n    println!(\"{:?}\", most_common(&[1, 2, 2, 3, 3]));\n    println!(\"{:?}\", most_common(&[5]));\n    println!(\"{:?}\", most_common(&[]));\n}\n", "expected": ["Some(2)", "Some(5)", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-vec-capacity', 23, 'rust', 'Не перевыделять', 'Напишите squares(n: usize) -> Vec<u64>: квадраты 0…n−1, предварительно зарезервировав память (with_capacity) — после заполнения capacity() должна быть равна n.', 'fn squares(n: usize) -> Vec<u64> {
    todo!()
}
', 'Vec::with_capacity(n)', '{"driver": "fn main() {\n    let v = squares(5);\n    println!(\"{:?} {}\", v, v.capacity() == 5);\n    let w = squares(100000);\n    println!(\"{} {}\", w.len(), w.capacity() == 100000);\n}\n", "expected": ["[0, 1, 4, 9, 16] true", "100000 true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-concat-join', 24, 'rust', 'concat и join', 'Напишите flatten_join(rows: &[Vec<&str>]) -> String: строки каждой подгруппы склеить пробелами, группы разделить « | » (метод join у среза).', 'fn flatten_join(rows: &[Vec<&str>]) -> String {
    todo!()
}
', 'Два join: внутренний и внешний.', '{"driver": "fn main() {\n    println!(\"{}\", flatten_join(&[vec![\"a\", \"b\"], vec![\"c\"], vec![]]));\n    println!(\"[{}]\", flatten_join(&[]));\n}\n", "expected": ["a b | c |", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-binary-search-by', 25, 'rust', 'binary_search_by', 'Напишите find_user(users: &[(u32, &str)], id: u32) -> Option<&str>: users отсортирован по id; найти имя бинарным поиском (binary_search_by_key).', 'fn find_user<''a>(users: &[(u32, &''a str)], id: u32) -> Option<&''a str> {
    todo!()
}
', 'binary_search_by_key(&id, |&(i, _)| i)', '{"driver": "fn main() {\n    let u = [(1, \"аня\"), (4, \"боря\"), (9, \"вера\")];\n    println!(\"{:?} {:?} {:?}\", find_user(&u, 4), find_user(&u, 5), find_user(&[], 1));\n}\n", "expected": ["Some(\"боря\") None None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-vec-of-vec-sort', 26, 'rust', 'Сортировка строк матрицы', 'Напишите sort_rows(m: &mut Vec<Vec<i32>>): отсортировать каждую строку по возрастанию, а затем строки между собой лексикографически.', 'fn sort_rows(m: &mut Vec<Vec<i32>>) {
    todo!()
}
', 'Vec<Vec<i32>> сам умеет сравниваться лексикографически.', '{"driver": "fn main() {\n    let mut m = vec![vec![3, 1, 2], vec![0, 9], vec![1, 0, 5], vec![]];\n    sort_rows(&mut m);\n    println!(\"{:?}\", m);\n}\n", "expected": ["[[], [0, 1, 5], [0, 9], [1, 2, 3]]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-set-visited', 27, 'rust', 'Посещённые состояния', 'Напишите steps_to_cycle(start: u32) -> usize: последовательность x → (x·x + 1) mod 1000; сколько шагов до первого повтора значения (HashSet посещённых; start считается посещённым в момент 0).', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn steps_to_cycle(start: u32) -> usize {
    todo!()
}
', 'insert возвращает false, когда значение уже было.', '{"driver": "fn main() {\n    println!(\"{}\", steps_to_cycle(0));\n    println!(\"{}\", steps_to_cycle(1));\n    println!(\"{}\", steps_to_cycle(500));\n}\n", "expected": ["10", "9", "10"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-reverse-heap-sorted', 28, 'rust', 'Сортировка кучей', 'Напишите heap_sort(v: &[i32]) -> Vec<i32>: отсортируйте по возрастанию через BinaryHeap (from + into_sorted_vec).', 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cmp::Reverse;

fn heap_sort(v: &[i32]) -> Vec<i32> {
    todo!()
}
', 'into_sorted_vec возвращает по возрастанию.', '{"driver": "fn main() {\n    println!(\"{:?}\", heap_sort(&[5, 2, 9, 1, 5, 6]));\n    println!(\"{:?}\", heap_sort(&[]));\n    let big: Vec<i32> = (0..100000i64).map(|x| ((x * 31337) % 10007) as i32).collect();\n    let s = heap_sort(&big);\n    println!(\"{} {}\", s[0], s[s.len() - 1]);\n}\n", "expected": ["[1, 2, 5, 5, 6, 9]", "[]", "0 10006"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 25, 'r25-linked-list-note', 29, 'rust', 'Когда список, а когда вектор', 'Напишите move_front(v: &mut Vec<i32>, i: usize): перенести элемент с индексом i в начало вектора, сохранив порядок остальных (remove + insert, либо rotate_right на срезе 0..=i).', 'fn move_front(v: &mut Vec<i32>, i: usize) {
    todo!()
}
', 'v[..=i].rotate_right(1) без копирования всего вектора.', '{"driver": "fn main() {\n    let mut v = vec![1, 2, 3, 4, 5];\n    move_front(&mut v, 3);\n    println!(\"{:?}\", v);\n    move_front(&mut v, 0);\n    println!(\"{:?}\", v);\n}\n", "expected": ["[4, 1, 2, 3, 5]", "[4, 1, 2, 3, 5]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-char-class', 0, 'rust', 'Классы символов', 'Напишите classify(s: &str) -> (usize, usize, usize, usize): число букв, цифр, пробельных и прочих символов (по правилам Unicode: is_alphabetic, is_numeric, is_whitespace).', 'fn classify(s: &str) -> (usize, usize, usize, usize) {
    todo!()
}
', 'Четыре счётчика и цепочка if / else if.', '{"driver": "fn main() {\n    println!(\"{:?}\", classify(\"Привет, мир 2026!\"));\n    println!(\"{:?}\", classify(\"\"));\n    println!(\"{:?}\", classify(\"a1 ٣\"));\n}\n", "expected": ["(9, 4, 2, 2)", "(0, 0, 0, 0)", "(1, 2, 1, 0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-hex-digits', 1, 'rust', 'Цифры в разных системах', 'Напишите hex_sum(s: &str) -> u32: сумма значений шестнадцатеричных цифр строки (to_digit(16)); не-hex-символы пропускаются.', 'fn hex_sum(s: &str) -> u32 {
    todo!()
}
', 'filter_map(|c| c.to_digit(16))', '{"driver": "fn main() {\n    println!(\"{}\", hex_sum(\"ff\"));\n    println!(\"{}\", hex_sum(\"1A z 0\"));\n    println!(\"{}\", hex_sum(\"\"));\n}\n", "expected": ["30", "11", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-from-digit', 2, 'rust', 'Число в строку любой системы', 'Напишите to_radix(n: u32, radix: u32) -> String: запись n в системе счисления radix (2…36) строчными буквами; для 0 — «0». Используйте char::from_digit.', 'fn to_radix(n: u32, radix: u32) -> String {
    todo!()
}
', 'Остатки от деления — цифры в обратном порядке.', '{"driver": "fn main() {\n    println!(\"{} {} {}\", to_radix(255, 16), to_radix(5, 2), to_radix(0, 8));\n    println!(\"{}\", to_radix(123456, 36));\n    println!(\"{}\", to_radix(u32::MAX, 2));\n}\n", "expected": ["ff 101 0", "2n9c", "11111111111111111111111111111111"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-split-multi', 3, 'rust', 'Разбить по нескольким разделителям', 'Напишите tokens(s: &str) -> Vec<String>: слова, разделённые любым из символов «,», «;», «:» или пробельным; пустые куски пропускаются.', 'fn tokens(s: &str) -> Vec<String> {
    todo!()
}
', 'split принимает замыкание-шаблон.', '{"driver": "fn main() {\n    println!(\"{:?}\", tokens(\"a, b;c:d  e,,f\"));\n    println!(\"{:?}\", tokens(\"\"));\n    println!(\"{:?}\", tokens(\";;;\"));\n}\n", "expected": ["[\"a\", \"b\", \"c\", \"d\", \"e\", \"f\"]", "[]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-splitn', 4, 'rust', 'splitn', 'Напишите parse_cmd(line: &str) -> (String, String): команда и остальная строка. Делить по первому пробелу (splitn(2, '' '')); если пробела нет — вторая часть пуста. Остаток не триммить.', 'fn parse_cmd(line: &str) -> (String, String) {
    todo!()
}
', 'splitn(2, '' '') не делит остаток.', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_cmd(\"echo hello  world\"));\n    println!(\"{:?}\", parse_cmd(\"quit\"));\n    println!(\"{:?}\", parse_cmd(\"\"));\n}\n", "expected": ["(\"echo\", \"hello  world\")", "(\"quit\", \"\")", "(\"\", \"\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-strip-prefix', 5, 'rust', 'strip_prefix', 'Напишите command(line: &str) -> String: «ECHO <текст>» → текст; «UP <текст>» → текст в верхнем регистре; иначе «неизвестная команда». Используйте strip_prefix.', 'fn command(line: &str) -> String {
    todo!()
}
', 'strip_prefix возвращает Option<&str>.', '{"driver": "fn main() {\n    println!(\"{}\", command(\"ECHO привет\"));\n    println!(\"{}\", command(\"UP привет\"));\n    println!(\"{}\", command(\"DOWN x\"));\n    println!(\"[{}]\", command(\"ECHO \"));\n}\n", "expected": ["привет", "ПРИВЕТ", "неизвестная команда", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-split-inclusive', 6, 'rust', 'Предложения', 'Напишите sentences(s: &str) -> Vec<String>: разбейте текст на предложения, оставляя знак конца (. ! ?) в конце каждого, и уберите пробелы по краям. split_inclusive с замыканием.', 'fn sentences(s: &str) -> Vec<String> {
    todo!()
}
', 'split_inclusive оставляет разделитель в куске.', '{"driver": "fn main() {\n    println!(\"{:?}\", sentences(\"Привет. Как дела? Отлично!\"));\n    println!(\"{:?}\", sentences(\"без точки\"));\n    println!(\"{:?}\", sentences(\"\"));\n}\n", "expected": ["[\"Привет.\", \"Как дела?\", \"Отлично!\"]", "[\"без точки\"]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-trim-matches', 7, 'rust', 'Убрать обрамление', 'Напишите unquote(s: &str) -> String: убрать с обоих концов любые кавычки «"» и «''» и пробелы (trim_matches с замыканием).', 'fn unquote(s: &str) -> String {
    todo!()
}
', 'trim_matches(|c| …) режет с обоих концов.', '{"driver": "fn main() {\n    println!(\"[{}]\", unquote(\"  \\\"привет\\\"  \"));\n    println!(\"[{}]\", unquote(\"''a b''\"));\n    println!(\"[{}]\", unquote(\"\\\"\\\"\"));\n}\n", "expected": ["[привет]", "[a b]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-match-indices', 8, 'rust', 'Позиции вхождений', 'Напишите positions(text: &str, pat: &str) -> Vec<usize>: байтовые позиции всех (непересекающихся) вхождений pat (match_indices); pat не пуст.', 'fn positions(text: &str, pat: &str) -> Vec<usize> {
    todo!()
}
', 'match_indices возвращает (позиция, совпадение).', '{"driver": "fn main() {\n    println!(\"{:?}\", positions(\"abcabcab\", \"ab\"));\n    println!(\"{:?}\", positions(\"привет привет\", \"ив\"));\n    println!(\"{:?}\", positions(\"aaaa\", \"aa\"));\n}\n", "expected": ["[0, 3, 6]", "[4, 17]", "[0, 2]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-rfind-ext', 9, 'rust', 'Расширение файла', 'Напишите extension(name: &str) -> Option<&str>: расширение после последней точки; None, если точки нет, точка в начале (скрытый файл «.bashrc») или в конце.', 'fn extension(name: &str) -> Option<&str> {
    todo!()
}
', 'rfind(''.'') и срез после точки.', '{"driver": "fn main() {\n    println!(\"{:?}\", extension(\"archive.tar.gz\"));\n    println!(\"{:?}\", extension(\"README\"));\n    println!(\"{:?}\", extension(\".bashrc\"));\n    println!(\"{:?}\", extension(\"file.\"));\n}\n", "expected": ["Some(\"gz\")", "None", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-string-edit', 10, 'rust', 'Правки на месте', 'Напишите censor(s: &mut String, bad: &str): заменить первое вхождение bad звёздочками той же длины в символах (replace_range) — если bad нет, ничего не менять.', 'fn censor(s: &mut String, bad: &str) {
    todo!()
}
', 'find даёт байтовый индекс; диапазон — i..i + bad.len().', '{"driver": "fn main() {\n    let mut s = String::from(\"это плохое слово\");\n    censor(&mut s, \"плохое\");\n    println!(\"{}\", s);\n    censor(&mut s, \"нет\");\n    println!(\"{}\", s);\n}\n", "expected": ["это ****** слово", "это ****** слово"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-retain-clean', 11, 'rust', 'Оставить только буквы', 'Напишите letters_only(s: &mut String): оставьте в строке только буквы (retain + is_alphabetic).', 'fn letters_only(s: &mut String) {
    todo!()
}
', 's.retain(|c| c.is_alphabetic())', '{"driver": "fn main() {\n    let mut s = String::from(\"a1б2 в!3\");\n    letters_only(&mut s);\n    println!(\"{}\", s);\n}\n", "expected": ["aбв"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-truncate-char', 12, 'rust', 'Обрезать по символам', 'Напишите truncate_chars(s: &str, n: usize) -> String: первые n символов; если строка длиннее, в конце «…». (не байтов; не резать посреди символа).', 'fn truncate_chars(s: &str, n: usize) -> String {
    todo!()
}
', 'chars().take(n).collect::<String>()', '{"driver": "fn main() {\n    println!(\"{}\", truncate_chars(\"привет, мир\", 6));\n    println!(\"{}\", truncate_chars(\"мир\", 6));\n    println!(\"{}\", truncate_chars(\"😀😀😀😀\", 2));\n    println!(\"[{}]\", truncate_chars(\"\", 3));\n}\n", "expected": ["привет…", "мир", "😀😀…", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-fmt-table', 13, 'rust', 'Таблица', 'Напишите table(rows: &[(&str, f64)]) -> Vec<String>: строки «<имя, ширина по самому длинному> | <число вправо в поле 8 с двумя знаками>»; имя — по левому краю.', 'fn table(rows: &[(&str, f64)]) -> Vec<String> {
    todo!()
}
', '{:<w$} и {:>8.2}', '{"driver": "fn main() {\n    for l in table(&[(\"яблоко\", 3.5), (\"груша\", 12.349), (\"слива\", 100.0)]) {\n        println!(\"{}\", l);\n    }\n}\n", "expected": ["яблоко |     3.50", "груша  |    12.35", "слива  |   100.00"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-fmt-radix', 14, 'rust', 'Системы счисления форматом', 'Напишите formats(n: u32) -> Vec<String>: n в десятичной, шестнадцатеричной (с префиксом 0x, 4 цифры с нулями), двоичной (8 цифр с нулями) и восьмеричной системах: для 255 → ["255", "0x00ff", "11111111", "377"].', 'fn formats(n: u32) -> Vec<String> {
    todo!()
}
', '{:#06x}, {:08b}, {:o}', '{"driver": "fn main() {\n    println!(\"{:?}\", formats(255));\n    println!(\"{:?}\", formats(5));\n}\n", "expected": ["[\"255\", \"0x00ff\", \"11111111\", \"377\"]", "[\"5\", \"0x0005\", \"00000101\", \"5\"]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-fmt-sign', 15, 'rust', 'Знак и точность', 'Напишите signed(x: f64) -> String: число с явным знаком и двумя знаками после запятой, выровненное по центру в поле 9 символов с заполнителем «.»: signed(3.14159) = «..+3.14..».', 'fn signed(x: f64) -> String {
    todo!()
}
', '{:.^+9.2} — заполнитель «.», центр, знак, ширина 9, точность 2.', '{"driver": "fn main() {\n    println!(\"{}\", signed(3.14159));\n    println!(\"{}\", signed(-0.5));\n    println!(\"{}\", signed(100.0));\n}\n", "expected": ["..+3.14..", "..-0.50..", ".+100.00."]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-fmt-dynamic', 16, 'rust', 'Ширина из аргумента', 'Напишите pad_left(s: &str, width: usize, fill: char) -> String: выровняйте s вправо до ширины width в символах, добавляя слева символ fill (формат не принимает заполнитель из переменной — добавьте его вручную). Если s не короче width — вернуть как есть.', 'fn pad_left(s: &str, width: usize, fill: char) -> String {
    todo!()
}
', 'Количество заполнителей — width - n.', '{"driver": "fn main() {\n    println!(\"{}\", pad_left(\"42\", 5, ''0''));\n    println!(\"{}\", pad_left(\"привет\", 3, ''-''));\n    println!(\"{}\", pad_left(\"\", 3, ''*''));\n}\n", "expected": ["00042", "привет", "***"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-display-money', 17, 'rust', 'Display для денег', 'Структура Money(i64) хранит копейки. Реализуйте Display: «123.05 ₽» для 12305, «-0.99 ₽» для −99, «0.00 ₽» для 0.', 'use std::fmt;

struct Money(i64);

impl fmt::Display for Money {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}
', 'Знак отдельно, рубли a / 100, копейки {:02}.', '{"driver": "fn main() {\n    println!(\"{}\", Money(12305));\n    println!(\"{}\", Money(-99));\n    println!(\"{}\", Money(0));\n    println!(\"{}\", Money(5));\n}\n", "expected": ["123.05 ₽", "-0.99 ₽", "0.00 ₽", "0.05 ₽"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-display-pad', 18, 'rust', 'Display, уважающий ширину', 'Структура Name(String) реализует Display через f.pad(&self.0), чтобы работали ширина и выравнивание: «[{:>8}]» для Name("Аня") даёт «[     Аня]».', 'use std::fmt;

struct Name(String);

impl fmt::Display for Name {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}
', 'f.pad учитывает ширину, выравнивание и точность (обрезку).', '{"driver": "fn main() {\n    let n = Name(String::from(\"Аня\"));\n    println!(\"[{:>8}]\", n);\n    println!(\"[{:<8}]\", n);\n    println!(\"[{:^8}]\", n);\n    println!(\"[{:.2}]\", n);\n}\n", "expected": ["[     Аня]", "[Аня     ]", "[  Аня   ]", "[Ан]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-debug-manual', 19, 'rust', 'Debug вручную', 'Структура User { name: String, age: u32, secret: String } — реализуйте Debug вручную через debug_struct так, чтобы поле secret не печаталось (вывод «User { name: "Аня", age: 30 }»).', 'use std::fmt;

struct User {
    name: String,
    age: u32,
    secret: String,
}

impl fmt::Debug for User {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}
', 'debug_struct("User").field(…).finish()', '{"driver": "fn main() {\n    let u = User { name: String::from(\"Аня\"), age: 30, secret: String::from(\"пароль\") };\n    println!(\"{:?}\", u);\n    println!(\"{:#?}\", u);\n    let _ = &u.secret;\n}\n", "expected": ["User { name: \"Аня\", age: 30 }", "User {", "    name: \"Аня\",", "    age: 30,", "}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-display-matrix', 20, 'rust', 'Display матрицы', 'Структура Matrix(Vec<Vec<i32>>) реализует Display: строки через перевод строки (без пустой строки в конце), числа в строке через пробел, каждое в поле шириной 3 вправо: «  1  2», «  3  4».', 'use std::fmt;

struct Matrix(Vec<Vec<i32>>);

impl fmt::Display for Matrix {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}
', 'writeln!(f)? между строками, write!(f, "{:>3}", x)? для чисел.', '{"driver": "fn main() {\n    let m = Matrix(vec![vec![1, 2], vec![30, -4]]);\n    println!(\"{}\", m);\n    println!(\"[{}]\", Matrix(vec![]));\n}\n", "expected": ["  1  2", " 30 -4", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-parse-kv', 21, 'rust', 'Разбор «ключ=значение»', 'Напишите parse_kv(line: &str) -> Option<(String, i32)>: «name = 42» → ("name", 42); None, если нет «=», ключ пуст или значение не целое.', 'fn parse_kv(line: &str) -> Option<(String, i32)> {
    todo!()
}
', 'split_once, trim, parse().ok()?', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_kv(\"name = 42\"));\n    println!(\"{:?}\", parse_kv(\"x=-7\"));\n    println!(\"{:?}\", parse_kv(\"= 5\"));\n    println!(\"{:?}\", parse_kv(\"a = b\"));\n    println!(\"{:?}\", parse_kv(\"нет\"));\n}\n", "expected": ["Some((\"name\", 42))", "Some((\"x\", -7))", "None", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-parse-csv', 22, 'rust', 'CSV-строка в числа', 'Напишите parse_row(s: &str) -> Result<Vec<f64>, String>: числа через запятую (с пробелами вокруг); при ошибке — Err(«плохое поле: <поле>»).', 'fn parse_row(s: &str) -> Result<Vec<f64>, String> {
    todo!()
}
', 'collect::<Result<Vec<_>, _>>()', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_row(\"1.5, 2, -3e2\"));\n    println!(\"{:?}\", parse_row(\"1, x, 3\"));\n    println!(\"{:?}\", parse_row(\"\"));\n}\n", "expected": ["Ok([1.5, 2.0, -300.0])", "Err(\"плохое поле: x\")", "Err(\"плохое поле: \")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-parse-radix', 23, 'rust', 'Число с префиксом', 'Напишите parse_num(s: &str) -> Option<i64>: десятичное, с префиксом 0x (hex), 0b (двоичное) или 0o (восьмеричное); знак «-» допустим перед префиксом. Подчёркивания игнорируются.', 'fn parse_num(s: &str) -> Option<i64> {
    todo!()
}
', 'Сначала снимите знак и подчёркивания, затем проверьте префиксы.', '{"driver": "fn main() {\n    for s in [\"42\", \"0xff\", \"-0b101\", \"0o17\", \"1_000\", \"0xZZ\", \"\", \"-\"] {\n        println!(\"{:?}\", parse_num(s));\n    }\n}\n", "expected": ["Some(42)", "Some(255)", "Some(-5)", "Some(15)", "Some(1000)", "None", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-word-freq-fmt', 24, 'rust', 'Отчёт о частотах', 'Напишите report(text: &str) -> Vec<String>: слова в нижнем регистре и их частоты; строки «слово: N», по убыванию N, при равных — по алфавиту.', 'fn report(text: &str) -> Vec<String> {
    todo!()
}
', 'Счётчики в Vec пар, затем sort_by.', '{"driver": "fn main() {\n    for l in report(\"Да нет да НЕТ да может\") {\n        println!(\"{}\", l);\n    }\n}\n", "expected": ["да: 3", "нет: 2", "может: 1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-wrap-text', 25, 'rust', 'Выравнивание по ширине', 'Напишите center_lines(text: &str, width: usize) -> Vec<String>: каждую строку текста (lines) выровнять по центру в поле width (форматом {:^w$}); строки длиннее width не менять.', 'fn center_lines(text: &str, width: usize) -> Vec<String> {
    todo!()
}
', 'format!("{:^w$}", l, w = width)', '{"driver": "fn main() {\n    for l in center_lines(\"а\\nбвг\\nдежзи\", 6) {\n        println!(\"[{}]\", l);\n    }\n    println!(\"{}\", center_lines(\"\", 5).len());\n}\n", "expected": ["[  а   ]", "[ бвг  ]", "[дежзи ]", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-case-convert', 26, 'rust', 'snake_case в CamelCase', 'Напишите to_camel(s: &str) -> String: «my_var_name» → «MyVarName» (разделитель «_»; пустые куски пропускаются).', 'fn to_camel(s: &str) -> String {
    todo!()
}
', 'Первая буква каждого куска — в верхний регистр.', '{"driver": "fn main() {\n    println!(\"{}\", to_camel(\"my_var_name\"));\n    println!(\"{}\", to_camel(\"__a__b_\"));\n    println!(\"[{}]\", to_camel(\"\"));\n    println!(\"{}\", to_camel(\"привет_мир\"));\n}\n", "expected": ["MyVarName", "AB", "[]", "ПриветМир"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-camel-to-snake', 27, 'rust', 'CamelCase в snake_case', 'Напишите to_snake(s: &str) -> String: «MyVarName» → «my_var_name» (перед каждой заглавной, кроме первой буквы, ставится «_»).', 'fn to_snake(s: &str) -> String {
    todo!()
}
', 'out.extend(c.to_lowercase()) — to_lowercase возвращает итератор.', '{"driver": "fn main() {\n    println!(\"{}\", to_snake(\"MyVarName\"));\n    println!(\"{}\", to_snake(\"x\"));\n    println!(\"{}\", to_snake(\"ПриветМир\"));\n    println!(\"[{}]\", to_snake(\"\"));\n}\n", "expected": ["my_var_name", "x", "привет_мир", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-caesar-unicode', 28, 'rust', 'Шифр Виженера', 'Напишите vigenere(text: &str, key: &str) -> String: шифр Виженера для латинских строчных букв (a–z); ключ — строчные буквы, не пуст; ключ продвигается только на буквах текста; остальные символы без изменений.', 'fn vigenere(text: &str, key: &str) -> String {
    todo!()
}
', 'Позиция в ключе j увеличивается только на латинской букве.', '{"driver": "fn main() {\n    println!(\"{}\", vigenere(\"attack at dawn\", \"lemon\"));\n    println!(\"{}\", vigenere(\"abc\", \"a\"));\n    println!(\"{}\", vigenere(\"привет\", \"b\"));\n}\n", "expected": ["lxfopv ef rnhr", "abc", "привет"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 26, 'r26-utf8-len', 29, 'rust', 'Байты символов', 'Напишите byte_lens(s: &str) -> Vec<(char, usize)>: каждый символ и сколько байт он занимает в UTF-8 (len_utf8).', 'fn byte_lens(s: &str) -> Vec<(char, usize)> {
    todo!()
}
', 'c.len_utf8() — 1…4.', '{"driver": "fn main() {\n    println!(\"{:?}\", byte_lens(\"aя世😀\"));\n    println!(\"{:?}\", byte_lens(\"\"));\n}\n", "expected": ["[(''a'', 1), (''я'', 2), (''世'', 3), (''😀'', 4)]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-read-all', 0, 'rust', 'Прочитать всё', 'Напишите slurp<R: Read>(mut r: R) -> io::Result<String>: прочитать источник целиком в строку.', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn slurp<R: Read>(mut r: R) -> io::Result<String> {
    todo!()
}
', '&[u8] и Cursor реализуют Read; ошибка UTF-8 приходит как io::Error.', '{"driver": "fn main() {\n    println!(\"{:?}\", slurp(\"привет\".as_bytes()).unwrap());\n    println!(\"{:?}\", slurp(Cursor::new(Vec::<u8>::new())).unwrap());\n    println!(\"{}\", slurp(Cursor::new(vec![0xff, 0xfe])).is_err());\n}\n", "expected": ["\"привет\"", "\"\"", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-count-lines', 1, 'rust', 'Строки и слова', 'Напишите wc<R: BufRead>(r: R) -> io::Result<(usize, usize, usize)>: число строк, слов (split_whitespace) и байтов (с символами конца строки) в потоке.', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn wc<R: BufRead>(mut r: R) -> io::Result<(usize, usize, usize)> {
    todo!()
}
', 'read_line возвращает число прочитанных байтов; 0 — конец.', '{"driver": "fn main() {\n    println!(\"{:?}\", wc(Cursor::new(\"раз два\\nтри\\n\\nчетыре пять шесть\")).unwrap());\n    println!(\"{:?}\", wc(Cursor::new(\"\")).unwrap());\n}\n", "expected": ["(4, 6, 54)", "(0, 0, 0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-sum-input', 2, 'rust', 'Сумма чисел из ввода', 'Напишите sum_input<R: BufRead>(r: R) -> io::Result<i64>: сумма целых по одному на строке; пустые строки пропускать, некорректные — ошибка InvalidData.', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn sum_input<R: BufRead>(r: R) -> io::Result<i64> {
    todo!()
}
', 'io::Error::new(ErrorKind::InvalidData, e)', '{"driver": "fn main() {\n    println!(\"{:?}\", sum_input(Cursor::new(\"1\\n2\\n\\n -3 \\n\")).unwrap());\n    let e = sum_input(Cursor::new(\"1\\nx\\n\")).unwrap_err();\n    println!(\"{:?}\", e.kind());\n}\n", "expected": ["0", "InvalidData"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-copy-upper', 3, 'rust', 'Копирование с преобразованием', 'Напишите shout<R: BufRead, W: Write>(r: R, w: &mut W) -> io::Result<()>: каждую строку входа записать в выход в верхнем регистре с «!» на конце и переводом строки.', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn shout<R: BufRead, W: Write>(r: R, w: &mut W) -> io::Result<()> {
    todo!()
}
', 'writeln!(w, …) пишет в любой Write.', '{"driver": "fn main() {\n    let mut out: Vec<u8> = Vec::new();\n    shout(Cursor::new(\"привет\\nrust\\n\"), &mut out).unwrap();\n    print!(\"{}\", String::from_utf8(out).unwrap());\n}\n", "expected": ["ПРИВЕТ!", "RUST!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-tee', 4, 'rust', 'Двойная запись', 'Напишите tee<R: Read, A: Write, B: Write>(mut r: R, a: &mut A, b: &mut B) -> io::Result<usize>: читать из r блоками по 4 байта и каждый блок писать и в a, и в b; вернуть число байтов.', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn tee<R: Read, A: Write, B: Write>(mut r: R, a: &mut A, b: &mut B) -> io::Result<usize> {
    todo!()
}
', 'read возвращает меньше байтов, чем размер буфера, — пишите buf[..n].', '{"driver": "fn main() {\n    let (mut a, mut b) = (Vec::new(), Vec::new());\n    let n = tee(\"0123456789\".as_bytes(), &mut a, &mut b).unwrap();\n    println!(\"{} {} {}\", n, String::from_utf8(a).unwrap(), String::from_utf8(b).unwrap());\n}\n", "expected": ["10 0123456789 0123456789"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-take', 5, 'rust', 'Ограничить чтение', 'Напишите head(r: impl Read, n: u64) -> io::Result<String>: первые n байтов (метод take), как строка (lossy).', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn head(r: impl Read, n: u64) -> io::Result<String> {
    todo!()
}
', 'r.take(n).read_to_end(&mut buf)', '{"driver": "fn main() {\n    println!(\"{:?}\", head(\"hello world\".as_bytes(), 5).unwrap());\n    println!(\"{:?}\", head(\"abc\".as_bytes(), 10).unwrap());\n    println!(\"{:?}\", head(\"abc\".as_bytes(), 0).unwrap());\n}\n", "expected": ["\"hello\"", "\"abc\"", "\"\""]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-chain', 6, 'rust', 'Склейка потоков', 'Напишите joined(a: &str, b: &str) -> String: прочитайте два источника подряд через chain как один и верните результат.', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn joined(a: &str, b: &str) -> String {
    todo!()
}
', 'Read::chain склеивает два источника.', '{"driver": "fn main() {\n    println!(\"{}\", joined(\"раз, \", \"два\"));\n    println!(\"[{}]\", joined(\"\", \"\"));\n}\n", "expected": ["раз, два", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-read-exact', 7, 'rust', 'Заголовок фиксированной длины', 'Напишите read_header<R: Read>(mut r: R) -> io::Result<(u16, u32)>: прочитать 6 байт — два байта u16 и четыре байта u32 в порядке little-endian; при коротких данных вернуть ошибку UnexpectedEof (read_exact).', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn read_header<R: Read>(mut r: R) -> io::Result<(u16, u32)> {
    todo!()
}
', 'from_le_bytes для каждого поля.', '{"driver": "fn main() {\n    println!(\"{:?}\", read_header(&[1u8, 0, 2, 0, 0, 0][..]).unwrap());\n    println!(\"{:?}\", read_header(&[1u8, 1, 1][..]).unwrap_err().kind());\n}\n", "expected": ["(1, 2)", "UnexpectedEof"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-write-numbers', 8, 'rust', 'Двоичная запись', 'Напишите write_u32s<W: Write>(w: &mut W, v: &[u32]) -> io::Result<()>: записать числа big-endian подряд (to_be_bytes).', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn write_u32s<W: Write>(w: &mut W, v: &[u32]) -> io::Result<()> {
    todo!()
}
', 'x.to_be_bytes() возвращает [u8; 4].', '{"driver": "fn main() {\n    let mut out = Vec::new();\n    write_u32s(&mut out, &[1, 258, 0xDEADBEEF]).unwrap();\n    println!(\"{:?}\", out);\n}\n", "expected": ["[0, 0, 0, 1, 0, 0, 1, 2, 222, 173, 190, 239]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-seek-tail', 9, 'rust', 'Хвост файла', 'Напишите tail_bytes<R: Read + Seek>(mut r: R, n: u64) -> io::Result<Vec<u8>>: последние n байтов (или всё, если данных меньше). Seek::seek(SeekFrom::End(…)).', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn tail_bytes<R: Read + Seek>(mut r: R, n: u64) -> io::Result<Vec<u8>> {
    todo!()
}
', 'seek(End(0)) возвращает размер.', '{"driver": "fn main() {\n    println!(\"{:?}\", tail_bytes(Cursor::new(b\"0123456789\".to_vec()), 3).unwrap());\n    println!(\"{:?}\", tail_bytes(Cursor::new(b\"ab\".to_vec()), 10).unwrap());\n    println!(\"{:?}\", tail_bytes(Cursor::new(Vec::new()), 4).unwrap());\n}\n", "expected": ["[55, 56, 57]", "[97, 98]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-seek-patch', 10, 'rust', 'Правка по смещению', 'Напишите patch<S: Read + Write + Seek>(mut s: S, pos: u64, data: &[u8]) -> io::Result<Vec<u8>>: записать data с позиции pos и вернуть всё содержимое после правки.', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn patch<S: Read + Write + Seek>(mut s: S, pos: u64, data: &[u8]) -> io::Result<Vec<u8>> {
    todo!()
}
', 'Курсор над вектором реализует Read, Write и Seek сразу.', '{"driver": "fn main() {\n    let c = Cursor::new(b\"0123456789\".to_vec());\n    println!(\"{:?}\", String::from_utf8(patch(c, 3, b\"ABC\").unwrap()).unwrap());\n}\n", "expected": ["\"012ABC6789\""]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-bufwriter', 11, 'rust', 'BufWriter', 'Напишите write_squares<W: Write>(w: W, n: u32) -> io::Result<()>: обернув w в BufWriter, записать квадраты чисел 1…n по одному на строке.', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn write_squares<W: Write>(w: W, n: u32) -> io::Result<()> {
    todo!()
}
', 'BufWriter::new(w) и flush() в конце.', '{"driver": "fn main() {\n    let mut v: Vec<u8> = Vec::new();\n    write_squares(&mut v, 5).unwrap();\n    print!(\"{}\", String::from_utf8(v).unwrap());\n    let mut big: Vec<u8> = Vec::new();\n    write_squares(&mut big, 100000).unwrap();\n    println!(\"{}\", big.len());\n}\n", "expected": ["1", "4", "9", "16", "25", "1039834"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-read-until', 12, 'rust', 'read_until', 'Напишите records<R: BufRead>(mut r: R) -> io::Result<Vec<String>>: записи, разделённые символом «;» (read_until); разделитель в запись не входит, пустые записи пропускаются.', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn records<R: BufRead>(mut r: R) -> io::Result<Vec<String>> {
    todo!()
}
', 'read_until включает разделитель в буфер — уберите его.', '{"driver": "fn main() {\n    println!(\"{:?}\", records(Cursor::new(\"a; b ;;c\")).unwrap());\n    println!(\"{:?}\", records(Cursor::new(\"\")).unwrap());\n}\n", "expected": ["[\"a\", \"b\", \"c\"]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-parse-grid', 13, 'rust', 'Прочитать сетку', 'Напишите read_grid<R: BufRead>(r: R) -> io::Result<Vec<Vec<i32>>>: первая строка — «N M», далее N строк по M чисел через пробел. Если не хватает строк или чисел — ошибка InvalidData.', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn read_grid<R: BufRead>(r: R) -> io::Result<Vec<Vec<i32>>> {
    todo!()
}
', 'Определите замыкание bad() для создания ошибки.', '{"driver": "fn main() {\n    println!(\"{:?}\", read_grid(Cursor::new(\"2 3\\n1 2 3\\n4 5 6\\n\")).unwrap());\n    println!(\"{}\", read_grid(Cursor::new(\"2 2\\n1 2\\n\")).is_err());\n    println!(\"{}\", read_grid(Cursor::new(\"1 2\\n1 x\\n\")).is_err());\n    println!(\"{}\", read_grid(Cursor::new(\"\")).is_err());\n}\n", "expected": ["[[1, 2, 3], [4, 5, 6]]", "true", "true", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-path-parts', 14, 'rust', 'Части пути', 'Напишите describe(p: &str) -> String: «каталог=…, имя=…, расширение=…» (parent, file_stem, extension; отсутствующее — «-»).', 'fn describe(p: &str) -> String {
    todo!()
}
', 'Path::new(p).parent(), file_stem(), extension() — все возвращают Option.', '{"driver": "fn main() {\n    println!(\"{}\", describe(\"/home/user/report.final.pdf\"));\n    println!(\"{}\", describe(\"notes.txt\"));\n    println!(\"{}\", describe(\"/etc/hosts\"));\n    println!(\"{}\", describe(\"dir/.hidden\"));\n}\n", "expected": ["каталог=/home/user, имя=report.final, расширение=pdf", "каталог=-, имя=notes, расширение=txt", "каталог=/etc, имя=hosts, расширение=-", "каталог=dir, имя=.hidden, расширение=-"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-path-join', 15, 'rust', 'Склейка путей', 'Напишите build_path(parts: &[&str]) -> String: склейте части в путь через PathBuf::push (абсолютная часть заменяет всё предыдущее); результат — строка. Для ["/a", "b", "c.txt"] это «/a/b/c.txt».', 'fn build_path(parts: &[&str]) -> String {
    todo!()
}
', 'push с абсолютным путём заменяет накопленное.', '{"driver": "fn main() {\n    println!(\"{}\", build_path(&[\"/a\", \"b\", \"c.txt\"]));\n    println!(\"{}\", build_path(&[\"a\", \"/b\", \"c\"]));\n    println!(\"[{}]\", build_path(&[]));\n}\n", "expected": ["/a/b/c.txt", "/b/c", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-ext-change', 16, 'rust', 'Сменить расширение', 'Напишите to_bak(name: &str) -> String: заменить расширение на «bak» (with_extension), а для имени без расширения — добавить.', 'fn to_bak(name: &str) -> String {
    todo!()
}
', 'with_extension заменяет последнее расширение.', '{"driver": "fn main() {\n    println!(\"{}\", to_bak(\"data.csv\"));\n    println!(\"{}\", to_bak(\"README\"));\n    println!(\"{}\", to_bak(\"a/b/c.tar.gz\"));\n}\n", "expected": ["data.bak", "README.bak", "a/b/c.tar.bak"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-file-roundtrip', 17, 'rust', 'Файл: запись и чтение', 'Напишите roundtrip(text: &str) -> io::Result<String>: запишите text во временный файл в каталоге std::env::temp_dir() (имя с номером процесса), прочитайте обратно, удалите файл и верните прочитанное.', 'use std::io;

fn roundtrip(text: &str) -> io::Result<String> {
    todo!()
}
', 'fs::write, fs::read_to_string, fs::remove_file.', '{"driver": "fn main() {\n    println!(\"{:?}\", roundtrip(\"привет\\nмир\").unwrap());\n    println!(\"{:?}\", roundtrip(\"\").unwrap());\n}\n", "expected": ["\"привет\\nмир\"", "\"\""]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-file-append', 18, 'rust', 'Дозапись в файл', 'Напишите append_lines(lines: &[&str]) -> io::Result<usize>: во временный файл (std::env::temp_dir(), имя с номером процесса) дозаписать строки по одной (OpenOptions append) двумя разными открытиями; вернуть число строк в файле; файл удалить.', 'use std::io::{self, Write};

fn append_lines(lines: &[&str]) -> io::Result<usize> {
    todo!()
}
', 'OpenOptions::new().append(true).create(true).open(&p)', '{"driver": "fn main() {\n    println!(\"{}\", append_lines(&[\"a\", \"b\", \"c\", \"d\", \"e\"]).unwrap());\n    println!(\"{}\", append_lines(&[]).unwrap());\n}\n", "expected": ["5", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-dir-walk', 19, 'rust', 'Обход каталога', 'Напишите make_and_list() -> io::Result<Vec<String>>: создайте во временном каталоге (temp_dir + имя с номером процесса) каталог с файлами c.txt, a.txt, b.log (пустые), прочитайте его read_dir, верните имена по алфавиту и удалите каталог со всем содержимым (remove_dir_all).', 'use std::io;

fn make_and_list() -> io::Result<Vec<String>> {
    todo!()
}
', 'read_dir возвращает итератор io::Result<DirEntry>; порядок не определён — сортируйте.', '{"driver": "fn main() {\n    println!(\"{:?}\", make_and_list().unwrap());\n}\n", "expected": ["[\"a.txt\", \"b.log\", \"c.txt\"]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-error-kind', 20, 'rust', 'Вид ошибки', 'Напишите open_kind(path: &str) -> String: попытайтесь открыть файл; верните «ok» при успехе, «нет файла» для NotFound, «нет доступа» для PermissionDenied и «ошибка» для остальных.', 'use std::io;

fn open_kind(path: &str) -> String {
    todo!()
}
', 'e.kind() возвращает ErrorKind. Каталог можно открыть для чтения, а вот читать его нельзя.', '{"driver": "fn main() {\n    println!(\"{}\", open_kind(\"/этого/файла/нет\"));\n    println!(\"{}\", open_kind(\"/\"));\n}\n", "expected": ["нет файла", "ok"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-custom-error', 21, 'rust', 'Свой тип ошибки', 'Объявите enum AppError { Io(io::Error), Parse(std::num::ParseIntError) } с derive(Debug) и реализуйте From для обоих вариантов. Тогда функция read_num(r: impl Read) -> Result<i32, AppError> читает строку и разбирает число одним ? на каждом шаге.', 'use std::io::{self, Read};

fn read_num(mut r: impl Read) -> Result<i32, AppError> {
    let mut s = String::new();
    r.read_to_string(&mut s)?;
    Ok(s.trim().parse()?)
}
', 'impl From<…> for AppError — тело: AppError::Вариант(e).', '{"driver": "fn main() {\n    println!(\"{:?}\", read_num(\" 42\\n\".as_bytes()).ok());\n    println!(\"{}\", matches!(read_num(\"x\".as_bytes()), Err(AppError::Parse(_))));\n    println!(\"{}\", matches!(read_num(&[0xffu8][..]), Err(AppError::Io(_))));\n}\n", "expected": ["Some(42)", "true", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-line-numbers', 22, 'rust', 'Номера строк', 'Напишите number_lines<R: BufRead, W: Write>(r: R, w: &mut W) -> io::Result<()>: записывать каждую строку с номером (с 1) в формате «   1: текст» (номер вправо в поле 4).', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn number_lines<R: BufRead, W: Write>(r: R, w: &mut W) -> io::Result<()> {
    todo!()
}
', 'enumerate() над lines().', '{"driver": "fn main() {\n    let mut out = Vec::new();\n    number_lines(Cursor::new(\"a\\nb\\n\\nd\"), &mut out).unwrap();\n    print!(\"{}\", String::from_utf8(out).unwrap());\n}\n", "expected": ["   1: a", "   2: b", "   3:", "   4: d"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-grep', 23, 'rust', 'grep', 'Напишите grep<R: BufRead>(r: R, pat: &str, ignore_case: bool) -> io::Result<Vec<(usize, String)>>: номера (с 1) и тексты строк, содержащих pat (при ignore_case — без учёта регистра).', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn grep<R: BufRead>(r: R, pat: &str, ignore_case: bool) -> io::Result<Vec<(usize, String)>> {
    todo!()
}
', 'Приводите и шаблон, и строку к нижнему регистру.', '{"driver": "fn main() {\n    let t = \"Rust is fast\\nrust is safe\\nGo is simple\\n\";\n    println!(\"{:?}\", grep(Cursor::new(t), \"Rust\", false).unwrap());\n    println!(\"{:?}\", grep(Cursor::new(t), \"rust\", true).unwrap());\n    println!(\"{:?}\", grep(Cursor::new(t), \"java\", true).unwrap());\n}\n", "expected": ["[(1, \"Rust is fast\")]", "[(1, \"Rust is fast\"), (2, \"rust is safe\")]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-csv-sum', 24, 'rust', 'Колонка CSV', 'Напишите column_sum<R: BufRead>(r: R, col: usize) -> io::Result<f64>: сумма чисел в столбце col (с 0) строк вида «a,1.5,b»; первая строка — заголовок и пропускается; пустые поля считаются нулём; нечисловое — ошибка InvalidData.', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn column_sum<R: BufRead>(r: R, col: usize) -> io::Result<f64> {
    todo!()
}
', 'split('','').nth(col) — нужное поле.', '{"driver": "fn main() {\n    let t = \"имя,цена,кол\\nхлеб,50.5,2\\nмолоко,,1\\nсыр,300,3\\n\";\n    println!(\"{:?}\", column_sum(Cursor::new(t), 1).unwrap());\n    println!(\"{:?}\", column_sum(Cursor::new(t), 2).unwrap());\n    println!(\"{}\", column_sum(Cursor::new(\"a,b\\nx,y\\n\"), 1).is_err());\n}\n", "expected": ["350.5", "6.0", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-hexdump', 25, 'rust', 'Hex-дамп', 'Напишите hexdump(data: &[u8]) -> Vec<String>: строки по 8 байт «смещение(4 цифры hex): байты через пробел» (последняя строка может быть короче): «0000: 48 65 6c …».', 'fn hexdump(data: &[u8]) -> Vec<String> {
    todo!()
}
', 'chunks(8) и enumerate; смещение — i * 8.', '{"driver": "fn main() {\n    for l in hexdump(b\"Hello, Rust language!\") {\n        println!(\"{}\", l);\n    }\n    println!(\"{}\", hexdump(&[]).len());\n}\n", "expected": ["0000: 48 65 6c 6c 6f 2c 20 52", "0008: 75 73 74 20 6c 61 6e 67", "0010: 75 61 67 65 21", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-run-command', 26, 'rust', 'Запуск программы', 'Напишите echo_via_shell(word: &str) -> String: запустите команду «echo» с аргументом word через std::process::Command и верните её вывод без завершающего перевода строки. (В песочнице есть /bin/echo.)', 'fn echo_via_shell(word: &str) -> String {
    todo!()
}
', 'Command::new("echo").arg(word).output()', '{"driver": "fn main() {\n    println!(\"{}\", echo_via_shell(\"привет\"));\n    println!(\"[{}]\", echo_via_shell(\"\"));\n}\n", "expected": ["привет", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-stdout-bytes', 27, 'rust', 'Сколько байтов напечатано', 'Напишите counted(f: impl Fn(&mut dyn Write)) -> usize: вызовите f, передав ему в качестве Write вектор байтов, и верните число записанных байтов.', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn counted(f: impl Fn(&mut dyn Write)) -> usize {
    todo!()
}
', '&mut Vec<u8> приводится к &mut dyn Write.', '{"driver": "fn main() {\n    println!(\"{}\", counted(|w| { write!(w, \"привет\").unwrap(); }));\n    println!(\"{}\", counted(|w| { writeln!(w, \"a\").unwrap(); writeln!(w, \"b\").unwrap(); }));\n    println!(\"{}\", counted(|_| {}));\n}\n", "expected": ["12", "4", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-reverse-lines', 28, 'rust', 'Строки в обратном порядке', 'Напишите reverse_lines<R: BufRead, W: Write>(r: R, w: &mut W) -> io::Result<()>: записать строки входа в обратном порядке (по одной на строку).', 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};

fn reverse_lines<R: BufRead, W: Write>(r: R, w: &mut W) -> io::Result<()> {
    todo!()
}
', 'lines().collect::<Result<Vec<_>, _>>()?', '{"driver": "fn main() {\n    let mut out = Vec::new();\n    reverse_lines(Cursor::new(\"раз\\nдва\\nтри\\n\"), &mut out).unwrap();\n    print!(\"{}\", String::from_utf8(out).unwrap());\n}\n", "expected": ["три", "два", "раз"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 27, 'r27-parse-args', 29, 'rust', 'Разбор аргументов', 'Напишите parse_args(args: &[&str]) -> (bool, Option<String>, Vec<String>): флаг «-v» (verbose), опция «-o <файл>» (выход) и остальные слова как позиционные аргументы; как у простых консольных утилит.', 'fn parse_args(args: &[&str]) -> (bool, Option<String>, Vec<String>) {
    todo!()
}
', 'Итератор по аргументам: после «-o» берём следующий элемент.', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_args(&[\"-v\", \"a.txt\", \"-o\", \"out.txt\", \"b.txt\"]));\n    println!(\"{:?}\", parse_args(&[]));\n    println!(\"{:?}\", parse_args(&[\"-o\"]));\n}\n", "expected": ["(true, Some(\"out.txt\"), [\"a.txt\", \"b.txt\"])", "(false, None, [])", "(false, None, [])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-duration-hms', 0, 'rust', 'Часы, минуты, секунды', 'Напишите hms(d: Duration) -> String: формат «ЧЧ:ММ:СС» (часы могут быть больше 24; доли секунды отбросить).', 'use std::time::Duration;

fn hms(d: Duration) -> String {
    todo!()
}
', 'as_secs() даёт целые секунды.', '{"driver": "fn main() {\n    println!(\"{}\", hms(Duration::from_secs(3725)));\n    println!(\"{}\", hms(Duration::from_millis(59999)));\n    println!(\"{}\", hms(Duration::from_secs(100 * 3600 + 5)));\n}\n", "expected": ["01:02:05", "00:00:59", "100:00:05"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-duration-parse', 1, 'rust', 'Разбор «1h30m15s»', 'Напишите parse_duration(s: &str) -> Option<Duration>: суммарная длительность из последовательности «<число><единица>» с единицами h, m, s; недопустимая строка или пустая — None.', 'use std::time::Duration;

fn parse_duration(s: &str) -> Option<Duration> {
    todo!()
}
', 'Накапливайте цифры; при букве — умножьте на единицу.', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_duration(\"1h30m15s\"));\n    println!(\"{:?}\", parse_duration(\"90s\"));\n    println!(\"{:?}\", parse_duration(\"5\"));\n    println!(\"{:?}\", parse_duration(\"2x\"));\n    println!(\"{:?}\", parse_duration(\"\"));\n}\n", "expected": ["Some(5415s)", "Some(90s)", "None", "None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-duration-arith', 2, 'rust', 'Арифметика длительностей', 'Напишите total(parts: &[Duration]) -> Duration (сумма) и average(parts: &[Duration]) -> Option<Duration> (среднее; для пустого — None).', 'use std::time::Duration;

fn average(parts: &[Duration]) -> Option<Duration> {
    todo!()
}

fn total(parts: &[Duration]) -> Duration {
    todo!()
}
', 'Duration реализует Sum; деление Duration / u32.', '{"driver": "fn main() {\n    let v = [Duration::from_millis(500), Duration::from_secs(2), Duration::from_millis(1500)];\n    println!(\"{:?}\", total(&v));\n    println!(\"{:?}\", total(&[]));\n    println!(\"{:?}\", average(&v));\n    println!(\"{:?}\", average(&[]));\n}\n", "expected": ["4s", "0ns", "Some(1.333333333s)", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-duration-checked', 3, 'rust', 'Безопасное вычитание', 'Напишите remaining(deadline: Duration, spent: Duration) -> Duration: сколько осталось (ноль, если время вышло) — saturating_sub.', 'use std::time::Duration;

fn remaining(deadline: Duration, spent: Duration) -> Duration {
    todo!()
}
', 'saturating_sub не паникует.', '{"driver": "fn main() {\n    println!(\"{:?}\", remaining(Duration::from_secs(10), Duration::from_secs(3)));\n    println!(\"{:?}\", remaining(Duration::from_secs(3), Duration::from_secs(10)));\n}\n", "expected": ["7s", "0ns"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-epoch-days', 4, 'rust', 'Секунды с 1970 года в дату', 'Напишите civil_from_secs(secs: u64) -> (u32, u32, u32): год, месяц и день (UTC) по секундам с 1 января 1970 года. Алгоритм «civil from days»: z = дни + 719468; era = z / 146097; doe = z − era·146097; yoe = (doe − doe/1460 + doe/36524 − doe/146096) / 365; y = yoe + era·400; doy = doe − (365·yoe + yoe/4 − yoe/100); mp = (5·doy + 2) / 153; d = doy − (153·mp + 2)/5 + 1; m = mp + 3 при mp < 10, иначе mp − 9; y + 1, если m ≤ 2.', 'fn civil_from_secs(secs: u64) -> (u32, u32, u32) {
    todo!()
}
', 'Целочисленная арифметика с i64; деление отсекает к нулю — для положительных чисел это то, что нужно.', '{"driver": "fn main() {\n    println!(\"{:?}\", civil_from_secs(0));\n    println!(\"{:?}\", civil_from_secs(86399));\n    println!(\"{:?}\", civil_from_secs(951782400));\n    println!(\"{:?}\", civil_from_secs(1709164800));\n    println!(\"{:?}\", civil_from_secs(4102444800));\n}\n", "expected": ["(1970, 1, 1)", "(1970, 1, 1)", "(2000, 2, 29)", "(2024, 2, 29)", "(2100, 1, 1)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-instant-measure', 5, 'rust', 'Измерение', 'Напишите time_it<F: FnOnce() -> u64>(f: F) -> (u64, Duration): вызовите f ровно один раз и верните её результат вместе с измеренной через Instant длительностью.', 'use std::time::Duration;

fn time_it<F: FnOnce() -> u64>(f: F) -> (u64, Duration) {
    todo!()
}
', 'Instant::now(), вызов, elapsed().', '{"driver": "fn main() {\n    let (r, d) = time_it(|| (1..=1000u64).sum());\n    println!(\"{} {}\", r, d < Duration::from_secs(5));\n    let (_, d2) = time_it(|| { std::thread::sleep(Duration::from_millis(30)); 0 });\n    println!(\"{}\", d2 >= Duration::from_millis(30));\n}\n", "expected": ["500500 true", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-checked-ops', 6, 'rust', 'Безопасные операции', 'Напишите safe_sum(v: &[i32]) -> Option<i32>: сумма с проверкой переполнения (None, если не поместилась).', 'fn safe_sum(v: &[i32]) -> Option<i32> {
    todo!()
}
', 'try_fold с checked_add.', '{"driver": "fn main() {\n    println!(\"{:?}\", safe_sum(&[1, 2, 3]));\n    println!(\"{:?}\", safe_sum(&[i32::MAX, 1]));\n    println!(\"{:?}\", safe_sum(&[]));\n    println!(\"{:?}\", safe_sum(&[i32::MIN, -1]));\n}\n", "expected": ["Some(6)", "None", "Some(0)", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-pow-mod', 7, 'rust', 'Степень по модулю', 'Напишите pow_mod(base: u64, exp: u64, m: u64) -> u64: base^exp mod m (m ≥ 1) быстрым возведением; промежуточные произведения в u128.', 'fn pow_mod(base: u64, exp: u64, m: u64) -> u64 {
    todo!()
}
', 'Возведение по битам показателя; u128 вмещает произведение двух u64.', '{"driver": "fn main() {\n    println!(\"{}\", pow_mod(2, 10, 1000));\n    println!(\"{}\", pow_mod(3, 200, 13));\n    println!(\"{}\", pow_mod(7, 0, 5));\n    println!(\"{}\", pow_mod(2, 1_000_000_007, 998_244_353));\n    println!(\"{}\", pow_mod(10, 18, 1_000_000_000_000_000_000));\n}\n", "expected": ["24", "9", "1", "132727571", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-bits-count', 8, 'rust', 'Биты', 'Напишите bit_stats(x: u32) -> (u32, u32, u32): число единиц, ведущих нулей и замыкающих нулей (x ≠ 0 — штатно; для 0 методы вернут 32).', 'fn bit_stats(x: u32) -> (u32, u32, u32) {
    todo!()
}
', 'Три метода целого.', '{"driver": "fn main() {\n    println!(\"{:?}\", bit_stats(0b1011000));\n    println!(\"{:?}\", bit_stats(1));\n    println!(\"{:?}\", bit_stats(u32::MAX));\n    println!(\"{:?}\", bit_stats(0));\n}\n", "expected": ["(3, 25, 3)", "(1, 31, 0)", "(32, 0, 0)", "(0, 32, 32)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-is-pow2', 9, 'rust', 'Степень двойки', 'Напишите round_up_pow2(n: u32) -> u32: наименьшая степень двойки не меньше n (для 0 — 1). Используйте метод next_power_of_two.', 'fn round_up_pow2(n: u32) -> u32 {
    todo!()
}
', 'u32::next_power_of_two.', '{"driver": "fn main() {\n    for n in [0, 1, 2, 3, 17, 64, 65, 1 << 30] {\n        print!(\"{} \", round_up_pow2(n));\n    }\n    println!();\n}\n", "expected": ["1 1 2 4 32 64 128 1073741824"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-gray', 10, 'rust', 'Код Грея', 'Напишите gray(n: u32) -> u32: n ^ (n >> 1) и ungray(g: u32) -> u32 — обратное преобразование (ungray(gray(n)) == n).', 'fn gray(n: u32) -> u32 {
    todo!()
}

fn ungray(g: u32) -> u32 {
    todo!()
}
', 'Обратное: xor всех сдвигов вправо.', '{"driver": "fn main() {\n    for n in 0..8 {\n        print!(\"{:03b} \", gray(n));\n    }\n    println!();\n    println!(\"{}\", (0..10000).all(|n| ungray(gray(n)) == n));\n}\n", "expected": ["000 001 011 010 110 111 101 100", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-rotate-bytes', 11, 'rust', 'Порядок байтов', 'Напишите swap_endian(x: u32) -> u32 без swap_bytes — через to_le_bytes и from_be_bytes.', 'fn swap_endian(x: u32) -> u32 {
    todo!()
}
', 'Байты записываем в одном порядке, читаем в другом.', '{"driver": "fn main() {\n    println!(\"{:#x}\", swap_endian(0x12345678));\n    println!(\"{}\", swap_endian(swap_endian(77)) == 77);\n}\n", "expected": ["0x78563412", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-isqrt', 12, 'rust', 'Целый корень', 'Напишите isqrt(n: u64) -> u64: наибольшее r с r·r ≤ n (бинарный поиск или метод isqrt, если он доступен). Проверка на больших значениях, включая u64::MAX.', 'fn isqrt(n: u64) -> u64 {
    todo!()
}
', 'Бинарный поиск по r; умножение — в u128.', '{"driver": "fn main() {\n    for n in [0u64, 1, 2, 3, 4, 15, 16, 17, 1_000_000_000_000, u64::MAX] {\n        print!(\"{} \", isqrt(n));\n    }\n    println!();\n}\n", "expected": ["0 1 1 1 2 3 4 4 1000000 4294967295"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-float-round', 13, 'rust', 'Округление до знаков', 'Напишите round_to(x: f64, digits: u32) -> f64: округлить до digits знаков после запятой (round, умножение и деление на 10^digits).', 'fn round_to(x: f64, digits: u32) -> f64 {
    todo!()
}
', '10f64.powi(digits as i32)', '{"driver": "fn main() {\n    println!(\"{}\", round_to(3.14159, 2));\n    println!(\"{}\", round_to(2.5, 0));\n    println!(\"{}\", round_to(-1.005, 1));\n    println!(\"{}\", round_to(1234.5678, 0));\n}\n", "expected": ["3.14", "3", "-1", "1235"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-float-compare', 14, 'rust', 'Сравнение с допуском', 'Напишите approx_eq(a: f64, b: f64, rel: f64) -> bool: |a − b| ≤ rel · max(|a|, |b|, 1.0).', 'fn approx_eq(a: f64, b: f64, rel: f64) -> bool {
    todo!()
}
', 'NaN не равен ничему: сравнение даёт false.', '{"driver": "fn main() {\n    println!(\"{}\", approx_eq(0.1 + 0.2, 0.3, 1e-9));\n    println!(\"{}\", approx_eq(1e10, 1e10 + 1.0, 1e-9));\n    println!(\"{}\", approx_eq(1.0, 1.1, 1e-3));\n    println!(\"{}\", approx_eq(f64::NAN, f64::NAN, 1e-3));\n}\n", "expected": ["true", "true", "false", "false"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-mean-std', 15, 'rust', 'Среднее и отклонение', 'Напишите stats(v: &[f64]) -> Option<(f64, f64)>: среднее и стандартное отклонение (по формуле для всей совокупности, делим на n); для пустого — None.', 'fn stats(v: &[f64]) -> Option<(f64, f64)> {
    todo!()
}
', 'Две суммы: значений и квадратов отклонений.', '{"driver": "fn main() {\n    println!(\"{:?}\", stats(&[2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]));\n    println!(\"{:?}\", stats(&[]));\n    println!(\"{:?}\", stats(&[3.0]));\n}\n", "expected": ["Some((5.0, 2.0))", "None", "Some((3.0, 0.0))"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-hypot-dist', 16, 'rust', 'Расстояния', 'Напишите path_len(points: &[(f64, f64)]) -> f64: длина ломаной через все точки по порядку (hypot).', 'fn path_len(points: &[(f64, f64)]) -> f64 {
    todo!()
}
', 'windows(2) и hypot.', '{"driver": "fn main() {\n    println!(\"{}\", path_len(&[(0.0, 0.0), (3.0, 4.0), (3.0, 10.0)]));\n    println!(\"{}\", path_len(&[(1.0, 1.0)]) == 0.0);\n}\n", "expected": ["11", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-nan-sort', 17, 'rust', 'Сортировка с NaN', 'Напишите sorted_floats(v: &[f64]) -> Vec<f64>: копия по возрастанию с NaN в конце (total_cmp).', 'fn sorted_floats(v: &[f64]) -> Vec<f64> {
    todo!()
}
', 'total_cmp задаёт полный порядок.', '{"driver": "fn main() {\n    println!(\"{:?}\", sorted_floats(&[2.5, f64::NAN, -1.0, f64::INFINITY, 0.0]));\n}\n", "expected": ["[-1.0, 0.0, 2.5, inf, NaN]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-nonzero', 18, 'rust', 'NonZero', 'Напишите to_nonzero(v: &[u32]) -> Vec<Option<std::num::NonZeroU32>>: каждое число как NonZeroU32 (None для нуля).', 'fn to_nonzero(v: &[u32]) -> Vec<Option<std::num::NonZeroU32>> {
    todo!()
}
', 'NonZeroU32::new(x) возвращает Option.', '{"driver": "fn main() {\n    let r = to_nonzero(&[3, 0, 7]);\n    println!(\"{:?}\", r);\n    println!(\"{}\", std::mem::size_of::<Option<std::num::NonZeroU32>>() == std::mem::size_of::<u32>());\n}\n", "expected": ["[Some(3), None, Some(7)]", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-wrapping-hash', 19, 'rust', 'Хеш с оборотом', 'Напишите fnv1a(data: &[u8]) -> u32: хеш FNV-1a: h = 2166136261; для каждого байта h ^= байт; h = h * 16777619 (с оборотом — wrapping_mul).', 'fn fnv1a(data: &[u8]) -> u32 {
    todo!()
}
', 'wrapping_mul не паникует при переполнении.', '{"driver": "fn main() {\n    println!(\"{:#010x}\", fnv1a(b\"\"));\n    println!(\"{:#010x}\", fnv1a(b\"a\"));\n    println!(\"{:#010x}\", fnv1a(b\"foobar\"));\n}\n", "expected": ["0x811c9dc5", "0xe40c292c", "0xbf9cf968"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-lcg', 20, 'rust', 'Свой генератор', 'Реализуйте struct Lcg { state: u64 } с функцией new(seed: u64) и методом next(&mut self) -> u64: state = state · 6364136223846793005 + 1442695040888963407 (с оборотом); результат — state >> 33. Одинаковое зерно даёт одинаковую последовательность.', 'struct Lcg {
    state: u64,
}

impl Lcg {
    fn new(seed: u64) -> Lcg {
        todo!()
    }
    fn next(&mut self) -> u64 {
        todo!()
    }
}
', 'Используйте wrapping_mul и wrapping_add.', '{"driver": "fn main() {\n    let mut a = Lcg::new(42);\n    let mut b = Lcg::new(42);\n    let va: Vec<u64> = (0..3).map(|_| a.next()).collect();\n    let vb: Vec<u64> = (0..3).map(|_| b.next()).collect();\n    println!(\"{:?}\", va);\n    println!(\"{}\", va == vb);\n    let mut c = Lcg::new(7);\n    let mut sum = 0u64;\n    for _ in 0..1000 {\n        sum += c.next() % 10;\n    }\n    println!(\"{}\", sum);\n}\n", "expected": ["[1220265334, 484179026, 886563538]", "true", "4369"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-shuffle', 21, 'rust', 'Перемешивание', 'Напишите shuffle(v: &mut [i32], seed: u64): перемешайте на месте алгоритмом Фишера — Йетса с генератором xorshift: x ^= x << 13; x ^= x >> 7; x ^= x << 17 (u64, зерно — состояние; зерно 0 заменить на 1); для i от len−1 до 1 меняйте v[i] и v[x % (i + 1)].', 'fn shuffle(v: &mut [i32], seed: u64) {
    todo!()
}
', 'Замыкание next() хранит состояние x.', '{"driver": "fn main() {\n    let mut v: Vec<i32> = (1..=10).collect();\n    shuffle(&mut v, 12345);\n    println!(\"{:?}\", v);\n    let mut s = v.clone();\n    s.sort();\n    println!(\"{:?}\", s);\n    let mut w: Vec<i32> = (1..=10).collect();\n    shuffle(&mut w, 12345);\n    println!(\"{}\", v == w);\n}\n", "expected": ["[1, 4, 9, 6, 5, 3, 8, 2, 7, 10]", "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-size-table', 22, 'rust', 'Размеры в байтах', 'Напишите sizes() -> Vec<(String, usize)>: пары (название, size_of) для типов: u8, u64, char, &u8, &[u8], String, Option<u32>, Option<&u8>, (u8, u32), [u16; 5], Box<u8>, Option<Box<u8>>.', 'fn sizes() -> Vec<(String, usize)> {
    todo!()
}
', 'size_of::<T>() для каждого типа.', '{"driver": "fn main() {\n    for (n, s) in sizes() {\n        println!(\"{} {}\", n, s);\n    }\n}\n", "expected": ["u8 1", "u64 8", "char 4", "&u8 8", "&[u8] 16", "String 24", "Option<u32> 8", "Option<&u8> 8", "(u8, u32) 8", "[u16; 5] 10", "Box<u8> 8", "Option<Box<u8>> 8"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-struct-packing', 23, 'rust', 'Порядок полей', 'Напишите packing() -> (usize, usize, usize): размеры трёх структур: A { a: u8, b: u32, c: u8 } без repr, A_C — та же с #[repr(C)], B { b: u32, a: u8, c: u8 } с #[repr(C)]. Структуры объявите внутри функции или рядом.', 'fn packing() -> (usize, usize, usize) {
    todo!()
}
', 'Структуры нужно объявить перед функцией.', '{"driver": "fn main() {\n    println!(\"{:?}\", packing());\n}\n", "expected": ["(8, 12, 8)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-discriminant', 24, 'rust', 'Тот же вариант', 'Объявлен enum Shape { Circle(f64), Rect(f64, f64), Dot }. Напишите same_kind(a: &Shape, b: &Shape) -> bool: true, если у значений один вариант (mem::discriminant).', 'enum Shape {
    Circle(f64),
    Rect(f64, f64),
    Dot,
}

fn same_kind(a: &Shape, b: &Shape) -> bool {
    todo!()
}
', 'discriminant сравнивается через ==.', '{"driver": "fn main() {\n    println!(\"{}\", same_kind(&Shape::Circle(1.0), &Shape::Circle(9.0)));\n    println!(\"{}\", same_kind(&Shape::Circle(1.0), &Shape::Rect(1.0, 2.0)));\n    println!(\"{}\", same_kind(&Shape::Dot, &Shape::Dot));\n}\n", "expected": ["true", "false", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-float-bits', 25, 'rust', 'Биты числа с плавающей точкой', 'Напишите float_parts(x: f32) -> (u32, u32, u32): знак (0/1), смещённая экспонента (8 бит) и мантисса (23 бита) через to_bits.', 'fn float_parts(x: f32) -> (u32, u32, u32) {
    todo!()
}
', 'x.to_bits() — u32 с теми же битами.', '{"driver": "fn main() {\n    println!(\"{:?}\", float_parts(1.0));\n    println!(\"{:?}\", float_parts(-2.5));\n    println!(\"{:?}\", float_parts(0.0));\n    println!(\"{:?}\", float_parts(f32::INFINITY));\n}\n", "expected": ["(0, 127, 0)", "(1, 128, 2097152)", "(0, 0, 0)", "(0, 255, 0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-mem-take-state', 26, 'rust', 'Автомат и mem::replace', 'Объявлен enum State { Idle, Running(u32), Done(String) }. Напишите finish(s: &mut State) -> Option<u32>: если Running(n) — заменить на Done(«готово за n»), вернуть Some(n); иначе ничего не менять и вернуть None. Используйте mem::replace.', 'enum State {
    Idle,
    Running(u32),
    Done(String),
}

fn finish(s: &mut State) -> Option<u32> {
    todo!()
}
', 'Заберите значение через replace, затем запишите нужное состояние.', '{"driver": "fn main() {\n    let mut a = State::Running(5);\n    println!(\"{:?}\", finish(&mut a));\n    if let State::Done(t) = &a { println!(\"{}\", t); }\n    let mut b = State::Idle;\n    println!(\"{:?}\", finish(&mut b));\n    println!(\"{}\", matches!(b, State::Idle));\n}\n", "expected": ["Some(5)", "готово за 5", "None", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-leap-days', 27, 'rust', 'Дни между датами', 'Напишите days_between(y1: i64, m1: u32, d1: u32, y2: i64, m2: u32, d2: u32) -> i64: сколько дней от первой даты до второй по григорианскому календарю (отрицательное, если вторая раньше). Подсказка: переведите каждую дату в «номер дня» алгоритмом days_from_civil.', 'fn days_between(y1: i64, m1: u32, d1: u32, y2: i64, m2: u32, d2: u32) -> i64 {
    todo!()
}
', 'days_from_civil: сдвиг года для января и февраля, 400-летние эры.', '{"driver": "fn main() {\n    println!(\"{}\", days_between(2024, 1, 1, 2024, 12, 31));\n    println!(\"{}\", days_between(2000, 2, 28, 2000, 3, 1));\n    println!(\"{}\", days_between(1970, 1, 1, 2026, 10, 16));\n    println!(\"{}\", days_between(2026, 10, 16, 2026, 10, 1));\n}\n", "expected": ["365", "2", "20742", "-15"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-timeout-loop', 28, 'rust', 'Ждать с таймаутом', 'Напишите spin_for(limit: Duration) -> bool: в цикле проверяйте Instant::elapsed(), пока не пройдёт limit; верните true, если реально прошло не меньше limit (всегда true).', 'use std::time::Duration;

fn spin_for(limit: Duration) -> bool {
    todo!()
}
', 'while t.elapsed() < limit {}', '{"driver": "fn main() {\n    println!(\"{}\", spin_for(Duration::from_millis(20)));\n    println!(\"{}\", spin_for(Duration::ZERO));\n}\n", "expected": ["true", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 28, 'r28-system-time', 29, 'rust', 'Секунды с 1970 года', 'Напишите unix_now() -> u64: число секунд с начала 1970 года (SystemTime::now().duration_since(UNIX_EPOCH)); результат при проверке должен быть больше 1.7 миллиарда.', 'fn unix_now() -> u64 {
    todo!()
}
', 'duration_since возвращает Result — unwrap.', '{"driver": "fn main() {\n    let t = unix_now();\n    println!(\"{}\", t > 1_700_000_000);\n    println!(\"{}\", t < 4_000_000_000);\n}\n", "expected": ["true", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-clone-manual', 0, 'rust', 'Свой Clone', 'Структура Doc { title: String, version: u32 }. Реализуйте Clone вручную так, чтобы клон получал версию на единицу больше, а заголовок — тот же.', 'struct Doc {
    title: String,
    version: u32,
}

impl Clone for Doc {
    fn clone(&self) -> Doc {
        todo!()
    }
}
', 'Поля клонируем по отдельности, у version прибавляем единицу.', '{"driver": "fn main() {\n    let a = Doc { title: String::from(\"план\"), version: 1 };\n    let b = a.clone();\n    let c = b.clone();\n    println!(\"{} {} {}\", a.version, b.version, c.version);\n    println!(\"{}\", b.title);\n}\n", "expected": ["1 2 3", "план"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-copy-derive', 1, 'rust', 'Copy и Clone', 'Структура Point { x: i32, y: i32 }: добавьте derive так, чтобы значения копировались при присваивании (Copy, Clone) и печатались (Debug).', 'struct Point {
    x: i32,
    y: i32,
}
', '#[derive(Debug, Clone, Copy)]', '{"driver": "fn main() {\n    let a = Point { x: 1, y: 2 };\n    let b = a;\n    println!(\"{:?} {:?}\", a, b);\n}\n", "expected": ["Point { x: 1, y: 2 } Point { x: 1, y: 2 }"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-default-manual', 2, 'rust', 'Default вручную', 'Структура Settings { volume: u8, name: String, ratio: f64 }. Реализуйте Default вручную: громкость 50, имя «по умолчанию», коэффициент 1.5.', 'struct Settings {
    volume: u8,
    name: String,
    ratio: f64,
}

impl Default for Settings {
    fn default() -> Settings {
        todo!()
    }
}
', 'impl Default for Settings — функция default().', '{"driver": "fn main() {\n    let s = Settings::default();\n    println!(\"{} {} {}\", s.volume, s.name, s.ratio);\n    let t = Settings { volume: 10, ..Default::default() };\n    println!(\"{} {}\", t.volume, t.name);\n}\n", "expected": ["50 по умолчанию 1.5", "10 по умолчанию"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-partial-eq-cross', 3, 'rust', 'Равенство разных типов', 'Структуры Meters(f64) и Feet(f64). Реализуйте PartialEq<Feet> for Meters: равны, если значения совпадают с точностью до 0.001 (1 м = 3.28084 фута).', 'struct Meters(f64);
struct Feet(f64);

impl PartialEq<Feet> for Meters {
    fn eq(&self, other: &Feet) -> bool {
        todo!()
    }
}
', 'Сравнивайте после перевода в футы с допуском.', '{"driver": "fn main() {\n    println!(\"{}\", Meters(1.0) == Feet(3.28084));\n    println!(\"{}\", Meters(2.0) == Feet(3.0));\n    println!(\"{}\", Meters(0.0) != Feet(1.0));\n}\n", "expected": ["true", "false", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-ord-manual', 4, 'rust', 'Порядок задач', 'Структура Task { pri: u32, name: String }. Реализуйте Ord так, чтобы большая priority считалась «больше», а при равенстве — имя по алфавиту раньше считалось «больше» (обратный порядок имени). Добавьте PartialOrd, Eq, PartialEq.', 'use std::cmp::Ordering;

#[derive(PartialEq, Eq, Debug)]
struct Task {
    pri: u32,
    name: String,
}

impl Ord for Task {
    fn cmp(&self, other: &Task) -> Ordering {
        todo!()
    }
}

impl PartialOrd for Task {
    fn partial_cmp(&self, other: &Task) -> Option<Ordering> {
        todo!()
    }
}
', 'then(other.name.cmp(&self.name)) переворачивает порядок имён.', '{"driver": "fn main() {\n    use std::collections::BinaryHeap;\n    let mut h = BinaryHeap::new();\n    for (p, n) in [(2, \"b\"), (5, \"z\"), (5, \"a\"), (1, \"x\")] {\n        h.push(Task { pri: p, name: n.to_string() });\n    }\n    while let Some(t) = h.pop() {\n        print!(\"{}{} \", t.pri, t.name);\n    }\n    println!();\n}\n", "expected": ["5a 5z 2b 1x"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-hash-manual', 5, 'rust', 'Хеш без учёта регистра', 'Структура CiKey(String): равна другой без учёта регистра. Реализуйте PartialEq, Eq и Hash вручную согласованно (хешируйте строку в нижнем регистре), чтобы HashSet<CiKey> считал «Rust» и «rUST» одним ключом.', 'use std::hash::{Hash, Hasher};

struct CiKey(String);

impl PartialEq for CiKey {
    fn eq(&self, o: &CiKey) -> bool {
        todo!()
    }
}
impl Eq for CiKey {}
impl Hash for CiKey {
    fn hash<H: Hasher>(&self, h: &mut H) {
        todo!()
    }
}
', 'Хеш и равенство используют один и тот же приведённый ключ.', '{"driver": "fn main() {\n    use std::collections::HashSet;\n    let mut s = HashSet::new();\n    for w in [\"Rust\", \"rUST\", \"Go\", \"RUST\", \"go\"] {\n        s.insert(CiKey(w.to_string()));\n    }\n    println!(\"{}\", s.len());\n}\n", "expected": ["2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-from-tuple', 6, 'rust', 'From для структуры', 'Структура Rgb(u8, u8, u8). Реализуйте From<(u8, u8, u8)>, From<[u8; 3]> и From<Rgb> for u32 (0xRRGGBB).', 'struct Rgb(u8, u8, u8);

impl From<(u8, u8, u8)> for Rgb {
    fn from(t: (u8, u8, u8)) -> Rgb {
        todo!()
    }
}
impl From<[u8; 3]> for Rgb {
    fn from(a: [u8; 3]) -> Rgb {
        todo!()
    }
}
impl From<Rgb> for u32 {
    fn from(c: Rgb) -> u32 {
        todo!()
    }
}
', 'Сдвиги << 16 и << 8.', '{"driver": "fn main() {\n    let a: Rgb = (255, 128, 0).into();\n    let b = Rgb::from([1, 2, 3]);\n    let n: u32 = a.into();\n    println!(\"{:#08x}\", n);\n    println!(\"{}\", u32::from(b));\n}\n", "expected": ["0xff8000", "66051"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-try-from', 7, 'rust', 'TryFrom', 'Структура Percent(u8). Реализуйте TryFrom<i32> for Percent: Ok для 0..=100, иначе Err(String) «вне диапазона: <n>».', '#[derive(Debug, PartialEq)]
struct Percent(u8);

impl TryFrom<i32> for Percent {
    type Error = String;
    fn try_from(n: i32) -> Result<Percent, String> {
        todo!()
    }
}
', '(0..=100).contains(&n)', '{"driver": "fn main() {\n    println!(\"{:?}\", Percent::try_from(55));\n    println!(\"{:?}\", Percent::try_from(101));\n    let r: Result<Percent, _> = (-5).try_into();\n    println!(\"{:?}\", r);\n}\n", "expected": ["Ok(Percent(55))", "Err(\"вне диапазона: 101\")", "Err(\"вне диапазона: -5\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-as-ref', 8, 'rust', 'AsRef для обёртки', 'Структура Name(String). Реализуйте AsRef<str> for Name и напишите функцию shout(x: impl AsRef<str>) -> String (в верхнем регистре), которая принимает и &str, и String, и Name.', 'struct Name(String);

impl AsRef<str> for Name {
    fn as_ref(&self) -> &str {
        todo!()
    }
}

fn shout(x: impl AsRef<str>) -> String {
    todo!()
}
', '&self.0 — String приводится к &str.', '{"driver": "fn main() {\n    println!(\"{}\", shout(\"привет\"));\n    println!(\"{}\", shout(String::from(\"rust\")));\n    println!(\"{}\", shout(Name(String::from(\"аня\"))));\n}\n", "expected": ["ПРИВЕТ", "RUST", "АНЯ"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-deref', 9, 'rust', 'Deref для обёртки', 'Структура Stack(Vec<i32>). Реализуйте Deref<Target = Vec<i32>> и DerefMut, чтобы у Stack работали методы вектора len(), last(), push() напрямую.', 'struct Stack(Vec<i32>);

impl std::ops::Deref for Stack {
    type Target = Vec<i32>;
    fn deref(&self) -> &Vec<i32> {
        todo!()
    }
}
impl std::ops::DerefMut for Stack {
    fn deref_mut(&mut self) -> &mut Vec<i32> {
        todo!()
    }
}
', 'Верните ссылку на внутренний вектор.', '{"driver": "fn main() {\n    let mut s = Stack(vec![1, 2]);\n    s.push(3);\n    println!(\"{} {:?}\", s.len(), s.last());\n    println!(\"{}\", s.iter().sum::<i32>());\n}\n", "expected": ["3 Some(3)", "6"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-index', 10, 'rust', 'Index для сетки', 'Структура Grid { w: usize, cells: Vec<char> }. Реализуйте Index<(usize, usize)> и IndexMut<(usize, usize)>: g[(x, y)] — клетка в столбце x и строке y.', 'struct Grid {
    w: usize,
    cells: Vec<char>,
}

impl std::ops::Index<(usize, usize)> for Grid {
    type Output = char;
    fn index(&self, (x, y): (usize, usize)) -> &char {
        todo!()
    }
}
impl std::ops::IndexMut<(usize, usize)> for Grid {
    fn index_mut(&mut self, (x, y): (usize, usize)) -> &mut char {
        todo!()
    }
}
', 'Индекс в плоском векторе: y * w + x.', '{"driver": "fn main() {\n    let mut g = Grid { w: 3, cells: vec![''.''; 6] };\n    g[(1, 1)] = ''#'';\n    g[(2, 0)] = ''@'';\n    let s: String = g.cells.iter().collect();\n    println!(\"{}\", s);\n    println!(\"{}\", g[(1, 1)]);\n}\n", "expected": ["..@.#.", "#"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-iterator-impl', 11, 'rust', 'Свой Iterator: Range со шагом', 'Структура Stepper { cur: i32, end: i32, step: i32 } (step > 0). Реализуйте Iterator<Item = i32>: от cur до end (не включая) с шагом step.', 'struct Stepper {
    cur: i32,
    end: i32,
    step: i32,
}

impl Iterator for Stepper {
    type Item = i32;
    fn next(&mut self) -> Option<i32> {
        todo!()
    }
}
', 'Пока cur < end — отдаём и сдвигаем.', '{"driver": "fn main() {\n    let v: Vec<i32> = Stepper { cur: 0, end: 10, step: 3 }.collect();\n    println!(\"{:?}\", v);\n    println!(\"{}\", Stepper { cur: 5, end: 5, step: 1 }.count());\n    let s: i32 = Stepper { cur: 1, end: 100, step: 7 }.filter(|x| x % 2 == 0).sum();\n    println!(\"{}\", s);\n}\n", "expected": ["[0, 3, 6, 9]", "0", "350"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-into-iterator', 12, 'rust', 'IntoIterator для своей коллекции', 'Структура Bag { items: Vec<String> }. Реализуйте IntoIterator для Bag (по значению) и для &Bag (по ссылке), чтобы работали for x in bag и for x in &bag.', 'struct Bag {
    items: Vec<String>,
}

impl IntoIterator for Bag {
    type Item = String;
    type IntoIter = std::vec::IntoIter<String>;
    fn into_iter(self) -> Self::IntoIter {
        todo!()
    }
}
impl<''a> IntoIterator for &''a Bag {
    type Item = &''a String;
    type IntoIter = std::slice::Iter<''a, String>;
    fn into_iter(self) -> Self::IntoIter {
        todo!()
    }
}
', 'Делегируйте вектору: into_iter() и iter().', '{"driver": "fn main() {\n    let b = Bag { items: vec![String::from(\"a\"), String::from(\"bb\")] };\n    for x in &b {\n        print!(\"{} \", x.len());\n    }\n    println!();\n    let mut total = String::new();\n    for x in b {\n        total.push_str(&x);\n    }\n    println!(\"{}\", total);\n}\n", "expected": ["1 2", "abb"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-from-iterator', 13, 'rust', 'FromIterator', 'Структура Bag { items: Vec<String> }. Реализуйте FromIterator<&str> for Bag, чтобы коллект из итератора строк работал: let b: Bag = words.into_iter().collect();', 'struct Bag {
    items: Vec<String>,
}

impl<''a> FromIterator<&''a str> for Bag {
    fn from_iter<I: IntoIterator<Item = &''a str>>(it: I) -> Bag {
        todo!()
    }
}
', 'Соберите вектор String из итератора &str.', '{"driver": "fn main() {\n    let b: Bag = \"раз два три\".split('' '').collect();\n    println!(\"{:?}\", b.items);\n    let e: Bag = std::iter::empty().collect();\n    println!(\"{}\", e.items.len());\n}\n", "expected": ["[\"раз\", \"два\", \"три\"]", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-extend-sum', 14, 'rust', 'Extend и Sum', 'Структура Money(i64). Реализуйте std::iter::Sum for Money (сумма значений Money) и Extend<Money>… для упрощения — только Sum и Add (Money + Money).', 'use std::ops::Add;

#[derive(Debug, Clone, Copy, PartialEq)]
struct Money(i64);

impl Add for Money {
    type Output = Money;
    fn add(self, o: Money) -> Money {
        todo!()
    }
}
impl std::iter::Sum for Money {
    fn sum<I: Iterator<Item = Money>>(it: I) -> Money {
        todo!()
    }
}
', 'fold(Money(0), |a, b| a + b)', '{"driver": "fn main() {\n    let total: Money = [Money(100), Money(250), Money(-50)].into_iter().sum();\n    println!(\"{:?}\", total);\n    let z: Money = Vec::<Money>::new().into_iter().sum();\n    println!(\"{:?}\", z);\n}\n", "expected": ["Money(300)", "Money(0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-fn-param', 15, 'rust', 'Fn, FnMut, FnOnce', 'Напишите три функции: call_twice(f: impl Fn() -> i32) -> i32 (сумма двух вызовов), call_mut(mut f: impl FnMut()) — вызвать 3 раза, call_once(f: impl FnOnce() -> String) -> String — вызвать один раз.', 'fn call_twice(f: impl Fn() -> i32) -> i32 {
    todo!()
}

fn call_mut(mut f: impl FnMut()) {
    todo!()
}

fn call_once(f: impl FnOnce() -> String) -> String {
    todo!()
}
', 'FnOnce можно вызвать только один раз: f() без повторов.', '{"driver": "fn main() {\n    let k = 5;\n    println!(\"{}\", call_twice(|| k * 2));\n    let mut count = 0;\n    call_mut(|| count += 1);\n    println!(\"{}\", count);\n    let s = String::from(\"перемещено\");\n    println!(\"{}\", call_once(move || s));\n}\n", "expected": ["20", "3", "перемещено"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-boxed-fns', 16, 'rust', 'Список замыканий', 'Напишите compose_all(fs: Vec<Box<dyn Fn(i32) -> i32>>) -> Box<dyn Fn(i32) -> i32>: функция, применяющая все по порядку.', 'fn compose_all(fs: Vec<Box<dyn Fn(i32) -> i32>>) -> Box<dyn Fn(i32) -> i32> {
    todo!()
}
', 'Box::new(move |x| fs.iter().fold(x, |acc, f| f(acc)))', '{"driver": "fn main() {\n    let f = compose_all(vec![Box::new(|x| x + 1), Box::new(|x| x * 10), Box::new(|x| x - 3)]);\n    println!(\"{}\", f(4));\n    println!(\"{}\", f(0));\n    let id = compose_all(vec![]);\n    println!(\"{}\", id(7));\n}\n", "expected": ["47", "7", "7"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-error-source', 17, 'rust', 'Ошибка с причиной', 'Объявлены ConfigError { path: String, cause: std::num::ParseIntError }. Реализуйте Display («ошибка в <path>»), Error и source() (возвращает Some(&self.cause)).', 'use std::fmt;
use std::error::Error;

#[derive(Debug)]
struct ConfigError {
    path: String,
    cause: std::num::ParseIntError,
}

impl fmt::Display for ConfigError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}

impl Error for ConfigError {
    fn source(&self) -> Option<&(dyn Error + ''static)> {
        todo!()
    }
}
', 'source() возвращает Option<&dyn Error>.', '{"driver": "fn main() {\n    let cause = \"x\".parse::<i32>().unwrap_err();\n    let e = ConfigError { path: String::from(\"app.toml\"), cause };\n    println!(\"{}\", e);\n    println!(\"{}\", e.source().is_some());\n    println!(\"{}\", e.source().unwrap());\n    let b: Box<dyn Error> = Box::new(e);\n    println!(\"{}\", b);\n}\n", "expected": ["ошибка в app.toml", "true", "invalid digit found in string", "ошибка в app.toml"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-error-from', 18, 'rust', 'Объединение ошибок', 'Объявите enum AppError { Parse(std::num::ParseIntError), Neg(i64) } с From<ParseIntError>, Display и Error. Функция positive(s: &str) -> Result<i64, AppError> парсит число и возвращает Err(Neg(n)) для отрицательных.', 'use std::fmt;

#[derive(Debug)]
enum AppError {
    Parse(std::num::ParseIntError),
    Neg(i64),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}
impl std::error::Error for AppError {}
impl From<std::num::ParseIntError> for AppError {
    fn from(e: std::num::ParseIntError) -> AppError {
        todo!()
    }
}

fn positive(s: &str) -> Result<i64, AppError> {
    todo!()
}
', '? превращает ParseIntError в AppError через From.', '{"driver": "fn main() {\n    println!(\"{}\", positive(\"42\").unwrap());\n    println!(\"{}\", positive(\"-7\").unwrap_err());\n    println!(\"{}\", positive(\"abc\").unwrap_err());\n}\n", "expected": ["42", "отрицательное: -7", "разбор: invalid digit found in string"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-send-sync', 19, 'rust', 'Send и Sync', 'Напишите функции assert_send<T: Send>() и assert_sync<T: Sync>() (пустые, проверка при компиляции), а в main (driver) проверяется, что String и Vec<i32> — Send, а Arc<Mutex<i32>> — Send и Sync. Ваше решение — только объявления функций.', 'fn assert_send<T: Send>() {
    todo!()
}

fn assert_sync<T: Sync>() {
    todo!()
}
', 'Пустое тело: проверка происходит при подстановке типа.', '{"driver": "fn main() {\n    assert_send::<String>();\n    assert_send::<Vec<i32>>();\n    assert_send::<std::sync::Arc<std::sync::Mutex<i32>>>();\n    assert_sync::<std::sync::Arc<std::sync::Mutex<i32>>>();\n    assert_sync::<i32>();\n    println!(\"ok\");\n}\n", "expected": ["ok"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-any-downcast', 20, 'rust', 'Динамический тип', 'Напишите describe(v: &dyn std::any::Any) -> String: «целое N» для i32, «строка S» для String, «дробное X» для f64, иначе «неизвестно» (downcast_ref).', 'fn describe(v: &dyn std::any::Any) -> String {
    todo!()
}
', 'downcast_ref::<T>() возвращает Option<&T>.', '{"driver": "fn main() {\n    println!(\"{}\", describe(&5i32));\n    println!(\"{}\", describe(&String::from(\"привет\")));\n    println!(\"{}\", describe(&2.5f64));\n    println!(\"{}\", describe(&''c''));\n    println!(\"{}\", describe(&\"str\"));\n}\n", "expected": ["целое 5", "строка привет", "дробное 2.5", "неизвестно", "неизвестно"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-cow', 21, 'rust', 'Cow', 'Напишите normalize(s: &str) -> std::borrow::Cow<str>: если в строке есть табуляции, вернуть Owned с табуляциями, заменёнными пробелами, иначе — Borrowed без копирования. Driver проверяет вариант.', 'fn normalize(s: &str) -> std::borrow::Cow<str> {
    todo!()
}
', 'Cow::Borrowed(s) — без копирования; Cow::Owned(String).', '{"driver": "fn main() {\n    use std::borrow::Cow;\n    let a = normalize(\"a\\tb\");\n    let b = normalize(\"ab\");\n    println!(\"{} {}\", a, matches!(a, Cow::Owned(_)));\n    println!(\"{} {}\", b, matches!(b, Cow::Borrowed(_)));\n}\n", "expected": ["a b true", "ab true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-phantom', 22, 'rust', 'Типизированные идентификаторы', 'Структура Id<T> { n: u32, _m: PhantomData<T> }. Реализуйте new(n), get(&self) и Clone/Copy/PartialEq/Debug вручную без ограничений на T (derive потребовал бы Clone для T). Типы User и Order — пустые структуры. Сравнение Id<User> с Id<Order> не должно компилироваться (проверять нечем — просто используйте PhantomData).', 'use std::marker::PhantomData;

struct User;
struct Order;

struct Id<T> {
    n: u32,
    _m: PhantomData<T>,
}

impl<T> Id<T> {
    fn new(n: u32) -> Id<T> {
        todo!()
    }
    fn get(&self) -> u32 {
        todo!()
    }
}

impl<T> Clone for Id<T> {
    fn clone(&self) -> Id<T> {
        todo!()
    }
}
impl<T> Copy for Id<T> {}
impl<T> PartialEq for Id<T> {
    fn eq(&self, o: &Id<T>) -> bool {
        todo!()
    }
}
', 'PhantomData — значение без данных: Id { n, _m: PhantomData }.', '{"driver": "fn main() {\n    let u: Id<User> = Id::new(7);\n    let v = u;\n    let o: Id<Order> = Id::new(7);\n    println!(\"{} {}\", u.get(), u == v);\n    println!(\"{}\", o.get());\n}\n", "expected": ["7 true", "7"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-borrow-lookup', 23, 'rust', 'Borrow и поиск', 'Напишите find_len(m: &std::collections::HashMap<String, usize>, key: &str) -> usize: значение по ключу или 0 — поиск по &str в карте с ключом String (обоснование — трейт Borrow<str>).', 'fn find_len(m: &std::collections::HashMap<String, usize>, key: &str) -> usize {
    todo!()
}
', 'm.get(key) принимает &str, потому что String: Borrow<str>.', '{"driver": "fn main() {\n    let mut m = std::collections::HashMap::new();\n    m.insert(String::from(\"a\"), 5);\n    println!(\"{} {}\", find_len(&m, \"a\"), find_len(&m, \"b\"));\n}\n", "expected": ["5 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-display-debug', 24, 'rust', 'Display и Debug вместе', 'Структура Ver(u32, u32, u32). Реализуйте Display «1.2.3» и derive(Debug); функция show(v: &impl std::fmt::Display) -> String возвращает «версия <v>».', 'use std::fmt;

#[derive(Debug)]
struct Ver(u32, u32, u32);

impl fmt::Display for Ver {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}

fn show(v: &impl fmt::Display) -> String {
    todo!()
}
', 'Display даёт to_string() бесплатно.', '{"driver": "fn main() {\n    let v = Ver(1, 2, 3);\n    println!(\"{}\", show(&v));\n    println!(\"{:?}\", v);\n    println!(\"{}\", v.to_string());\n    println!(\"{}\", show(&42));\n}\n", "expected": ["версия 1.2.3", "Ver(1, 2, 3)", "1.2.3", "версия 42"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-generic-bound', 25, 'rust', 'Ограничения трейтов', 'Напишите largest_by_key<T, K: Ord>(items: &[T], key: impl Fn(&T) -> K) -> Option<&T>: элемент с наибольшим ключом (при равенстве — первый).', 'fn largest_by_key<T, K: Ord>(items: &[T], key: impl Fn(&T) -> K) -> Option<&T> {
    todo!()
}
', 'Заменяйте best только при строго большем ключе.', '{"driver": "fn main() {\n    let words = [\"aa\", \"bbbb\", \"c\", \"dddd\"];\n    println!(\"{:?}\", largest_by_key(&words, |w| w.len()));\n    println!(\"{:?}\", largest_by_key(&[3i32, -9, 5], |x| x.abs()));\n    println!(\"{:?}\", largest_by_key(&Vec::<i32>::new(), |x| *x));\n}\n", "expected": ["Some(\"bbbb\")", "Some(-9)", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-trait-assoc', 26, 'rust', 'Ассоциированный тип', 'Трейт Container { type Item; fn first(&self) -> Option<&Self::Item>; fn size(&self) -> usize; }. Реализуйте его для структуры Words(Vec<String>) (Item = String).', 'trait Container {
    type Item;
    fn first(&self) -> Option<&Self::Item>;
    fn size(&self) -> usize;
}

struct Words(Vec<String>);

impl Container for Words {
    type Item = String;
    fn first(&self) -> Option<&String> {
        todo!()
    }
    fn size(&self) -> usize {
        todo!()
    }
}
', 'type Item = String; делегируйте методы вектору.', '{"driver": "fn main() {\n    let w = Words(vec![String::from(\"a\"), String::from(\"b\")]);\n    println!(\"{:?} {}\", w.first(), w.size());\n    println!(\"{:?}\", Words(vec![]).first());\n}\n", "expected": ["Some(\"a\") 2", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-supertrait', 27, 'rust', 'Супертрейт', 'Трейт Named: fmt::Display + ... — объявите trait Entity: std::fmt::Display { fn id(&self) -> u32; fn label(&self) -> String { format!("#{} {}", self.id(), self) } }. Реализуйте Entity и Display для структуры Item { id: u32, name: String } (Display печатает имя).', 'use std::fmt;

trait Entity: fmt::Display {
    fn id(&self) -> u32;
    fn label(&self) -> String {
        format!("#{} {}", self.id(), self)
    }
}

struct Item {
    id: u32,
    name: String,
}

impl fmt::Display for Item {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        todo!()
    }
}
impl Entity for Item {
    fn id(&self) -> u32 {
        todo!()
    }
}
', 'Супертрейт гарантирует, что Display доступен внутри метода по умолчанию.', '{"driver": "fn main() {\n    let i = Item { id: 7, name: String::from(\"болт\") };\n    println!(\"{}\", i.label());\n    println!(\"{}\", i);\n}\n", "expected": ["#7 болт", "болт"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-blanket', 28, 'rust', 'Общая реализация', 'Трейт Shout { fn shout(&self) -> String; }. Реализуйте его сразу для всех типов, у которых есть Display (impl<T: Display> Shout for T): текст в верхнем регистре с «!».', 'use std::fmt::Display;

trait Shout {
    fn shout(&self) -> String;
}

impl<T: Display> Shout for T {
    fn shout(&self) -> String {
        todo!()
    }
}
', 'Общая реализация (blanket impl) действует для любого T: Display.', '{"driver": "fn main() {\n    println!(\"{}\", \"привет\".shout());\n    println!(\"{}\", 42.shout());\n    println!(\"{}\", 2.5.shout());\n    println!(\"{}\", String::from(\"ok\").shout());\n}\n", "expected": ["ПРИВЕТ!", "42!", "2.5!", "OK!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 29, 'r29-unsized', 29, 'rust', '?Sized', 'Напишите byte_len<T: ?Sized + AsRef<[u8]>>(x: &T) -> usize: длина в байтах для str, срезов и векторов (ослабление Sized позволяет принимать str и [u8] напрямую).', 'fn byte_len<T: ?Sized + AsRef<[u8]>>(x: &T) -> usize {
    todo!()
}
', 'x.as_ref().len(); T: ?Sized разрешает str и [u8].', '{"driver": "fn main() {\n    println!(\"{}\", byte_len(\"привет\"));\n    println!(\"{}\", byte_len(&b\"ab\"[..]));\n    println!(\"{}\", byte_len(&vec![1u8, 2, 3]));\n    println!(\"{}\", byte_len(&String::from(\"яя\")));\n}\n", "expected": ["12", "2", "3", "4"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-first-async', 0, 'rust', 'Первая async-функция', 'Напишите async fn greet(name: &str) -> String, возвращающую «Привет, <имя>!», и вызовите её с .await в main с атрибутом #[tokio::main]. Напечатайте результат для «Аня».

Ожидаемый вывод:
Привет, Аня!', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'async fn возвращает Future; .await внутри async main.', '{"crates": ["tokio"], "driver": "", "expected": ["Привет, Аня!"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-lazy', 1, 'rust', 'Future ленив', 'Создайте future f = work() (async fn work печатает «работа»), напечатайте «до», затем .await, затем «после». Ожидается: «до», «работа», «после» — вызов async fn сам ничего не печатает.

Ожидаемый вывод:
до
работа
после', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Тело выполняется только на .await.', '{"crates": ["tokio"], "driver": "", "expected": ["до", "работа", "после"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-order-await', 2, 'rust', 'Порядок выполнения', 'Две async fn a() и b() печатают «a» и «b». Вызовите их последовательно через .await: a, затем b, затем напечатайте «конец».

Ожидаемый вывод:
a
b
конец', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Последовательные .await выполняются один за другим.', '{"crates": ["tokio"], "driver": "", "expected": ["a", "b", "конец"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-return-value', 3, 'rust', 'Значения из async', 'async fn square(x: u64) -> u64 и async fn sum_squares(n: u64) -> u64, которая в цикле вызывает square(i).await для i от 1 до n. Напечатайте sum_squares(10) = 385.

Ожидаемый вывод:
385', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Внутри async fn можно вызывать другие async fn через .await.', '{"crates": ["tokio"], "driver": "", "expected": ["385"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-question-mark', 4, 'rust', '? в async', 'async fn parse_sum(a: &str, b: &str) -> Result<i32, std::num::ParseIntError>: разберите оба числа и сложите, используя ?. Напечатайте результаты для («2», «40»), («2», «x») — «Ok(42)» и признак ошибки «true».

Ожидаемый вывод:
Ok(42)
true', '#[tokio::main]
async fn main() {
    // ваш код
}
', '? работает в async fn, возвращающей Result.', '{"crates": ["tokio"], "driver": "", "expected": ["Ok(42)", "true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-sleep-order', 5, 'rust', 'Конкурентно: join!', 'Две задачи: «медленная» спит 60 мс и печатает «медленная», «быстрая» — 10 мс и печатает «быстрая». Запустите обе одновременно через tokio::join! и напечатайте «готово» после. Ожидается: «быстрая», «медленная», «готово».

Ожидаемый вывод:
быстрая
медленная
готово', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'join! запускает фьючеры вместе; порядок вывода определяется временем сна.', '{"crates": ["tokio"], "driver": "", "expected": ["быстрая", "медленная", "готово"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-join-results', 6, 'rust', 'join! и результаты', 'async fn fetch(id: u32, ms: u64) -> String: ждёт ms миллисекунд и возвращает «данные <id>». Запустите fetch(1, 30), fetch(2, 10), fetch(3, 20) через join! и напечатайте результаты в порядке аргументов (не времени завершения): «данные 1 / данные 2 / данные 3».

Ожидаемый вывод:
данные 1
данные 2
данные 3', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'join! возвращает кортеж результатов в порядке аргументов.', '{"crates": ["tokio"], "driver": "", "expected": ["данные 1", "данные 2", "данные 3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-gather-vec', 7, 'rust', 'gather для списка', 'Python: await asyncio.gather(*[f(i) for i in range(5)]). Запустите 5 одинаковых задач double(i) (async, спит (5 − i)·5 мс и возвращает 2i) через futures::future::join_all и напечатайте вектор результатов: [0, 2, 4, 6, 8].

Ожидаемый вывод:
[0, 2, 4, 6, 8]', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'join_all сохраняет порядок входных фьючеров.', '{"crates": ["tokio"], "driver": "", "expected": ["[0, 2, 4, 6, 8]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-try-join', 8, 'rust', 'try_join! останавливается на ошибке', 'Две async fn: ok_task() -> Result<u32, String> (возвращает Ok(1) после 10 мс) и bad_task() -> Result<u32, String> (Err("сбой") после 20 мс). Выполните их через tokio::try_join! и напечатайте результат: «Err("сбой")».

Ожидаемый вывод:
Err("сбой")', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'try_join! возвращает Err при первой ошибке.', '{"crates": ["tokio"], "driver": "", "expected": ["Err(\"сбой\")"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-spawn', 9, 'rust', 'spawn вместо create_task', 'Запустите через tokio::spawn задачу, которая спит 20 мс и возвращает 42. Тем временем main печатает «жду»; затем получите результат через .await хэндла (это Result): «жду», «42».

Ожидаемый вывод:
жду
42', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'JoinHandle<T>.await возвращает Result<T, JoinError>.', '{"crates": ["tokio"], "driver": "", "expected": ["жду", "42"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-spawn-many', 10, 'rust', 'Много задач', 'Запустите 100 задач spawn; задача i возвращает i·i. Соберите хэндлы в вектор, дождитесь всех по порядку и напечатайте сумму результатов 328350.

Ожидаемый вывод:
328350', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'async move переносит i внутрь задачи.', '{"crates": ["tokio"], "driver": "", "expected": ["328350"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-timeout', 11, 'rust', 'wait_for → timeout', 'Python: asyncio.wait_for(f(), 0.05). Запустите задачу, которая спит 200 мс, с tokio::time::timeout на 50 мс и напечатайте «таймаут»; затем быструю (10 мс) с тем же лимитом: «успех».

Ожидаемый вывод:
таймаут
успех', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'timeout возвращает Err(Elapsed), если время вышло.', '{"crates": ["tokio"], "driver": "", "expected": ["таймаут", "успех"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-select-first', 12, 'rust', 'Кто первый', 'Две задачи спят 30 и 70 мс. Через tokio::select! выведите имя первой завершившейся: «быстрая».

Ожидаемый вывод:
быстрая', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'select! выбирает первую готовую ветку и отменяет остальные.', '{"crates": ["tokio"], "driver": "", "expected": ["быстрая"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-spawn-blocking', 13, 'rust', 'spawn_blocking', 'Python: run_in_executor. Посчитайте в spawn_blocking сумму простых чисел до 20000 (простое — без делителей до √n) и напечатайте её: 21171191.

Ожидаемый вывод:
21171191', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'spawn_blocking возвращает JoinHandle; вычисление — в замыкании.', '{"crates": ["tokio"], "driver": "", "expected": ["21171191"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-block-on-bridge', 14, 'rust', 'Мост из обычного кода', 'В обычной fn main (без #[tokio::main]) создайте рантайм tokio::runtime::Runtime::new() и выполните rt.block_on(async { … }), в котором ждёте 10 мс и возвращаете «из async». Напечатайте результат.

Ожидаемый вывод:
из async', 'fn main() {
    // ваш код
}
', 'Runtime::new().unwrap().block_on(…).', '{"crates": ["tokio"], "driver": "", "expected": ["из async"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-futures-block-on', 15, 'rust', 'block_on из futures', 'Выполните async-блок без tokio: futures::executor::block_on. Блок складывает async-функции add(2, 3) и add(10, 20) и возвращает 35. Напечатайте результат.

Ожидаемый вывод:
35', 'use futures::executor::block_on;

fn main() {
    block_on(async {
        // ваш код
    });
}
', 'block_on запускает любой фьючер в текущем потоке.', '{"crates": ["tokio"], "driver": "", "expected": ["35"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-boxed-futures', 16, 'rust', 'Разные фьючеры в одном векторе', 'Соберите вектор из трёх фьючеров разных типов (async-блоки: возвращают 1, 2 и 3 после разных пауз) в Vec<Pin<Box<dyn Future<Output = i32>>>> и выполните join_all: [1, 2, 3].

Ожидаемый вывод:
[1, 2, 3]', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Box::pin(async { … }) даёт Pin<Box<dyn Future>>.', '{"crates": ["tokio"], "driver": "", "expected": ["[1, 2, 3]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-recursion-boxed', 17, 'rust', 'Рекурсивная async-функция', 'Напишите рекурсивную async-функцию fact(n: u64) -> u64 (через Box::pin(fact(n − 1)).await) и напечатайте fact(10) = 3628800.

Ожидаемый вывод:
3628800', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Рекурсивный async fn нужно упаковать в Box::pin: размер автомата иначе бесконечен.', '{"crates": ["tokio"], "driver": "", "expected": ["3628800"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-stream-basic', 18, 'rust', 'Поток значений', 'Python: async for. Из futures::stream::iter(1..=5) через StreamExt: .map(|x| x * x).filter(|x| ready(x % 2 == 1)).collect::<Vec<_>>().await — напечатайте [1, 9, 25].

Ожидаемый вывод:
[1, 9, 25]', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'StreamExt::filter принимает замыкание, возвращающее фьючер: ready(bool).', '{"crates": ["tokio"], "driver": "", "expected": ["[1, 9, 25]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-unordered', 19, 'rust', 'Порядок завершения', 'Python: asyncio.as_completed. Запустите в FuturesUnordered три задачи, спящие 30, 10 и 20 мс и возвращающие своё время, и выведите результаты в порядке завершения: 10, 20, 30.

Ожидаемый вывод:
10
20
30', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'FuturesUnordered выдаёт результаты по мере готовности.', '{"crates": ["tokio"], "driver": "", "expected": ["10", "20", "30"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-joinset', 20, 'rust', 'TaskGroup → JoinSet', 'Запустите в JoinSet пять задач, i-я спит (5 − i)·4 мс и возвращает i. Соберите результаты по мере завершения в вектор и напечатайте его отсортированным: [0, 1, 2, 3, 4], а также порядок завершения: [4, 3, 2, 1, 0].

Ожидаемый вывод:
[3, 4, 2, 1, 0]
[0, 1, 2, 3, 4]', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'set.join_next().await возвращает Option<Result<T, JoinError>>.', '{"crates": ["tokio"], "driver": "", "expected": ["[3, 4, 2, 1, 0]", "[0, 1, 2, 3, 4]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-panic-isolated', 21, 'rust', 'Паника в задаче', 'Запустите через spawn задачу, которая паникует (panic!("бум")), и вторую, возвращающую 7. Напечатайте: есть ли ошибка у первой (JoinError, is_panic) — «true» и значение второй — «7». Сообщение паники в stderr не проверяется.

Ожидаемый вывод:
true
7', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Паника изолируется в задаче и приходит как JoinError.', '{"crates": ["tokio"], "driver": "", "expected": ["true", "7"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-abort', 22, 'rust', 'Отмена задачи', 'Запустите задачу, которая бесконечно в цикле спит 5 мс и увеличивает общий AtomicUsize. Дождитесь в main, пока счётчик станет не меньше 2 (опрашивайте через sleep 5 мс), отмените задачу методом abort() и напечатайте: «отменено», затем is_cancelled у ошибки await — «true».

Ожидаемый вывод:
отменено
true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'abort() прерывает задачу на ближайшем .await.', '{"crates": ["tokio"], "driver": "", "expected": ["отменено", "true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-send-bound', 23, 'rust', 'Send и spawn', 'Напишите функцию run<F>(f: F) -> impl Future<Output = u32>, где F: Future<Output = u32> + Send + ''static и которая запускает f через tokio::spawn и ждёт результата (unwrap). Передайте async { 5 + 6 } и напечатайте 11.

Ожидаемый вывод:
11', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'spawn требует Send + ''static.', '{"crates": ["tokio"], "driver": "", "expected": ["11"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-async-block-move', 24, 'rust', 'async move и владение', 'Создайте String s = «привет», переместите её в async move-блок, который возвращает s.len(), выполните и напечатайте 12. После блока s недоступна (не используйте её).

Ожидаемый вывод:
12', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'async move забирает захваченные значения во владение.', '{"crates": ["tokio"], "driver": "", "expected": ["12"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-yield-now', 25, 'rust', 'Уступить управление', 'На однопоточном рантайме (#[tokio::main(flavor = "current_thread")]) запустите задачу, которая крутится в цикле «пока флаг done не поднят — yield_now().await», считает итерации и затем печатает «задача завершилась». Main даёт ей поработать одним yield_now, поднимает флаг (AtomicBool), ждёт задачу и печатает «итераций>=1: true».

Ожидаемый вывод:
задача завершилась
итераций>=1: true', '#[tokio::main(flavor = "current_thread")]
async fn main() {
    // ваш код
}
', 'На одном потоке задача не продвинется, пока main не уступит управление.', '{"crates": ["tokio"], "driver": "", "expected": ["задача завершилась", "итераций>=1: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-interval', 26, 'rust', 'Периодические события', 'Python: while True: await asyncio.sleep(…). Создайте tokio::time::interval(20 мс) и дождитесь четырёх тиков, замерив общее время: напечатайте «4 тика» и «время >= 60 мс: true» (первый тик срабатывает сразу).

Ожидаемый вывод:
4 тика
время >= 60 мс: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Первый tick() срабатывает сразу, остальные — через период.', '{"crates": ["tokio"], "driver": "", "expected": ["4 тика", "время >= 60 мс: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-mpsc-intro', 27, 'rust', 'Очередь между задачами', 'Python: asyncio.Queue. Создайте tokio::sync::mpsc::channel(8); задача-производитель отправляет числа 1…5 и завершается; main принимает через rx.recv().await до закрытия и печатает сумму 15.

Ожидаемый вывод:
15', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'recv возвращает None, когда все отправители уничтожены.', '{"crates": ["tokio"], "driver": "", "expected": ["15"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-mutex-intro', 28, 'rust', 'Общее состояние', 'Запустите 10 задач, каждая добавляет 100 раз по 1 в общий счётчик Arc<tokio::sync::Mutex<u32>>. Напечатайте итог 1000.

Ожидаемый вывод:
1000', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Arc клонируется в каждую задачу; lock().await возвращает guard.', '{"crates": ["tokio"], "driver": "", "expected": ["1000"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 30, 'r30-oneshot', 29, 'rust', 'Один ответ', 'Создайте oneshot-канал; задача отправляет «ответ» через 10 мс; main ждёт rx.await и печатает «получено: ответ».

Ожидаемый вывод:
получено: ответ', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'oneshot::channel() — один отправитель, один получатель, одно значение.', '{"crates": ["tokio"], "driver": "", "expected": ["получено: ответ"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-ready', 0, 'rust', 'Ready<T>', 'Напишите future-структуру Ready<T>(Option<T>) с реализацией Future<Output = T>: первый poll возвращает значение.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct Ready<T>(Option<T>);

impl<T: Unpin> Future for Ready<T> {
    type Output = T;
    fn poll(mut self: Pin<&mut Self>, _cx: &mut Context<''_>) -> Poll<T> {
        todo!()
    }
}
', 'self.0.take() достаёт значение из Option.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    println!(\"{}\", run(Ready(Some(5))));\n    println!(\"{}\", run(Ready(Some(String::from(\"привет\")))));\n    println!(\"{:?}\", polls(Ready(Some(1)), 3));\n}\n", "expected": ["5", "привет", "[Some(1)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-yield-once', 1, 'rust', 'YieldOnce', 'Напишите YieldOnce { done: bool }: первый poll вызывает cx.waker().wake_by_ref() и возвращает Pending, второй — Ready(()).', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct YieldOnce {
    done: bool,
}

impl Future for YieldOnce {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        todo!()
    }
}
', 'Состояние done меняется при первом опросе.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    println!(\"{:?}\", polls(YieldOnce { done: false }, 5));\n}\n", "expected": ["[None, Some(())]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-countdown', 2, 'rust', 'CountDown', 'Напишите CountDown(u32): пока счётчик больше нуля, каждый poll уменьшает его и возвращает Pending (с wake_by_ref), а когда ноль — Ready("поехали").', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct CountDown(u32);

impl Future for CountDown {
    type Output = &''static str;
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<&''static str> {
        todo!()
    }
}
', 'Перед Pending не забудьте wake_by_ref.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    println!(\"{:?}\", polls(CountDown(3), 10));\n    println!(\"{}\", run(CountDown(100)));\n    println!(\"{:?}\", polls(CountDown(0), 3));\n}\n", "expected": ["[None, None, None, Some(\"поехали\")]", "поехали", "[Some(\"поехали\")]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-poll-counter', 3, 'rust', 'Счётчик опросов', 'Напишите обёртку Counted<F> { inner: Pin<Box<F>>, polls: u32 }: каждый poll увеличивает polls и опрашивает inner; метод polls(&self) -> u32. Driver оборачивает CountDown и сообщает число опросов.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct CountDown(u32);
impl Future for CountDown {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        if self.0 == 0 {
            Poll::Ready(())
        } else {
            self.0 -= 1;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

struct Counted<F: Future> {
    inner: Pin<Box<F>>,
    polls: u32,
}

impl<F: Future> Counted<F> {
    fn new(f: F) -> Counted<F> {
        todo!()
    }
}

impl<F: Future> Future for Counted<F> {
    type Output = F::Output;
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<F::Output> {
        todo!()
    }
}
', 'inner: Pin<Box<F>> можно опрашивать через as_mut().poll(cx); структура Unpin (Pin<Box<…>> всегда Unpin), поэтому поля доступны через self.get_mut().', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    let mut c = Box::pin(Counted::new(CountDown(4)));\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut n = 0;\n    loop {\n        n += 1;\n        if c.as_mut().poll(&mut cx).is_ready() {\n            break;\n        }\n    }\n    println!(\"{} {}\", n, c.polls);\n}\n", "expected": ["5 5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-map', 4, 'rust', 'Map', 'Напишите комбинатор Map<F, G> { inner: Pin<Box<F>>, f: Option<G> }: poll опрашивает inner; когда готово — применяет функцию f (один раз) и возвращает результат.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct YieldOnce(bool);
impl Future for YieldOnce {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        if self.0 {
            Poll::Ready(())
        } else {
            self.0 = true;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

struct Map<F: Future, G> {
    inner: Pin<Box<F>>,
    f: Option<G>,
}

impl<F: Future, G: FnOnce(F::Output) -> T, T> Future for Map<F, G> {
    type Output = T;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<T> {
        todo!()
    }
}
', 'Результат inner передайте в f.take().unwrap().', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    let m = Map { inner: Box::pin(async { 20 }), f: Some(|x: i32| x + 1) };\n    println!(\"{}\", run(m));\n    let m2 = Map { inner: Box::pin(async { YieldOnce(false).await; \"слово\" }), f: Some(|s: &str| s.len()) };\n    println!(\"{:?}\", polls(m2, 5));\n}\n", "expected": ["21", "[None, Some(10)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-then', 5, 'rust', 'Последовательность', 'Напишите функцию-комбинатор then<A, B, FB>(a: A, f: impl FnOnce(A::Output) -> FB) -> impl Future<Output = B::Output>: сначала дождаться a, затем запустить фьючер, который вернёт f (async-блок).', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

fn then<A, FB, F>(a: A, f: F) -> impl Future<Output = FB::Output>
where
    A: Future,
    FB: Future,
    F: FnOnce(A::Output) -> FB,
{
    todo!()
}
', 'async move { let v = a.await; f(v).await }', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    let r = run(then(async { 5 }, |x| async move { x * 2 }));\n    println!(\"{}\", r);\n    let r2 = run(then(async { \"а\" }, |s| async move { format!(\"{}б\", s) }));\n    println!(\"{}\", r2);\n}\n", "expected": ["10", "аб"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-join2', 6, 'rust', 'Join2', 'Напишите Join2<A, B> { a: Pin<Box<A>>, b: Pin<Box<B>>, ra: Option<A::Output>, rb: Option<B::Output> }: poll опрашивает ещё не готовые части и возвращает пару, когда готовы обе.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct YieldOnce(bool);
impl Future for YieldOnce {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        if self.0 {
            Poll::Ready(())
        } else {
            self.0 = true;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

struct Join2<A: Future, B: Future> {
    a: Pin<Box<A>>,
    b: Pin<Box<B>>,
    ra: Option<A::Output>,
    rb: Option<B::Output>,
}

impl<A: Future, B: Future> Join2<A, B> {
    fn new(a: A, b: B) -> Self {
        Join2 { a: Box::pin(a), b: Box::pin(b), ra: None, rb: None }
    }
}

impl<A: Future, B: Future> Future for Join2<A, B>
where
    A::Output: Unpin,
    B::Output: Unpin,
{
    type Output = (A::Output, B::Output);
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<Self::Output> {
        todo!()
    }
}
', 'Опрашивайте только части без результата; пара — когда оба Some.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    let a = async { YieldOnce(false).await; 1 };\n    let b = async { YieldOnce(false).await; YieldOnce(false).await; \"два\" };\n    println!(\"{:?}\", polls(Join2::new(a, b), 6));\n    println!(\"{:?}\", run(Join2::new(async { 7 }, async { 8.5 })));\n}\n", "expected": ["[None, None, Some((1, \"два\"))]", "(7, 8.5)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-select2', 7, 'rust', 'Select2', 'Напишите Select2<A, B>: poll опрашивает a, затем b; возвращает Either::Left(значение a) или Either::Right(значение b) — того, кто готов раньше (при одновременной готовности — a).', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct YieldOnce(bool);
impl Future for YieldOnce {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        if self.0 {
            Poll::Ready(())
        } else {
            self.0 = true;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

#[derive(Debug)]
enum Either<L, R> {
    Left(L),
    Right(R),
}

struct Select2<A, B> {
    a: Pin<Box<A>>,
    b: Pin<Box<B>>,
}

impl<A: Future, B: Future> Future for Select2<A, B> {
    type Output = Either<A::Output, B::Output>;
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<Self::Output> {
        todo!()
    }
}
', 'Опрос a, затем b; первый Ready выигрывает.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    let slow = async { YieldOnce(false).await; YieldOnce(false).await; \"медленный\" };\n    let fast = async { YieldOnce(false).await; 42 };\n    let s = Select2 { a: Box::pin(slow), b: Box::pin(fast) };\n    println!(\"{:?}\", run(s));\n    let s2 = Select2 { a: Box::pin(async { 1 }), b: Box::pin(async { 2 }) };\n    println!(\"{:?}\", run(s2));\n}\n", "expected": ["Right(42)", "Left(1)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-block-on-noop', 8, 'rust', 'Свой block_on', 'Напишите block_on<F: Future>(f: F) -> F::Output: закрепите фьючер (Box::pin), создайте Context с Waker::noop() и опрашивайте в цикле, пока не будет готово.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

use std::task::Waker;

fn block_on<F: Future>(f: F) -> F::Output {
    todo!()
}
', 'Waker::noop() — вейкер-пустышка (Rust ≥ 1.85).', '{"driver": "fn main() {\n    println!(\"{}\", block_on(async { 1 + 2 }));\n    let r = block_on(async {\n        let mut s = 0;\n        for i in 0..100 {\n            s += i;\n        }\n        s\n    });\n    println!(\"{}\", r);\n}\n", "expected": ["3", "4950"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-block-on-park', 9, 'rust', 'block_on с park', 'Напишите block_on_park<F: Future>(f: F) -> F::Output: вейкер должен будить текущий поток (thread::unpark) — реализуйте трейт Wake для структуры со ссылкой на Thread; цикл после Pending вызывает thread::park().', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

use std::sync::Arc;
use std::task::{Wake, Waker};
use std::thread::{self, Thread};

struct ThreadWaker(Thread);

impl Wake for ThreadWaker {
    fn wake(self: Arc<Self>) {
        todo!()
    }
}

fn block_on_park<F: Future>(f: F) -> F::Output {
    todo!()
}
', 'ThreadWaker::wake — self.0.unpark(); цикл: Ready → return, Pending → park.', '{"driver": "fn main() {\n    use std::sync::{Arc, Mutex};\n    struct Late(Arc<Mutex<(bool, Option<std::task::Waker>)>>);\n    impl Future for Late {\n        type Output = u32;\n        fn poll(self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<u32> {\n            let mut g = self.0.lock().unwrap();\n            if g.0 {\n                Poll::Ready(77)\n            } else {\n                g.1 = Some(cx.waker().clone());\n                Poll::Pending\n            }\n        }\n    }\n    let st: Arc<Mutex<(bool, Option<std::task::Waker>)>> = Arc::new(Mutex::new((false, None)));\n    let st2 = st.clone();\n    std::thread::spawn(move || {\n        std::thread::sleep(std::time::Duration::from_millis(30));\n        let mut g = st2.lock().unwrap();\n        g.0 = true;\n        if let Some(w) = g.1.take() {\n            w.wake();\n        }\n    });\n    println!(\"{}\", block_on_park(Late(st)));\n    println!(\"{}\", block_on_park(async { 5 }));\n}\n", "expected": ["77", "5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-delay', 10, 'rust', 'Свой таймер', 'Напишите Delay { shared: Arc<Mutex<Shared>> }: new(ms) запускает поток, который через ms миллисекунд ставит флаг и будит сохранённый вейкер. poll: если флаг стоит — Ready(()), иначе сохраняет cx.waker().clone() и Pending.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

use std::sync::{Arc, Mutex};
use std::task::Waker;
use std::time::Duration;

struct Shared {
    done: bool,
    waker: Option<Waker>,
}

struct Delay {
    shared: Arc<Mutex<Shared>>,
}

impl Delay {
    fn new(ms: u64) -> Delay {
        todo!()
    }
}

impl Future for Delay {
    type Output = ();
    fn poll(self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        todo!()
    }
}
', 'Поток-таймер пишет в общее состояние и будит вейкер.', '{"driver": "fn main() {\n    use std::sync::Arc;\n    use std::task::{Wake, Waker};\n    struct W(std::thread::Thread);\n    impl Wake for W {\n        fn wake(self: Arc<Self>) {\n            self.0.unpark();\n        }\n    }\n    let waker = Waker::from(Arc::new(W(std::thread::current())));\n    let mut cx = Context::from_waker(&waker);\n    let start = std::time::Instant::now();\n    let mut d = Box::pin(Delay::new(40));\n    let mut pendings = 0;\n    loop {\n        match d.as_mut().poll(&mut cx) {\n            Poll::Ready(()) => break,\n            Poll::Pending => {\n                pendings += 1;\n                std::thread::park();\n            }\n        }\n    }\n    println!(\"pending>=1: {}\", pendings >= 1);\n    println!(\"прошло>=40мс: {}\", start.elapsed() >= std::time::Duration::from_millis(40));\n}\n", "expected": ["pending>=1: true", "прошло>=40мс: true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-oneshot-own', 11, 'rust', 'Свой oneshot', 'Реализуйте oneshot-канал: fn channel<T>() -> (Sender<T>, Receiver<T>); Sender::send(self, v) кладёт значение и будит вейкер получателя; Receiver — Future<Output = Option<T>> (None, если Sender уничтожен без отправки).', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

use std::sync::{Arc, Mutex};
use std::task::Waker;

struct Inner<T> {
    value: Option<T>,
    closed: bool,
    waker: Option<Waker>,
}

struct Sender<T>(Arc<Mutex<Inner<T>>>);
struct Receiver<T>(Arc<Mutex<Inner<T>>>);

fn channel<T>() -> (Sender<T>, Receiver<T>) {
    todo!()
}

impl<T> Sender<T> {
    fn send(self, v: T) {
        todo!()
    }
}

impl<T> Drop for Sender<T> {
    fn drop(&mut self) {
        todo!()
    }
}

impl<T> Future for Receiver<T> {
    type Output = Option<T>;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<Option<T>> {
        todo!()
    }
}
', 'Drop для Sender помечает канал закрытым и будит получателя.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    let (tx, rx) = channel::<i32>();\n    println!(\"{:?}\", polls(rx, 3));\n    let (tx2, rx2) = channel();\n    tx2.send(5);\n    println!(\"{:?}\", run(rx2));\n    let (tx3, rx3) = channel::<i32>();\n    drop(tx3);\n    println!(\"{:?}\", run(rx3));\n    drop(tx);\n}\n", "expected": ["[None, None, None]", "Some(5)", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-signal', 12, 'rust', 'Событие между потоками', 'Структура Signal { inner: Arc<Mutex<(bool, Option<Waker>)>> }: метод fire(&self) ставит флаг и будит; Signal клонируется (Clone) и является Future<Output = ()>. Driver опрашивает фьючер до и после fire.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

use std::sync::{Arc, Mutex};
use std::task::Waker;

#[derive(Clone)]
struct Signal {
    inner: Arc<Mutex<(bool, Option<Waker>)>>,
}

impl Signal {
    fn new() -> Signal {
        todo!()
    }
    fn fire(&self) {
        todo!()
    }
}

impl Future for Signal {
    type Output = ();
    fn poll(self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        todo!()
    }
}
', 'Флаг и вейкер под одним мьютексом.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    let s = Signal::new();\n    let mut f = Box::pin(s.clone());\n    let mut cx = Context::from_waker(Waker::noop());\n    println!(\"{:?}\", f.as_mut().poll(&mut cx));\n    s.fire();\n    println!(\"{:?}\", f.as_mut().poll(&mut cx));\n}\n", "expected": ["Pending", "Ready(())"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-counting-waker', 13, 'rust', 'Считающий waker', 'Реализуйте структуру CountWake { n: AtomicUsize } с трейтом Wake (wake и wake_by_ref увеличивают n). Driver создаёт Waker::from(arc), опрашивает YieldOnce и CountDown-подобные фьючеры и печатает число пробуждений.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct YieldOnce(bool);
impl Future for YieldOnce {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        if self.0 {
            Poll::Ready(())
        } else {
            self.0 = true;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::task::{Wake, Waker};

struct CountWake {
    n: AtomicUsize,
}

impl Wake for CountWake {
    fn wake(self: Arc<Self>) {
        todo!()
    }
    fn wake_by_ref(self: &Arc<Self>) {
        todo!()
    }
}
', 'n.fetch_add(1, Ordering::SeqCst) в обоих методах.', '{"driver": "fn main() {\n    let cw = Arc::new(CountWake { n: AtomicUsize::new(0) });\n    let waker = Waker::from(cw.clone());\n    let mut cx = Context::from_waker(&waker);\n    let mut a = Box::pin(YieldOnce(false));\n    let mut b = Box::pin(async { YieldOnce(false).await; YieldOnce(false).await; });\n    while a.as_mut().poll(&mut cx).is_pending() {}\n    while b.as_mut().poll(&mut cx).is_pending() {}\n    println!(\"{}\", cw.n.load(Ordering::SeqCst));\n    waker.wake_by_ref();\n    waker.clone().wake();\n    println!(\"{}\", cw.n.load(Ordering::SeqCst));\n}\n", "expected": ["3", "5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-poll-once', 14, 'rust', 'Один опрос', 'Напишите poll_once<F: Future + Unpin>(f: &mut F) -> Option<F::Output>: опросить фьючер один раз с Waker::noop(): Some(значение) при Ready, None при Pending.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

use std::task::Waker;

fn poll_once<F: Future + Unpin>(f: &mut F) -> Option<F::Output> {
    todo!()
}
', 'Pin::new(f) допустим для Unpin-фьючеров.', '{"driver": "fn main() {\n    struct Twice(u8);\n    impl Future for Twice {\n        type Output = &''static str;\n        fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<&''static str> {\n            if self.0 < 2 {\n                self.0 += 1;\n                cx.waker().wake_by_ref();\n                Poll::Pending\n            } else {\n                Poll::Ready(\"готово\")\n            }\n        }\n    }\n    let mut t = Twice(0);\n    println!(\"{:?}\", poll_once(&mut t));\n    println!(\"{:?}\", poll_once(&mut t));\n    println!(\"{:?}\", poll_once(&mut t));\n}\n", "expected": ["None", "None", "Some(\"готово\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-state-machine', 15, 'rust', 'Ручной автомат', 'Напишите вручную автомат TwoSteps, эквивалентный async { YieldOnce.await; YieldOnce.await; a + b } для a = 10 и b = 5: enum состояний Start, First, Second, Done; poll переходит от состояния к состоянию, возвращая Pending после каждого YieldOnce, и в конце Ready(15).', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

enum TwoSteps {
    Start,
    First,
    Second,
    Done,
}

impl Future for TwoSteps {
    type Output = i32;
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<i32> {
        todo!()
    }
}
', 'Каждое .await — переход в следующее состояние.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    println!(\"{:?}\", polls(TwoSteps::Start, 10));\n}\n", "expected": ["[None, None, Some(15)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-async-iter', 16, 'rust', 'Асинхронный итератор', 'Объявлен трейт AsyncIter { type Item; fn poll_next(self: Pin<&mut Self>, cx) -> Poll<Option<Item>> }. Реализуйте для Ticks { left: u32, yielded: bool }: поочерёдно Pending (один раз перед каждым элементом) и значение left, left−1, …, 1, затем Ready(None).', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

trait AsyncIter {
    type Item;
    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<Option<Self::Item>>;
}

struct Ticks {
    left: u32,
    yielded: bool,
}

impl AsyncIter for Ticks {
    type Item = u32;
    fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<Option<u32>> {
        todo!()
    }
}
', 'Pending перед каждым элементом, затем Some(left).', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    let mut t = Box::pin(Ticks { left: 3, yielded: false });\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut log = Vec::new();\n    loop {\n        match t.as_mut().poll_next(&mut cx) {\n            Poll::Ready(Some(v)) => log.push(format!(\"{}\", v)),\n            Poll::Ready(None) => {\n                log.push(String::from(\"конец\"));\n                break;\n            }\n            Poll::Pending => log.push(String::from(\"…\")),\n        }\n    }\n    println!(\"{}\", log.join(\" \"));\n}\n", "expected": ["… 3 … 2 … 1 конец"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-executor', 17, 'rust', 'Исполнитель с очередью', 'Напишите Executor { queue: VecDeque<Pin<Box<dyn Future<Output = ()>>>> }: spawn(fut) ставит задачу; run() по очереди опрашивает задачи (Waker::noop()), Pending-задачи возвращает в конец, пока очередь не опустеет.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct YieldOnce(bool);
impl Future for YieldOnce {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        if self.0 {
            Poll::Ready(())
        } else {
            self.0 = true;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

use std::collections::VecDeque;
use std::task::Waker;

struct Executor {
    queue: VecDeque<Pin<Box<dyn Future<Output = ()>>>>,
}

impl Executor {
    fn new() -> Executor {
        todo!()
    }
    fn spawn(&mut self, f: impl Future<Output = ()> + ''static) {
        todo!()
    }
    fn run(&mut self) {
        todo!()
    }
}
', 'Задача, вернувшая Pending, идёт в конец очереди.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    let mut ex = Executor::new();\n    ex.spawn(async { println!(\"a1\"); YieldOnce(false).await; println!(\"a2\"); });\n    ex.spawn(async { println!(\"b1\"); YieldOnce(false).await; println!(\"b2\"); YieldOnce(false).await; println!(\"b3\"); });\n    ex.spawn(async { println!(\"c1\"); });\n    ex.run();\n    println!(\"{}\", ex.queue.len());\n}\n", "expected": ["a1", "b1", "c1", "a2", "b2", "b3", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-run-all', 18, 'rust', 'Исполнитель с результатами', 'Напишите run_all<T>(futs: Vec<Pin<Box<dyn Future<Output = T>>>>) -> Vec<T>: по кругу опрашивайте не готовые фьючеры (Waker::noop()), результаты верните в порядке входа.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct YieldOnce(bool);
impl Future for YieldOnce {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        if self.0 {
            Poll::Ready(())
        } else {
            self.0 = true;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

use std::task::Waker;

fn run_all<T>(futs: Vec<Pin<Box<dyn Future<Output = T>>>>) -> Vec<T> {
    todo!()
}
', 'Хранить результаты в Vec<Option<T>> и считать оставшиеся.', '{"driver": "fn main() {\n    let mut v: Vec<Pin<Box<dyn Future<Output = String>>>> = Vec::new();\n    v.push(Box::pin(async { YieldOnce(false).await; YieldOnce(false).await; String::from(\"медленно\") }));\n    v.push(Box::pin(async { String::from(\"сразу\") }));\n    v.push(Box::pin(async { YieldOnce(false).await; String::from(\"средне\") }));\n    println!(\"{:?}\", run_all(v));\n    println!(\"{:?}\", run_all::<i32>(vec![]));\n}\n", "expected": ["[\"медленно\", \"сразу\", \"средне\"]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-timeout-polls', 19, 'rust', 'Таймаут по числу опросов', 'Напишите Timeout<F> { inner: Pin<Box<F>>, left: u32 }: каждый poll уменьшает left; если inner готов — Ok(значение); если left исчерпан, а inner Pending — Err("таймаут").', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct YieldOnce(bool);
impl Future for YieldOnce {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        if self.0 {
            Poll::Ready(())
        } else {
            self.0 = true;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

struct Timeout<F: Future> {
    inner: Pin<Box<F>>,
    left: u32,
}

impl<F: Future> Future for Timeout<F> {
    type Output = Result<F::Output, &''static str>;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<Self::Output> {
        todo!()
    }
}
', 'Сначала опросите inner; если Pending — проверьте оставшиеся попытки.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    let slow = async { for _ in 0..10 { YieldOnce(false).await; } 1 };\n    println!(\"{:?}\", run(Timeout { inner: Box::pin(slow), left: 3 }));\n    let fast = async { YieldOnce(false).await; 2 };\n    println!(\"{:?}\", run(Timeout { inner: Box::pin(fast), left: 3 }));\n}\n", "expected": ["Err(\"таймаут\")", "Ok(2)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-pin-macro', 20, 'rust', 'pin!', 'Напишите run_pinned<F: Future>(f: F) -> F::Output: закрепите фьючер на стеке макросом std::pin::pin! (без Box) и опрашивайте с Waker::noop() до готовности.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

use std::task::Waker;

fn run_pinned<F: Future>(f: F) -> F::Output {
    todo!()
}
', 'let mut f = std::pin::pin!(f); затем f.as_mut().poll(…).', '{"driver": "fn main() {\n    println!(\"{}\", run_pinned(async { 6 * 7 }));\n    println!(\"{}\", run_pinned(async {\n        struct Y(bool);\n        impl Future for Y {\n            type Output = ();\n            fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {\n                if self.0 { Poll::Ready(()) } else { self.0 = true; cx.waker().wake_by_ref(); Poll::Pending }\n            }\n        }\n        Y(false).await;\n        \"после Pending\"\n    }));\n}\n", "expected": ["42", "после Pending"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-size-of-future', 21, 'rust', 'Размер автомата', 'Напишите sizes() -> (usize, usize): size_of_val для двух async-блоков: small — просто возвращает 1; big — держит через .await массив [0u8; 1024]. Driver проверяет, что big ≥ 1024, а small < 64.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct YieldOnce(bool);
impl Future for YieldOnce {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        if self.0 {
            Poll::Ready(())
        } else {
            self.0 = true;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

fn sizes() -> (usize, usize) {
    todo!()
}
', 'size_of_val(&async_block) — размер автомата.', '{"driver": "fn main() {\n    let (s, b) = sizes();\n    println!(\"{} {}\", s < 64, b >= 1024);\n}\n", "expected": ["true true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-box-recursion', 22, 'rust', 'Рекурсия с Box::pin', 'Напишите sum_to(n: u64) -> Pin<Box<dyn Future<Output = u64>>>: сумма 1…n рекурсивным async-блоком (через .await на sum_to(n − 1)); sum_to(0) = 0.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

fn sum_to(n: u64) -> Pin<Box<dyn Future<Output = u64>>> {
    todo!()
}
', 'Рекурсивный async fn нельзя без упаковки: размер автомата был бы бесконечным.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    println!(\"{}\", run(sum_to(0)));\n    println!(\"{}\", run(sum_to(10)));\n    println!(\"{}\", run(sum_to(500)));\n}\n", "expected": ["0", "55", "125250"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-join-all', 23, 'rust', 'JoinAll', 'Напишите JoinAll<F: Future> { futs: Vec<Pin<Box<F>>>, results: Vec<Option<F::Output>> }: poll опрашивает не готовые и возвращает Vec результатов в порядке входа, когда все готовы.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct YieldOnce(bool);
impl Future for YieldOnce {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        if self.0 {
            Poll::Ready(())
        } else {
            self.0 = true;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

struct JoinAll<F: Future> {
    futs: Vec<Pin<Box<F>>>,
    results: Vec<Option<F::Output>>,
}

impl<F: Future> JoinAll<F> {
    fn new(v: Vec<F>) -> Self {
        let n = v.len();
        JoinAll { futs: v.into_iter().map(Box::pin).collect(), results: (0..n).map(|_| None).collect() }
    }
}

impl<F: Future> Future for JoinAll<F> {
    type Output = Vec<F::Output>;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<Vec<F::Output>> {
        todo!()
    }
}
', 'Если все части готовы — собираем результаты в порядке входа.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    let fs: Vec<Pin<Box<dyn Future<Output = usize>>>> = (0..4usize)\n        .map(|i| -> Pin<Box<dyn Future<Output = usize>>> {\n            Box::pin(async move {\n                for _ in 0..(4 - i) {\n                    YieldOnce(false).await;\n                }\n                i * 10\n            })\n        })\n        .collect();\n    println!(\"{:?}\", run(JoinAll::new(fs)));\n    println!(\"{:?}\", run(JoinAll::new(Vec::<std::future::Ready<i32>>::new())));\n}\n", "expected": ["[0, 10, 20, 30]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-async-trait', 24, 'rust', 'async fn в трейте', 'Объявите trait Source { async fn get(&self) -> u32; }; реализуйте для Const(u32) (возвращает число) и Delayed(u32) (один YieldOnce, затем число). Функция total(a: &impl Source, b: &impl Source) -> u32 складывает результаты.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct YieldOnce(bool);
impl Future for YieldOnce {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        if self.0 {
            Poll::Ready(())
        } else {
            self.0 = true;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

trait Source {
    async fn get(&self) -> u32;
}

struct Const(u32);
struct Delayed(u32);

impl Source for Const {
    async fn get(&self) -> u32 {
        todo!()
    }
}

impl Source for Delayed {
    async fn get(&self) -> u32 {
        todo!()
    }
}

async fn total(a: &impl Source, b: &impl Source) -> u32 {
    todo!()
}
', 'async fn в трейтах стабильны (Rust ≥ 1.75).', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    println!(\"{}\", run(total(&Const(3), &Delayed(4))));\n    println!(\"{:?}\", polls(total(&Delayed(1), &Delayed(2)), 5));\n}\n", "expected": ["7", "[None, None, Some(3)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-drop-on-cancel', 25, 'rust', 'Отмена = drop', 'Структура Job { name: String, steps: u32 } — Future<Output = ()>: каждый poll уменьшает steps и возвращает Pending; при steps == 0 — Ready. Реализуйте Drop: печатает «drop <имя> (steps=<осталось>)». Driver опрашивает Job один раз и отбрасывает его.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct Job {
    name: String,
    steps: u32,
}

impl Future for Job {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {
        todo!()
    }
}

impl Drop for Job {
    fn drop(&mut self) {
        todo!()
    }
}
', 'Drop вызывается и при отмене, и при нормальном завершении.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    let mut j = Box::pin(Job { name: String::from(\"A\"), steps: 3 });\n    let mut cx = Context::from_waker(Waker::noop());\n    println!(\"{:?}\", j.as_mut().poll(&mut cx));\n    drop(j);\n    run(Job { name: String::from(\"B\"), steps: 2 });\n    println!(\"конец\");\n}\n", "expected": ["Pending", "drop A (steps=2)", "drop B (steps=0)", "конец"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-fuse', 26, 'rust', 'Fuse', 'Напишите Fuse<F> { inner: Option<Pin<Box<F>>> }: после того как inner вернул Ready, дальнейшие poll возвращают Pending (а не паникуют): внутренний фьючер удаляется.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct Fuse<F: Future> {
    inner: Option<Pin<Box<F>>>,
}

impl<F: Future> Future for Fuse<F> {
    type Output = F::Output;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<F::Output> {
        todo!()
    }
}
', 'После Ready заменяем inner на None.', '{"driver": "use std::future::Future;\nuse std::pin::Pin;\nuse std::task::{Context, Poll, Waker};\n\nfn run<F: Future>(f: F) -> F::Output {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    loop {\n        if let Poll::Ready(v) = f.as_mut().poll(&mut cx) {\n            return v;\n        }\n    }\n}\n\n/// Опросить фьючер не более n раз и вернуть результаты опросов (None = Pending).\nfn polls<F: Future>(f: F, n: usize) -> Vec<Option<F::Output>> {\n    let mut f = Box::pin(f);\n    let mut cx = Context::from_waker(Waker::noop());\n    let mut out = Vec::new();\n    for _ in 0..n {\n        match f.as_mut().poll(&mut cx) {\n            Poll::Ready(v) => {\n                out.push(Some(v));\n                break;\n            }\n            Poll::Pending => out.push(None),\n        }\n    }\n    out\n}\n\nfn main() {\n    let mut f = Box::pin(Fuse { inner: Some(Box::pin(async { 5 })) });\n    let mut cx = Context::from_waker(Waker::noop());\n    println!(\"{:?}\", f.as_mut().poll(&mut cx));\n    println!(\"{:?}\", f.as_mut().poll(&mut cx));\n    println!(\"{:?}\", f.as_mut().poll(&mut cx));\n}\n", "expected": ["Ready(5)", "Pending", "Pending"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-will-wake', 27, 'rust', 'Не клонировать лишний раз', 'Структура WakerSlot { w: Option<Waker> } с методом register(&mut self, new: &Waker) -> bool: если сохранённый вейкер не будит ту же задачу (will_wake) — заменить на клон и вернуть true; иначе false (без клонирования).', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

use std::task::Waker;

struct WakerSlot {
    w: Option<Waker>,
}

impl WakerSlot {
    fn register(&mut self, new: &Waker) -> bool {
        todo!()
    }
}
', 'Waker::will_wake сообщает, будят ли два вейкера одну задачу.', '{"driver": "fn main() {\n    use std::sync::Arc;\n    use std::task::Wake;\n    struct A;\n    impl Wake for A {\n        fn wake(self: Arc<Self>) {}\n    }\n    let w1 = Waker::from(Arc::new(A));\n    let w2 = w1.clone();\n    let w3 = Waker::from(Arc::new(A));\n    let mut slot = WakerSlot { w: None };\n    println!(\"{}\", slot.register(&w1));\n    println!(\"{}\", slot.register(&w2));\n    println!(\"{}\", slot.register(&w3));\n}\n", "expected": ["true", "false", "true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-wake-executor', 28, 'rust', 'Исполнитель с вейкерами', 'Напишите настоящий исполнитель: Executor { tx: SyncSender<Arc<Task>>, rx: Receiver<Arc<Task>> }. Task { fut: Mutex<Option<Pin<Box<dyn Future<Output = ()> + Send>>>>, tx: SyncSender<Arc<Task>> }; spawn создаёт задачу и отправляет в очередь; Wake для Task отправляет себя в очередь; run() обрабатывает очередь, пока не придёт сигнал (drop внешнего tx) и задачи не закончатся.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

use std::sync::mpsc::{sync_channel, Receiver, SyncSender};
use std::sync::{Arc, Mutex};
use std::task::{Wake, Waker};

struct Task {
    fut: Mutex<Option<Pin<Box<dyn Future<Output = ()> + Send>>>>,
    tx: SyncSender<Arc<Task>>,
}

impl Wake for Task {
    fn wake(self: Arc<Self>) {
        todo!()
    }
}

struct Executor {
    rx: Receiver<Arc<Task>>,
    tx: SyncSender<Arc<Task>>,
}

impl Executor {
    fn new() -> Executor {
        todo!()
    }
    fn spawn(&self, f: impl Future<Output = ()> + Send + ''static) {
        todo!()
    }
    fn run(self) {
        todo!()
    }
}
', 'Очередь — sync_channel; run: drop(self.tx), чтобы цикл закончился, когда все задачи отдадут свои копии tx.', '{"driver": "fn main() {\n    struct Y(bool);\n    impl Future for Y {\n        type Output = ();\n        fn poll(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<()> {\n            if self.0 {\n                Poll::Ready(())\n            } else {\n                self.0 = true;\n                cx.waker().wake_by_ref();\n                Poll::Pending\n            }\n        }\n    }\n    let ex = Executor::new();\n    ex.spawn(async { println!(\"a1\"); Y(false).await; println!(\"a2\"); });\n    ex.spawn(async { println!(\"b1\"); Y(false).await; println!(\"b2\"); });\n    ex.run();\n    println!(\"конец\");\n}\n", "expected": ["a1", "b1", "a2", "b2", "конец"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 31, 'r31-collect-async', 29, 'rust', 'Собрать асинхронный итератор', 'Объявлен trait AsyncIter. Напишите collect_all<S: AsyncIter + Unpin>(mut s: S) -> Vec<S::Item>: опрашивайте poll_next с Waker::noop() в цикле (Pending пропускайте) до None.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

use std::task::Waker;

trait AsyncIter {
    type Item;
    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<Option<Self::Item>>;
}

fn collect_all<S: AsyncIter + Unpin>(mut s: S) -> Vec<S::Item> {
    todo!()
}
', 'Pin::new(&mut s) допустим, потому что S: Unpin.', '{"driver": "fn main() {\n    struct Evens {\n        cur: u32,\n        end: u32,\n        flip: bool,\n    }\n    impl AsyncIter for Evens {\n        type Item = u32;\n        fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<''_>) -> Poll<Option<u32>> {\n            if self.cur > self.end {\n                return Poll::Ready(None);\n            }\n            self.flip = !self.flip;\n            if self.flip {\n                cx.waker().wake_by_ref();\n                return Poll::Pending;\n            }\n            let v = self.cur;\n            self.cur += 2;\n            Poll::Ready(Some(v))\n        }\n    }\n    println!(\"{:?}\", collect_all(Evens { cur: 0, end: 10, flip: false }));\n    println!(\"{:?}\", collect_all(Evens { cur: 5, end: 1, flip: false }));\n}\n", "expected": ["[0, 2, 4, 6, 8, 10]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-desugar', 0, 'rust', 'Десахаринг async fn', 'Напишите функцию double(x: u32) -> impl Future<Output = u32> без ключевого слова async в сигнатуре: тело — async move-блок, возвращающий x * 2.', 'use std::future::Future;

fn double(x: u32) -> impl Future<Output = u32> {
    todo!()
}
', 'async fn f(x) -> T ≈ fn f(x) -> impl Future<Output = T> { async move { … } }.', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    println!(\"{}\", double(21).await);\n    let f = double(5);\n    println!(\"{}\", f.await + double(1).await);\n}\n", "expected": ["42", "12"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-lifetime-future', 1, 'rust', 'Время жизни фьючера', 'Напишите fn longer<''a>(a: &''a str, b: &''a str) -> impl Future<Output = &''a str> + ''a: async-блок возвращает более длинную строку (по числу символов; при равенстве — a).', 'use std::future::Future;

fn longer<''a>(a: &''a str, b: &''a str) -> impl Future<Output = &''a str> + ''a {
    todo!()
}
', 'Время жизни ''a входит в тип фьючера.', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    let x = String::from(\"привет\");\n    let y = String::from(\"мир\");\n    println!(\"{}\", longer(&x, &y).await);\n    println!(\"{}\", longer(\"ab\", \"cd\").await);\n}\n", "expected": ["привет", "ab"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-block-question', 2, 'rust', '? в async-блоке', 'Выполните async-блок, разбирающий «12» и «30» в числа с ? и возвращающий их сумму. Тип ошибки блока нужно указать: Ok::<i32, std::num::ParseIntError>(…). Напечатайте «Ok(42)»; затем то же для «12» и «x» — «true» (признак ошибки).

Ожидаемый вывод:
Ok(42)
true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Ok::<T, E>(…) подсказывает компилятору тип ошибки.', '{"crates": ["tokio"], "driver": "", "expected": ["Ok(42)", "true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-ref-across-await', 3, 'rust', 'Ссылка через .await', 'Напишите async fn sum_with_yield(v: &[i32]) -> i32: суммируйте элементы, на каждом шаге делая tokio::task::yield_now().await (ссылка на срез живёт через .await).', 'async fn sum_with_yield(v: &[i32]) -> i32 {
    todo!()
}
', 'Срез-параметр — ссылка; фьючер живёт, пока она действительна.', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    let v = vec![1, 2, 3, 4];\n    println!(\"{}\", sum_with_yield(&v).await);\n    println!(\"{}\", sum_with_yield(&v[1..3]).await);\n    println!(\"{}\", sum_with_yield(&[]).await);\n}\n", "expected": ["10", "5", "0"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-box-future', 4, 'rust', 'BoxFuture', 'Напишите fn make(n: u32) -> BoxFuture<''static, u32> (futures::future::BoxFuture): фьючер, который засыпает n мс и возвращает n·n. Затем driver собирает вектор таких фьючеров и выполняет join_all.', 'use futures::future::BoxFuture;

fn make(n: u32) -> BoxFuture<''static, u32> {
    todo!()
}
', 'Box::pin(async move { … }) подходит под BoxFuture.', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    let v: Vec<BoxFuture<u32>> = (1..=4).map(make).collect();\n    println!(\"{:?}\", futures::future::join_all(v).await);\n}\n", "expected": ["[1, 4, 9, 16]"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-pin-new', 5, 'rust', 'Pin::new для Unpin', 'Напишите poll_ready_now<F: Future + Unpin>(f: &mut F) -> Option<F::Output>: один опрос с Waker::noop() через Pin::new(f); None при Pending.', 'use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll, Waker};

fn poll_ready_now<F: Future + Unpin>(f: &mut F) -> Option<F::Output> {
    todo!()
}
', 'ready() и pending() из futures — Unpin.', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    let mut r = futures::future::ready(5);\n    println!(\"{:?}\", poll_ready_now(&mut r));\n    let mut p = futures::future::pending::<i32>();\n    println!(\"{:?}\", poll_ready_now(&mut p));\n}\n", "expected": ["Some(5)", "None"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-pin-select-loop', 6, 'rust', 'pin! и повторный select!', 'Закрепите макросом tokio::pin! долгий фьючер (сон 100 мс, возвращает «готово») и в цикле select! ждите либо его (&mut fut), либо тик interval(30 мс). Считайте тики, пока не придёт «готово». Напечатайте «готово» и «тиков>=2: true».

Ожидаемый вывод:
готово
тиков>=2: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', '&mut fut в select! не отменяет фьючер на повторных итерациях.', '{"crates": ["tokio"], "driver": "", "expected": ["готово", "тиков>=2: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-pin-mut-api', 7, 'rust', 'Pin<&mut T>', 'Структура Counter { n: u32 } (Unpin). Напишите fn bump(mut p: Pin<&mut Counter>): увеличить n на 1 через p.as_mut().get_mut().', 'use std::pin::Pin;

struct Counter {
    n: u32,
}

fn bump(mut p: Pin<&mut Counter>) {
    todo!()
}
', 'get_mut доступен только для Unpin-типов.', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    let mut c = Counter { n: 0 };\n    bump(Pin::new(&mut c));\n    bump(Pin::new(&mut c));\n    let mut b = Box::pin(Counter { n: 10 });\n    bump(b.as_mut());\n    println!(\"{} {}\", c.n, b.n);\n}\n", "expected": ["2 11"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-poll-fn', 8, 'rust', 'poll_fn', 'Напишите fn countdown(mut n: u32) -> impl Future<Output = &''static str> через std::future::poll_fn: пока n > 0 — уменьшить, wake_by_ref и Pending; затем Ready("пуск"). Driver считает число опросов.', 'use std::future::{poll_fn, Future};
use std::task::Poll;

fn countdown(mut n: u32) -> impl Future<Output = &''static str> {
    poll_fn(move |cx| {
        todo!()
    })
}
', 'poll_fn превращает замыкание в Future.', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    println!(\"{}\", countdown(5).await);\n    use std::sync::atomic::{AtomicUsize, Ordering};\n    static POLLS: AtomicUsize = AtomicUsize::new(0);\n    let f = std::future::poll_fn(|cx| { POLLS.fetch_add(1, Ordering::SeqCst); cx.waker().wake_by_ref(); if POLLS.load(Ordering::SeqCst) < 4 { std::task::Poll::Pending } else { std::task::Poll::Ready(()) } });\n    f.await;\n    println!(\"{}\", POLLS.load(Ordering::SeqCst));\n}\n", "expected": ["пуск", "4"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-pending-timeout', 9, 'rust', 'ready и pending', 'Покажите: tokio::time::timeout(50 мс) над std::future::pending::<u8>() даёт Err — напечатайте «таймаут»; над std::future::ready(7) даёт Ok(7) — «7».

Ожидаемый вывод:
таймаут
7', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'pending никогда не завершается; ready завершается сразу.', '{"crates": ["tokio"], "driver": "", "expected": ["таймаут", "7"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-into-future', 10, 'rust', 'IntoFuture', 'Структура Request { url: String } реализует std::future::IntoFuture так, чтобы Request::new("x").await возвращал «ответ от x» (Output = String; IntoFuture = Pin<Box<dyn Future<Output = String>>>; внутри — sleep 5 мс).', 'use std::future::{Future, IntoFuture};
use std::pin::Pin;

struct Request {
    url: String,
}

impl Request {
    fn new(u: &str) -> Request {
        Request { url: u.to_string() }
    }
}

impl IntoFuture for Request {
    type Output = String;
    type IntoFuture = Pin<Box<dyn Future<Output = String>>>;
    fn into_future(self) -> Self::IntoFuture {
        todo!()
    }
}
', 'await вызывает into_future для типа, реализующего IntoFuture.', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    println!(\"{}\", Request::new(\"a.ru\").await);\n    let (x, y) = tokio::join!(Request::new(\"1\"), Request::new(\"2\"));\n    println!(\"{} / {}\", x, y);\n}\n", "expected": ["ответ от a.ru", "ответ от 1 / ответ от 2"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-async-closure', 11, 'rust', 'Async-замыкание', 'Напишите async fn apply_all(items: &[i32], f: impl AsyncFn(i32) -> i32) -> Vec<i32>: применить f к каждому элементу последовательно (с .await). В driver передаются async-замыкания (Rust ≥ 1.85).', 'async fn apply_all(items: &[i32], f: impl AsyncFn(i32) -> i32) -> Vec<i32> {
    todo!()
}
', 'Ограничение impl AsyncFn(i32) -> i32; вызов f(x).await.', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    let k = 10;\n    let r = apply_all(&[1, 2, 3], async |x| {\n        tokio::task::yield_now().await;\n        x * k\n    })\n    .await;\n    println!(\"{:?}\", r);\n    println!(\"{:?}\", apply_all(&[], async |x| x).await);\n}\n", "expected": ["[10, 20, 30]", "[]"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-closure-future', 12, 'rust', 'Замыкание, возвращающее фьючер', 'Напишите fn make_adder(k: i32) -> impl Fn(i32) -> Pin<Box<dyn Future<Output = i32>>>: замыкание, которое для x возвращает упакованный фьючер x + k (после yield_now).', 'use std::future::Future;
use std::pin::Pin;

fn make_adder(k: i32) -> impl Fn(i32) -> Pin<Box<dyn Future<Output = i32>>> {
    todo!()
}
', 'Замыкание move, внутри — Box::pin(async move { … }).', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    let add5 = make_adder(5);\n    println!(\"{}\", add5(1).await);\n    println!(\"{}\", add5(10).await);\n    let r = futures::future::join_all((0..3).map(|i| add5(i))).await;\n    println!(\"{:?}\", r);\n}\n", "expected": ["6", "15", "[5, 6, 7]"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-spawn-arc', 13, 'rust', 'Данные для задач: Arc', 'Разделите вектор 1..=1000 на 4 части (по 250), посчитайте сумму каждой в отдельной задаче spawn (данные — Arc<Vec<u64>>, диапазон — копия индексов), сложите результаты: 500500.

Ожидаемый вывод:
500500', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Arc::clone в каждую задачу; async move забирает клон.', '{"crates": ["tokio"], "driver": "", "expected": ["500500"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-fix-static', 14, 'rust', 'Исправьте: ''static в spawn', 'Программа не собирается: задача spawn использует ссылку на локальную переменную. Исправьте так, чтобы она печатала «длина 6».

Ожидаемый вывод:
длина 6', '#[tokio::main]
async fn main() {
    let s = String::from("привет");
    let h = tokio::spawn(async {
        println!("длина {}", s.chars().count());
    });
    h.await.unwrap();
}
', 'Добавьте move и отдайте строку в задачу.', '{"crates": ["tokio"], "driver": "", "expected": ["длина 6"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-fix-send-guard', 15, 'rust', 'Исправьте: guard через .await', 'Программа не собирается: std::sync::MutexGuard удерживается через .await, и фьючер перестаёт быть Send. Исправьте (освободите guard до .await), чтобы напечатать «счётчик 3».

Ожидаемый вывод:
счётчик 3', 'use std::sync::{Arc, Mutex};

#[tokio::main]
async fn main() {
    let c = Arc::new(Mutex::new(0));
    let c2 = c.clone();
    tokio::spawn(async move {
        for _ in 0..3 {
            let mut g = c2.lock().unwrap();
            *g += 1;
            tokio::time::sleep(std::time::Duration::from_millis(5)).await;
        }
    })
    .await
    .unwrap();
    println!("счётчик {}", c.lock().unwrap());
}
', 'Заключите lock() в отдельный блок { … } перед .await.', '{"crates": ["tokio"], "driver": "", "expected": ["счётчик 3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-fix-rc', 16, 'rust', 'Исправьте: Rc в задаче', 'Rc не Send, поэтому spawn не принимает такую задачу. Замените Rc на Arc, чтобы напечатать «сумма 6».

Ожидаемый вывод:
сумма 6', 'use std::rc::Rc;

#[tokio::main]
async fn main() {
    let data = Rc::new(vec![1, 2, 3]);
    let d = data.clone();
    let s = tokio::spawn(async move { d.iter().sum::<i32>() }).await.unwrap();
    println!("сумма {}", s);
}
', 'Arc вместо Rc: счётчик ссылок атомарный.', '{"crates": ["tokio"], "driver": "", "expected": ["сумма 6"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-async-trait-static', 17, 'rust', 'async fn в трейте', 'Трейт Store { async fn get(&self, k: &str) -> Option<String>; }. Реализуйте для MemStore(HashMap<String, String>): после yield_now вернуть значение (клон) или None. Функция lookup(s: &impl Store, k: &str) -> String возвращает значение или «нет».', 'use std::collections::HashMap;

trait Store {
    async fn get(&self, k: &str) -> Option<String>;
}

struct MemStore(HashMap<String, String>);

impl Store for MemStore {
    async fn get(&self, k: &str) -> Option<String> {
        todo!()
    }
}

async fn lookup(s: &impl Store, k: &str) -> String {
    todo!()
}
', 'async fn в трейте — статическая диспетчеризация, вызов через impl Store.', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    let mut m = HashMap::new();\n    m.insert(String::from(\"a\"), String::from(\"1\"));\n    let s = MemStore(m);\n    println!(\"{} {}\", lookup(&s, \"a\").await, lookup(&s, \"b\").await);\n}\n", "expected": ["1 нет"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-async-trait-dyn', 18, 'rust', 'Динамические асинхронные трейты', 'Трейт Source { fn name(&self) -> String; fn get(&self) -> BoxFuture<''_, u32>; } (futures::future::BoxFuture). Реализуйте для Fast (сразу 1) и Slow (sleep 10 мс, затем 2). Функция total(v: &[Box<dyn Source>]) -> u32 — сумма get().await.', 'use futures::future::BoxFuture;

trait Source {
    fn name(&self) -> String;
    fn get(&self) -> BoxFuture<''_, u32>;
}

struct Fast;
struct Slow;

impl Source for Fast {
    fn name(&self) -> String {
        todo!()
    }
    fn get(&self) -> BoxFuture<''_, u32> {
        todo!()
    }
}

impl Source for Slow {
    fn name(&self) -> String {
        todo!()
    }
    fn get(&self) -> BoxFuture<''_, u32> {
        todo!()
    }
}

async fn total(v: &[Box<dyn Source>]) -> u32 {
    todo!()
}
', 'BoxFuture<''_, u32> позволяет использовать dyn Source.', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    let v: Vec<Box<dyn Source>> = vec![Box::new(Fast), Box::new(Slow), Box::new(Fast)];\n    println!(\"{}\", total(&v).await);\n    println!(\"{}\", v.iter().map(|s| s.name()).collect::<Vec<_>>().join(\",\"));\n}\n", "expected": ["4", "fast,slow,fast"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-async-recursion', 19, 'rust', 'Асинхронная рекурсия по дереву', 'Объявлено дерево enum Tree { Leaf(u32), Node(Vec<Tree>) }. Напишите fn sum(t: &Tree) -> BoxFuture<''_, u32> — рекурсивная сумма листьев (на каждом узле yield_now).', 'use futures::future::BoxFuture;

enum Tree {
    Leaf(u32),
    Node(Vec<Tree>),
}

fn sum(t: &Tree) -> BoxFuture<''_, u32> {
    todo!()
}
', 'Рекурсивный вызов оборачивается в Box::pin.', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    let t = Tree::Node(vec![Tree::Leaf(1), Tree::Node(vec![Tree::Leaf(2), Tree::Leaf(3)]), Tree::Leaf(4)]);\n    println!(\"{}\", sum(&t).await);\n    println!(\"{}\", sum(&Tree::Node(vec![])).await);\n}\n", "expected": ["10", "0"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-cancel-guard', 20, 'rust', 'Учёт отмен', 'Структура Guard увеличивает общий счётчик в Drop, если задача не завершилась (флаг done == false). Запустите 5 задач с timeout 20 мс: у трёх сон 100 мс, у двух — 5 мс. Напечатайте число отменённых «3».

Ожидаемый вывод:
3', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Drop срабатывает при отмене по таймауту.', '{"crates": ["tokio"], "driver": "", "expected": ["3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-cancel-safe-recv', 21, 'rust', 'recv безопасен к отмене', 'В select! по mpsc::Receiver::recv и таймеру (sleep 5 мс в цикле) отправитель шлёт числа 1…10 с паузой 2 мс. Убедитесь, что все 10 сообщений получены, несмотря на отмену recv при срабатывании таймера: напечатайте сумму «55».

Ожидаемый вывод:
55', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'recv безопасен к отмене: сообщение не теряется.', '{"crates": ["tokio"], "driver": "", "expected": ["55"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-abort-cleanup', 22, 'rust', 'Очистка при abort', 'Задача держит Guard, который в Drop печатает «очистка». Запустите задачу (спит 1 с), через 20 мс abort() и дождитесь результата. Ожидается: «старт», «очистка», «отменена: true».

Ожидаемый вывод:
старт
очистка
отменена: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'abort уничтожает фьючер: Drop выполняется.', '{"crates": ["tokio"], "driver": "", "expected": ["старт", "очистка", "отменена: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-join-all-box', 23, 'rust', 'Фьючеры разных типов в цикле', 'В цикле создайте три фьючера разных async-блоков (число, строка длины, булево) как Pin<Box<dyn Future<Output = String>>> (результат превращайте в String), выполните join_all и напечатайте «["42", "3", "true"]».

Ожидаемый вывод:
["42", "3", "true"]', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Box::pin приводит разные async-блоки к одному типу.', '{"crates": ["tokio"], "driver": "", "expected": ["[\"42\", \"3\", \"true\"]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-future-ext', 24, 'rust', 'Цепочка FutureExt', 'С помощью futures::FutureExt соберите цепочку: ready(3).map(|x| x + 1).then(|x| async move { x * 10 }).boxed(); напечатайте результат 40. Затем lazy-фьючер (futures::future::lazy) вернёт «лениво»: напечатайте его.

Ожидаемый вывод:
40
лениво', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'FutureExt: map, then, boxed.', '{"crates": ["tokio"], "driver": "", "expected": ["40", "лениво"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-shared', 25, 'rust', 'Shared', 'Создайте фьючер, который увеличивает глобальный счётчик AtomicUsize и возвращает «результат»; превратите его в Shared (FutureExt::shared) и дождитесь двумя клонами одновременно через join!. Напечатайте оба результата и счётчик: счётчик должен быть 1.

Ожидаемый вывод:
результат результат
1', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Shared выполняет внутренний фьючер один раз и раздаёт результат клонам.', '{"crates": ["tokio"], "driver": "", "expected": ["результат результат", "1"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-select-future', 26, 'rust', 'futures::future::select', 'С помощью futures::future::select (функция, не макрос) определите, какой из двух фьючеров (сон 50 и 10 мс) завершился первым. Напечатайте «второй»; затем дождитесь и оставшегося — напечатайте «оба готовы».

Ожидаемый вывод:
второй
оба готовы', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'select возвращает Either и «остаток» — неготовый фьючер.', '{"crates": ["tokio"], "driver": "", "expected": ["второй", "оба готовы"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-try-join-all', 27, 'rust', 'try_join_all', 'futures::future::try_join_all: три фьючера с Result<u32, String>: Ok(1), Ok(2), Ok(3) — «Ok([1, 2, 3])»; затем замените средний на Err("сбой") — получите «Err("сбой")».

Ожидаемый вывод:
Ok([1, 2, 3])
Err("сбой")', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'try_join_all собирает Ok в вектор или возвращает первую ошибку.', '{"crates": ["tokio"], "driver": "", "expected": ["Ok([1, 2, 3])", "Err(\"сбой\")"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-buffered', 28, 'rust', 'Ограниченная параллельность', 'stream::iter(0..8).map(|i| work(i)).buffered(3): work увеличивает счётчик «в работе», спит 10 мс, уменьшает и запоминает максимум. Напечатайте результаты по порядку [0, 1, 4, 9, 16, 25, 36, 49] и «макс одновременных<=3: true».

Ожидаемый вывод:
[0, 1, 4, 9, 16, 25, 36, 49]
макс одновременных<=3: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'buffered(n) сохраняет порядок; buffer_unordered(n) — по готовности.', '{"crates": ["tokio"], "driver": "", "expected": ["[0, 1, 4, 9, 16, 25, 36, 49]", "макс одновременных<=3: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 32, 'r32-size-compare', 29, 'rust', 'Размеры фьючеров', 'Напишите sizes() -> (usize, usize, usize): size_of_val трёх async-блоков: пустого (async {}), держащего через .await массив [0u8; 512] и такого же, но хранящего массив в Box (vec![0u8; 512] в куче). Проверьте: первый < 64, второй ≥ 512, третий < 128.', 'fn sizes() -> (usize, usize, usize) {
    todo!()
}
', 'Вектор хранит данные в куче, в автомате — только три слова.', '{"crates": ["tokio"], "driver": "#[tokio::main]\nasync fn main() {\n    let (a, b, c) = sizes();\n    println!(\"{} {} {}\", a < 64, b >= 512, c < 128);\n}\n", "expected": ["true true true"], "standalone": false}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-builder-threads', 0, 'rust', 'Рантайм через Builder', 'В обычной fn main постройте многопоточный рантайм: Builder::new_multi_thread() с 2 рабочими потоками, именем потоков «воркер» (thread_name("worker")) и enable_all(). Запустите через block_on задачу spawn, которая печатает «имя начинается с worker: true» (проверяя std::thread::current().name()).

Ожидаемый вывод:
имя начинается с worker: true', 'fn main() {
    // ваш код
}
', 'Builder::new_multi_thread().worker_threads(2).thread_name("worker").enable_all().build().', '{"crates": ["tokio"], "driver": "", "expected": ["имя начинается с worker: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-current-thread', 1, 'rust', 'Однопоточный рантайм', 'Используйте #[tokio::main(flavor = "current_thread")]. Запустите 5 задач spawn, каждая возвращает номер потока (std::thread::current().id()) как строку; проверьте, что поток один и тот же и совпадает с потоком main: «потоков: 1».

Ожидаемый вывод:
потоков: 1', '#[tokio::main(flavor = "current_thread")]
async fn main() {
    // ваш код
}
', 'current_thread: всё выполняется на одном потоке.', '{"crates": ["tokio"], "driver": "", "expected": ["потоков: 1"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-handle-from-thread', 2, 'rust', 'Handle из обычного потока', 'Внутри #[tokio::main] получите Handle::current(), передайте в std::thread::spawn; поток запускает через handle.spawn асинхронную задачу (сон 10 мс, возвращает 99) и отправляет результат обратно через std::sync::mpsc. Напечатайте «99».

Ожидаемый вывод:
99', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Handle можно передать в другой поток и использовать для spawn и block_on.', '{"crates": ["tokio"], "driver": "", "expected": ["99"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-runtime-twice', 3, 'rust', 'block_on дважды', 'В обычной main создайте один Runtime и дважды вызовите block_on: сначала положите значение в общий Arc<Mutex<Vec<u32>>> из задачи, затем второй block_on прочитает его. Напечатайте «[1, 2]».

Ожидаемый вывод:
[1, 2]', 'fn main() {
    // ваш код
}
', 'Один Runtime можно использовать для нескольких block_on.', '{"crates": ["tokio"], "driver": "", "expected": ["[1, 2]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-join-values', 4, 'rust', 'Значения из задач', 'Запустите три задачи spawn: возвращающие String «a», Vec<u32> [1, 2] и кортеж (3, true). Дождитесь через tokio::join! и напечатайте по строке: «a», «[1, 2]», «(3, true)».

Ожидаемый вывод:
a
[1, 2]
(3, true)', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'join! над JoinHandle возвращает кортеж Result.', '{"crates": ["tokio"], "driver": "", "expected": ["a", "[1, 2]", "(3, true)"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-abort-finished', 5, 'rust', 'abort и is_finished', 'Запустите задачу со сном 1 с; сразу проверьте is_finished() (false), вызовите abort(), дождитесь и напечатайте: «false», «cancelled: true», затем is_finished() — «true».

Ожидаемый вывод:
false
cancelled: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'abort() прерывает на ближайшем .await; ожидание хэндла вернёт JoinError::is_cancelled.', '{"crates": ["tokio"], "driver": "", "expected": ["false", "cancelled: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-panic-payload', 6, 'rust', 'Паника и её сообщение', 'Запустите задачу, паникующую panic!("бум"). Достаньте сообщение: JoinError::into_panic() даёт Box<dyn Any + Send>; приведите к &str (downcast_ref::<&str>()). Напечатайте «паника: бум».

Ожидаемый вывод:
паника: бум', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'into_panic() возвращает полезную нагрузку паники.', '{"crates": ["tokio"], "driver": "", "expected": ["паника: бум"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-joinset-order', 7, 'rust', 'JoinSet и индексы', 'В JoinSet запустите 6 задач; i-я спит (6 − i)·5 мс и возвращает (i, i·i). Соберите результаты и напечатайте отсортированными по i: [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25)].

Ожидаемый вывод:
[(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25)]', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Результаты приходят в порядке завершения — сортируйте по индексу.', '{"crates": ["tokio"], "driver": "", "expected": ["[(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25)]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-joinset-abort-all', 8, 'rust', 'abort_all', 'Запустите в JoinSet 4 бесконечные задачи (sleep 1 с), вызовите abort_all() и дождитесь всех join_next: посчитайте ошибки is_cancelled. Напечатайте «отменено: 4».

Ожидаемый вывод:
отменено: 4', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'После abort_all join_next возвращает Err(cancelled) для каждой задачи.', '{"crates": ["tokio"], "driver": "", "expected": ["отменено: 4"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-joinset-drop', 9, 'rust', 'Drop набора отменяет задачи', 'Задача хранит Guard, который в Drop увеличивает общий AtomicUsize. Запустите 3 таких задачи (сон 1 с) в JoinSet, дайте им стартовать (sleep 10 мс), уничтожьте набор (drop) и дайте время на завершение (sleep 20 мс). Напечатайте «очищено: 3».

Ожидаемый вывод:
очищено: 3', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Drop для JoinSet вызывает abort_all.', '{"crates": ["tokio"], "driver": "", "expected": ["очищено: 3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-blocking-parallel', 10, 'rust', 'Блокирующие задачи параллельны', 'Запустите 4 задачи spawn_blocking, каждая спит (std::thread::sleep) 100 мс. Дождитесь всех и убедитесь, что общее время меньше 300 мс: «параллельно: true».

Ожидаемый вывод:
параллельно: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Пул блокирующих потоков выполняет задачи одновременно.', '{"crates": ["tokio"], "driver": "", "expected": ["параллельно: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-block-in-place', 11, 'rust', 'block_in_place', 'На многопоточном рантайме внутри задачи (spawn) вызовите block_in_place для вычисления суммы квадратов 1..=1000 (u64) и верните её: «333833500».

Ожидаемый вывод:
333833500', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'block_in_place разрешён только на multi_thread.', '{"crates": ["tokio"], "driver": "", "expected": ["333833500"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-local-set', 12, 'rust', 'LocalSet и Rc', 'На current_thread создайте LocalSet; внутри run_until запустите 5 задач spawn_local, каждая увеличивает Rc<RefCell<u32>> на своё число (1…5) и после yield_now ничего не делает. Дождитесь всех и напечатайте «15».

Ожидаемый вывод:
15', '#[tokio::main(flavor = "current_thread")]
async fn main() {
    // ваш код
}
', 'spawn_local принимает !Send-фьючеры внутри LocalSet.', '{"crates": ["tokio"], "driver": "", "expected": ["15"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-task-local', 13, 'rust', 'task_local!', 'Объявите tokio::task_local! { static REQ_ID: u32; }. Запустите две задачи: в одной REQ_ID.scope(1, …), в другой scope(2, …); каждая вызывает общую async fn log() -> String, возвращающую «запрос <id>» из REQ_ID.get(). Напечатайте оба результата: «запрос 1», «запрос 2».

Ожидаемый вывод:
запрос 1
запрос 2', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'REQ_ID.scope(значение, фьючер) даёт значение на время выполнения.', '{"crates": ["tokio"], "driver": "", "expected": ["запрос 1", "запрос 2"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-task-id', 14, 'rust', 'Номера задач', 'Запустите 5 задач, каждая возвращает tokio::task::id(). Убедитесь, что все номера разные и не совпадают с номером... (main — не задача): напечатайте «уникальных: 5».

Ожидаемый вывод:
уникальных: 5', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'tokio::task::id() возвращает Id, реализующий Hash.', '{"crates": ["tokio"], "driver": "", "expected": ["уникальных: 5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-yield-fairness', 15, 'rust', 'Справедливость', 'На current_thread запустите «занятую» задачу: while !flag { yield_now().await } и вторую, которая поднимает флаг (AtomicBool) сразу. Дождитесь обеих и напечатайте «флаг поднят». (Без yield_now задача зависла бы.)

Ожидаемый вывод:
флаг поднят', '#[tokio::main(flavor = "current_thread")]
async fn main() {
    // ваш код
}
', 'yield_now отдаёт управление другим задачам на том же потоке.', '{"crates": ["tokio"], "driver": "", "expected": ["флаг поднят"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-detach', 16, 'rust', 'Открепление', 'Выбросьте JoinHandle (drop) сразу после spawn и убедитесь, что задача продолжает работать: она через 10 мс отправляет «жива» через oneshot. Напечатайте «жива».

Ожидаемый вывод:
жива', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Выброшенный JoinHandle не отменяет задачу.', '{"crates": ["tokio"], "driver": "", "expected": ["жива"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-runtime-drop', 17, 'rust', 'Уничтожение рантайма', 'В обычной main создайте Runtime, запустите spawn задачу с Guard (Drop увеличивает AtomicUsize), которая спит 10 с. Дайте ей стартовать (block_on sleep 10 мс), затем drop(rt). Напечатайте число сработавших Drop: «1».

Ожидаемый вывод:
1', 'fn main() {
    // ваш код
}
', 'При уничтожении рантайма задачи отменяются, их деструкторы вызываются.', '{"crates": ["tokio"], "driver": "", "expected": ["1"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-shutdown-timeout', 18, 'rust', 'shutdown_timeout', 'Запустите в рантайме spawn_blocking на 50 мс (std sleep) и вызовите rt.shutdown_timeout(Duration::from_secs(2)); напечатайте «рантайм остановлен» и «быстрее 2 с: true».

Ожидаемый вывод:
рантайм остановлен
быстрее 2 с: true', 'fn main() {
    // ваш код
}
', 'shutdown_timeout ждёт блокирующие задачи не дольше лимита.', '{"crates": ["tokio"], "driver": "", "expected": ["рантайм остановлен", "быстрее 2 с: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-handle-try-current', 19, 'rust', 'Handle::try_current', 'Покажите, что Handle::try_current() вне рантайма возвращает Err (напечатайте «вне: false»), а внутри — Ok («внутри: true»). Сначала вызовите в обычной main до создания рантайма, затем внутри block_on.

Ожидаемый вывод:
вне: false
внутри: true', 'fn main() {
    // ваш код
}
', 'try_current не паникует: это Result.', '{"crates": ["tokio"], "driver": "", "expected": ["вне: false", "внутри: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-par-map', 20, 'rust', 'Параллельный map', 'Напишите async fn par_map(items: Vec<u32>, f: fn(u32) -> u32) -> Vec<u32>: каждый элемент обрабатывается в своей задаче spawn_blocking; результат — в порядке входа. Для f = |x| x * x и items 1..=8 напечатайте [1, 4, 9, 16, 25, 36, 49, 64].

Ожидаемый вывод:
[1, 4, 9, 16, 25, 36, 49, 64]', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Хэндлы ожидайте по порядку запуска, чтобы сохранить порядок.', '{"crates": ["tokio"], "driver": "", "expected": ["[1, 4, 9, 16, 25, 36, 49, 64]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-many-tasks', 21, 'rust', 'Много задач', 'Запустите 20000 задач spawn, каждая увеличивает общий AtomicUsize; дождитесь всех (JoinSet) и напечатайте «20000».

Ожидаемый вывод:
20000', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Задачи tokio очень дёшевы: десятки тысяч — не проблема.', '{"crates": ["tokio"], "driver": "", "expected": ["20000"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-fan-out-in', 22, 'rust', 'Рассылка и сбор', 'Рассылка-сбор: 4 рабочих (spawn), каждый обрабатывает свою четверть чисел 1..=100 (сумма) и отправляет частичную сумму в mpsc-канал; main суммирует полученные 4 значения: «5050».

Ожидаемый вывод:
5050', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'drop(tx) нужен, чтобы recv вернул None после последнего отправителя.', '{"crates": ["tokio"], "driver": "", "expected": ["5050"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-retry', 23, 'rust', 'Повтор с отменой', 'Напишите async fn retry<F, Fut>(n: u32, mut f: F) -> Result<u32, String>, где F: FnMut(u32) -> Fut, Fut: Future<Output = Result<u32, String>>: пробует f(attempt) для attempt = 1…n и возвращает первый Ok или последнюю ошибку. Для f, успешной только с третьей попытки, напечатайте «Ok(3)»; для безнадёжной — «Err("сбой 3")».

Ожидаемый вывод:
Ok(3)
Err("сбой 3")', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Цикл по попыткам; ранний return при Ok.', '{"crates": ["tokio"], "driver": "", "expected": ["Ok(3)", "Err(\"сбой 3\")"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-run-all-result', 24, 'rust', 'Result из задач', 'Напишите async fn run_all(n: u32) -> Result<Vec<u32>, tokio::task::JoinError>: запустить n задач (i·10) и собрать результаты с помощью ? по хэндлам; для n = 4 напечатайте «Ok([0, 10, 20, 30])».

Ожидаемый вывод:
Ok([0, 10, 20, 30])', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'JoinError реализует Error: оператор ? подходит.', '{"crates": ["tokio"], "driver": "", "expected": ["Ok([0, 10, 20, 30])"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-blocking-abort', 25, 'rust', 'abort у блокирующей задачи', 'Покажите, что abort() не останавливает уже запущенную spawn_blocking: задача ставит started, спит 60 мс и ставит done (AtomicBool). Main ждёт started (опрос sleep 1 мс), вызывает abort(), ждёт 100 мс и печатает «флаг: true».

Ожидаемый вывод:
флаг: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Блокирующий поток доработает до конца: отмена применима только к ещё не стартовавшим.', '{"crates": ["tokio"], "driver": "", "expected": ["флаг: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-worker-pool', 26, 'rust', 'Пул рабочих', 'Пул из 3 рабочих читает задания (числа 1…12) из общего mpsc-канала (Arc<tokio::sync::Mutex<Receiver<u32>>>), каждый прибавляет квадрат числа в общий AtomicU64. Отправитель закрывается, main дожидается рабочих (JoinSet) и печатает «650».

Ожидаемый вывод:
650', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Получатель общий: оборачиваем в Arc<Mutex<…>>; None — сигнал завершения.', '{"crates": ["tokio"], "driver": "", "expected": ["650"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-timeout-spawn', 27, 'rust', 'timeout над JoinHandle', 'Оберните JoinHandle задачи (сон 200 мс) в tokio::time::timeout(30 мс): напечатайте «таймаут»; задача при этом продолжает работать — проверьте через oneshot, что через 250 мс она всё же завершилась: «задача дожила».

Ожидаемый вывод:
таймаут
задача дожила', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'timeout отбрасывает ожидание хэндла, но не саму задачу.', '{"crates": ["tokio"], "driver": "", "expected": ["таймаут", "задача дожила"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-multi-thread-count', 28, 'rust', 'Сколько потоков', 'Постройте многопоточный рантайм с worker_threads(3) и запустите 50 задач spawn, каждая возвращает имя своего потока (после короткого sleep 1 мс). Напечатайте: потоков не больше 3: true.

Ожидаемый вывод:
потоков не больше 3: true', '#[tokio::main(flavor = "multi_thread", worker_threads = 3)]
async fn main() {
    // ваш код
}
', 'Все задачи выполняются на рабочих потоках пула.', '{"crates": ["tokio"], "driver": "", "expected": ["потоков не больше 3: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 33, 'r33-spawn-borrowed-fix', 29, 'rust', 'Исправьте: spawn и ссылка', 'Программа не собирается: задача заимствует локальный вектор. Исправьте через Arc, чтобы напечатать «сумма 10».

Ожидаемый вывод:
сумма 10
4', '#[tokio::main]
async fn main() {
    let v = vec![1, 2, 3, 4];
    let h = tokio::spawn(async { v.iter().sum::<i32>() });
    println!("сумма {}", h.await.unwrap());
    println!("{}", v.len());
}
', 'Arc::clone и move.', '{"crates": ["tokio"], "driver": "", "expected": ["сумма 10", "4"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-sleep-elapsed', 0, 'rust', 'sleep и elapsed', 'Запомните Instant::now(), усните на 100 мс через tokio::time::sleep и напечатайте «прошло не меньше 100 мс: true» (сравните elapsed() с Duration::from_millis(100)).

Ожидаемый вывод:
прошло не меньше 100 мс: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'start.elapsed() >= Duration::from_millis(100).', '{"crates": ["tokio"], "driver": "", "expected": ["прошло не меньше 100 мс: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-fix-thread-sleep', 1, 'rust', 'Исправьте: блокирующий sleep', 'Три задачи спят блокирующим std::thread::sleep на однопоточном рантайме, поэтому выполняются одна за другой. Исправьте программу, чтобы они спали одновременно: нужно «быстро: true».

Ожидаемый вывод:
быстро: true', 'use std::time::{Duration, Instant};

#[tokio::main(flavor = "current_thread")]
async fn main() {
    let start = Instant::now();
    let mut hs = Vec::new();
    for _ in 0..3 {
        hs.push(tokio::spawn(async {
            std::thread::sleep(Duration::from_millis(100));
        }));
    }
    for h in hs {
        h.await.unwrap();
    }
    println!("быстро: {}", start.elapsed() < Duration::from_millis(250));
}
', 'Замените std::thread::sleep(..) на tokio::time::sleep(..).await — задача отдаст поток.', '{"crates": ["tokio"], "driver": "", "expected": ["быстро: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-join-sleeps', 2, 'rust', 'Три сна одновременно', 'Через tokio::join! запустите три сна по 100 мс одновременно и напечатайте «параллельно: true», если всё заняло меньше 200 мс.

Ожидаемый вывод:
параллельно: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'tokio::join!(sleep(d), sleep(d), sleep(d)).await не нужен: join! уже возвращает фьючер, его ждут .await.', '{"crates": ["tokio"], "driver": "", "expected": ["параллельно: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-sleep-until', 3, 'rust', 'sleep_until', 'Вычислите дедлайн: Instant::now() + 120 мс, дождитесь его через sleep_until и напечатайте «дедлайн достигнут: true» (Instant::now() >= deadline).

Ожидаемый вывод:
дедлайн достигнут: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'time::sleep_until(deadline).await.', '{"crates": ["tokio"], "driver": "", "expected": ["дедлайн достигнут: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-completion-order', 4, 'rust', 'Порядок завершения', 'Запустите три задачи: «a» спит 60 мс, «b» — 20 мс, «c» — 40 мс; каждая после сна печатает своё имя. Дождитесь всех. Порядок вывода определяют сны.

Ожидаемый вывод:
b
c
a', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Для каждой задачи tokio::spawn(async move { sleep(..).await; println!(..) }); потом .await на каждом JoinHandle.', '{"crates": ["tokio"], "driver": "", "expected": ["b", "c", "a"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-timeout-ok', 5, 'rust', 'timeout: успел', 'Оберните async-блок (сон 20 мс, затем возвращает 5) в timeout 200 мс и напечатайте результат через {:?}.

Ожидаемый вывод:
Ok(5)', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'time::timeout(Duration, future).await возвращает Result<T, Elapsed>.', '{"crates": ["tokio"], "driver": "", "expected": ["Ok(5)"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-timeout-err', 6, 'rust', 'timeout: не успел', 'Оберните сон на 200 мс в timeout на 30 мс. Если вернулась ошибка, напечатайте её через {} (Display у Elapsed).

Ожидаемый вывод:
deadline has elapsed', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'if let Err(e) = r { println!("{}", e); }', '{"crates": ["tokio"], "driver": "", "expected": ["deadline has elapsed"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-timeout-map-err', 7, 'rust', 'Elapsed в свою ошибку', 'Напишите async fn fetch() -> Result<u32, String>: ожидает сон 200 мс через timeout на 30 мс и превращает Elapsed в строку «таймаут» методом map_err. Напечатайте результат через {:?}.

Ожидаемый вывод:
Err("таймаут")', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'time::timeout(..).await.map_err(|_| "таймаут".to_string()) — получится Result<(), String>.', '{"crates": ["tokio"], "driver": "", "expected": ["Err(\"таймаут\")"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-timeout-at', 8, 'rust', 'Общий дедлайн', 'Задайте дедлайн «сейчас + 100 мс». Выполните два шага подряд, каждый — сон 60 мс, и оба ограничьте timeout_at(deadline, ..). Для каждого напечатайте «шаг N: ok» или «шаг N: просрочен».

Ожидаемый вывод:
шаг 1: ok
шаг 2: просрочен', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Дедлайн один на оба шага: второй шаг уже не успевает.', '{"crates": ["tokio"], "driver": "", "expected": ["шаг 1: ok", "шаг 2: просрочен"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-first-tick', 9, 'rust', 'Первый тик сразу', 'Создайте interval на 100 мс, дождитесь первого tick() и напечатайте «первый тик сразу: true», если прошло меньше 30 мс.

Ожидаемый вывод:
первый тик сразу: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'time::interval(Duration) — первый tick() возвращается немедленно.', '{"crates": ["tokio"], "driver": "", "expected": ["первый тик сразу: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-four-ticks', 10, 'rust', 'Четыре тика', 'Interval на 50 мс: дождитесь 4 тиков (первый сразу). Напечатайте «4 тика за 140–220 мс: true», если общее время попало в этот диапазон.

Ожидаемый вывод:
4 тика за 140–220 мс: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Тики на 0, 50, 100 и 150 мс — около 150 мс в сумме.', '{"crates": ["tokio"], "driver": "", "expected": ["4 тика за 140–220 мс: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-no-drift', 11, 'rust', 'Интервал без дрейфа', '5 раз выполните: tick() интервала 50 мс, затем «работа» (сон 20 мс). Напечатайте «без дрейфа: true», если всё заняло меньше 300 мс. (С sleep(50) вместо интервала получилось бы около 350 мс.)

Ожидаемый вывод:
без дрейфа: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Период интервала отсчитывается от запуска, а не от конца работы.', '{"crates": ["tokio"], "driver": "", "expected": ["без дрейфа: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-missed-delay', 12, 'rust', 'MissedTickBehavior::Delay', 'Interval на 50 мс с MissedTickBehavior::Delay. Возьмите первый тик, усните на 120 мс (тики опоздали), возьмите второй тик (он срабатывает сразу), затем замерьте время до третьего. Напечатайте «пауза после опоздания: true», если оно не меньше 45 мс.

Ожидаемый вывод:
пауза после опоздания: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'iv.set_missed_tick_behavior(time::MissedTickBehavior::Delay).', '{"crates": ["tokio"], "driver": "", "expected": ["пауза после опоздания: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-missed-burst', 13, 'rust', 'MissedTickBehavior::Burst', 'Тот же сценарий с поведением по умолчанию (Burst): первый тик, сон 120 мс, затем два тика подряд. Напечатайте «Burst подряд: true», если второй пришёл менее чем через 20 мс после первого из них.

Ожидаемый вывод:
Burst подряд: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Burst отдаёт пропущенные тики без пауз, чтобы догнать расписание.', '{"crates": ["tokio"], "driver": "", "expected": ["Burst подряд: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-missed-skip', 14, 'rust', 'MissedTickBehavior::Skip', 'Interval на 50 мс с MissedTickBehavior::Skip. Первый тик, сон 120 мс (пропущены тики на 50 и 100), затем один tick() (он опоздал и срабатывает сразу) и замер ожидания следующего tick(). Напечатайте «Skip ждёт сетку: true», если оно от 10 до 50 мс (до тика на 150-й мс).

Ожидаемый вывод:
Skip ждёт сетку: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Skip отбрасывает пропущенные и ждёт ближайший тик исходной сетки.', '{"crates": ["tokio"], "driver": "", "expected": ["Skip ждёт сетку: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-interval-reset', 15, 'rust', 'reset интервала', 'Interval на 100 мс: первый тик сразу, усните 30 мс, вызовите reset(), замерьте следующий tick(). Напечатайте «после reset ждали ≥ 90 мс: true».

Ожидаемый вывод:
после reset ждали ≥ 90 мс: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'reset() сдвигает следующий тик на полный период от текущего момента.', '{"crates": ["tokio"], "driver": "", "expected": ["после reset ждали ≥ 90 мс: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-interval-at', 16, 'rust', 'interval_at', 'Создайте interval_at(Instant::now() + 100 мс, 50 мс), замерьте первый tick(). Напечатайте «первый тик позже: true», если прошло не меньше 95 мс.

Ожидаемый вывод:
первый тик позже: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'interval_at(start, period): первый тик — в момент start.', '{"crates": ["tokio"], "driver": "", "expected": ["первый тик позже: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-select-first', 17, 'rust', 'Кто первый', 'В select! ждите два сна: 20 мс (печатает «a») и 100 мс (печатает «b»). Выполнится только первый.

Ожидаемый вывод:
a', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'tokio::select! { _ = sleep(..) => println!(..), _ = sleep(..) => println!(..) }', '{"crates": ["tokio"], "driver": "", "expected": ["a"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-select-timeout', 18, 'rust', 'select! как таймаут', 'В select! ждите медленную операцию (async-блок: сон 200 мс, затем возвращает «готово») и сон 50 мс. Если победила операция — напечатайте её значение, иначе — «тайм-аут».

Ожидаемый вывод:
тайм-аут', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'v = async { .. } => println!("{v}"), _ = sleep(..) => println!("тайм-аут")', '{"crates": ["tokio"], "driver": "", "expected": ["тайм-аут"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-select-value', 19, 'rust', 'select! как выражение', 'Присвойте результат select! переменной: первая ветка — async-блок со сном 30 мс и значением 1, вторая — сон 10 мс и значение 2. Напечатайте переменную.

Ожидаемый вывод:
2', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let r = tokio::select! { v = f1 => v, v = f2 => v };', '{"crates": ["tokio"], "driver": "", "expected": ["2"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-select-else', 20, 'rust', 'Ветка else', 'Заведите let ready = false; и в select! поставьте ветку со сном 10 мс с условием `if ready` и ветку else. Напечатайте «else» из else-ветки.

Ожидаемый вывод:
else', '#[tokio::main]
async fn main() {
    // ваш код
}
', '_ = sleep(..), if ready => .., else => println!("else")', '{"crates": ["tokio"], "driver": "", "expected": ["else"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-select-biased', 21, 'rust', 'biased', 'В цикле на 100 итераций вызывайте select! с biased; и двумя сразу готовыми ветками (std::future::ready(())). Считайте, сколько раз победила первая. Напечатайте «первая ветка: 100».

Ожидаемый вывод:
первая ветка: 100', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'tokio::select! { biased; _ = ready(()) => first += 1, _ = ready(()) => {} }', '{"crates": ["tokio"], "driver": "", "expected": ["первая ветка: 100"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-select-fair', 22, 'rust', 'Справедливый выбор', 'Без biased; в цикле на 1000 итераций вызывайте select! с двумя готовыми ветками и считайте победы каждой. Напечатайте «обе выигрывали: true», если у обеих победы больше нуля.

Ожидаемый вывод:
обе выигрывали: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'По умолчанию порядок опроса случаен, поэтому выигрывают обе ветки.', '{"crates": ["tokio"], "driver": "", "expected": ["обе выигрывали: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-select-drop', 23, 'rust', 'Проигравший отбрасывается', 'Заведите структуру Guard(&''static str) с Drop, который печатает «drop <имя>». В select! первая ветка — async-блок: создаёт Guard("медленный") и спит 200 мс; вторая — сон 10 мс. После select! напечатайте «после select». Посмотрите, в каком порядке появились строки: проигравший фьючер отбрасывается (и Guard вместе с ним) до этого.

Ожидаемый вывод:
drop медленный
после select', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Guard живёт внутри async-блока: он освобождается, когда блок отбрасывают.', '{"crates": ["tokio"], "driver": "", "expected": ["drop медленный", "после select"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-fix-pin-loop', 24, 'rust', 'Исправьте: сон в цикле select!', 'Отправитель шлёт сообщения каждые 50 мс. Нужно остановить цикл через 125 мс от старта, но сон создаётся заново на каждой итерации и никогда не срабатывает. Исправьте: создайте сон до цикла, закрепите (tokio::pin!) и передайте в select! по &mut. Ожидается «сообщений: 2».

Ожидаемый вывод:
сообщений: 2', 'use std::time::Duration;
use tokio::sync::mpsc;
use tokio::time::sleep;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel::<u32>(8);
    tokio::spawn(async move {
        for i in 0..6 {
            sleep(Duration::from_millis(50)).await;
            if tx.send(i).await.is_err() {
                break;
            }
        }
    });
    let mut got = 0;
    loop {
        tokio::select! {
            _ = sleep(Duration::from_millis(125)) => break,
            m = rx.recv() => {
                if m.is_none() {
                    break;
                }
                got += 1;
            }
        }
    }
    println!("сообщений: {got}");
}
', 'let deadline = sleep(..); tokio::pin!(deadline); и в select! — _ = &mut deadline => break.', '{"crates": ["tokio"], "driver": "", "expected": ["сообщений: 2"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-recv-cancel-safe', 25, 'rust', 'recv безопасен к отмене', 'Отправитель шлёт числа 1, 2, 3 с паузой 40 мс и закрывает канал. Получатель в цикле: select! между rx.recv() и сном на 15 мс (сон лишь считает «пустые» ожидания и отбрасывает recv). Все сообщения должны дойти. Напечатайте «получено: 3».

Ожидаемый вывод:
получено: 3', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'recv() можно отбрасывать безопасно: сообщение остаётся в канале.', '{"crates": ["tokio"], "driver": "", "expected": ["получено: 3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-retry-backoff', 26, 'rust', 'Повтор с растущей паузой', 'Напишите повтор: операция падает на первых двух попытках (Err("fail")) и удаётся на третьей. После неудач ждите 20 мс, затем 40 мс (удвоение). Для каждой попытки печатайте «попытка N: fail» или «попытка N: ok», а в конце — «ждали не меньше 60 мс: true».

Ожидаемый вывод:
попытка 1: fail
попытка 2: fail
попытка 3: ok
ждали не меньше 60 мс: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Цикл по попыткам; после неудачи sleep(delay).await и delay *= 2.', '{"crates": ["tokio"], "driver": "", "expected": ["попытка 1: fail", "попытка 2: fail", "попытка 3: ok", "ждали не меньше 60 мс: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-attempt-timeout', 27, 'rust', 'Таймаут на каждую попытку', 'Операция attempt(n): первые две попытки спят 200 мс, третья возвращает 42 сразу. Ограничьте каждую попытку timeout на 50 мс. Печатайте «попытка N: таймаут» или «попытка N: 42».

Ожидаемый вывод:
попытка 1: таймаут
попытка 2: таймаут
попытка 3: 42', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'for n in 1..=3 { match timeout(.., attempt(n)).await { Ok(v) => .., Err(_) => .. } }', '{"crates": ["tokio"], "driver": "", "expected": ["попытка 1: таймаут", "попытка 2: таймаут", "попытка 3: 42"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-nested-timeout', 28, 'rust', 'Вложенные таймауты', 'Внутренний timeout 30 мс оборачивает сон 80 мс, внешний timeout 200 мс оборачивает внутренний. Напечатайте «внутренний: просрочен, внешний: ok».

Ожидаемый вывод:
внутренний: просрочен, внешний: ok', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Внешний вернёт Ok(Err(Elapsed)): сам он успел, а внутренний — нет.', '{"crates": ["tokio"], "driver": "", "expected": ["внутренний: просрочен, внешний: ok"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 34, 'r34-heartbeat', 29, 'rust', 'Сердцебиение', 'В цикле select! соедините interval 100 мс (считайте тики) и общий дедлайн 250 мс (sleep, закреплённый до цикла). Когда дедлайн сработает, выйдите и напечатайте «сердцебиений: 3» (тики на 0, 100 и 200 мс).

Ожидаемый вывод:
сердцебиений: 3', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'tokio::pin! для дедлайна; в select! — _ = &mut deadline => break и _ = iv.tick() => n += 1.', '{"crates": ["tokio"], "driver": "", "expected": ["сердцебиений: 3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-mpsc-basic', 0, 'rust', 'Первый канал', 'Создайте mpsc::channel(4). Из запущенной задачи отправьте 1, 2, 3 (и закройте канал, уничтожив отправитель). В main читайте через while let Some(v) = rx.recv().await и печатайте значения, а после цикла — «конец».

Ожидаемый вывод:
1
2
3
конец', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Sender переезжает в задачу через async move; когда он уничтожен, recv() вернёт None.', '{"crates": ["tokio"], "driver": "", "expected": ["1", "2", "3", "конец"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-mpsc-producers', 1, 'rust', 'Несколько производителей', 'Запустите три задачи, каждая отправляет свой номер 0, 1, 2 по общему каналу (tx.clone()). Соберите все значения, отсортируйте и напечатайте вектор через {:?}.

Ожидаемый вывод:
[0, 1, 2]', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Исходный tx уничтожьте (drop), иначе recv() не закончится.', '{"crates": ["tokio"], "driver": "", "expected": ["[0, 1, 2]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-recv-none', 2, 'rust', 'Закрытый канал', 'Создайте канал mpsc::channel::<u32>(1), уничтожьте отправителя и напечатайте rx.recv().await через {:?}.

Ожидаемый вывод:
None', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Закрытый и пустой канал возвращает None.', '{"crates": ["tokio"], "driver": "", "expected": ["None"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-send-closed', 3, 'rust', 'Нет получателя', 'Создайте канал, уничтожьте получателя и отправьте значение. Напечатайте «отправка не удалась: true», если send вернул ошибку.

Ожидаемый вывод:
отправка не удалась: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'tx.send(1).await.is_err() после drop(rx).', '{"crates": ["tokio"], "driver": "", "expected": ["отправка не удалась: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-try-send', 4, 'rust', 'try_send и переполнение', 'Канал ёмкостью 2. Три раза вызовите try_send: для успешных печатайте «ok», для переполнения (TrySendError::Full) — «переполнен».

Ожидаемый вывод:
ok
ok
переполнен', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'use tokio::sync::mpsc::error::TrySendError; match tx.try_send(i) { Ok(()) => .., Err(TrySendError::Full(_)) => .., _ => .. }', '{"crates": ["tokio"], "driver": "", "expected": ["ok", "ok", "переполнен"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-capacity', 5, 'rust', 'capacity', 'Канал ёмкостью 3. Напечатайте tx.capacity() до отправки и после одной отправки (send без ожидания: try_send).

Ожидаемый вывод:
3
2', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'capacity() — сколько свободного места осталось.', '{"crates": ["tokio"], "driver": "", "expected": ["3", "2"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-reserve', 6, 'rust', 'reserve и permit', 'Канал ёмкостью 1. Зарезервируйте место через tx.reserve().await, отправьте 5 через разрешение (permit.send(5)) и напечатайте rx.recv().await через {:?}.

Ожидаемый вывод:
Some(5)', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let permit = tx.reserve().await.unwrap(); permit.send(5);', '{"crates": ["tokio"], "driver": "", "expected": ["Some(5)"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-unbounded', 7, 'rust', 'Неограниченный канал', 'Через mpsc::unbounded_channel отправьте числа от 0 до 999 (send без .await), уничтожьте отправитель и напечатайте «сумма: …» (сложите всё, что принято).

Ожидаемый вывод:
сумма: 499500', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'tx.send(i).unwrap(); потом drop(tx) и while let Some(v) = rx.recv().await.', '{"crates": ["tokio"], "driver": "", "expected": ["сумма: 499500"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-order', 8, 'rust', 'Порядок от одного отправителя', 'Одна задача отправляет 0, 1, 2, 3, 4; получатель собирает значения в вектор. Напечатайте вектор через {:?}: порядок сохраняется.

Ожидаемый вывод:
[0, 1, 2, 3, 4]', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'mpsc сохраняет порядок сообщений одного отправителя.', '{"crates": ["tokio"], "driver": "", "expected": ["[0, 1, 2, 3, 4]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-oneshot', 9, 'rust', 'oneshot: результат задачи', 'Запустите задачу, которая отправляет по oneshot-каналу 21 * 2. Дождитесь значения через rx.await и напечатайте его.

Ожидаемый вывод:
42', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let (tx, rx) = oneshot::channel(); tx.send(..); rx.await.unwrap().', '{"crates": ["tokio"], "driver": "", "expected": ["42"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-request-reply', 10, 'rust', 'Запрос с ответом', 'Запустите рабочую задачу: она принимает по mpsc пары (u32, oneshot::Sender<u32>) и отвечает квадратом числа. Отправьте запрос (5, reply_tx) и напечатайте ответ.

Ожидаемый вывод:
25', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Рабочий: while let Some((n, reply)) = rx.recv().await { reply.send(n * n).ok(); }', '{"crates": ["tokio"], "driver": "", "expected": ["25"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-oneshot-dropped', 11, 'rust', 'Отправитель oneshot пропал', 'Создайте oneshot-канал, уничтожьте отправитель без отправки и напечатайте ошибку от rx.await через {} (Display у RecvError).

Ожидаемый вывод:
channel closed', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'if let Err(e) = rx.await { println!("{}", e); }', '{"crates": ["tokio"], "driver": "", "expected": ["channel closed"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-oneshot-try-recv', 12, 'rust', 'try_recv у oneshot', 'Создайте oneshot-канал. Напечатайте rx.try_recv() через {:?} до отправки, затем отправьте 7 и напечатайте try_recv() снова.

Ожидаемый вывод:
Err(Empty)
Ok(7)', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Receiver должен быть изменяемым: let (tx, mut rx) = …', '{"crates": ["tokio"], "driver": "", "expected": ["Err(Empty)", "Ok(7)"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-broadcast', 13, 'rust', 'Рассылка двум получателям', 'Создайте broadcast::channel(8) и двух подписчиков (tx.subscribe()). Отправьте «a» и «b». Каждый подписчик читает два сообщения. Напечатайте «r1: a b» и «r2: a b».

Ожидаемый вывод:
r1: a b
r2: a b', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Каждый подписчик получает копию каждого сообщения.', '{"crates": ["tokio"], "driver": "", "expected": ["r1: a b", "r2: a b"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-broadcast-lagged', 14, 'rust', 'Отставший подписчик', 'broadcast::channel(2): отправьте 1, 2, 3, 4, не читая. Затем читайте: на ошибку Lagged(n) напечатайте «пропущено n», значения печатайте как есть, до конца буфера (3 чтения).

Ожидаемый вывод:
пропущено 2
3
4', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'use tokio::sync::broadcast::error::RecvError; Err(RecvError::Lagged(n)) => ..', '{"crates": ["tokio"], "driver": "", "expected": ["пропущено 2", "3", "4"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-broadcast-late', 15, 'rust', 'Поздняя подписка', 'Создайте broadcast-канал, отправьте «old», затем подпишитесь (subscribe) и напечатайте late.try_recv() через {:?}: старое сообщение подписчик не увидит.

Ожидаемый вывод:
Err(Empty)', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Сохраните первого получателя (let (tx, _rx)), иначе send вернёт ошибку.', '{"crates": ["tokio"], "driver": "", "expected": ["Err(Empty)"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-watch-borrow', 16, 'rust', 'watch: текущее значение', 'Создайте watch::channel(0), отправьте 5 и напечатайте *rx.borrow().

Ожидаемый вывод:
5', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'tx.send(5).unwrap(); *rx.borrow().', '{"crates": ["tokio"], "driver": "", "expected": ["5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-watch-changed', 17, 'rust', 'watch: ждём изменений', 'Задача обновляет значение watch-канала: 1, 2, 3 с паузой 40 мс между обновлениями и затем завершается. В main ждите rx.changed().await в цикле и печатайте новое значение.

Ожидаемый вывод:
1
2
3', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'while rx.changed().await.is_ok() { println!("{}", *rx.borrow()); }', '{"crates": ["tokio"], "driver": "", "expected": ["1", "2", "3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-mutex-counter', 18, 'rust', 'Счётчик под Mutex', 'Десять задач увеличивают общий счётчик Arc<tokio::sync::Mutex<u32>> на 1. Дождитесь всех и напечатайте значение.

Ожидаемый вывод:
10', '#[tokio::main]
async fn main() {
    // ваш код
}
', '*m.lock().await += 1;', '{"crates": ["tokio"], "driver": "", "expected": ["10"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-mutex-across-await', 19, 'rust', 'Замок через await', 'Две задачи берут один tokio::sync::Mutex, держат охранника во время sleep 50 мс. Напечатайте «последовательно: true», если вся работа заняла не меньше 90 мс.

Ожидаемый вывод:
последовательно: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let _g = m.lock().await; sleep(..).await; — охранник живёт до конца блока.', '{"crates": ["tokio"], "driver": "", "expected": ["последовательно: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-fix-std-mutex', 20, 'rust', 'Исправьте: std Mutex через await', 'Программа не компилируется: охранник std::sync::Mutex живёт через .await внутри spawn. Исправьте, сократив его время жизни (увеличивайте счётчик в отдельном блоке до sleep). Ожидается «счётчик: 1».

Ожидаемый вывод:
счётчик: 1', 'use std::sync::{Arc, Mutex};
use std::time::Duration;
use tokio::time::sleep;

#[tokio::main]
async fn main() {
    let m = Arc::new(Mutex::new(0));
    let m2 = Arc::clone(&m);
    let h = tokio::spawn(async move {
        let mut g = m2.lock().unwrap();
        *g += 1;
        sleep(Duration::from_millis(10)).await;
    });
    h.await.unwrap();
    println!("счётчик: {}", *m.lock().unwrap());
}
', 'Оберните let mut g … *g += 1; в отдельные фигурные скобки до .await — охранник уничтожится раньше.', '{"crates": ["tokio"], "driver": "", "expected": ["счётчик: 1"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-rwlock', 21, 'rust', 'RwLock: писатель и читатели', 'Положите число в Arc<RwLock<u32>>: сначала запишите 10, затем запустите три читающие задачи, каждая возвращает прочитанное. Сложите результаты и напечатайте «сумма: …».

Ожидаемый вывод:
сумма: 30', '#[tokio::main]
async fn main() {
    // ваш код
}
', '*lock.write().await = 10; let v = *lock.read().await;', '{"crates": ["tokio"], "driver": "", "expected": ["сумма: 30"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-semaphore-limit', 22, 'rust', 'Ограничение параллелизма', 'Семафор на 2 разрешения, шесть задач: каждая берёт разрешение, увеличивает счётчик одновременно работающих (AtomicUsize), обновляет максимум, спит 50 мс и уменьшает счётчик. Напечатайте «максимум одновременно: 2».

Ожидаемый вывод:
максимум одновременно: 2', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'cur.fetch_add(1) + 1; max.fetch_max(now); потом cur.fetch_sub(1).', '{"crates": ["tokio"], "driver": "", "expected": ["максимум одновременно: 2"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-acquire-owned', 23, 'rust', 'acquire_owned', 'Семафор Arc::new(Semaphore::new(3)): запустите три задачи, каждая получает разрешение через acquire_owned().await (оно переезжает внутрь задачи) и спит 30 мс. После всех напечатайте available_permits().

Ожидаемый вывод:
3', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'sem.clone().acquire_owned().await.unwrap() — разрешение с владением.', '{"crates": ["tokio"], "driver": "", "expected": ["3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-try-acquire', 24, 'rust', 'try_acquire', 'Семафор на одно разрешение. Первый try_acquire — успех (напечатайте «ok»), и пока разрешение держится, второй — отказ (напечатайте «занято»).

Ожидаемый вывод:
ok
занято', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let p = sem.try_acquire(); … sem.try_acquire().is_err()', '{"crates": ["tokio"], "driver": "", "expected": ["ok", "занято"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-notify', 25, 'rust', 'Notify: разбудить задачу', 'Задача ждёт notify.notified().await и затем печатает «проснулась». Главная задача печатает «будим» и вызывает notify_one(), после чего дожидается завершения.

Ожидаемый вывод:
будим
проснулась', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Notify в Arc; ждущая задача — spawn; будить notify.notify_one().', '{"crates": ["tokio"], "driver": "", "expected": ["будим", "проснулась"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-notify-permit', 26, 'rust', 'Notify: запомненное разрешение', 'Вызовите notify_one() до ожидания, затем notified().await — он не должен заблокироваться. Напечатайте «не блокируется».

Ожидаемый вывод:
не блокируется', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Notify запоминает одно разрешение, если никто не ждёт.', '{"crates": ["tokio"], "driver": "", "expected": ["не блокируется"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-barrier', 27, 'rust', 'Barrier', 'Barrier::new(3) и три задачи: каждая увеличивает общий счётчик AtomicUsize, затем ждёт на барьере и после него проверяет, что счётчик равен 3. Напечатайте «все видят 3: true».

Ожидаемый вывод:
все видят 3: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'barrier.wait().await; после барьера все три увеличения уже сделаны.', '{"crates": ["tokio"], "driver": "", "expected": ["все видят 3: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-actor', 28, 'rust', 'Актор-счётчик', 'Напишите актор: задача владеет счётчиком и принимает команды enum Cmd { Add(u32), Get(oneshot::Sender<u32>) } по mpsc. Отправьте Add(3), Add(3), Add(4), затем Get и напечатайте ответ.

Ожидаемый вывод:
10', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Актор: let mut total = 0; while let Some(cmd) = rx.recv().await { match cmd { .. } }', '{"crates": ["tokio"], "driver": "", "expected": ["10"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 35, 'r35-worker-pool', 29, 'rust', 'Пул рабочих', 'Три рабочих берут задания из общего канала (приёмник в Arc<tokio::sync::Mutex<Receiver<u32>>>), считают квадрат и отправляют результат в канал результатов. Отправьте задания 1…9, закройте канал заданий и напечатайте «сумма квадратов: …».

Ожидаемый вывод:
сумма квадратов: 285', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Рабочий: let job = { let mut g = rx.lock().await; g.recv().await }; None — выход из цикла.', '{"crates": ["tokio"], "driver": "", "expected": ["сумма квадратов: 285"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-bind-port0', 0, 'rust', 'Порт 0', 'Привяжите TcpListener к 127.0.0.1:0, возьмите порт из local_addr() и напечатайте «порт больше нуля: true».

Ожидаемый вывод:
порт больше нуля: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'TcpListener::bind("127.0.0.1:0").await?.local_addr()?.port()', '{"crates": ["tokio"], "driver": "", "expected": ["порт больше нуля: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-accept-connect', 1, 'rust', 'Сервер принял клиента', 'Запустите сервер в задаче: он принимает одно соединение и печатает «подключился». Клиент в main подключается (TcpStream::connect). Дождитесь задачи сервера.

Ожидаемый вывод:
подключился', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Адрес возьмите у listener.local_addr() до spawn.', '{"crates": ["tokio"], "driver": "", "expected": ["подключился"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-write-read', 2, 'rust', 'Отправить и прочитать', 'Клиент отправляет «привет» и закрывает соединение. Сервер читает до конца (read_to_end) и печатает «получено: привет».

Ожидаемый вывод:
получено: привет', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Клиента уничтожьте (drop) — сервер получит EOF.', '{"crates": ["tokio"], "driver": "", "expected": ["получено: привет"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-read-zero', 3, 'rust', 'read вернул 0', 'Клиент подключается и сразу закрывает соединение. Сервер вызывает read один раз и печатает «EOF: n», где n — число прочитанных байт.

Ожидаемый вывод:
EOF: 0', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Закрытое собеседником соединение: read возвращает Ok(0).', '{"crates": ["tokio"], "driver": "", "expected": ["EOF: 0"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-echo-once', 4, 'rust', 'Эхо на одно сообщение', 'Сервер читает до 64 байт (один read) и отправляет их обратно. Клиент отправляет «ping», читает ответ и печатает «echo: ping».

Ожидаемый вывод:
echo: ping', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Сервер: let n = s.read(&mut buf).await?; s.write_all(&buf[..n]).await?.', '{"crates": ["tokio"], "driver": "", "expected": ["echo: ping"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-echo-loop', 5, 'rust', 'Эхо-сервер для многих', 'Напишите сервер с циклом accept и spawn на каждого клиента: обработчик читает и пишет обратно, пока не получит EOF. Три клиента по очереди подключаются, отправляют «id N», читают ответ и печатают «эхо N» для N = 0, 1, 2.

Ожидаемый вывод:
эхо 0
эхо 1
эхо 2', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'loop { let (s, _) = l.accept().await?; tokio::spawn(handle(s)); } — сервер запускайте в отдельной задаче.', '{"crates": ["tokio"], "driver": "", "expected": ["эхо 0", "эхо 1", "эхо 2"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-lines', 6, 'rust', 'Чтение построчно', 'Сервер отправляет клиенту «a\nb\nc\n» и закрывает соединение. Клиент читает через BufReader::lines() и печатает каждую строку.

Ожидаемый вывод:
a
b
c', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'use tokio::io::{AsyncBufReadExt, BufReader}; BufReader::new(c).lines(); next_line().await.', '{"crates": ["tokio"], "driver": "", "expected": ["a", "b", "c"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-read-line', 7, 'rust', 'read_line и счёт байт', 'Клиент отправляет «hello\nworld\n» и закрывает соединение. Сервер читает read_line в цикле и печатает «N: строка», где N — число байт (с переводом строки), а на конце потока — «EOF».

Ожидаемый вывод:
6: hello
6: world
EOF', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let n = reader.read_line(&mut s).await?; if n == 0 { break }', '{"crates": ["tokio"], "driver": "", "expected": ["6: hello", "6: world", "EOF"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-length-prefix', 8, 'rust', 'Префикс длины', 'Клиент отправляет кадр: 4 байта длины (big-endian) и затем «hello». Сервер читает заголовок (read_exact на 4 байта), затем ровно столько байт данных и печатает «длина 5, данные hello».

Ожидаемый вывод:
длина 5, данные hello', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'u32::from_be_bytes(hdr) as usize; (5u32).to_be_bytes().', '{"crates": ["tokio"], "driver": "", "expected": ["длина 5, данные hello"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-read-u32', 9, 'rust', 'read_u32 и write_u32', 'Клиент отправляет число 256 через write_u32 (big-endian). Сервер читает его через read_u32 и печатает.

Ожидаемый вывод:
256', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'AsyncWriteExt::write_u32 и AsyncReadExt::read_u32 используют сетевой порядок байт.', '{"crates": ["tokio"], "driver": "", "expected": ["256"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-split', 10, 'rust', 'into_split', 'Эхо-сервер (читает и пишет обратно). Клиент разделяет сокет через into_split(): задача-писатель отправляет «split», основная задача читает ровно 5 байт (read_exact) и печатает «ответ: split».

Ожидаемый вывод:
ответ: split', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let (mut r, mut w) = c.into_split(); tokio::spawn(async move { w.write_all(..).await });', '{"crates": ["tokio"], "driver": "", "expected": ["ответ: split"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-half-close', 11, 'rust', 'shutdown записи', 'Клиент отправляет «запрос», закрывает запись (shutdown), затем читает ответ до конца. Сервер читает до конца запроса, отвечает «ok» и закрывается. Клиент печатает «ответ: ok».

Ожидаемый вывод:
ответ: ok', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'c.shutdown().await закрывает запись; read_to_end у сервера завершится.', '{"crates": ["tokio"], "driver": "", "expected": ["ответ: ok"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-refused', 12, 'rust', 'Отказ в соединении', 'Привяжите listener, узнайте адрес и уничтожьте listener. Попытка TcpStream::connect к этому адресу должна завершиться ошибкой. Напечатайте её вид через {:?}: e.kind().

Ожидаемый вывод:
ConnectionRefused', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'match TcpStream::connect(addr).await { Err(e) => println!("{:?}", e.kind()), .. }', '{"crates": ["tokio"], "driver": "", "expected": ["ConnectionRefused"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-udp-echo', 13, 'rust', 'UDP: эхо', 'Сервер на UdpSocket (bind 127.0.0.1:0) принимает датаграмму через recv_from и отправляет её обратно отправителю. Клиент посылает «ping» и печатает «ответ: ping».

Ожидаемый вывод:
ответ: ping', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let (n, from) = s.recv_from(&mut buf).await?; s.send_to(&buf[..n], from).await?;', '{"crates": ["tokio"], "driver": "", "expected": ["ответ: ping"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-udp-boundaries', 14, 'rust', 'Границы датаграмм', 'Отправьте с одного UDP-сокета на другой «ab» и «cd» двумя send_to. Принимающий делает два recv_from и печатает каждую датаграмму отдельной строкой.

Ожидаемый вывод:
ab
cd', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Одна отправка — одно чтение, без слияния.', '{"crates": ["tokio"], "driver": "", "expected": ["ab", "cd"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-read-timeout', 15, 'rust', 'Таймаут чтения', 'Сервер принимает соединение и молчит (держит сокет 300 мс). Клиент пытается прочитать с timeout 50 мс и при ошибке печатает «таймаут чтения».

Ожидаемый вывод:
таймаут чтения', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'tokio::time::timeout(Duration::from_millis(50), c.read(&mut buf)).await', '{"crates": ["tokio"], "driver": "", "expected": ["таймаут чтения"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-accept-shutdown', 16, 'rust', 'Остановка цикла accept', 'Цикл accept в задаче с select!: либо принять клиента (считать), либо получить сигнал остановки по oneshot. Один клиент подключается, затем (после паузы 50 мс) отправляется сигнал. Задача печатает «принято: 1» и «остановлен».

Ожидаемый вывод:
принято: 1
остановлен', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'select! { r = l.accept() => { r.unwrap(); n += 1; }, _ = &mut stop => break }', '{"crates": ["tokio"], "driver": "", "expected": ["принято: 1", "остановлен"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-count-conns', 17, 'rust', 'Подсчёт соединений', 'Сервер в цикле принимает ровно 5 соединений и считает их в AtomicUsize (каждое — в своей задаче spawn). Пять клиентов подключаются. Дождитесь сервера и напечатайте «подключений: 5».

Ожидаемый вывод:
подключений: 5', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'for _ in 0..5 { let (s, _) = l.accept().await?; counter.fetch_add(1, SeqCst); spawn(..) }', '{"crates": ["tokio"], "driver": "", "expected": ["подключений: 5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-io-copy', 18, 'rust', 'io::copy', 'Скопируйте байты из среза &[u8] (b"hello world") в Vec<u8> функцией tokio::io::copy и напечатайте «скопировано: N».

Ожидаемый вывод:
скопировано: 11', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let mut r: &[u8] = b"hello world"; let mut w = Vec::new(); tokio::io::copy(&mut r, &mut w).await?', '{"crates": ["tokio"], "driver": "", "expected": ["скопировано: 11"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-duplex', 19, 'rust', 'duplex в памяти', 'Создайте пару tokio::io::duplex(64). Запишите в одну половину «hi», закройте её и прочитайте всё из другой в String. Напечатайте строку.

Ожидаемый вывод:
hi', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let (mut a, mut b) = tokio::io::duplex(64); drop(a) после записи; b.read_to_string(&mut s).', '{"crates": ["tokio"], "driver": "", "expected": ["hi"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-proxy', 20, 'rust', 'Прокси через copy_bidirectional', 'Эхо-сервер, прокси и клиент. Прокси принимает соединение клиента, подключается к эхо-серверу и гонит данные в обе стороны через tokio::io::copy_bidirectional. Клиент отправляет «via proxy», читает столько же байт и печатает «через прокси: via proxy».

Ожидаемый вывод:
через прокси: via proxy', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'copy_bidirectional(&mut client_side, &mut upstream).await — в отдельной задаче.', '{"crates": ["tokio"], "driver": "", "expected": ["через прокси: via proxy"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-stream-map', 21, 'rust', 'Stream: map и collect', 'Из tokio_stream::iter(1..=3) получите поток, умножьте каждое значение на 2 (map) и соберите в Vec (collect). Напечатайте вектор через {:?}.

Ожидаемый вывод:
[2, 4, 6]', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'use tokio_stream::{self as stream, StreamExt}; stream::iter(..).map(..).collect::<Vec<_>>().await', '{"crates": ["tokio"], "driver": "", "expected": ["[2, 4, 6]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-receiver-stream', 22, 'rust', 'ReceiverStream', 'Оберните приёмник mpsc-канала в ReceiverStream, отправьте из задачи 1, 2, 3 и соберите поток в вектор. Напечатайте вектор через {:?}.

Ожидаемый вывод:
[1, 2, 3]', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'tokio_stream::wrappers::ReceiverStream::new(rx).collect::<Vec<_>>().await', '{"crates": ["tokio"], "driver": "", "expected": ["[1, 2, 3]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-stream-filter-take', 23, 'rust', 'Stream: filter и take', 'Из iter(1..=10) оставьте чётные (filter), возьмите первые три (take) и соберите в Vec. Напечатайте вектор через {:?}.

Ожидаемый вывод:
[2, 4, 6]', '#[tokio::main]
async fn main() {
    // ваш код
}
', '.filter(|x| x % 2 == 0).take(3).collect::<Vec<_>>().await', '{"crates": ["tokio"], "driver": "", "expected": ["[2, 4, 6]"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-fs', 24, 'rust', 'tokio::fs', 'Запишите «hello» в файл /tmp/say_r36.txt через tokio::fs::write, прочитайте обратно read_to_string, напечатайте содержимое и удалите файл (remove_file).

Ожидаемый вывод:
hello', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'tokio::fs::write(path, data).await?; tokio::fs::read_to_string(path).await?', '{"crates": ["tokio"], "driver": "", "expected": ["hello"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-spawn-blocking', 25, 'rust', 'spawn_blocking', 'Через tokio::task::spawn_blocking вычислите сумму чисел от 1 до 1_000_000 (u64) и напечатайте результат.

Ожидаемый вывод:
500000500000', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'spawn_blocking(|| (1..=1_000_000u64).sum::<u64>()).await?', '{"crates": ["tokio"], "driver": "", "expected": ["500000500000"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-lookup-host', 26, 'rust', 'lookup_host', 'Через tokio::net::lookup_host("127.0.0.1:80") получите адреса и напечатайте «адресов: N».

Ожидаемый вывод:
адресов: 1', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'lookup_host(..).await?.count()', '{"crates": ["tokio"], "driver": "", "expected": ["адресов: 1"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-peer-addr', 27, 'rust', 'Адрес клиента', 'Сервер получает адрес клиента из accept() и печатает «клиент с петли: true», если addr.ip().is_loopback().

Ожидаемый вывод:
клиент с петли: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let (_s, peer) = l.accept().await?; peer.ip().is_loopback()', '{"crates": ["tokio"], "driver": "", "expected": ["клиент с петли: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-unix-socket', 28, 'rust', 'Unix-сокет', 'Привяжите UnixListener к /tmp/say_r36.sock, подключитесь UnixStream-клиентом, отправьте «ping», сервер читает и печатает «unix: ping». После работы удалите файл сокета.

Ожидаемый вывод:
unix: ping', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'use tokio::net::{UnixListener, UnixStream}; перед bind удалите старый файл (let _ = std::fs::remove_file).', '{"crates": ["tokio"], "driver": "", "expected": ["unix: ping"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 36, 'r36-line-protocol', 29, 'rust', 'Текстовый протокол', 'Сервер читает строку «ADD 2 3», складывает числа и отвечает строкой с результатом и переводом строки. Клиент отправляет «ADD 2 3\n», читает строку ответа и печатает её без перевода строки.

Ожидаемый вывод:
5', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'BufReader::new(socket).read_line(..); split_whitespace(); write_all(format!("{}\n", sum)).', '{"crates": ["tokio"], "driver": "", "expected": ["5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-abort-inflight', 0, 'rust', 'abort в полёте', 'Запустите задачу: печатает «start», спит 100 мс и печатает «end». Через 20 мс отмените её (abort), дождитесь хэндла и напечатайте «отменена: true» (JoinError::is_cancelled).

Ожидаемый вывод:
start
отменена: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let e = h.await.unwrap_err(); e.is_cancelled()', '{"crates": ["tokio"], "driver": "", "expected": ["start", "отменена: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-drop-future', 1, 'rust', 'Drop отменённого фьючера', 'Заведите структуру Guard с Drop, печатающим «drop guard». В select! первая ветка — async-блок: создаёт Guard и спит 200 мс; вторая — сон 20 мс и печать «тайм-аут». Посмотрите, что и в каком порядке напечатано: проигравший фьючер уничтожается вместе со своими локальными значениями.

Ожидаемый вывод:
drop guard
тайм-аут', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Guard живёт внутри async-блока и уничтожается при отбрасывании блока.', '{"crates": ["tokio"], "driver": "", "expected": ["drop guard", "тайм-аут"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-is-finished', 2, 'rust', 'abort и is_finished', 'Запустите задачу со сном 1 с, отмените её (abort), подождите 10 мс и напечатайте «завершена: true» по is_finished().

Ожидаемый вывод:
завершена: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'После abort задача завершается на ближайшем .await; is_finished() покажет true.', '{"crates": ["tokio"], "driver": "", "expected": ["завершена: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-detached', 3, 'rust', 'Уничтоженный хэндл не отменяет', 'Запустите задачу: сон 30 мс и печать «работает». Сразу уничтожьте JoinHandle (drop) и ждите в main 100 мс. Задача должна успеть напечатать своё.

Ожидаемый вывод:
работает', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'drop(handle) не вызывает abort: задача продолжает жить.', '{"crates": ["tokio"], "driver": "", "expected": ["работает"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-token-loop', 4, 'rust', 'Цикл с токеном', 'Задача в цикле select!: ждёт tokio_util::sync::CancellationToken::cancelled() или сон 10 мс (считать). Через 50 мс main отменяет токен. Задача печатает «остановлена», main дожидается её.

Ожидаемый вывод:
остановлена', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'tokio::select! { _ = token.cancelled() => break, _ = sleep(..) => n += 1 }', '{"crates": ["tokio"], "driver": "", "expected": ["остановлена"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-child-token', 5, 'rust', 'Дерево токенов', 'Создайте родительский токен и дочерний (child_token()). Отмените родителя и напечатайте «дочерний: true» (child.is_cancelled()). Затем создайте новую пару, отмените ребёнка и напечатайте «родитель: false».

Ожидаемый вывод:
дочерний: true
родитель: false', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Отмена идёт вниз по дереву, но не вверх.', '{"crates": ["tokio"], "driver": "", "expected": ["дочерний: true", "родитель: false"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-cancelled-await', 6, 'rust', 'Ждём сигнал', 'Запущенная задача ждёт token.cancelled().await и печатает «сигнал получен». Main печатает «отменяем» (после паузы 20 мс), отменяет токен и дожидается задачи.

Ожидаемый вывод:
отменяем
сигнал получен', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'cancel() будит все ожидающие cancelled().', '{"crates": ["tokio"], "driver": "", "expected": ["отменяем", "сигнал получен"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-drop-guard', 7, 'rust', 'DropGuard токена', 'Получите drop_guard() у клона токена в отдельном блоке; после выхода из блока напечатайте «отменён: true» (token.is_cancelled()).

Ожидаемый вывод:
отменён: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', '{ let _g = token.clone().drop_guard(); }', '{"crates": ["tokio"], "driver": "", "expected": ["отменён: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-broadcast-shutdown', 8, 'rust', 'Остановка рассылкой', 'Запустите три рабочих задачи, каждая ждёт сообщение остановки из broadcast-канала и возвращает свой номер. Через 20 мс main отправляет сигнал, собирает номера (JoinSet) и печатает «остановлено: 3».

Ожидаемый вывод:
остановлено: 3', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let mut rx = tx.subscribe(); rx.recv().await; JoinSet::join_next().', '{"crates": ["tokio"], "driver": "", "expected": ["остановлено: 3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-task-tracker', 9, 'rust', 'TaskTracker', 'Запустите через TaskTracker три задачи со снами 10, 20 и 30 мс, закройте трекер (close) и дождитесь (wait). Напечатайте «все завершены».

Ожидаемый вывод:
все завершены', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'use tokio_util::task::TaskTracker; tracker.spawn(..); tracker.close(); tracker.wait().await', '{"crates": ["tokio"], "driver": "", "expected": ["все завершены"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-joinset-sum', 10, 'rust', 'JoinSet: сумма', 'Запустите в JoinSet три задачи, возвращающие 1, 2 и 3. Сложите результаты по мере готовности (join_next) и напечатайте «сумма: 6».

Ожидаемый вывод:
сумма: 6', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'while let Some(r) = set.join_next().await { sum += r.unwrap(); }', '{"crates": ["tokio"], "driver": "", "expected": ["сумма: 6"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-cleanup-abort', 11, 'rust', 'Очистка при abort', 'Задача создаёт Guard с Drop, печатающим «очистка», и спит секунду. Через 20 мс отмените её, дождитесь хэндла и напечатайте «отменена». Очистка должна пройти раньше.

Ожидаемый вывод:
очистка
отменена', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Drop сработает при отбрасывании фьючера, до возврата h.await.', '{"crates": ["tokio"], "driver": "", "expected": ["очистка", "отменена"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-semaphore-peak', 12, 'rust', 'Предел параллелизма', 'Обработайте 10 заданий, ограничив одновременность семафором на 3 разрешения. В каждом задании увеличивайте счётчик активных (AtomicUsize), обновляйте максимум, спите 30 мс и уменьшайте. Напечатайте «пик: 3».

Ожидаемый вывод:
пик: 3', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'fetch_max для пика; разрешение — в переменной на время сна.', '{"crates": ["tokio"], "driver": "", "expected": ["пик: 3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-load-shed', 13, 'rust', 'Сброс нагрузки', 'Очередь на 2 места, потребителя нет. Отправьте 5 заданий через try_send; считайте принятые и отброшенные (Full). Напечатайте «принято 2, отброшено 3».

Ожидаемый вывод:
принято 2, отброшено 3', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Err(TrySendError::Full(_)) => rejected += 1', '{"crates": ["tokio"], "driver": "", "expected": ["принято 2, отброшено 3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-timeout-error', 14, 'rust', 'Своя ошибка таймаута', 'Опишите enum Error { Timeout } (derive Debug) и async fn call() -> Result<u32, Error>: ожидание сна 200 мс под timeout 30 мс, при просрочке — Error::Timeout. Напечатайте результат вызова через {:?}.

Ожидаемый вывод:
Err(Timeout)', '#[tokio::main]
async fn main() {
    // ваш код
}
', '.await.map_err(|_| Error::Timeout)?; затем Ok(..)', '{"crates": ["tokio"], "driver": "", "expected": ["Err(Timeout)"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-blocking-parallel', 15, 'rust', 'spawn_blocking не мешает', 'На однопоточном рантайме (flavor = "current_thread") запустите задачу-тикер: каждые 10 мс увеличивает счётчик. Одновременно дождитесь spawn_blocking с блокирующим std::thread::sleep на 100 мс. Затем остановите тикер и напечатайте «работал параллельно: true», если тиков не меньше 5.

Ожидаемый вывод:
работал параллельно: true', '#[tokio::main(flavor = "current_thread")]
async fn main() {
    // ваш код
}
', 'spawn_blocking(|| std::thread::sleep(..)).await — пока ждём, поток рантайма свободен для тикера.', '{"crates": ["tokio"], "driver": "", "expected": ["работал параллельно: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-fix-blocking', 16, 'rust', 'Исправьте: блокирующий сон в задаче', 'Тикер на однопоточном рантайме не получает времени: main выполняет «тяжёлую работу» (std::thread::sleep на 100 мс) прямо в асинхронной функции. Вынесите её в spawn_blocking, чтобы тикер успел сработать не менее 5 раз: должно быть «тиков не меньше 5: true».

Ожидаемый вывод:
тиков не меньше 5: true', 'use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::Duration;
use tokio::time::sleep;

#[tokio::main(flavor = "current_thread")]
async fn main() {
    let ticks = Arc::new(AtomicUsize::new(0));
    let t = ticks.clone();
    let ticker = tokio::spawn(async move {
        loop {
            sleep(Duration::from_millis(10)).await;
            t.fetch_add(1, Ordering::SeqCst);
        }
    });
    std::thread::sleep(Duration::from_millis(100)); // тяжёлая работа
    ticker.abort();
    println!("тиков не меньше 5: {}", ticks.load(Ordering::SeqCst) >= 5);
}
', 'tokio::task::spawn_blocking(|| std::thread::sleep(..)).await.unwrap();', '{"crates": ["tokio"], "driver": "", "expected": ["тиков не меньше 5: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-join-panic', 17, 'rust', 'Паника в задаче', 'Запустите задачу, которая паникует (panic!), дождитесь хэндла и напечатайте «паника: true» по JoinError::is_panic(). Программа при этом не должна упасть.

Ожидаемый вывод:
паника: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let e = h.await.unwrap_err(); e.is_panic()', '{"crates": ["tokio"], "driver": "", "expected": ["паника: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-supervisor', 18, 'rust', 'Супервайзер', 'Задача при первых двух запусках паникует, на третьем завершается нормально; каждый запуск печатает «запуск N». Напишите цикл-супервайзер: пока хэндл возвращает ошибку, запускайте задачу заново. После успеха напечатайте «готово».

Ожидаемый вывод:
запуск 1
запуск 2
запуск 3
готово', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'AtomicUsize считает запуски; if tokio::spawn(..).await.is_ok() { break }', '{"crates": ["tokio"], "driver": "", "expected": ["запуск 1", "запуск 2", "запуск 3", "готово"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-retry-limit', 19, 'rust', 'Повторы с пределом', 'Операция всегда падает (Err("fail")). Повторите её не более 3 раз с паузой 10 мс между попытками. Напечатайте «попыток: 3» и «итог: Err».

Ожидаемый вывод:
попыток: 3
итог: Err', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Счётчик попыток, пауза после каждой неудачи, выход по пределу.', '{"crates": ["tokio"], "driver": "", "expected": ["попыток: 3", "итог: Err"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-interval-limit', 20, 'rust', 'Ограничение частоты интервалом', 'Обработайте 5 событий, перед каждым ожидая tick() интервала 20 мс (первый тик сразу). Напечатайте «ограничено: true», если всё заняло не меньше 70 мс.

Ожидаемый вывод:
ограничено: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Тики на 0, 20, 40, 60, 80 мс — до последнего события 80 мс.', '{"crates": ["tokio"], "driver": "", "expected": ["ограничено: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-refill', 21, 'rust', 'Ведро токенов', 'Семафор без разрешений и фоновая задача: каждые 20 мс добавляет одно разрешение (add_permits(1)). Main берёт три разрешения подряд (acquire().await.forget()). Напечатайте «пополнение работает: true», если это заняло не меньше 55 мс.

Ожидаемый вывод:
пополнение работает: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'sem.acquire().await.unwrap().forget() — токен потрачен, а не возвращён.', '{"crates": ["tokio"], "driver": "", "expected": ["пополнение работает: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-bucket-burst', 22, 'rust', 'Всплеск и ожидание', 'Ведро на 3 токена изначально полное, пополнение — по одному каждые 50 мс. Возьмите 3 токена (должно занять меньше 20 мс) и напечатайте «всплеск: true», затем возьмите четвёртый и напечатайте «четвёртый ждал: true» (не меньше 40 мс).

Ожидаемый вывод:
всплеск: true
четвёртый ждал: true', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'Измеряйте Instant перед и после acquire; пополнение — в фоновой задаче.', '{"crates": ["tokio"], "driver": "", "expected": ["всплеск: true", "четвёртый ждал: true"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-metrics', 23, 'rust', 'Метрики рантайма', 'В обычной fn main постройте многопоточный рантайм с 2 рабочими потоками (Builder, enable_all) и напечатайте rt.metrics().num_workers().

Ожидаемый вывод:
2', 'fn main() {
    // ваш код
}
', 'tokio::runtime::Builder::new_multi_thread().worker_threads(2).enable_all().build()', '{"crates": ["tokio"], "driver": "", "expected": ["2"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-yield', 24, 'rust', 'yield_now: уступить поток', 'На однопоточном рантайме запустите задачу, которая поднимает общий AtomicBool. В main ждите, пока флаг поднимется, циклом с tokio::task::yield_now().await (без sleep) и напечатайте «флаг поднят».

Ожидаемый вывод:
флаг поднят', '#[tokio::main(flavor = "current_thread")]
async fn main() {
    // ваш код
}
', 'while !flag.load(Ordering::SeqCst) { tokio::task::yield_now().await; } — без yield_now задача никогда не получит поток.', '{"crates": ["tokio"], "driver": "", "expected": ["флаг поднят"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-actor-timeout', 25, 'rust', 'Актор не отвечает', 'Актор принимает запрос с oneshot::Sender и «зависает» (сон 500 мс, ответа нет). Клиент ждёт ответ с timeout 50 мс и при просрочке печатает «актор не ответил».

Ожидаемый вывод:
актор не ответил', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'timeout(Duration::from_millis(50), reply_rx).await.is_err()', '{"crates": ["tokio"], "driver": "", "expected": ["актор не ответил"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-drain', 26, 'rust', 'Дочитать очередь', 'Производитель отправляет 5 заданий и закрывает канал. Потребитель обрабатывает каждое (сон 5 мс) до закрытия и затем печатает «обработано: 5» — очередь не теряется при закрытии.

Ожидаемый вывод:
обработано: 5', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'while let Some(_) = rx.recv().await — выходит только после того, как все сообщения прочитаны.', '{"crates": ["tokio"], "driver": "", "expected": ["обработано: 5"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-biased-stop', 27, 'rust', 'Остановка в приоритете', 'Токен уже отменён, а в очереди лежат задания. Цикл select! с biased; проверяет сначала cancelled(), затем recv(). Напечатайте «после остановки: 0» — число обработанных заданий.

Ожидаемый вывод:
после остановки: 0', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'tokio::select! { biased; _ = token.cancelled() => break, job = rx.recv() => .. }', '{"crates": ["tokio"], "driver": "", "expected": ["после остановки: 0"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-watch-flag', 28, 'rust', 'Флаг остановки через watch', 'Три рабочих ждут, пока watch-значение станет true (rx.wait_for(|v| *v).await). Main через 20 мс отправляет true и дожидается всех (JoinSet). Напечатайте «остановлены: 3».

Ожидаемый вывод:
остановлены: 3', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'let (tx, rx) = watch::channel(false); в задаче let mut rx = rx.clone(); rx.wait_for(|v| *v).await', '{"crates": ["tokio"], "driver": "", "expected": ["остановлены: 3"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 37, 'r37-explicit-close', 29, 'rust', 'Явное закрытие вместо async Drop', 'Структура Conn { closed: bool } с Drop: если closed == false, печатает «не закрыто!». Добавьте async fn close(mut self): ставит closed = true и спит 10 мс (имитация сброса буферов). Вызовите close и напечатайте «закрыто явно». Предупреждения из Drop быть не должно.

Ожидаемый вывод:
закрыто явно', '#[tokio::main]
async fn main() {
    // ваш код
}
', 'В close(mut self) выставьте флаг до того, как self уничтожится в конце функции.', '{"crates": ["tokio"], "driver": "", "expected": ["закрыто явно"], "standalone": true}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 38, 'r38-binary-search', 0, 'rust', 'Бинарный поиск со счётчиком шагов', 'Напишите binary_search(v: &[i32], x: i32) -> (Option<usize>, u32): индекс значения в отсортированном срезе (любой из подходящих при повторах) и число выполненных сравнений. Проверка подаёт миллион элементов и требует не больше 21 шага.', 'fn binary_search(v: &[i32], x: i32) -> (Option<usize>, u32) {
    todo!()
}
', 'Сравнивайте v[mid] с x и сдвигайте границы lo / hi; считайте каждую итерацию цикла.', '{"driver": "fn main() {\n    println!(\"{:?} {:?}\", binary_search(&[], 5).0, binary_search(&[5], 5).0);\n    let v: Vec<i32> = (0..1_000_000).map(|x| x * 2).collect();\n    let mut worst = 0;\n    let mut found = 0;\n    for x in (0..2_000_000).step_by(7919) {\n        let (idx, steps) = binary_search(&v, x);\n        worst = worst.max(steps);\n        if let Some(i) = idx {\n            assert_eq!(v[i], x);\n            found += 1;\n        }\n    }\n    println!(\"{} {}\", found, worst <= 21);\n    println!(\"{:?}\", binary_search(&v, -1).0);\n}\n", "expected": ["None Some(0)", "127 true", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 38, 'r38-merge-sort', 1, 'rust', 'Сортировка слиянием', 'Напишите merge_sort(v: &[i64]) -> Vec<i64> — устойчивая сортировка слиянием за O(n log n). Проверка подаёт 300 000 чисел.', 'fn merge_sort(v: &[i64]) -> Vec<i64> {
    todo!()
}
', 'split_at делит срез на две части; слияние — два индекса; рекурсия до длины 1.', '{"driver": "struct Lcg(u64);\nimpl Lcg {\n    fn next(&mut self) -> u64 {\n        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n        self.0 >> 33\n    }\n}\nfn main() {\n    println!(\"{:?} {:?}\", merge_sort(&[]), merge_sort(&[3, 1, 2, 1, -5]));\n    let mut rng = Lcg(42);\n    let v: Vec<i64> = (0..300_000).map(|_| (rng.next() % 1_000_000) as i64 - 500_000).collect();\n    let sorted = merge_sort(&v);\n    let mut expected = v.clone();\n    expected.sort();\n    println!(\"{} {}\", sorted == expected, sorted.len());\n}\n", "expected": ["[] [-5, 1, 1, 2, 3]", "true 300000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 38, 'r38-kth-largest', 2, 'rust', 'k-й по величине через кучу', 'Напишите kth_largest(v: &[i32], k: usize) -> Option<i32>: k-й по величине элемент (k = 1 — максимум; повторы считаются отдельно); None, если k = 0 или k > длины. Память O(k): проверка подаёт 2 миллиона чисел.', 'fn kth_largest(v: &[i32], k: usize) -> Option<i32> {
    todo!()
}
', 'Куча на k элементов с обёрткой Reverse: после просмотра всех элементов на вершине — k-й по величине.', '{"driver": "struct Lcg(u64);\nimpl Lcg {\n    fn next(&mut self) -> u64 {\n        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n        self.0 >> 33\n    }\n}\nfn main() {\n    println!(\"{:?} {:?} {:?}\", kth_largest(&[3, 1, 4, 1, 5, 9, 2, 6], 1), kth_largest(&[3, 1, 4, 1, 5, 9, 2, 6], 3), kth_largest(&[3, 1, 4, 1, 5, 9, 2, 6], 8));\n    println!(\"{:?} {:?} {:?}\", kth_largest(&[1, 2], 0), kth_largest(&[1, 2], 3), kth_largest(&[], 1));\n    let mut rng = Lcg(7);\n    let v: Vec<i32> = (0..2_000_000).map(|_| (rng.next() % 1_000_000_000) as i32).collect();\n    let mut sorted = v.clone();\n    sorted.sort_by(|a, b| b.cmp(a));\n    println!(\"{} {}\", kth_largest(&v, 10) == Some(sorted[9]), kth_largest(&v, 1000) == Some(sorted[999]));\n}\n", "expected": ["Some(9) Some(5) Some(1)", "None None None", "true true"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 38, 'r38-grid-bfs', 3, 'rust', 'Кратчайший путь в лабиринте', 'Напишите shortest_path(grid: &[&str], start: (usize, usize), goal: (usize, usize)) -> Option<usize>: число шагов по клеткам (вверх, вниз, влево, вправо) из start в goal; ''#'' — стена, ''.'' — свободно. Если пути нет или start/goal — стены — None. Проверка подаёт поле 1000×1000.', 'fn shortest_path(grid: &[&str], start: (usize, usize), goal: (usize, usize)) -> Option<usize> {
    todo!()
}
', 'BFS по клеткам: dist — таблица расстояний, usize::MAX — «не посещена»; соседей вычисляйте осторожно, чтобы не вычесть из нуля.', '{"driver": "fn main() {\n    let maze = [\"..#....\", \".##.##.\", \"....#..\", \".##...#\", \"...#...\"];\n    println!(\"{:?}\", shortest_path(&maze, (0, 0), (4, 6)));\n    println!(\"{:?}\", shortest_path(&maze, (0, 0), (0, 3)));\n    println!(\"{:?}\", shortest_path(&maze, (0, 0), (0, 2)));\n    println!(\"{:?}\", shortest_path(&[\".\"], (0, 0), (0, 0)));\n    let open: Vec<String> = (0..1000).map(|_| \".\".repeat(1000)).collect();\n    let refs: Vec<&str> = open.iter().map(|s| s.as_str()).collect();\n    println!(\"{:?}\", shortest_path(&refs, (0, 0), (999, 999)));\n}\n", "expected": ["Some(10)", "Some(7)", "None", "Some(0)", "Some(1998)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 38, 'r38-dijkstra', 4, 'rust', 'Дейкстра на большом графе', 'Напишите dijkstra(n: usize, edges: &[(usize, usize, u64)], s: usize) -> Vec<Option<u64>>: ориентированные взвешенные рёбра (от, к, вес); расстояния от s (None — недостижима). Проверка подаёт 100 000 вершин и 500 000 рёбер.', 'fn dijkstra(n: usize, edges: &[(usize, usize, u64)], s: usize) -> Vec<Option<u64>> {
    todo!()
}
', 'Список смежности + BinaryHeap<Reverse<(u64, usize)>>; устаревшие записи пропускайте при извлечении.', '{"driver": "struct Lcg(u64);\nimpl Lcg {\n    fn next(&mut self) -> u64 {\n        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n        self.0 >> 33\n    }\n}\nfn main() {\n    let e = [(0, 1, 7), (0, 2, 2), (2, 1, 3), (1, 3, 1), (2, 3, 8)];\n    println!(\"{:?}\", dijkstra(5, &e, 0));\n    println!(\"{:?}\", dijkstra(1, &[], 0));\n    let mut rng = Lcg(99);\n    let n = 100_000;\n    let edges: Vec<(usize, usize, u64)> = (0..500_000)\n        .map(|_| ((rng.next() % n as u64) as usize, (rng.next() % n as u64) as usize, rng.next() % 1000 + 1))\n        .collect();\n    let d = dijkstra(n, &edges, 0);\n    let reachable = d.iter().filter(|x| x.is_some()).count();\n    let sum: u64 = d.iter().flatten().sum();\n    println!(\"{} {}\", reachable, sum);\n}\n", "expected": ["[Some(0), Some(5), Some(2), Some(6), None]", "[Some(0)]", "99374 206257411"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 38, 'r38-lcs', 5, 'rust', 'LCS на длинных строках', 'Напишите lcs(a: &str, b: &str) -> usize: длина наибольшей общей подпоследовательности (по символам). Проверка подаёт две строки по 4000 символов — таблица во всю длину не нужна.', 'fn lcs(a: &str, b: &str) -> usize {
    todo!()
}
', 'Две строки таблицы (prev, cur); строки превратите в Vec<char>, чтобы индексировать символы.', '{"driver": "struct Lcg(u64);\nimpl Lcg {\n    fn next(&mut self) -> u64 {\n        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n        self.0 >> 33\n    }\n}\nfn main() {\n    println!(\"{} {} {}\", lcs(\"abcde\", \"ace\"), lcs(\"abc\", \"xyz\"), lcs(\"\", \"abc\"));\n    println!(\"{}\", lcs(\"привет мир\", \"превед медвед\"));\n    let mut rng = Lcg(5);\n    let a: String = (0..4000).map(|_| (b''a'' + (rng.next() % 4) as u8) as char).collect();\n    let b: String = (0..4000).map(|_| (b''a'' + (rng.next() % 4) as u8) as char).collect();\n    println!(\"{} {}\", lcs(&a, &a), lcs(&a, &b));\n}\n", "expected": ["3 0 0", "6", "4000 2591"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 38, 'r38-components', 6, 'rust', 'Компоненты связности', 'Напишите count_components(n: usize, edges: &[(usize, usize)]) -> usize: число компонент связности неориентированного графа (изолированные вершины — отдельные компоненты). Проверка: миллион вершин и миллион рёбер.', 'fn count_components(n: usize, edges: &[(usize, usize)]) -> usize {
    todo!()
}
', 'Union-Find с сжатием путей (итеративным, чтобы не переполнить стек на длинных цепочках).', '{"driver": "struct Lcg(u64);\nimpl Lcg {\n    fn next(&mut self) -> u64 {\n        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n        self.0 >> 33\n    }\n}\nfn main() {\n    println!(\"{} {} {}\", count_components(5, &[(0, 1), (1, 2), (3, 4)]), count_components(3, &[]), count_components(0, &[]));\n    println!(\"{}\", count_components(4, &[(0, 0), (1, 1)]));\n    let mut rng = Lcg(3);\n    let n = 1_000_000;\n    let edges: Vec<(usize, usize)> = (0..1_000_000).map(|_| ((rng.next() % n as u64) as usize, (rng.next() % n as u64) as usize)).collect();\n    println!(\"{}\", count_components(n, &edges));\n}\n", "expected": ["2 3 0", "4", "161915"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 38, 'r38-kruskal', 7, 'rust', 'Минимальное остовное дерево', 'Напишите mst_weight(n: usize, edges: &[(usize, usize, u64)]) -> Option<u64>: суммарный вес минимального остовного дерева (Краскал) или None, если граф несвязен. n = 0 или 1 — вес 0.', 'fn mst_weight(n: usize, edges: &[(usize, usize, u64)]) -> Option<u64> {
    todo!()
}
', 'Отсортируйте рёбра по весу и добавляйте те, что соединяют разные компоненты; в остове ровно n − 1 ребро.', '{"driver": "struct Lcg(u64);\nimpl Lcg {\n    fn next(&mut self) -> u64 {\n        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n        self.0 >> 33\n    }\n}\nfn main() {\n    let e = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8)];\n    println!(\"{:?} {:?} {:?}\", mst_weight(4, &e), mst_weight(5, &e), mst_weight(1, &[]));\n    println!(\"{:?}\", mst_weight(0, &[]));\n    let mut rng = Lcg(11);\n    let n = 50_000;\n    let mut edges: Vec<(usize, usize, u64)> = (1..n).map(|i| (i - 1, i, rng.next() % 1000 + 1)).collect();\n    for _ in 0..300_000 {\n        edges.push(((rng.next() % n as u64) as usize, (rng.next() % n as u64) as usize, rng.next() % 1000 + 1));\n    }\n    println!(\"{:?}\", mst_weight(n, &edges));\n}\n", "expected": ["Some(8) None Some(0)", "Some(0)", "Some(4271456)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 38, 'r38-topo', 8, 'rust', 'Топологическая сортировка', 'Напишите topo_order(n: usize, edges: &[(usize, usize)]) -> Option<Vec<usize>>: порядок вершин 0..n так, чтобы для каждого ребра (a, b) вершина a стояла раньше b; из доступных всегда берите вершину с наименьшим номером. При цикле — None.', 'fn topo_order(n: usize, edges: &[(usize, usize)]) -> Option<Vec<usize>> {
    todo!()
}
', 'Алгоритм Кана: степени входа + куча готовых вершин (наименьший номер первым).', '{"driver": "fn main() {\n    println!(\"{:?}\", topo_order(6, &[(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]));\n    println!(\"{:?}\", topo_order(3, &[(0, 1), (1, 2), (2, 0)]));\n    println!(\"{:?} {:?}\", topo_order(0, &[]), topo_order(3, &[]));\n    let n = 200_000;\n    let chain: Vec<(usize, usize)> = (1..n).map(|i| (i, i - 1)).collect();\n    let r = topo_order(n, &chain).unwrap();\n    println!(\"{} {} {}\", r.len(), r[0], r[n - 1]);\n}\n", "expected": ["Some([4, 5, 0, 2, 3, 1])", "None", "Some([]) Some([0, 1, 2])", "200000 199999 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 38, 'r38-safe-arith', 9, 'rust', 'Осторожная арифметика', 'Напишите safe_factorial(n: u32) -> Option<u64> (None при переполнении u64), mean_u8(v: &[u8]) -> Option<u8> (среднее с округлением вниз, без переполнения; None для пустого) и distance(a: usize, b: usize) -> usize (|a − b| без паники).', 'fn safe_factorial(n: u32) -> Option<u64> {
    todo!()
}

fn mean_u8(v: &[u8]) -> Option<u8> {
    todo!()
}

fn distance(a: usize, b: usize) -> usize {
    todo!()
}
', 'checked_mul возвращает None при переполнении, оператор ? прерывает функцию; сумму u8 копите в более широком типе.', '{"driver": "fn main() {\n    println!(\"{:?} {:?} {:?} {:?}\", safe_factorial(0), safe_factorial(5), safe_factorial(20), safe_factorial(21));\n    println!(\"{:?} {:?} {:?}\", mean_u8(&[255, 255, 254]), mean_u8(&[]), mean_u8(&[1, 2]));\n    println!(\"{} {} {}\", distance(3, 10), distance(10, 3), distance(0, 0));\n}\n", "expected": ["Some(1) Some(120) Some(2432902008176640000) None", "Some(254) None Some(1)", "7 7 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 39, 'r39-bit-tricks', 0, 'rust', 'Битовые трюки', 'Напишите без готовых методов count_ones, is_power_of_two и reverse_bits: lowest_set_bit(n: u32) -> u32 (само младшее «горящее» значение, 0 для 0), is_pow2(n: u64) -> bool (0 — нет), parity(n: u32) -> bool (число единичных битов нечётно) и reverse8(n: u8) -> u8 (биты в обратном порядке).', 'fn lowest_set_bit(n: u32) -> u32 {
    todo!()
}

fn is_pow2(n: u64) -> bool {
    todo!()
}

fn parity(n: u32) -> bool {
    todo!()
}

fn reverse8(n: u8) -> u8 {
    todo!()
}
', 'n & n.wrapping_neg() выделяет младшую единицу; n & (n - 1) сбрасывает её.', '{"driver": "fn main() {\n    println!(\"{} {} {} {}\", lowest_set_bit(0), lowest_set_bit(12), lowest_set_bit(0x8000_0000), lowest_set_bit(7));\n    println!(\"{} {} {} {}\", is_pow2(0), is_pow2(1), is_pow2(1 << 40), is_pow2(96));\n    println!(\"{} {} {} {}\", parity(0), parity(1), parity(3), parity(0b1011_0000));\n    println!(\"{:08b} {:08b} {:08b}\", reverse8(0b0000_0001), reverse8(0b1011_0000), reverse8(0xFF));\n}\n", "expected": ["0 4 2147483648 1", "false true true false", "false true false true", "10000000 00001101 11111111"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 39, 'r39-header', 1, 'rust', 'Разбор двоичного заголовка', 'Формат заголовка (8 байт): магическое число 0xCAFE (u16, старший байт первым), версия (u8), длина данных (u32, младший байт первым), флаги (u8). Напишите parse_header(b: &[u8]) -> Option<(u8, u32, u8)> (версия, длина, флаги; None — если байтов меньше 8 или магия не совпала) и build_header(version: u8, len: u32, flags: u8) -> [u8; 8].', 'fn parse_header(b: &[u8]) -> Option<(u8, u32, u8)> {
    todo!()
}

fn build_header(version: u8, len: u32, flags: u8) -> [u8; 8] {
    todo!()
}
', 'u16::from_be_bytes([b[0], b[1]]), u32::from_le_bytes([...4 байта...]); массив байтов собирайте из to_be_bytes / to_le_bytes.', '{"driver": "fn main() {\n    let h = build_header(2, 0x0001_0203, 0b101);\n    println!(\"{:02x?}\", h);\n    println!(\"{:?}\", parse_header(&h));\n    println!(\"{:?} {:?}\", parse_header(&h[..7]), parse_header(&[0xCA, 0xFF, 1, 0, 0, 0, 0, 0]));\n    let mut longer = h.to_vec();\n    longer.extend_from_slice(&[9, 9, 9]);\n    println!(\"{:?}\", parse_header(&longer));\n}\n", "expected": ["[ca, fe, 02, 03, 02, 01, 00, 05]", "Some((2, 66051, 5))", "None None", "Some((2, 66051, 5))"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 39, 'r39-varint', 2, 'rust', 'Varint с проверкой ошибок', 'Напишите varint_encode(n: u64) -> Vec<u8> и varint_decode(b: &[u8]) -> Result<(u64, usize), &''static str>: число и сколько байтов прочитано. Ошибки: пустой вход или оборвавшаяся запись (все байты с признаком продолжения) → "truncated"; запись длиннее 10 байтов или не помещающаяся в u64 → "overflow".', 'fn varint_encode(n: u64) -> Vec<u8> {
    todo!()
}

fn varint_decode(b: &[u8]) -> Result<(u64, usize), &''static str> {
    todo!()
}
', 'Каждый байт даёт 7 бит со сдвигом 7·i; десятый байт может нести только один значащий бит.', '{"driver": "fn main() {\n    for n in [0u64, 1, 127, 128, 300, 16384, u32::MAX as u64, u64::MAX] {\n        let e = varint_encode(n);\n        println!(\"{} {} {:?}\", n, e.len(), varint_decode(&e) == Ok((n, e.len())));\n    }\n    println!(\"{:?} {:?}\", varint_decode(&[]), varint_decode(&[0x80, 0x80]));\n    println!(\"{:?}\", varint_decode(&[0xff; 11]));\n    println!(\"{:?}\", varint_decode(&[0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x02]));\n    println!(\"{:?}\", varint_decode(&[0xac, 0x02, 0xff]));\n}\n", "expected": ["0 1 true", "1 1 true", "127 1 true", "128 2 true", "300 2 true", "16384 3 true", "4294967295 5 true", "18446744073709551615 10 true", "Err(\"truncated\") Err(\"truncated\")", "Err(\"overflow\")", "Err(\"overflow\")", "Ok((300, 2))"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 39, 'r39-crc32', 3, 'rust', 'CRC-32 по таблице', 'Напишите crc32(data: &[u8]) -> u32 (многочлен 0xEDB88320 в отражённом виде, начальное значение 0xFFFFFFFF, итог инвертируется) — как zlib.crc32 в питоне. Проверка подаёт 8 МБ данных.', 'fn crc32(data: &[u8]) -> u32 {
    todo!()
}
', 'Таблицу из 256 значений считайте один раз перед циклом по данным.', '{"driver": "fn main() {\n    println!(\"{:08x} {:08x} {:08x}\", crc32(b\"\"), crc32(b\"hello\"), crc32(b\"123456789\"));\n    let big: Vec<u8> = (0..8_000_000u32).map(|i| (i % 251) as u8).collect();\n    println!(\"{:08x}\", crc32(&big));\n}\n", "expected": ["00000000 3610a686 cbf43926", "37ac4d4a"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 39, 'r39-base64', 4, 'rust', 'Base64', 'Напишите base64_encode(data: &[u8]) -> String (алфавит A–Z a–z 0–9 + /, добивка ''='') и base64_decode(s: &str) -> Option<Vec<u8>> (None при недопустимом символе или неверной длине).', 'fn base64_encode(data: &[u8]) -> String {
    todo!()
}

fn base64_decode(s: &str) -> Option<Vec<u8>> {
    todo!()
}
', 'Три байта = 24 бита = четыре шестибитных индекса в алфавите; недостающие байты — нули, а в выводе знаки ''=''.', '{"driver": "fn main() {\n    for s in [\"\", \"f\", \"fo\", \"foo\", \"foob\", \"fooba\", \"foobar\", \"Привет\"] {\n        let e = base64_encode(s.as_bytes());\n        let d = base64_decode(&e).unwrap();\n        println!(\"{:?} {} {}\", s, e, d == s.as_bytes());\n    }\n    println!(\"{:?} {:?} {:?}\", base64_decode(\"Zm9v!\"), base64_decode(\"Zm9\"), base64_decode(\"Zg=A\"));\n    println!(\"{}\", base64_encode(&[0xff, 0xfe, 0xfd]));\n}\n", "expected": ["\"\"  true", "\"f\" Zg== true", "\"fo\" Zm8= true", "\"foo\" Zm9v true", "\"foob\" Zm9vYg== true", "\"fooba\" Zm9vYmE= true", "\"foobar\" Zm9vYmFy true", "\"Привет\" 0J/RgNC40LLQtdGC true", "None None None", "//79"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 39, 'r39-bitset', 5, 'rust', 'Битовое множество и решето', 'Дополните BitSet: new(len), set(i), clear(i), get(i), count() -> u32, ones() -> Vec<usize> (номера единиц по возрастанию), union_with(&mut self, other: &BitSet). Затем напишите primes_below(n: usize) -> Vec<usize> — решето Эратосфена на BitSet (проверка: n = 20 миллионов).', 'struct BitSet {
    words: Vec<u64>,
    len: usize,
}

impl BitSet {
    fn new(len: usize) -> BitSet {
        todo!()
    }
    fn set(&mut self, i: usize) {
        todo!()
    }
    fn clear(&mut self, i: usize) {
        todo!()
    }
    fn get(&self, i: usize) -> bool {
        todo!()
    }
    fn count(&self) -> u32 {
        todo!()
    }
    fn ones(&self) -> Vec<usize> {
        todo!()
    }
    fn union_with(&mut self, other: &BitSet) {
        todo!()
    }
}

fn primes_below(n: usize) -> Vec<usize> {
    todo!()
}
', 'trailing_zeros() + w &= w - 1 перебирают единичные биты слова; решето: пометьте кратные i, начиная с i·i.', '{"driver": "fn main() {\n    let mut a = BitSet::new(130);\n    for i in [0, 5, 64, 129] {\n        a.set(i);\n    }\n    let mut b = BitSet::new(130);\n    b.set(5);\n    b.set(100);\n    a.union_with(&b);\n    a.clear(0);\n    println!(\"{:?} {} {} {}\", a.ones(), a.count(), a.get(100), a.get(0));\n    println!(\"{:?} {}\", primes_below(30), primes_below(2).len());\n    let p = primes_below(20_000_000);\n    println!(\"{} {:?}\", p.len(), p.last());\n}\n", "expected": ["[5, 64, 100, 129] 4 true false", "[2, 3, 5, 7, 11, 13, 17, 19, 23, 29] 0", "1270607 Some(19999999)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 39, 'r39-cpu', 6, 'rust', 'Эмулятор процессора', 'Реализуйте run(prog: &[Instr], limit: u32) -> Result<Cpu, Trap>. Процессор: регистры regs: [u8; 4], память mem: [u8; 16], pc, zero, steps. Команды: Ldi(r, v), Mov(a, b), Add(a, b), Sub(a, b) (оборачивающие, обновляют флаг zero по результату), Ld(r, addr), St(r, addr), Jmp(t), Jz(t), Jnz(t), Hlt (останавливает; тоже считается шагом). Ловушки: адрес памяти ≥ 16 → Trap::BadAddress(addr), pc ≥ длины программы без Hlt → Trap::PcOutOfRange(pc), больше limit шагов → Trap::Timeout. Каждое выполнение команды увеличивает steps.', '#[derive(Debug, Clone, Copy)]
enum Instr {
    Ldi(usize, u8),
    Mov(usize, usize),
    Add(usize, usize),
    Sub(usize, usize),
    Ld(usize, usize),
    St(usize, usize),
    Jmp(usize),
    Jz(usize),
    Jnz(usize),
    Hlt,
}

#[derive(Debug, PartialEq)]
enum Trap {
    BadAddress(usize),
    PcOutOfRange(usize),
    Timeout,
}

#[derive(Debug)]
struct Cpu {
    regs: [u8; 4],
    mem: [u8; 16],
    pc: usize,
    zero: bool,
    steps: u32,
}

fn run(prog: &[Instr], limit: u32) -> Result<Cpu, Trap> {
    todo!()
}
', 'Проверяйте pc перед чтением команды; ?-оператор вместе с ok_or превращает выход за массив в Trap.', '{"driver": "fn main() {\n    use Instr::*;\n    let sum = [Ldi(0, 0), Ldi(1, 5), Ldi(2, 1), Add(0, 1), Sub(1, 2), Jnz(3), Hlt];\n    let c = run(&sum, 1000).unwrap();\n    println!(\"{:?} {} {}\", c.regs, c.steps, c.zero);\n    let mem = [Ldi(0, 42), St(0, 3), Ldi(0, 0), Ld(1, 3), Hlt];\n    let c = run(&mem, 100).unwrap();\n    println!(\"{:?} {:?}\", c.regs, &c.mem[..5]);\n    println!(\"{:?}\", run(&[Ldi(0, 1), St(0, 16)], 100).err());\n    println!(\"{:?}\", run(&[Ldi(0, 1)], 100).err());\n    println!(\"{:?}\", run(&[Jmp(0)], 50).err());\n    println!(\"{:?}\", run(&[Ldi(0, 250), Ldi(1, 10), Add(0, 1), Hlt], 10).map(|c| (c.regs[0], c.zero)));\n    println!(\"{:?}\", run(&[Jmp(7)], 10).err());\n}\n", "expected": ["[15, 0, 1, 0] 19 true", "[0, 42, 0, 0] [0, 0, 0, 42, 0]", "Some(BadAddress(16))", "Some(PcOutOfRange(1))", "Some(Timeout)", "Ok((4, false))", "Some(PcOutOfRange(7))"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 39, 'r39-encode-instr', 7, 'rust', 'Машинный код команд', 'Кодируйте команды в два байта: байт 0 = код операции << 4 | a << 2 | b, байт 1 = число или адрес (0, если нет). Коды: Hlt 0, Ldi 1, Mov 2, Add 3, Sub 4, Ld 5, St 6, Jmp 7, Jz 8, Jnz 9. Для Ldi(r, v): a = r, байт 1 = v; для Mov/Add/Sub(a, b): a, b; для Ld(r, addr) и St(r, addr): a = r, байт 1 = addr (адрес ≤ 255); для переходов: байт 1 = цель. Напишите encode(i: &Instr) -> [u8; 2] и decode(b: [u8; 2]) -> Option<Instr> (None для неизвестного кода операции).', '#[derive(Debug, Clone, Copy, PartialEq)]
enum Instr {
    Ldi(usize, u8),
    Mov(usize, usize),
    Add(usize, usize),
    Sub(usize, usize),
    Ld(usize, usize),
    St(usize, usize),
    Jmp(usize),
    Jz(usize),
    Jnz(usize),
    Hlt,
}

fn encode(i: &Instr) -> [u8; 2] {
    todo!()
}

fn decode(b: [u8; 2]) -> Option<Instr> {
    todo!()
}
', 'Поля байта 0 собираются сдвигами: op << 4 | a << 2 | b; разбор — обратными сдвигами и маской 3.', '{"driver": "fn main() {\n    use Instr::*;\n    let prog = [Ldi(1, 5), Add(0, 1), Sub(1, 2), Jnz(3), Ld(2, 200), St(3, 17), Mov(3, 0), Jz(9), Jmp(0), Hlt];\n    for i in &prog {\n        let e = encode(i);\n        println!(\"{:02x} {:02x} {}\", e[0], e[1], decode(e) == Some(*i));\n    }\n    println!(\"{:?} {:?}\", decode([0xA0, 0]), decode([0xF3, 9]));\n}\n", "expected": ["14 05 true", "31 00 true", "46 00 true", "90 03 true", "58 c8 true", "6c 11 true", "2c 00 true", "80 09 true", "70 00 true", "00 00 true", "None None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 39, 'r39-cache', 8, 'rust', 'Симулятор кэша', 'Напишите cache_sim(trace: &[u64], lines: usize, line_size: u64) -> (u64, u64): кэш с прямым отображением (как в курсе по архитектуре): блок = адрес / line_size, строка = блок % lines, тег = блок / lines; верните (попадания, промахи). Проверка: 5 миллионов обращений.', 'fn cache_sim(trace: &[u64], lines: usize, line_size: u64) -> (u64, u64) {
    todo!()
}
', 'Таблица тегов Vec<Option<u64>>; сравнивайте tags[idx] с Some(tag).', '{"driver": "struct Lcg(u64);\nimpl Lcg {\n    fn next(&mut self) -> u64 {\n        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n        self.0 >> 33\n    }\n}\nfn main() {\n    println!(\"{:?}\", cache_sim(&[0, 4, 8, 16, 0, 64, 0], 4, 16));\n    println!(\"{:?} {:?}\", cache_sim(&[], 4, 16), cache_sim(&[0, 0, 0], 4, 16));\n    let seq: Vec<u64> = (0..1_000_000u64).map(|i| i * 4).collect();\n    println!(\"{:?}\", cache_sim(&seq, 64, 64));\n    let mut rng = Lcg(1);\n    let rnd: Vec<u64> = (0..5_000_000).map(|_| rng.next() % 100_000).collect();\n    let (h, m) = cache_sim(&rnd, 1024, 64);\n    println!(\"{}\", h + m);\n}\n", "expected": ["(3, 4)", "(0, 0) (2, 1)", "(937500, 62500)", "5000000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 39, 'r39-alu-flags', 9, 'rust', 'АЛУ с флагами', 'Напишите alu(op: &str, a: u8, b: u8) -> (u8, bool, bool, bool, bool): op — "ADD" или "SUB"; результат и флаги (zero, negative, carry, overflow). carry — перенос при сложении или заём (a < b) при вычитании; overflow — знаковое переполнение (операнды как числа в дополнительном коде).', 'fn alu(op: &str, a: u8, b: u8) -> (u8, bool, bool, bool, bool) {
    todo!()
}
', 'overflowing_add/sub возвращают (результат, признак); для знакового переполнения выполните ту же операцию над i8.', '{"driver": "fn main() {\n    for (op, a, b) in [(\"ADD\", 100, 100), (\"ADD\", 255, 1), (\"ADD\", 127, 1), (\"ADD\", 128, 128), (\"SUB\", 5, 7), (\"SUB\", 128, 1), (\"SUB\", 0, 0), (\"SUB\", 127, 255)] {\n        println!(\"{} {} {} {:?}\", op, a, b, alu(op, a, b));\n    }\n}\n", "expected": ["ADD 100 100 (200, false, true, false, true)", "ADD 255 1 (0, true, false, true, false)", "ADD 127 1 (128, false, true, false, true)", "ADD 128 128 (0, true, false, true, true)", "SUB 5 7 (254, false, true, true, false)", "SUB 128 1 (127, false, false, false, true)", "SUB 0 0 (0, true, false, false, false)", "SUB 127 255 (128, false, true, true, true)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 40, 'r40-wc', 0, 'rust', 'wc: строки, слова, байты', 'Напишите count_stats<R: std::io::Read>(r: R) -> std::io::Result<(usize, usize, usize)>: число строк (символов ''\n'' плюс последняя строка без перевода), слов (по пробельным символам) и байтов. Читайте буферизованно: проверка подаёт 20 МБ.', 'use std::io::Read;

fn count_stats<R: Read>(r: R) -> std::io::Result<(usize, usize, usize)> {
    todo!()
}
', 'read_until(b''\n'', &mut buf) читает строку вместе с переводом; считайте байты по числу прочитанного.', '{"driver": "use std::io::Cursor;\n\nfn main() {\n    println!(\"{:?}\", count_stats(Cursor::new(\"one two\\nthree\\n\\nfour five six\")).unwrap());\n    println!(\"{:?} {:?}\", count_stats(Cursor::new(\"\")).unwrap(), count_stats(Cursor::new(\"\\n\")).unwrap());\n    println!(\"{:?}\", count_stats(Cursor::new(\"привет мир\\n\")).unwrap());\n    let big = \"lorem ipsum dolor sit amet\\n\".repeat(750_000);\n    println!(\"{:?}\", count_stats(Cursor::new(big)).unwrap());\n}\n", "expected": ["(4, 6, 28)", "(0, 0, 0) (1, 0, 1)", "(1, 2, 20)", "(750000, 3750000, 20250000)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 40, 'r40-paths', 1, 'rust', 'Лексический разбор путей', 'Напишите без обращения к файловой системе: normalize(path: &str) -> String (как в курсе по ОС: убрать ''.'', повторные ''/'', обработать ''..'', результат абсолютный; для относительного пути ''..'' выше начала сохраняются) и ext_of(path: &str) -> Option<String> (расширение без точки; None для имён без точки или вида ''.bashrc'').', 'fn normalize(path: &str) -> String {
    todo!()
}

fn ext_of(path: &str) -> Option<String> {
    todo!()
}
', 'Стек компонентов; ''..'' снимает предыдущий компонент, но не другой ''..''; в абсолютном пути выше корня подняться нельзя.', '{"driver": "fn main() {\n    for p in [\"/usr/./bin/../lib//x/\", \"/\", \"/../..\", \"a/b/../../c\", \"../x/./y\", \"a/..\", \"\", \"./\", \"../../a/../b\"] {\n        println!(\"{:?} -> {:?}\", p, normalize(p));\n    }\n    for p in [\"/a/report.final.txt\", \"Makefile\", \"/a/.bashrc\", \"archive.tar.gz\", \"dir.d/file\", \"trailing.\"] {\n        println!(\"{:?} {:?}\", p, ext_of(p));\n    }\n}\n", "expected": ["\"/usr/./bin/../lib//x/\" -> \"/usr/lib/x\"", "\"/\" -> \"/\"", "\"/../..\" -> \"/\"", "\"a/b/../../c\" -> \"c\"", "\"../x/./y\" -> \"../x/y\"", "\"a/..\" -> \".\"", "\"\" -> \".\"", "\"./\" -> \".\"", "\"../../a/../b\" -> \"../../b\"", "\"/a/report.final.txt\" Some(\"txt\")", "\"Makefile\" None", "\"/a/.bashrc\" None", "\"archive.tar.gz\" Some(\"gz\")", "\"dir.d/file\" None", "\"trailing.\" None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 40, 'r40-list-tree', 2, 'rust', 'Дерево каталогов', 'Напишите list_tree(root: &Path) -> io::Result<Vec<String>>: относительные пути всех файлов и каталогов внутри root (каталоги — с ''/'' на конце), отсортированные по полному пути как строке.', 'use std::io;
use std::path::Path;

fn list_tree(root: &Path) -> io::Result<Vec<String>> {
    todo!()
}
', 'Рекурсия с префиксом пути; тип записи — e.file_type()?.is_dir(); в конце sort().', '{"driver": "fn tmp_dir(name: &str) -> std::path::PathBuf {\n    let d = std::env::temp_dir().join(format!(\"say13-{}-{}\", name, std::process::id()));\n    let _ = std::fs::remove_dir_all(&d);\n    std::fs::create_dir_all(&d).unwrap();\n    d\n}\nuse std::fs;\n\nfn main() {\n    let root = tmp_dir(\"tree\");\n    fs::create_dir_all(root.join(\"src/util\")).unwrap();\n    fs::create_dir_all(root.join(\"empty\")).unwrap();\n    fs::write(root.join(\"Cargo.toml\"), \"x\").unwrap();\n    fs::write(root.join(\"src/main.rs\"), \"m\").unwrap();\n    fs::write(root.join(\"src/util/mod.rs\"), \"\").unwrap();\n    println!(\"{:?}\", list_tree(&root).unwrap());\n    println!(\"{:?}\", list_tree(&root.join(\"empty\")).unwrap());\n    println!(\"{:?}\", list_tree(&root.join(\"nope\")).map_err(|e| e.kind()));\n    fs::remove_dir_all(&root).unwrap();\n}\n", "expected": ["[\"Cargo.toml\", \"empty/\", \"src/\", \"src/main.rs\", \"src/util/\", \"src/util/mod.rs\"]", "[]", "Err(NotFound)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 40, 'r40-dir-size', 3, 'rust', 'Размер каталога', 'Напишите dir_size(root: &Path) -> io::Result<u64>: суммарный размер всех обычных файлов внутри root (рекурсивно). Символические ссылки не разыменовывайте (не заходите и не считайте).', 'use std::io;
use std::path::Path;

fn dir_size(root: &Path) -> io::Result<u64> {
    todo!()
}
', 'e.file_type() не следует по ссылкам (в отличие от fs::metadata): is_file / is_dir у ссылки ложны.', '{"driver": "fn tmp_dir(name: &str) -> std::path::PathBuf {\n    let d = std::env::temp_dir().join(format!(\"say13-{}-{}\", name, std::process::id()));\n    let _ = std::fs::remove_dir_all(&d);\n    std::fs::create_dir_all(&d).unwrap();\n    d\n}\nuse std::fs;\n\nfn main() {\n    let root = tmp_dir(\"size\");\n    fs::create_dir_all(root.join(\"a/b\")).unwrap();\n    fs::write(root.join(\"one\"), vec![0u8; 100]).unwrap();\n    fs::write(root.join(\"a/two\"), vec![0u8; 2000]).unwrap();\n    fs::write(root.join(\"a/b/three\"), vec![1u8; 30]).unwrap();\n    #[cfg(unix)]\n    std::os::unix::fs::symlink(&root, root.join(\"a/loop\")).unwrap();\n    println!(\"{}\", dir_size(&root).unwrap());\n    println!(\"{}\", dir_size(&root.join(\"a/b\")).unwrap());\n    println!(\"{:?}\", dir_size(&root.join(\"zzz\")).map_err(|e| e.kind()));\n    fs::remove_dir_all(&root).unwrap();\n}\n", "expected": ["2130", "30", "Err(NotFound)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 40, 'r40-grep-file', 4, 'rust', 'grep по файлу', 'Напишите grep_file(path: &Path, needle: &str) -> io::Result<Vec<(usize, String)>>: пары (номер строки с единицы, строка), содержащие подстроку needle. Читайте построчно через BufReader.', 'use std::io;
use std::path::Path;

fn grep_file(path: &Path, needle: &str) -> io::Result<Vec<(usize, String)>> {
    todo!()
}
', 'lines() даёт Result<String>; enumerate() — номера с нуля, прибавьте единицу.', '{"driver": "fn tmp_dir(name: &str) -> std::path::PathBuf {\n    let d = std::env::temp_dir().join(format!(\"say13-{}-{}\", name, std::process::id()));\n    let _ = std::fs::remove_dir_all(&d);\n    std::fs::create_dir_all(&d).unwrap();\n    d\n}\nuse std::fs;\n\nfn main() {\n    let dir = tmp_dir(\"grep\");\n    let f = dir.join(\"log.txt\");\n    fs::write(&f, \"start\\nERROR disk full\\nok\\nERROR timeout\\n\\nend ERROR\").unwrap();\n    println!(\"{:?}\", grep_file(&f, \"ERROR\").unwrap());\n    println!(\"{:?} {:?}\", grep_file(&f, \"nothing\").unwrap(), grep_file(&f, \"\").unwrap().len());\n    println!(\"{:?}\", grep_file(&dir.join(\"missing\"), \"x\").map_err(|e| e.kind()));\n    fs::remove_dir_all(&dir).unwrap();\n}\n", "expected": ["[(2, \"ERROR disk full\"), (4, \"ERROR timeout\"), (6, \"end ERROR\")]", "[] 6", "Err(NotFound)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 40, 'r40-copy-filtered', 5, 'rust', 'Копирование с фильтром', 'Напишите copy_filtered(src: &Path, dst: &Path, keep: impl Fn(&str) -> bool) -> io::Result<usize>: читает src построчно, записывает в dst (через BufWriter, каждая строка заканчивается ''\n'') только строки, для которых keep вернул true; возвращает число записанных строк.', 'use std::io;
use std::path::Path;

fn copy_filtered(src: &Path, dst: &Path, keep: impl Fn(&str) -> bool) -> io::Result<usize> {
    todo!()
}
', 'BufWriter сам сбросится при уничтожении, но flush() явно возвращает ошибку записи — лучше вызвать его.', '{"driver": "fn tmp_dir(name: &str) -> std::path::PathBuf {\n    let d = std::env::temp_dir().join(format!(\"say13-{}-{}\", name, std::process::id()));\n    let _ = std::fs::remove_dir_all(&d);\n    std::fs::create_dir_all(&d).unwrap();\n    d\n}\nuse std::fs;\n\nfn main() {\n    let dir = tmp_dir(\"copy\");\n    let (a, b) = (dir.join(\"in.txt\"), dir.join(\"out.txt\"));\n    fs::write(&a, \"# comment\\nkey=1\\n\\nkey=2\\n# other\\nlast\").unwrap();\n    let n = copy_filtered(&a, &b, |l| !l.is_empty() && !l.starts_with(''#'')).unwrap();\n    println!(\"{} {:?}\", n, fs::read_to_string(&b).unwrap());\n    println!(\"{:?}\", copy_filtered(&dir.join(\"none\"), &b, |_| true).map_err(|e| e.kind()));\n    let big = dir.join(\"big.txt\");\n    fs::write(&big, \"line\\n\".repeat(300_000)).unwrap();\n    println!(\"{}\", copy_filtered(&big, &dir.join(\"big2.txt\"), |_| true).unwrap());\n    fs::remove_dir_all(&dir).unwrap();\n}\n", "expected": ["3 \"key=1\\nkey=2\\nlast\\n\"", "Err(NotFound)", "300000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 40, 'r40-run-capture', 6, 'rust', 'Запуск программы с отчётом', 'Напишите run_capture(cmd: &str, args: &[&str]) -> Result<(String, i32), String>: запускает программу и возвращает (stdout без перевода строки в конце, код возврата). Если программы нет — Err("not found: <cmd>"); если процесс убит сигналом (кода нет) — код −1; другие ошибки запуска — Err(текст ошибки).', 'use std::process::Command;

fn run_capture(cmd: &str, args: &[&str]) -> Result<(String, i32), String> {
    todo!()
}
', 'output() возвращает Err, только если процесс не удалось запустить; ненулевой код — это Ok со статусом.', '{"driver": "fn main() {\n    println!(\"{:?}\", run_capture(\"echo\", &[\"hi\", \"there\"]));\n    println!(\"{:?}\", run_capture(\"sh\", &[\"-c\", \"echo partial; exit 4\"]));\n    println!(\"{:?}\", run_capture(\"sh\", &[\"-c\", \"kill -9 $$\"]));\n    println!(\"{:?}\", run_capture(\"no-such-program-xyz\", &[]));\n    println!(\"{:?}\", run_capture(\"printf\", &[\"a\\\\nb\\\\n\\\\n\"]));\n}\n", "expected": ["Ok((\"hi there\", 0))", "Ok((\"partial\", 4))", "Ok((\"\", -1))", "Err(\"not found: no-such-program-xyz\")", "Ok((\"a\\nb\", 0))"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 40, 'r40-sort-process', 7, 'rust', 'Сортировка внешней программой', 'Напишите sort_with_process(lines: &[&str]) -> io::Result<Vec<String>>: отправьте строки на стандартный ввод программы sort, закройте ввод и верните строки её вывода.', 'use std::io;

fn sort_with_process(lines: &[&str]) -> io::Result<Vec<String>> {
    todo!()
}
', 'Стандартный ввод дочернего процесса нужно закрыть (уничтожить владельца) до wait_with_output.', '{"driver": "fn main() {\n    println!(\"{:?}\", sort_with_process(&[\"pear\", \"apple\", \"fig\", \"banana\"]).unwrap());\n    println!(\"{:?}\", sort_with_process(&[]).unwrap());\n    let many: Vec<String> = (0..50_000).map(|i| format!(\"{:06}\", (i * 7919) % 50_000)).collect();\n    let refs: Vec<&str> = many.iter().map(|s| s.as_str()).collect();\n    let r = sort_with_process(&refs).unwrap();\n    println!(\"{} {} {}\", r.len(), r[0], r[r.len() - 1]);\n}\n", "expected": ["[\"apple\", \"banana\", \"fig\", \"pear\"]", "[]", "50000 000000 049999"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 40, 'r40-kv-server', 8, 'rust', 'Сервер ключ-значение', 'Напишите handle_kv(stream: TcpStream, store: Arc<Mutex<HashMap<String, String>>>) -> io::Result<()>: читает команды по одной в строке и отвечает строкой: ''SET k v'' (v — остаток строки, может содержать пробелы) → ''OK''; ''GET k'' → значение или ''NIL''; ''DEL k'' → ''OK'' или ''NIL'' (если ключа не было); ''INCR k'' → новое число (отсутствующий ключ — 0, значение не число — ''ERR''); всё остальное → ''ERR''. Заканчивайте, когда клиент закрыл соединение.', 'use std::collections::HashMap;
use std::io;
use std::net::TcpStream;
use std::sync::{Arc, Mutex};

fn handle_kv(stream: TcpStream, store: Arc<Mutex<HashMap<String, String>>>) -> io::Result<()> {
    todo!()
}
', 'Один Mutex на всю обработку команды — просто и корректно; клиент закрывает соединение, и lines() заканчивается.', '{"driver": "use std::io::{BufRead, BufReader, Write};\nuse std::net::{TcpListener, TcpStream};\nuse std::thread;\n\nfn session(addr: std::net::SocketAddr, cmds: &[&str]) -> Vec<String> {\n    let mut c = TcpStream::connect(addr).unwrap();\n    let mut r = BufReader::new(c.try_clone().unwrap());\n    let mut out = Vec::new();\n    for cmd in cmds {\n        writeln!(c, \"{}\", cmd).unwrap();\n        let mut line = String::new();\n        r.read_line(&mut line).unwrap();\n        out.push(line.trim_end().to_string());\n    }\n    out\n}\n\nfn main() {\n    let listener = TcpListener::bind(\"127.0.0.1:0\").unwrap();\n    let addr = listener.local_addr().unwrap();\n    let store = Arc::new(Mutex::new(HashMap::new()));\n    let st = Arc::clone(&store);\n    let server = thread::spawn(move || {\n        for _ in 0..2 {\n            let (s, _) = listener.accept().unwrap();\n            handle_kv(s, Arc::clone(&st)).unwrap();\n        }\n    });\n    println!(\"{:?}\", session(addr, &[\"SET greeting hello big world\", \"GET greeting\", \"GET x\", \"INCR n\", \"INCR n\", \"SET s abc\", \"INCR s\", \"DEL n\", \"DEL n\", \"FOO\", \"SET onlykey\"]));\n    println!(\"{:?}\", session(addr, &[\"GET greeting\", \"GET n\"]));\n    server.join().unwrap();\n    println!(\"{}\", store.lock().unwrap().len());\n}\n", "expected": ["[\"OK\", \"hello big world\", \"NIL\", \"1\", \"2\", \"OK\", \"ERR\", \"OK\", \"NIL\", \"ERR\", \"ERR\"]", "[\"hello big world\", \"NIL\"]", "2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 40, 'r40-udp-reverse', 9, 'rust', 'UDP: ответ задом наперёд', 'Напишите udp_reverse_once(sock: &UdpSocket) -> io::Result<usize>: принять одну дейтаграмму (до 1024 байт), отправить обратно отправителю те же байты в обратном порядке и вернуть длину. Если за 500 мс ничего не пришло — вернуть ошибку вида TimedOut или WouldBlock (установите таймаут чтения на сокете).', 'use std::io;
use std::net::UdpSocket;

fn udp_reverse_once(sock: &UdpSocket) -> io::Result<usize> {
    todo!()
}
', 'recv_from возвращает размер и адрес отправителя; send_to ему же.', '{"driver": "use std::net::UdpSocket;\nuse std::thread;\nuse std::time::Duration;\n\nfn main() {\n    let server = UdpSocket::bind(\"127.0.0.1:0\").unwrap();\n    let addr = server.local_addr().unwrap();\n    let h = thread::spawn(move || {\n        let a = udp_reverse_once(&server).map_err(|e| e.kind());\n        let b = udp_reverse_once(&server).map_err(|e| e.kind());\n        let kind_ok = matches!(b, Err(std::io::ErrorKind::TimedOut) | Err(std::io::ErrorKind::WouldBlock));\n        (a, kind_ok)\n    });\n    let c = UdpSocket::bind(\"127.0.0.1:0\").unwrap();\n    c.set_read_timeout(Some(Duration::from_secs(2))).unwrap();\n    c.send_to(b\"abc123\", addr).unwrap();\n    let mut buf = [0u8; 64];\n    let (n, _) = c.recv_from(&mut buf).unwrap();\n    println!(\"{}\", String::from_utf8_lossy(&buf[..n]));\n    println!(\"{:?}\", h.join().unwrap());\n}\n", "expected": ["321cba", "(Ok(6), true)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 41, 'r41-parse-request', 0, 'rust', 'Разбор HTTP-запроса целиком', 'Напишите parse_request(raw: &str) -> Result<Request, String> (структура Request дана): стартовая строка (3 части, иначе Err("bad request line")), заголовки (ключ → значение; имена в нижнем регистре, значения без пробелов по краям; строка без '':'' — Err("bad header")), параметры из query после ''?'' (без декодирования: пары ''a=b'', без ''='' — значение пустое), тело — всё после пустой строки; Content-Length должен быть числом (иначе Err("bad content-length")) и не больше длины тела в байтах (иначе Err("incomplete body")); тело обрезается до этой длины.', 'use std::collections::BTreeMap;

#[derive(Debug, PartialEq)]
struct Request {
    method: String,
    path: String,
    query: BTreeMap<String, String>,
    headers: BTreeMap<String, String>,
    body: String,
}

fn parse_request(raw: &str) -> Result<Request, String> {
    todo!()
}
', 'Начните с split_once("\r\n\r\n"); проверки делайте в порядке: стартовая строка, заголовки, длина тела.', '{"driver": "fn main() {\n    let r = parse_request(\"POST /items?id=7&flag&x= HTTP/1.1\\r\\nHost: Example\\r\\nContent-Length: 5\\r\\n\\r\\nhello EXTRA\").unwrap();\n    println!(\"{} {} {:?} {:?} {:?}\", r.method, r.path, r.query, r.headers, r.body);\n    println!(\"{:?}\", parse_request(\"GET / HTTP/1.1\\r\\n\\r\\n\").map(|r| (r.path, r.body)));\n    for raw in [\"GET /\\r\\n\\r\\n\", \"GET / HTTP/1.1\\r\\nbroken\\r\\n\\r\\n\", \"POST / HTTP/1.1\\r\\nContent-Length: x\\r\\n\\r\\n\", \"POST / HTTP/1.1\\r\\nContent-Length: 9\\r\\n\\r\\nshort\", \"\"] {\n        println!(\"{:?}\", parse_request(raw).err());\n    }\n}\n", "expected": ["POST /items {\"flag\": \"\", \"id\": \"7\", \"x\": \"\"} {\"content-length\": \"5\", \"host\": \"Example\"} \"hello\"", "Ok((\"/\", \"\"))", "Some(\"bad request line\")", "Some(\"bad header\")", "Some(\"bad content-length\")", "Some(\"incomplete body\")", "Some(\"bad request line\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 41, 'r41-percent', 1, 'rust', 'Процентное кодирование', 'Напишите percent_encode(s: &str) -> String: байты A–Z a–z 0–9 - _ . ~ остаются, остальные байты UTF-8 заменяются на %XX (заглавные цифры); и percent_decode(s: &str) -> String: ''+'' → пробел, %XX → байт; некорректная последовательность (нет двух шестнадцатеричных цифр) остаётся как есть; итог собирается из байтов с заменой недопустимых UTF-8 последовательностей (from_utf8_lossy).', 'fn percent_encode(s: &str) -> String {
    todo!()
}

fn percent_decode(s: &str) -> String {
    todo!()
}
', 'Кодируйте по байтам (s.as_bytes()), формат {:02X}; при декодировании накапливайте Vec<u8> и только в конце превращайте в строку.', '{"driver": "fn main() {\n    for s in [\"hello world\", \"a/b?c=d&e\", \"Москва\", \"safe-_.~\", \"100%\", \"\"] {\n        let e = percent_encode(s);\n        println!(\"{:?} -> {} -> {}\", s, e, percent_decode(&e) == s);\n    }\n    println!(\"{:?} {:?} {:?}\", percent_decode(\"a+b%20c\"), percent_decode(\"%zz%4\"), percent_decode(\"%D0%9F\"));\n}\n", "expected": ["\"hello world\" -> hello%20world -> true", "\"a/b?c=d&e\" -> a%2Fb%3Fc%3Dd%26e -> true", "\"Москва\" -> %D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0 -> true", "\"safe-_.~\" -> safe-_.~ -> true", "\"100%\" -> 100%25 -> true", "\"\" ->  -> true", "\"a b c\" \"%zz%4\" \"П\""]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 41, 'r41-build-response', 2, 'rust', 'Сборка ответа', 'Напишите build_response(status: u16, headers: &[(&str, &str)], body: &[u8]) -> Vec<u8>: стартовая строка ''HTTP/1.1 КОД ПОЯСНЕНИЕ'' (пояснения: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 404 Not Found, 405 Method Not Allowed, 413 Payload Too Large, 500 Internal Server Error; для прочих кодов — ''Unknown''), переданные заголовки в порядке, затем автоматически ''Content-Length: N'' (N — байты тела) и ''Connection: close'', пустая строка и тело. Концы строк — \r\n.', 'fn build_response(status: u16, headers: &[(&str, &str)], body: &[u8]) -> Vec<u8> {
    todo!()
}
', 'body.len() — байты; собирайте заголовок строкой, потом превращайте в байты и дописывайте тело.', '{"driver": "fn show(b: &[u8]) -> String {\n    String::from_utf8_lossy(b).replace(\"\\r\\n\", \"|\")\n}\n\nfn main() {\n    println!(\"{}\", show(&build_response(200, &[(\"Content-Type\", \"text/plain\")], \"привет\".as_bytes())));\n    println!(\"{}\", show(&build_response(404, &[], b\"\")));\n    println!(\"{}\", show(&build_response(418, &[(\"X-A\", \"1\"), (\"X-B\", \"2\")], b\"tea\")));\n    println!(\"{}\", build_response(204, &[], b\"\").len());\n}\n", "expected": ["HTTP/1.1 200 OK|Content-Type: text/plain|Content-Length: 12|Connection: close||привет", "HTTP/1.1 404 Not Found|Content-Length: 0|Connection: close||", "HTTP/1.1 418 Unknown|X-A: 1|X-B: 2|Content-Length: 3|Connection: close||tea", "65"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 41, 'r41-json-encode', 3, 'rust', 'Кодирование JSON', 'Для enum Json { Null, Bool(bool), Num(f64), Str(String), Arr(Vec<Json>), Obj(Vec<(String, Json)>) } напишите to_json(v: &Json) -> String (компактно, без пробелов, порядок ключей как в Vec). Числа: целые значения без дробной части (3.0 → 3), иначе стандартный вывод {}; строки экранируются: \" \\ \n \r \t, прочие управляющие символы (< 0x20) — \u00XX строчными шестнадцатеричными цифрами.', 'enum Json {
    Null,
    Bool(bool),
    Num(f64),
    Str(String),
    Arr(Vec<Json>),
    Obj(Vec<(String, Json)>),
}

fn to_json(v: &Json) -> String {
    todo!()
}
', 'Рекурсия по вариантам; целое число — через as i64, чтобы не печатать «31.0».', '{"driver": "fn main() {\n    let v = Json::Obj(vec![\n        (\"name\".to_string(), Json::Str(\"Ann \\\"A\\\"\\nLee\\t\\u{1}\".to_string())),\n        (\"age\".to_string(), Json::Num(31.0)),\n        (\"score\".to_string(), Json::Num(4.5)),\n        (\"tags\".to_string(), Json::Arr(vec![Json::Str(\"a\\\\b\".to_string()), Json::Null, Json::Bool(true)])),\n        (\"nested\".to_string(), Json::Obj(vec![(\"empty\".to_string(), Json::Arr(vec![]))])),\n        (\"neg\".to_string(), Json::Num(-0.25)),\n    ]);\n    println!(\"{}\", to_json(&v));\n    println!(\"{} {}\", to_json(&Json::Null), to_json(&Json::Obj(vec![])));\n}\n", "expected": ["{\"name\":\"Ann \\\"A\\\"\\nLee\\t\\u0001\",\"age\":31,\"score\":4.5,\"tags\":[\"a\\\\b\",null,true],\"nested\":{\"empty\":[]},\"neg\":-0.25}", "null {}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 41, 'r41-json-parse', 4, 'rust', 'Разбор JSON', 'Напишите parse_json(s: &str) -> Result<Json, String> (enum Json дан): null, true/false, числа (как у f64::from_str; без ведущих плюсов), строки с экранированием \" \\ \/ \n \r \t \uXXXX (только базовая плоскость), массивы и объекты; пробелы между элементами игнорируются. Любая ошибка синтаксиса или лишние символы после значения — Err("parse error"). Глубина вложенности в тестах небольшая.', '#[derive(Debug, PartialEq)]
enum Json {
    Null,
    Bool(bool),
    Num(f64),
    Str(String),
    Arr(Vec<Json>),
    Obj(Vec<(String, Json)>),
}

fn parse_json(s: &str) -> Result<Json, String> {
    todo!()
}
', 'Рекурсивный спуск: структура с позицией i; value() смотрит на первый байт и выбирает ветку; после значения останутся только пробелы.', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_json(r#\"{\"a\": 1, \"b\": [true, null, \"x\\ny\"], \"c\": {\"d\": -2.5e1}}\"#));\n    println!(\"{:?} {:?}\", parse_json(\"  [ ]  \"), parse_json(\"{}\"));\n    println!(\"{:?}\", parse_json(r#\"\"Aé \\\"q\\\" \\/\"\"#));\n    for bad in [\"\", \"[1,\", \"{\\\"a\\\" 1}\", \"tru\", \"[1] x\", \"\\\"abc\", \"+1\", \"{''a'':1}\", \"[1 2]\"] {\n        println!(\"{:?} {:?}\", bad, parse_json(bad));\n    }\n}\n", "expected": ["Ok(Obj([(\"a\", Num(1.0)), (\"b\", Arr([Bool(true), Null, Str(\"x\\ny\")])), (\"c\", Obj([(\"d\", Num(-25.0))]))]))", "Ok(Arr([])) Ok(Obj([]))", "Ok(Str(\"Aé \\\"q\\\" /\"))", "\"\" Err(\"parse error\")", "\"[1,\" Err(\"parse error\")", "\"{\\\"a\\\" 1}\" Err(\"parse error\")", "\"tru\" Err(\"parse error\")", "\"[1] x\" Err(\"parse error\")", "\"\\\"abc\" Err(\"parse error\")", "\"+1\" Err(\"parse error\")", "\"{''a'':1}\" Err(\"parse error\")", "\"[1 2]\" Err(\"parse error\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 41, 'r41-safe-path', 5, 'rust', 'Безопасный путь и тип содержимого', 'Напишите safe_join(root: &str, url_path: &str) -> Option<String>: путь из запроса (без query) присоединяется к корню; допустимы только обычные компоненты, пустые и ''.'' пропускаются, любой ''..'' или обратная косая черта в компоненте — None; процентное кодирование НЕ декодируется (но компонент ''%2e%2e'' — тоже None). Результат — root + ''/'' + компоненты через ''/''. И mime(path: &str) -> &''static str: html → text/html; css → text/css; js → text/javascript; json → application/json; png → image/png; txt → text/plain; прочее — application/octet-stream (регистр расширения не важен).', 'fn safe_join(root: &str, url_path: &str) -> Option<String> {
    todo!()
}

fn mime(path: &str) -> &''static str {
    todo!()
}
', 'Проверяйте каждый компонент отдельно; «..» запрещён всегда, даже если в итоге не выходит за корень.', '{"driver": "fn main() {\n    for p in [\"/index.html\", \"/a/./b//c.css\", \"/\", \"/../etc/passwd\", \"/a/../../x\", \"/a\\\\..\\\\b\", \"/%2E%2e/x\", \"/ok/..hidden\"] {\n        println!(\"{:?} -> {:?}\", p, safe_join(\"/srv/www/\", p));\n    }\n    for f in [\"a.HTML\", \"x/y.js\", \"data.json\", \"logo.PNG\", \"README\", \"archive.tar.gz\", \".txt\", \"a.b/c\"] {\n        println!(\"{} {}\", f, mime(f));\n    }\n}\n", "expected": ["\"/index.html\" -> Some(\"/srv/www/index.html\")", "\"/a/./b//c.css\" -> Some(\"/srv/www/a/b/c.css\")", "\"/\" -> Some(\"/srv/www\")", "\"/../etc/passwd\" -> None", "\"/a/../../x\" -> None", "\"/a\\\\..\\\\b\" -> None", "\"/%2E%2e/x\" -> None", "\"/ok/..hidden\" -> Some(\"/srv/www/ok/..hidden\")", "a.HTML text/html", "x/y.js text/javascript", "data.json application/json", "logo.PNG image/png", "README application/octet-stream", "archive.tar.gz application/octet-stream", ".txt text/plain", "a.b/c application/octet-stream"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 41, 'r41-range', 6, 'rust', 'Заголовок Range', 'Напишите parse_range(header: &str, size: u64) -> Option<(u64, u64)>: значение ''bytes=START-END'' для файла размером size → включительные границы (первый, последний). ''bytes=500-'' — до конца файла; ''bytes=-100'' — последние 100 байт (если файл короче — весь файл); END больше размера обрезается до size − 1; None — если формат неверный, START ≥ size, START > END, size = 0 или диапазонов несколько (запятая).', 'fn parse_range(header: &str, size: u64) -> Option<(u64, u64)> {
    todo!()
}
', 'Три формы: «a-b», «a-» и «-n»; последнюю считайте через saturating_sub.', '{"driver": "fn main() {\n    for h in [\"bytes=0-99\", \"bytes=500-\", \"bytes=-100\", \"bytes=-5000\", \"bytes=900-2000\", \"bytes=1000-1005\", \"bytes=50-10\", \"bytes=0-1,5-6\", \"items=0-1\", \"bytes=\", \"bytes=a-b\", \"bytes=-0\", \"bytes=-\"] {\n        println!(\"{} {:?}\", h, parse_range(h, 1000));\n    }\n    println!(\"{:?}\", parse_range(\"bytes=0-0\", 0));\n}\n", "expected": ["bytes=0-99 Some((0, 99))", "bytes=500- Some((500, 999))", "bytes=-100 Some((900, 999))", "bytes=-5000 Some((0, 999))", "bytes=900-2000 Some((900, 999))", "bytes=1000-1005 None", "bytes=50-10 None", "bytes=0-1,5-6 None", "items=0-1 None", "bytes= None", "bytes=a-b None", "bytes=-0 None", "bytes=- None", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 41, 'r41-cookies', 7, 'rust', 'Cookie', 'Напишите parse_cookies(header: &str) -> BTreeMap<String, String> (формат ''a=1; b=two; flag''; пробелы вокруг имён и значений обрезаются; пара без ''='' — пустое значение; пустые части пропускаются; при повторе побеждает последнее) и set_cookie(name: &str, value: &str, max_age: Option<u32>, http_only: bool) -> String: ''name=value'' + ''; Max-Age=N'' (если задан) + ''; HttpOnly'' (если нужно) + всегда ''; Path=/''. Порядок частей: Max-Age, Path, HttpOnly.', 'use std::collections::BTreeMap;

fn parse_cookies(header: &str) -> BTreeMap<String, String> {
    todo!()
}

fn set_cookie(name: &str, value: &str, max_age: Option<u32>, http_only: bool) -> String {
    todo!()
}
', 'split('';''), trim, split_once(''='') — значение может содержать ''='' (берётся всё после первого).', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_cookies(\"a=1; b = two ;flag; ; a=3; c=x=y\"));\n    println!(\"{:?} {:?}\", parse_cookies(\"\"), parse_cookies(\" ; \"));\n    println!(\"{}\", set_cookie(\"sid\", \"abc123\", Some(3600), true));\n    println!(\"{}\", set_cookie(\"theme\", \"dark\", None, false));\n}\n", "expected": ["{\"a\": \"3\", \"b\": \"two\", \"c\": \"x=y\", \"flag\": \"\"}", "{} {}", "sid=abc123; Max-Age=3600; Path=/; HttpOnly", "theme=dark; Path=/"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 41, 'r41-serve-one', 8, 'rust', 'Мини-сервер: один запрос', 'Напишите serve_one(stream: TcpStream) -> io::Result<()>: прочитайте один HTTP/1.1-запрос (заголовки до пустой строки, тело по Content-Length), отправьте ответ и закройте соединение (Connection: close; Content-Length в байтах). Маршруты: GET /hello?name=X → 200 text/plain "Hello, X!" (X без декодирования; без параметра — "Hello, world!"); POST /echo → 200 с телом запроса; любой другой путь → 404 "not found"; для /hello и /echo с неверным методом → 405 "method not allowed"; неразборчивая стартовая строка → 400 "bad request". Тело ответа — текст.', 'use std::io;
use std::net::TcpStream;

fn serve_one(stream: TcpStream) -> io::Result<()> {
    todo!()
}
', 'Читайте через BufReader: read_line для стартовой строки и заголовков, read_exact для тела; ответ собирайте одной строкой и пишите write!.', '{"driver": "use std::io::{Read, Write};\nuse std::net::{TcpListener, TcpStream};\nuse std::thread;\n\nfn call(addr: std::net::SocketAddr, raw: &str) -> (String, String) {\n    let mut c = TcpStream::connect(addr).unwrap();\n    for chunk in raw.as_bytes().chunks(7) {\n        c.write_all(chunk).unwrap();\n        c.flush().unwrap();\n    }\n    let mut out = String::new();\n    c.read_to_string(&mut out).unwrap();\n    let (head, body) = out.split_once(\"\\r\\n\\r\\n\").unwrap();\n    let status = head.lines().next().unwrap().to_string();\n    let clen: usize = head.lines().find_map(|l| l.strip_prefix(\"Content-Length: \")).unwrap().parse().unwrap();\n    assert_eq!(clen, body.len());\n    (status, body.to_string())\n}\n\nfn main() {\n    let l = TcpListener::bind(\"127.0.0.1:0\").unwrap();\n    let addr = l.local_addr().unwrap();\n    let reqs = [\n        \"GET /hello?name=Ann HTTP/1.1\\r\\nHost: x\\r\\n\\r\\n\",\n        \"GET /hello HTTP/1.1\\r\\nHost: x\\r\\n\\r\\n\",\n        \"POST /echo HTTP/1.1\\r\\nHost: x\\r\\nContent-Length: 21\\r\\n\\r\\nпривет, мир\\n\",\n        \"DELETE /echo HTTP/1.1\\r\\n\\r\\n\",\n        \"GET /nope HTTP/1.1\\r\\n\\r\\n\",\n        \"BROKEN\\r\\n\\r\\n\",\n    ];\n    let n = reqs.len();\n    let srv = thread::spawn(move || {\n        for s in l.incoming().take(n) {\n            serve_one(s.unwrap()).unwrap();\n        }\n    });\n    for r in reqs {\n        println!(\"{:?}\", call(addr, r));\n    }\n    srv.join().unwrap();\n}\n", "expected": ["(\"HTTP/1.1 200 OK\", \"Hello, Ann!\")", "(\"HTTP/1.1 200 OK\", \"Hello, world!\")", "(\"HTTP/1.1 200 OK\", \"привет, мир\\n\")", "(\"HTTP/1.1 405 Method Not Allowed\", \"method not allowed\")", "(\"HTTP/1.1 404 Not Found\", \"not found\")", "(\"HTTP/1.1 400 Bad Request\", \"bad request\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 42, 'r42-match-route', 0, 'rust', 'Сопоставление маршрута', 'Напишите match_route(pattern: &str, path: &str) -> Option<BTreeMap<String, String>>: сегменты через ''/'', ведущие и хвостовые ''/'' игнорируются. Сегмент шаблона '':имя'' захватывает один сегмент пути; последний сегмент ''*имя'' захватывает весь остаток пути (сегменты через ''/'', может быть пустым); остальные сегменты должны совпасть дословно. Число сегментов без ''*'' должно совпасть.', 'use std::collections::BTreeMap;

fn match_route(pattern: &str, path: &str) -> Option<BTreeMap<String, String>> {
    todo!()
}
', 'Разберите оба пути на сегменты и идите по шаблону: '':'' — захват, ''*'' — хвост (return), иначе — равенство.', '{"driver": "fn main() {\n    println!(\"{:?}\", match_route(\"/users/:id/posts/:post\", \"/users/42/posts/7/\"));\n    println!(\"{:?} {:?}\", match_route(\"/users/:id\", \"/users\"), match_route(\"/users/:id\", \"/accounts/5\"));\n    println!(\"{:?} {:?}\", match_route(\"/\", \"/\"), match_route(\"/\", \"/x\"));\n    println!(\"{:?}\", match_route(\"/static/*path\", \"/static/css/site/main.css\"));\n    println!(\"{:?} {:?}\", match_route(\"/static/*path\", \"/static\"), match_route(\"/static/*path\", \"/other/a\"));\n    println!(\"{:?}\", match_route(\"/a/:x/*rest\", \"/a/1/b/c\"));\n}\n", "expected": ["Some({\"id\": \"42\", \"post\": \"7\"})", "None None", "Some({}) None", "Some({\"path\": \"css/site/main.css\"})", "Some({\"path\": \"\"}) None", "Some({\"rest\": \"b/c\", \"x\": \"1\"})"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 42, 'r42-router', 1, 'rust', 'Маршрутизатор с 404 и 405', 'Дополните Router: new(), add(&mut self, method, pattern, handler) и handle(&self, method, path) -> (u16, String): первая запись, у которой совпали метод и шаблон, вызывает обработчик с параметрами и возвращает (200, результат). Если ни одна не подошла, но шаблон совпал для другого метода — (405, "method not allowed"); если шаблон не совпал нигде — (404, "not found"). Функция match_route уже написана.', 'use std::collections::BTreeMap;

type Params = BTreeMap<String, String>;
type Handler = Box<dyn Fn(&Params) -> String>;

fn match_route(pattern: &str, path: &str) -> Option<Params> {
    let segs = |s: &str| -> Vec<String> { s.split(''/'').filter(|x| !x.is_empty()).map(|x| x.to_string()).collect() };
    let (p, q) = (segs(pattern), segs(path));
    if p.len() != q.len() {
        return None;
    }
    let mut params = Params::new();
    for (a, b) in p.iter().zip(q.iter()) {
        if let Some(name) = a.strip_prefix('':'') {
            params.insert(name.to_string(), b.clone());
        } else if a != b {
            return None;
        }
    }
    Some(params)
}

struct Router {
    routes: Vec<(String, String, Handler)>,
}

impl Router {
    fn new() -> Router {
        todo!()
    }
    fn add(&mut self, method: &str, pattern: &str, h: Handler) {
        todo!()
    }
    fn handle(&self, method: &str, path: &str) -> (u16, String) {
        todo!()
    }
}
', 'Один проход: запоминайте, совпал ли шаблон при другом методе; результат — после цикла.', '{"driver": "fn main() {\n    let mut r = Router::new();\n    r.add(\"GET\", \"/users/new\", Box::new(|_| \"new form\".to_string()));\n    r.add(\"GET\", \"/users/:id\", Box::new(|p| format!(\"user {}\", p[\"id\"])));\n    r.add(\"DELETE\", \"/users/:id\", Box::new(|p| format!(\"deleted {}\", p[\"id\"])));\n    r.add(\"GET\", \"/\", Box::new(|_| \"home\".to_string()));\n    for (m, p) in [(\"GET\", \"/users/new\"), (\"GET\", \"/users/42\"), (\"DELETE\", \"/users/7\"), (\"POST\", \"/users/7\"), (\"GET\", \"/nope\"), (\"GET\", \"/\"), (\"PUT\", \"/\")] {\n        println!(\"{} {} -> {:?}\", m, p, r.handle(m, p));\n    }\n}\n", "expected": ["GET /users/new -> (200, \"new form\")", "GET /users/42 -> (200, \"user 42\")", "DELETE /users/7 -> (200, \"deleted 7\")", "POST /users/7 -> (405, \"method not allowed\")", "GET /nope -> (404, \"not found\")", "GET / -> (200, \"home\")", "PUT / -> (405, \"method not allowed\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 42, 'r42-middleware', 2, 'rust', 'Цепочка слоёв', 'Типы: Handler = Rc<dyn Fn(&Request) -> Response>, Layer = Rc<dyn Fn(&Request, &Handler) -> Response> (слой получает запрос и «следующий» обработчик). Напишите compose(layers: Vec<Layer>, endpoint: Handler) -> Handler: первый слой в списке — самый внешний (вызывается первым), последний вызывает endpoint.', 'use std::rc::Rc;

struct Request {
    path: String,
    auth: Option<String>,
}

#[derive(Debug, PartialEq)]
struct Response {
    status: u16,
    body: String,
}

type Handler = Rc<dyn Fn(&Request) -> Response>;
type Layer = Rc<dyn Fn(&Request, &Handler) -> Response>;

fn compose(layers: Vec<Layer>, endpoint: Handler) -> Handler {
    todo!()
}
', 'Оборачивайте с конца: последний слой — вокруг endpoint, предпоследний — вокруг получившегося и так далее; layer и next перемещаются в замыкание.', '{"driver": "use std::cell::RefCell;\n\nfn main() {\n    let log: Rc<RefCell<Vec<String>>> = Rc::new(RefCell::new(Vec::new()));\n    let l1 = Rc::clone(&log);\n    let logging: Layer = Rc::new(move |req, next| {\n        l1.borrow_mut().push(format!(\"in {}\", req.path));\n        let r = next(req);\n        l1.borrow_mut().push(format!(\"out {}\", r.status));\n        r\n    });\n    let auth: Layer = Rc::new(|req, next| {\n        if req.auth.as_deref() == Some(\"secret\") {\n            next(req)\n        } else {\n            Response { status: 401, body: \"unauthorized\".to_string() }\n        }\n    });\n    let l2 = Rc::clone(&log);\n    let tag: Layer = Rc::new(move |req, next| {\n        l2.borrow_mut().push(\"tag\".to_string());\n        let mut r = next(req);\n        r.body.push(''!'');\n        r\n    });\n    let endpoint: Handler = Rc::new(|req| Response { status: 200, body: format!(\"hello {}\", req.path) });\n    let app = compose(vec![logging, auth, tag], endpoint);\n    println!(\"{:?}\", app(&Request { path: \"/a\".into(), auth: Some(\"secret\".into()) }));\n    println!(\"{:?}\", app(&Request { path: \"/b\".into(), auth: None }));\n    println!(\"{:?}\", log.borrow());\n    let bare = compose(vec![], Rc::new(|_| Response { status: 204, body: String::new() }));\n    println!(\"{:?}\", bare(&Request { path: \"/\".into(), auth: None }));\n}\n", "expected": ["Response { status: 200, body: \"hello /a!\" }", "Response { status: 401, body: \"unauthorized\" }", "[\"in /a\", \"tag\", \"out 200\", \"in /b\", \"out 401\"]", "Response { status: 204, body: \"\" }"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 42, 'r42-todo-api', 3, 'rust', 'REST-интерфейс списка дел', 'Хранилище Store уже написано. Напишите handle(store: &Mutex<Store>, method: &str, path: &str, body: &str) -> (u16, String): GET /todos → (200, JSON-массив по возрастанию id: [{"id":1,"title":"a","done":false}], пустой — []); POST /todos (тело — название без кавычек, обрезается; пустое → (400, "empty title")) → (201, {"id":N}); GET /todos/ID → (200, объект) или (404, "not found"); нечисловой ID → (400, "bad id"); PUT /todos/ID/done → (200, "done") или 404; DELETE /todos/ID → (204, "") или 404. Известный путь с другим методом — (405, "method not allowed"); неизвестный путь — (404, "not found").', 'use std::collections::BTreeMap;
use std::sync::Mutex;

struct Todo {
    title: String,
    done: bool,
}

struct Store {
    next: u32,
    items: BTreeMap<u32, Todo>,
}

impl Store {
    fn new() -> Store {
        Store { next: 1, items: BTreeMap::new() }
    }
    fn create(&mut self, title: &str) -> u32 {
        let id = self.next;
        self.next += 1;
        self.items.insert(id, Todo { title: title.to_string(), done: false });
        id
    }
}

fn handle(store: &Mutex<Store>, method: &str, path: &str, body: &str) -> (u16, String) {
    todo!()
}
', 'Разбейте путь на сегменты и сопоставляйте срез: ["todos"], ["todos", id], ["todos", id, "done"]; блокировку берите один раз в начале.', '{"driver": "fn main() {\n    let s = Mutex::new(Store::new());\n    for (m, p, b) in [\n        (\"GET\", \"/todos\", \"\"),\n        (\"POST\", \"/todos\", \"  write chapter \"),\n        (\"POST\", \"/todos\", \"test server\"),\n        (\"POST\", \"/todos\", \"   \"),\n        (\"GET\", \"/todos/1\", \"\"),\n        (\"PUT\", \"/todos/1/done\", \"\"),\n        (\"GET\", \"/todos\", \"\"),\n        (\"GET\", \"/todos/9\", \"\"),\n        (\"GET\", \"/todos/abc\", \"\"),\n        (\"DELETE\", \"/todos/2\", \"\"),\n        (\"DELETE\", \"/todos/2\", \"\"),\n        (\"PATCH\", \"/todos\", \"\"),\n        (\"GET\", \"/todos/1/done\", \"\"),\n        (\"GET\", \"/nope\", \"\"),\n    ] {\n        println!(\"{} {} -> {:?}\", m, p, handle(&s, m, p, b));\n    }\n}\n", "expected": ["GET /todos -> (200, \"[]\")", "POST /todos -> (201, \"{\\\"id\\\":1}\")", "POST /todos -> (201, \"{\\\"id\\\":2}\")", "POST /todos -> (400, \"empty title\")", "GET /todos/1 -> (200, \"{\\\"id\\\":1,\\\"title\\\":\\\"write chapter\\\",\\\"done\\\":false}\")", "PUT /todos/1/done -> (200, \"done\")", "GET /todos -> (200, \"[{\\\"id\\\":1,\\\"title\\\":\\\"write chapter\\\",\\\"done\\\":true},{\\\"id\\\":2,\\\"title\\\":\\\"test server\\\",\\\"done\\\":false}]\")", "GET /todos/9 -> (404, \"not found\")", "GET /todos/abc -> (400, \"bad id\")", "DELETE /todos/2 -> (204, \"\")", "DELETE /todos/2 -> (404, \"not found\")", "PATCH /todos -> (405, \"method not allowed\")", "GET /todos/1/done -> (405, \"method not allowed\")", "GET /nope -> (404, \"not found\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 42, 'r42-thread-pool', 4, 'rust', 'Пул потоков', 'Реализуйте ThreadPool: new(n) запускает n рабочих потоков, execute(&self, f) отправляет задание (FnOnce + Send + ''static) в общую очередь, а Drop закрывает очередь и дожидается всех рабочих (принятые задания выполняются до конца).', 'use std::sync::{mpsc, Arc, Mutex};
use std::thread;

type Job = Box<dyn FnOnce() + Send + ''static>;

struct ThreadPool {
    workers: Vec<thread::JoinHandle<()>>,
    tx: Option<mpsc::Sender<Job>>,
}

impl ThreadPool {
    fn new(n: usize) -> ThreadPool {
        todo!()
    }
    fn execute<F: FnOnce() + Send + ''static>(&self, f: F) {
        todo!()
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        todo!()
    }
}
', 'Приёмник один — оберните его в Arc<Mutex<_>>; в Drop сначала закройте канал (take + drop), потом join.', '{"driver": "use std::sync::atomic::{AtomicUsize, Ordering};\n\nfn main() {\n    let done = Arc::new(AtomicUsize::new(0));\n    let running = Arc::new(AtomicUsize::new(0));\n    let peak = Arc::new(AtomicUsize::new(0));\n    {\n        let pool = ThreadPool::new(4);\n        for _ in 0..40 {\n            let (d, r, p) = (Arc::clone(&done), Arc::clone(&running), Arc::clone(&peak));\n            pool.execute(move || {\n                let now = r.fetch_add(1, Ordering::SeqCst) + 1;\n                p.fetch_max(now, Ordering::SeqCst);\n                std::thread::sleep(std::time::Duration::from_millis(5));\n                r.fetch_sub(1, Ordering::SeqCst);\n                d.fetch_add(1, Ordering::SeqCst);\n            });\n        }\n    }\n    println!(\"{} {}\", done.load(Ordering::SeqCst), peak.load(Ordering::SeqCst) <= 4);\n    let empty = ThreadPool::new(2);\n    drop(empty);\n    println!(\"ok\");\n}\n", "expected": ["40 true", "ok"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 42, 'r42-serve-until', 5, 'rust', 'Сервер с мягкой остановкой', 'Напишите serve_until(listener: TcpListener, stop: Arc<AtomicBool>, handler: fn(TcpStream)) -> usize: переведите сокет в неблокирующий режим и, пока флаг stop не поднят, принимайте соединения (каждое передаётся в handler в этом же потоке); если принимать нечего — спите 2 мс. Верните число обработанных соединений.', 'use std::net::{TcpListener, TcpStream};
use std::sync::atomic::AtomicBool;
use std::sync::Arc;

fn serve_until(listener: TcpListener, stop: Arc<AtomicBool>, handler: fn(TcpStream)) -> usize {
    todo!()
}
', 'accept() неблокирующего сокета возвращает ошибку WouldBlock, если соединений нет; принятому потоку верните блокирующий режим.', '{"driver": "use std::io::{Read, Write};\nuse std::net::{TcpListener, TcpStream};\nuse std::sync::atomic::{AtomicBool, Ordering};\nuse std::sync::Arc;\nuse std::thread;\nuse std::time::Duration;\n\nfn upper(mut s: TcpStream) {\n    let mut buf = [0u8; 64];\n    let n = s.read(&mut buf).unwrap();\n    s.write_all(&buf[..n].to_ascii_uppercase()).unwrap();\n}\n\nfn main() {\n    let listener = TcpListener::bind(\"127.0.0.1:0\").unwrap();\n    let addr = listener.local_addr().unwrap();\n    let stop = Arc::new(AtomicBool::new(false));\n    let flag = Arc::clone(&stop);\n    let server = thread::spawn(move || serve_until(listener, flag, upper));\n    for word in [\"alpha\", \"beta\", \"gamma\"] {\n        let mut c = TcpStream::connect(addr).unwrap();\n        c.write_all(word.as_bytes()).unwrap();\n        let mut reply = String::new();\n        c.read_to_string(&mut reply).unwrap();\n        println!(\"{}\", reply);\n    }\n    thread::sleep(Duration::from_millis(20));\n    stop.store(true, Ordering::SeqCst);\n    println!(\"handled {}\", server.join().unwrap());\n    let l2 = TcpListener::bind(\"127.0.0.1:0\").unwrap();\n    let stopped = Arc::new(AtomicBool::new(true));\n    println!(\"handled {}\", serve_until(l2, stopped, upper));\n}\n", "expected": ["ALPHA", "BETA", "GAMMA", "handled 3", "handled 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 42, 'r42-rate-limiter', 6, 'rust', 'Ограничитель по клиентам', 'Реализуйте RateLimiter: new(capacity: f64, rate: f64) (у каждого нового ключа ведро полное; last = момент первого обращения) и allow(&mut self, key: &str, now: f64) -> bool: ведро пополняется на (now − last) · rate, не больше capacity; запрос стоит один жетон. Клиенты не влияют друг на друга. Время приходит неубывающим для одного ключа.', 'use std::collections::HashMap;

struct RateLimiter {
    capacity: f64,
    rate: f64,
    buckets: HashMap<String, (f64, f64)>,
}

impl RateLimiter {
    fn new(capacity: f64, rate: f64) -> RateLimiter {
        todo!()
    }
    fn allow(&mut self, key: &str, now: f64) -> bool {
        todo!()
    }
}
', 'Состояние ключа — пара (жетоны, последнее время); обновляйте её и при отказе (жетоны пополнились).', '{"driver": "fn main() {\n    let mut rl = RateLimiter::new(2.0, 0.5);\n    let calls = [(\"a\", 0.0), (\"a\", 0.0), (\"a\", 0.0), (\"b\", 0.0), (\"a\", 1.0), (\"a\", 2.0), (\"a\", 2.0), (\"b\", 0.5), (\"b\", 4.0), (\"b\", 4.0), (\"b\", 4.0)];\n    let r: Vec<String> = calls.iter().map(|&(k, t)| format!(\"{}@{}={}\", k, t, rl.allow(k, t))).collect();\n    println!(\"{}\", r.join(\" \"));\n    let mut hot = RateLimiter::new(1.0, 1000.0);\n    let allowed = (0..100_000).filter(|&i| hot.allow(&format!(\"c{}\", i % 10), i as f64 / 1000.0)).count();\n    println!(\"{}\", allowed);\n}\n", "expected": ["a@0=true a@0=true a@0=false b@0=true a@1=false a@2=true a@2=false b@0.5=true b@4=true b@4=true b@4=false", "100000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 42, 'r42-histogram', 7, 'rust', 'Гистограмма задержек', 'Реализуйте Histogram::new(bounds: &[u64]) (верхние границы корзин в мс по возрастанию), observe(&mut self, ms: u64) и render(&self, name: &str) -> String в стиле Prometheus: для каждой границы строка name_bucket{le="B"} N, где N — число наблюдений ≤ B (накопительно); затем name_bucket{le="+Inf"} (все наблюдения), name_count и name_sum. Строки разделены \n, без завершающего.', 'struct Histogram {
    bounds: Vec<u64>,
    counts: Vec<u64>,
    total: u64,
    sum: u64,
}

impl Histogram {
    fn new(bounds: &[u64]) -> Histogram {
        todo!()
    }
    fn observe(&mut self, ms: u64) {
        todo!()
    }
    fn render(&self, name: &str) -> String {
        todo!()
    }
}
', 'Накопительные корзины: наблюдение увеличивает счётчик каждой границы, которая не меньше значения.', '{"driver": "fn main() {\n    let mut h = Histogram::new(&[10, 50, 100]);\n    for ms in [3, 10, 11, 49, 50, 99, 250, 1000] {\n        h.observe(ms);\n    }\n    println!(\"{}\", h.render(\"latency_ms\"));\n    println!(\"{}\", Histogram::new(&[]).render(\"x\"));\n}\n", "expected": ["latency_ms_bucket{le=\"10\"} 2", "latency_ms_bucket{le=\"50\"} 5", "latency_ms_bucket{le=\"100\"} 6", "latency_ms_bucket{le=\"+Inf\"} 8", "latency_ms_count 8", "latency_ms_sum 1472", "x_bucket{le=\"+Inf\"} 0", "x_count 0", "x_sum 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 42, 'r42-parse-args', 8, 'rust', 'Разбор командной строки', 'Напишите parse_args(args: &[&str]) -> Result<Options, String> (Options дана): ''--name=value'' и ''--name value'' → options[name] = value; ''--flag'' без значения (следующий элемент начинается с ''-'' или это конец списка) → flags содержит flag; ''-v'', ''-vv'', ''-vvv'' → verbose += число букв v; ''--'' — всё остальное позиционные аргументы; прочее — позиционные. Ошибки: ''-x'' с буквой, не v → Err("unknown option -x"); ''--=v'' → Err("empty option name").', 'use std::collections::BTreeMap;

#[derive(Debug, Default, PartialEq)]
struct Options {
    options: BTreeMap<String, String>,
    flags: Vec<String>,
    verbose: u32,
    positional: Vec<String>,
}

fn parse_args(args: &[&str]) -> Result<Options, String> {
    todo!()
}
', 'Один цикл с индексом: у «--имя» значение берётся из следующего элемента, если он не начинается с ''-''.', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_args(&[\"--port=8080\", \"--host\", \"localhost\", \"-vv\", \"--debug\", \"file.txt\", \"-v\", \"--\", \"--not-an-option\", \"-x\"]));\n    println!(\"{:?}\", parse_args(&[]));\n    println!(\"{:?}\", parse_args(&[\"--a\", \"--b\", \"val\", \"pos\"]));\n    println!(\"{:?} {:?} {:?}\", parse_args(&[\"-x\"]), parse_args(&[\"--=v\"]), parse_args(&[\"--\"]));\n    println!(\"{:?}\", parse_args(&[\"-\"]));\n}\n", "expected": ["Ok(Options { options: {\"debug\": \"file.txt\", \"host\": \"localhost\", \"port\": \"8080\"}, flags: [], verbose: 3, positional: [\"--not-an-option\", \"-x\"] })", "Ok(Options { options: {}, flags: [], verbose: 0, positional: [] })", "Ok(Options { options: {\"b\": \"val\"}, flags: [\"a\"], verbose: 0, positional: [\"pos\"] })", "Err(\"unknown option -x\") Err(\"empty option name\") Ok(Options { options: {}, flags: [], verbose: 0, positional: [] })", "Ok(Options { options: {}, flags: [], verbose: 0, positional: [\"-\"] })"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 43, 'r43-encode-messages', 0, 'rust', 'Сообщения клиента Postgres', 'Напишите startup_message(params: &[(&str, &str)]) -> Vec<u8> (длина i32 включая себя; версия протокола 196608 (3.0) как i32; затем пары ''имя\0значение\0''; в конце ещё один нулевой байт), query_message(sql: &str) -> Vec<u8> (''Q'', длина i32 = 4 + байты sql + 1, текст, нулевой байт), terminate_message() -> Vec<u8> (''X'', длина 4) и password_message(pw: &str) -> Vec<u8> (''p'', длина, пароль и нулевой байт). Все числа — старшим байтом вперёд.', 'fn startup_message(params: &[(&str, &str)]) -> Vec<u8> {
    todo!()
}

fn query_message(sql: &str) -> Vec<u8> {
    todo!()
}

fn terminate_message() -> Vec<u8> {
    todo!()
}

fn password_message(pw: &str) -> Vec<u8> {
    todo!()
}
', 'Общий помощник: метка + (длина тела + 4) как u32::to_be_bytes + тело.', '{"driver": "fn main() {\n    let s = startup_message(&[(\"user\", \"app\"), (\"database\", \"shop\")]);\n    println!(\"{} {:?}\", s.len(), &s[..8]);\n    println!(\"{:?}\", String::from_utf8_lossy(&s[8..]).replace(''\\0'', \"|\"));\n    println!(\"{:?}\", startup_message(&[]));\n    println!(\"{:?}\", query_message(\"SELECT 1\"));\n    println!(\"{:?} {:?}\", terminate_message(), password_message(\"pw\"));\n    let q = query_message(\"SELECT ''привет''\");\n    println!(\"{} {}\", q.len(), u32::from_be_bytes([q[1], q[2], q[3], q[4]]));\n}\n", "expected": ["32 [0, 0, 0, 32, 0, 3, 0, 0]", "\"user|app|database|shop||\"", "[0, 0, 0, 9, 0, 3, 0, 0, 0]", "[81, 0, 0, 0, 13, 83, 69, 76, 69, 67, 84, 32, 49, 0]", "[88, 0, 0, 0, 4] [112, 0, 0, 0, 7, 112, 119, 0]", "27 26"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 43, 'r43-decode-messages', 1, 'rust', 'Сообщения сервера Postgres', 'Напишите read_message(buf: &[u8]) -> Option<(u8, Vec<u8>, usize)> (метка, содержимое, сколько байтов занято; None — если сообщение неполное), data_row(payload: &[u8]) -> Result<Vec<Option<String>>, String> (число колонок i16, для каждой длина i32 и байты; −1 — NULL; ошибка "truncated", если данных не хватает) и error_fields(payload: &[u8]) -> BTreeMap<char, String> (ErrorResponse: пары ''метка-байт, строка с нулём'', завершается нулевым байтом).', 'use std::collections::BTreeMap;

fn read_message(buf: &[u8]) -> Option<(u8, Vec<u8>, usize)> {
    todo!()
}

fn data_row(payload: &[u8]) -> Result<Vec<Option<String>>, String> {
    todo!()
}

fn error_fields(payload: &[u8]) -> BTreeMap<char, String> {
    todo!()
}
', 'Проверяйте границы всегда через get(..) — неполные данные не должны вызывать панику.', '{"driver": "fn msg(tag: u8, payload: &[u8]) -> Vec<u8> {\n    let mut m = vec![tag];\n    m.extend_from_slice(&((payload.len() + 4) as u32).to_be_bytes());\n    m.extend_from_slice(payload);\n    m\n}\n\nfn main() {\n    let mut row = vec![0, 3];\n    for c in [Some(\"42\"), None, Some(\"привет\")] {\n        match c {\n            Some(s) => {\n                row.extend_from_slice(&(s.len() as i32).to_be_bytes());\n                row.extend_from_slice(s.as_bytes());\n            }\n            None => row.extend_from_slice(&(-1i32).to_be_bytes()),\n        }\n    }\n    let mut stream = msg(b''D'', &row);\n    stream.extend(msg(b''C'', b\"SELECT 1\\0\"));\n    stream.extend(msg(b''Z'', b\"I\"));\n    let mut off = 0;\n    while let Some((tag, payload, used)) = read_message(&stream[off..]) {\n        println!(\"{} {} {}\", tag as char, payload.len(), used);\n        off += used;\n    }\n    println!(\"{}\", off == stream.len());\n    let (_, p, _) = read_message(&stream).unwrap();\n    println!(\"{:?}\", data_row(&p));\n    println!(\"{:?} {:?}\", data_row(&p[..10]), data_row(&[0, 1, 0, 0, 0, 9, 1]));\n    println!(\"{:?} {:?}\", read_message(&stream[..4]), read_message(&stream[..8]).map(|m| m.0));\n    let err = b\"SERROR\\0C42P01\\0Mrelation \\\"users\\\" does not exist\\0\\0\";\n    println!(\"{:?}\", error_fields(err));\n}\n", "expected": ["D 28 33", "C 9 14", "Z 1 6", "true", "Ok([Some(\"42\"), None, Some(\"привет\")])", "Err(\"truncated\") Err(\"truncated\")", "None None", "{''C'': \"42P01\", ''M'': \"relation \\\"users\\\" does not exist\", ''S'': \"ERROR\"}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 43, 'r43-from-column', 2, 'rust', 'Отображение колонок в типы', 'Трейт FromColumn с методом from_col(c: Option<&str>) -> Result<Self, String> дан. Реализуйте его для i32 (NULL → Err("NULL"), нечисло → Err("bad int: ТЕКСТ")), f64 (аналогично "bad float: ТЕКСТ"), bool (''t''/''f''; иное — Err("bad bool: ТЕКСТ")), String и Option<T> (для любого T: FromColumn; None → Ok(None)). Затем напишите product_from_row(row: &[Option<&str>]) -> Result<Product, String>; ошибки колонки оформляются как "column N: ошибка" (N с нуля).', 'trait FromColumn: Sized {
    fn from_col(c: Option<&str>) -> Result<Self, String>;
}

#[derive(Debug, PartialEq)]
struct Product {
    id: i32,
    title: String,
    price: f64,
    in_stock: bool,
    discount: Option<f64>,
}

// impl FromColumn for i32, f64, bool, String, Option<T> ...

fn product_from_row(row: &[Option<&str>]) -> Result<Product, String> {
    todo!()
}
', 'Вспомогательная обобщённая функция col::<T>(row, i) собирает префикс «column N: » к любой ошибке.', '{"driver": "fn main() {\n    println!(\"{:?}\", product_from_row(&[Some(\"1\"), Some(\"Laptop\"), Some(\"999.5\"), Some(\"t\"), None]));\n    println!(\"{:?}\", product_from_row(&[Some(\"2\"), Some(\"Mouse\"), Some(\"15\"), Some(\"f\"), Some(\"0.1\")]));\n    println!(\"{:?}\", product_from_row(&[Some(\"x\"), Some(\"A\"), Some(\"1\"), Some(\"t\"), None]));\n    println!(\"{:?}\", product_from_row(&[Some(\"3\"), None, Some(\"1\"), Some(\"t\"), None]));\n    println!(\"{:?}\", product_from_row(&[Some(\"3\"), Some(\"B\"), Some(\"1.x\"), Some(\"t\"), None]));\n    println!(\"{:?}\", product_from_row(&[Some(\"3\"), Some(\"B\"), Some(\"1\"), Some(\"yes\"), None]));\n    println!(\"{:?}\", product_from_row(&[Some(\"3\"), Some(\"B\"), Some(\"1\"), Some(\"t\"), Some(\"zz\")]));\n    println!(\"{:?}\", product_from_row(&[Some(\"3\")]));\n}\n", "expected": ["Ok(Product { id: 1, title: \"Laptop\", price: 999.5, in_stock: true, discount: None })", "Ok(Product { id: 2, title: \"Mouse\", price: 15.0, in_stock: false, discount: Some(0.1) })", "Err(\"column 0: bad int: x\")", "Err(\"column 1: NULL\")", "Err(\"column 2: bad float: 1.x\")", "Err(\"column 3: bad bool: yes\")", "Err(\"column 4: bad float: zz\")", "Err(\"column 1: NULL\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 43, 'r43-render-query', 3, 'rust', 'Подстановка параметров для журнала', 'Для лога запросов напишите quote_literal(s: &str) -> String (кавычки вокруг, внутренние '' удваиваются) и render_query(sql: &str, params: &[Option<&str>]) -> String: каждое $N (N — число из одной или нескольких цифр, нумерация с единицы) заменяется на NULL для None и quote_literal для Some; $N с номером вне списка и одиночный ''$'' остаются как есть. Внутри строковых литералов в sql замен не делайте (текст между одинарными кавычками копируется без изменений; '''' внутри — экранированная кавычка).', 'fn quote_literal(s: &str) -> String {
    todo!()
}

fn render_query(sql: &str, params: &[Option<&str>]) -> String {
    todo!()
}
', 'Идите по символам, помните, внутри ли вы строкового литерала; число после ''$'' читайте до конца цифр, чтобы $10 не превратился в $1 и ''0''.', '{"driver": "fn main() {\n    println!(\"{}\", quote_literal(\"O''Brien\"));\n    println!(\"{}\", render_query(\"SELECT * FROM u WHERE name = $1 AND age > $2 AND note IS NOT DISTINCT FROM $3\", &[Some(\"x'' OR ''1''=''1\"), Some(\"18\"), None]));\n    println!(\"{}\", render_query(\"SELECT $1, $10, $2, ''$1 stays'', $5, $\", &[Some(\"a\"), Some(\"b\")]));\n    let many: Vec<String> = (1..=10).map(|i| format!(\"v{}\", i)).collect();\n    let refs: Vec<Option<&str>> = many.iter().map(|s| Some(s.as_str())).collect();\n    println!(\"{}\", render_query(\"$1 $10 $2\", &refs));\n    println!(\"{}\", render_query(\"SELECT ''it''''s $1'' || $1\", &[Some(\"z\")]));\n}\n", "expected": ["''O''''Brien''", "SELECT * FROM u WHERE name = ''x'''' OR ''''1''''=''''1'' AND age > ''18'' AND note IS NOT DISTINCT FROM NULL", "SELECT ''a'', $10, ''b'', ''$1 stays'', $5, $", "''v1'' ''v10'' ''v2''", "SELECT ''it''''s $1'' || ''z''"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 43, 'r43-select-builder', 4, 'rust', 'Построитель SELECT', 'Реализуйте Select: from(table), filter(mut self, col, op, value) (добавляет «col op $N»), filter_in(mut self, col, values: &[&str]) («col IN ($N, $N+1, …)»; пустой список — условие «FALSE»), order_by(mut self, col, desc: bool), limit(mut self, n), offset(mut self, n) и build(&self) -> (String, Vec<String>): ''SELECT * FROM t'' + '' WHERE a AND b'' + '' ORDER BY col ASC|DESC'' + '' LIMIT n'' + '' OFFSET n''; параметры — в порядке нумерации.', 'struct Select {
    table: String,
    conds: Vec<String>,
    params: Vec<String>,
    order: Option<String>,
    limit: Option<u32>,
    offset: Option<u32>,
}

impl Select {
    fn from(table: &str) -> Select {
        todo!()
    }
    fn filter(mut self, col: &str, op: &str, value: &str) -> Select {
        todo!()
    }
    fn filter_in(mut self, col: &str, values: &[&str]) -> Select {
        todo!()
    }
    fn order_by(mut self, col: &str, desc: bool) -> Select {
        todo!()
    }
    fn limit(mut self, n: u32) -> Select {
        todo!()
    }
    fn offset(mut self, n: u32) -> Select {
        todo!()
    }
    fn build(&self) -> (String, Vec<String>) {
        todo!()
    }
}
', 'Номер параметра = длина списка params после добавления; filter_in добавляет сразу несколько.', '{"driver": "fn main() {\n    let (sql, p) = Select::from(\"users\").build();\n    println!(\"{} {:?}\", sql, p);\n    let q = Select::from(\"orders\")\n        .filter(\"total\", \">\", \"100\")\n        .filter_in(\"status\", &[\"new\", \"paid\", \"shipped\"])\n        .filter(\"city\", \"=\", \"Moscow\")\n        .order_by(\"created_at\", true)\n        .limit(20)\n        .offset(40);\n    let (sql, p) = q.build();\n    println!(\"{}\", sql);\n    println!(\"{:?}\", p);\n    let (sql, p) = Select::from(\"t\").filter_in(\"id\", &[]).limit(1).build();\n    println!(\"{} {:?}\", sql, p);\n}\n", "expected": ["SELECT * FROM users []", "SELECT * FROM orders WHERE total > $1 AND status IN ($2, $3, $4) AND city = $5 ORDER BY created_at DESC LIMIT 20 OFFSET 40", "[\"100\", \"new\", \"paid\", \"shipped\", \"Moscow\"]", "SELECT * FROM t WHERE FALSE LIMIT 1 []"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 43, 'r43-pool-timeout', 5, 'rust', 'Пул соединений с таймаутом', 'Реализуйте Pool: new(n: u32) -> Arc<Pool> (соединения 1…n), get(self: &Arc<Self>, timeout: Duration) -> Option<PooledConn> (ждёт свободного соединения, но не дольше timeout; None по истечении) и Drop для PooledConn, возвращающий соединение и будящий ожидающего. Метод idle(&self) -> usize — сколько соединений свободно.', 'use std::sync::{Arc, Condvar, Mutex};
use std::time::Duration;

struct Pool {
    conns: Mutex<Vec<u32>>,
    cv: Condvar,
}

struct PooledConn {
    id: u32,
    pool: Arc<Pool>,
}

impl Pool {
    fn new(n: u32) -> Arc<Pool> {
        todo!()
    }
    fn get(self: &Arc<Self>, timeout: Duration) -> Option<PooledConn> {
        todo!()
    }
    fn idle(&self) -> usize {
        todo!()
    }
}

impl Drop for PooledConn {
    fn drop(&mut self) {
        todo!()
    }
}
', 'Condvar::wait_timeout(guard, остаток) возвращает защитник; пересчитывайте остаток времени в цикле — возможны ложные пробуждения.', '{"driver": "use std::thread;\nuse std::time::{Duration, Instant};\n\nfn main() {\n    let pool = Pool::new(2);\n    let a = pool.get(Duration::from_millis(10)).unwrap();\n    let b = pool.get(Duration::from_millis(10)).unwrap();\n    println!(\"{} {} {}\", pool.idle(), a.id != b.id, a.id + b.id);\n    let t = Instant::now();\n    let none = pool.get(Duration::from_millis(60));\n    println!(\"{} {}\", none.is_none(), t.elapsed() >= Duration::from_millis(55));\n    let p2 = Arc::clone(&pool);\n    let waiter = thread::spawn(move || p2.get(Duration::from_secs(5)).map(|c| c.id));\n    thread::sleep(Duration::from_millis(30));\n    let a_id = a.id;\n    drop(a);\n    println!(\"{}\", waiter.join().unwrap() == Some(a_id));\n    drop(b);\n    println!(\"{}\", pool.idle());\n    let workers: Vec<_> = (0..8)\n        .map(|_| {\n            let p = Arc::clone(&pool);\n            thread::spawn(move || {\n                let mut got = 0;\n                for _ in 0..20 {\n                    if let Some(c) = p.get(Duration::from_secs(5)) {\n                        thread::sleep(Duration::from_millis(1));\n                        got += (c.id > 0) as u32;\n                    }\n                }\n                got\n            })\n        })\n        .collect();\n    let total: u32 = workers.into_iter().map(|h| h.join().unwrap()).sum();\n    println!(\"{} {}\", total, pool.idle());\n}\n", "expected": ["0 true 3", "true true", "true", "2", "160 2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 43, 'r43-tx-savepoint', 6, 'rust', 'Транзакции и точки сохранения', 'Дано Conn (журнал команд). Реализуйте Tx<''a>: begin(conn) → ''BEGIN''; commit(self) → ''COMMIT''; rollback(self) → ''ROLLBACK''; Drop без commit/rollback → ''ROLLBACK''. Метод savepoint(&mut self, name: &str) -> Savepoint<''_, ''a> шлёт ''SAVEPOINT name''; у Savepoint метод release(self) шлёт ''RELEASE SAVEPOINT name'', а Drop без release — ''ROLLBACK TO SAVEPOINT name''.', 'use std::cell::RefCell;

struct Conn {
    log: RefCell<Vec<String>>,
}

impl Conn {
    fn exec(&self, sql: &str) {
        self.log.borrow_mut().push(sql.to_string());
    }
}

struct Tx<''a> {
    conn: &''a Conn,
    done: bool,
}

struct Savepoint<''t, ''a> {
    tx: &''t Tx<''a>,
    name: String,
    done: bool,
}

impl<''a> Tx<''a> {
    fn begin(conn: &''a Conn) -> Tx<''a> {
        todo!()
    }
    fn commit(mut self) {
        todo!()
    }
    fn rollback(mut self) {
        todo!()
    }
    fn savepoint<''t>(&''t mut self, name: &str) -> Savepoint<''t, ''a> {
        todo!()
    }
}

impl<''a> Drop for Tx<''a> {
    fn drop(&mut self) {
        todo!()
    }
}

impl<''t, ''a> Savepoint<''t, ''a> {
    fn release(mut self) {
        todo!()
    }
}

impl<''t, ''a> Drop for Savepoint<''t, ''a> {
    fn drop(&mut self) {
        todo!()
    }
}
', 'Флаг done у обоих охранных объектов; commit/rollback/release забирают self по значению и помечают done, чтобы Drop ничего не отправил.', '{"driver": "fn work(conn: &Conn, fail_inner: bool, fail_outer: bool) -> Result<(), String> {\n    let mut tx = Tx::begin(conn);\n    conn.exec(\"INSERT a\");\n    {\n        let sp = tx.savepoint(\"s1\");\n        conn.exec(\"INSERT b\");\n        if fail_inner {\n            return_inner(&sp)?;\n        }\n        sp.release();\n    }\n    if fail_outer {\n        return Err(\"outer\".to_string());\n    }\n    tx.commit();\n    Ok(())\n}\n\nfn return_inner(_sp: &Savepoint) -> Result<(), String> {\n    Err(\"inner\".to_string())\n}\n\nfn main() {\n    let c = Conn { log: RefCell::new(vec![]) };\n    println!(\"{:?}\", work(&c, false, false));\n    println!(\"{:?}\", work(&c, true, false));\n    println!(\"{:?}\", work(&c, false, true));\n    let tx = Tx::begin(&c);\n    tx.rollback();\n    for l in c.log.borrow().iter() {\n        println!(\"{}\", l);\n    }\n}\n", "expected": ["Ok(())", "Err(\"inner\")", "Err(\"outer\")", "BEGIN", "INSERT a", "SAVEPOINT s1", "INSERT b", "RELEASE SAVEPOINT s1", "COMMIT", "BEGIN", "INSERT a", "SAVEPOINT s1", "INSERT b", "ROLLBACK TO SAVEPOINT s1", "ROLLBACK", "BEGIN", "INSERT a", "SAVEPOINT s1", "INSERT b", "RELEASE SAVEPOINT s1", "ROLLBACK", "BEGIN", "ROLLBACK"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 43, 'r43-migrations', 7, 'rust', 'Запуск миграций', 'Напишите run_migrations(applied: &mut Vec<u32>, migrations: &[Migration], exec: &mut dyn FnMut(&str) -> Result<(), String>) -> Result<Vec<u32>, String>: миграции сортируются по версии; если у двух одинаковая версия — Err("duplicate version N") до выполнения чего-либо; уже применённые (есть в applied) пропускаются; остальные выполняются по одной через exec(sql); после успеха версия добавляется в applied и в результат; при ошибке — остановка и Err("migration N failed: ТЕКСТ"), уже выполненные остаются в applied. Результат — список новых версий по порядку.', 'struct Migration {
    version: u32,
    sql: &''static str,
}

fn run_migrations(applied: &mut Vec<u32>, migrations: &[Migration], exec: &mut dyn FnMut(&str) -> Result<(), String>) -> Result<Vec<u32>, String> {
    todo!()
}
', 'Сначала проверка дубликатов на отсортированном списке (windows(2)); дальше цикл с ранним выходом по ошибке.', '{"driver": "fn main() {\n    let ms = [\n        Migration { version: 3, sql: \"CREATE INDEX i\" },\n        Migration { version: 1, sql: \"CREATE TABLE t\" },\n        Migration { version: 2, sql: \"ALTER TABLE t\" },\n        Migration { version: 4, sql: \"BROKEN\" },\n        Migration { version: 5, sql: \"DROP TABLE x\" },\n    ];\n    let mut executed: Vec<String> = Vec::new();\n    let mut applied = vec![1];\n    let mut exec = |sql: &str| -> Result<(), String> {\n        if sql == \"BROKEN\" {\n            Err(\"syntax error\".to_string())\n        } else {\n            executed.push(sql.to_string());\n            Ok(())\n        }\n    };\n    println!(\"{:?}\", run_migrations(&mut applied, &ms, &mut exec));\n    println!(\"{:?}\", applied);\n    println!(\"{:?}\", run_migrations(&mut applied, &ms[..3], &mut exec));\n    let dup = [Migration { version: 1, sql: \"A\" }, Migration { version: 1, sql: \"B\" }];\n    println!(\"{:?}\", run_migrations(&mut applied, &dup, &mut exec));\n    println!(\"{:?}\", executed);\n}\n", "expected": ["Err(\"migration 4 failed: syntax error\")", "[1, 2, 3]", "Ok([])", "Err(\"duplicate version 1\")", "[\"ALTER TABLE t\", \"CREATE INDEX i\"]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 43, 'r43-db-url', 8, 'rust', 'Адрес подключения', 'Напишите parse_url(url: &str) -> Result<DbUrl, String> для ''postgres://[user[:password]@]host[:port]/db[?k=v&k2=v2]'' (также допустима схема ''postgresql://''): пароль и пользователь декодируются из процентного кодирования; порт по умолчанию 5432; IPv6-хост в квадратных скобках (''[::1]'') возвращается без скобок; параметры запроса — в BTreeMap. Ошибки: "bad scheme", "missing host", "missing database", "bad port".', 'use std::collections::BTreeMap;

#[derive(Debug, PartialEq)]
struct DbUrl {
    user: String,
    password: String,
    host: String,
    port: u16,
    db: String,
    params: BTreeMap<String, String>,
}

fn parse_url(url: &str) -> Result<DbUrl, String> {
    todo!()
}
', 'Разбирайте с конца к началу: сначала query, затем учётные данные (rsplit_once(''@'') — пароль может содержать ''@'' в закодированном виде), потом хост и база.', '{"driver": "fn main() {\n    println!(\"{:?}\", parse_url(\"postgres://app:p%40ss%3Aw@db.local:6543/shop?sslmode=require&connect_timeout=5\"));\n    println!(\"{:?}\", parse_url(\"postgresql://localhost/mydb\"));\n    println!(\"{:?}\", parse_url(\"postgres://u@[::1]:5433/d\"));\n    println!(\"{:?}\", parse_url(\"postgres://u:pw@[2001:db8::1]/d?x\"));\n    for bad in [\"mysql://a@b/c\", \"postgres://u@h\", \"postgres://u@h/\", \"postgres://u@:5432/d\", \"postgres://u@h:99999/d\", \"postgres://u@[::1/d\"] {\n        println!(\"{:?}\", parse_url(bad).err());\n    }\n}\n", "expected": ["Ok(DbUrl { user: \"app\", password: \"p@ss:w\", host: \"db.local\", port: 6543, db: \"shop\", params: {\"connect_timeout\": \"5\", \"sslmode\": \"require\"} })", "Ok(DbUrl { user: \"\", password: \"\", host: \"localhost\", port: 5432, db: \"mydb\", params: {} })", "Ok(DbUrl { user: \"u\", password: \"\", host: \"::1\", port: 5433, db: \"d\", params: {} })", "Ok(DbUrl { user: \"u\", password: \"pw\", host: \"2001:db8::1\", port: 5432, db: \"d\", params: {\"x\": \"\"} })", "Some(\"bad scheme\")", "Some(\"missing database\")", "Some(\"missing database\")", "Some(\"missing host\")", "Some(\"bad port\")", "Some(\"missing host\")"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (10, 43, 'r43-aggregate', 9, 'rust', 'Агрегирование строк результата', 'Напишите aggregate(rows: &[Vec<Option<String>>], key: usize, val: usize) -> BTreeMap<String, (i64, usize)>: для каждой строки ключ — колонка key (строки с NULL в ключе пропускаются), значение — колонка val как i64 (NULL и не число пропускаются, но строка всё равно учитывается как существующая группа). Результат: ключ → (сумма значений, число учтённых значений).', 'use std::collections::BTreeMap;

fn aggregate(rows: &[Vec<Option<String>>], key: usize, val: usize) -> BTreeMap<String, (i64, usize)> {
    todo!()
}
', 'entry(ключ).or_insert((0, 0)) создаёт группу даже если значение не удалось разобрать; get(i) защищает от коротких строк.', '{"driver": "fn row(cells: &[Option<&str>]) -> Vec<Option<String>> {\n    cells.iter().map(|c| c.map(|s| s.to_string())).collect()\n}\n\nfn main() {\n    let rows = vec![\n        row(&[Some(\"north\"), Some(\"10\")]),\n        row(&[Some(\"south\"), Some(\"5\")]),\n        row(&[Some(\"north\"), Some(\"7\")]),\n        row(&[None, Some(\"100\")]),\n        row(&[Some(\"west\"), None]),\n        row(&[Some(\"south\"), Some(\"x\")]),\n        row(&[Some(\"south\")]),\n        row(&[Some(\"north\"), Some(\"-2\")]),\n    ];\n    println!(\"{:?}\", aggregate(&rows, 0, 1));\n    println!(\"{:?}\", aggregate(&[], 0, 1));\n    println!(\"{:?}\", aggregate(&rows, 5, 1));\n}\n", "expected": ["{\"north\": (15, 3), \"south\": (5, 1), \"west\": (0, 0)}", "{}", "{}"]}');
