"""Задачи книги «Изучаем Rust»: глава 18 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {18: [{'id': 'r18-vec-stats',
       'mode': 'rust',
       'title': 'Vec: минимум, максимум, среднее',
       'statement': 'stats(v: &[i32]) → Option<(i32, i32, f64)>: минимум, максимум и среднее арифметическое; '
                    'для пустого среза — None.',
       'starter': 'fn stats(v: &[i32]) -> Option<(i32, i32, f64)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", stats(&[3, -1, 4, 1, 5]));\n'
                 '    println!("{:?}", stats(&[7]));\n'
                 '    println!("{:?}", stats(&[]));\n'
                 '    println!("{:?}", stats(&vec![i32::MAX, i32::MAX]));\n'
                 '}\n',
       'hint': 'min() и max() возвращают Option<&i32>; сумму считайте в i64, чтобы не переполнить i32.',
       'expected': ['Some((-1, 5, 2.4))',
                    'Some((7, 7, 7.0))',
                    'None',
                    'Some((2147483647, 2147483647, 2147483647.0))']},
      {'id': 'r18-vec-clean',
       'mode': 'rust',
       'title': 'Vec: retain, sort, dedup',
       'statement': 'clean(v: &mut Vec<i32>) приводит вектор в порядок на месте: убирает отрицательные '
                    'числа, сортирует по возрастанию, убирает повторы. Новый вектор создавать не нужно.',
       'starter': 'fn clean(v: &mut Vec<i32>) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![5, -2, 3, 5, 0, -7, 3, 9, 0];\n'
                 '    clean(&mut v);\n'
                 '    println!("{:?}", v);\n'
                 '    let mut e: Vec<i32> = vec![-1, -2];\n'
                 '    clean(&mut e);\n'
                 '    println!("{:?} {}", e, e.is_empty());\n'
                 '}\n',
       'hint': 'retain(|&x| x >= 0) оставляет подходящие элементы; dedup убирает соседние повторы, поэтому '
               'сначала sort.',
       'expected': ['[0, 3, 5, 9]', '[] true']},
      {'id': 'r18-chunks',
       'mode': 'rust',
       'title': 'Срезы Vec: chunks и windows',
       'statement': 'chunked(v, n) → Vec<Vec<i32>>: разбить на куски по n элементов (последний может быть '
                    'короче; n ≥ 1). window_sums(v, k) → Vec<i32>: суммы всех подряд идущих окон длины k (k '
                    '≥ 1; если окно не помещается — пустой вектор).',
       'starter': 'fn chunked(v: &[i32], n: usize) -> Vec<Vec<i32>> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn window_sums(v: &[i32], k: usize) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", chunked(&[1, 2, 3, 4, 5, 6, 7], 3));\n'
                 '    println!("{:?}", chunked(&[], 2));\n'
                 '    println!("{:?}", window_sums(&[1, 2, 3, 4, 5], 2));\n'
                 '    println!("{:?}", window_sums(&[1, 2], 3));\n'
                 '    println!("{:?}", window_sums(&[4, 4, 4], 3));\n'
                 '}\n',
       'hint': 'chunks(n) и windows(k) — методы срезов; каждый элемент — тоже срез, to_vec() копирует его.',
       'expected': ['[[1, 2, 3], [4, 5, 6], [7]]', '[]', '[3, 5, 7, 9]', '[]', '[12]']},
      {'id': 'r18-vec-reallocs',
       'mode': 'rust',
       'title': 'Сколько раз вырастет буфер',
       'statement': 'reallocs(n, start_cap) → usize: создайте Vec<u64> через with_capacity(start_cap), '
                    'добавьте n чисел и верните, сколько раз за это изменилась ёмкость (capacity). Сравните '
                    'с reallocs(100, 100): ровно ноль — резервировать ёмкость заранее выгодно.',
       'starter': 'fn reallocs(n: usize, start_cap: usize) -> usize {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{} {}", reallocs(0, 0), reallocs(1, 0));\n'
                 '    println!("{} {}", reallocs(100, 0), reallocs(100, 100));\n'
                 '    println!("{} {}", reallocs(1000, 0), reallocs(1000, 1000));\n'
                 '    println!("{}", reallocs(100, 60));\n'
                 '}\n',
       'hint': 'Запоминайте последнюю ёмкость и считайте, сколько раз она менялась после push.',
       'expected': ['0 1', '6 0', '9 0', '1']},
      {'id': 'r18-drain-evens',
       'mode': 'rust',
       'title': 'Разделить вектор на месте',
       'statement': 'take_evens(v: &mut Vec<i32>) → Vec<i32>: убрать из v все чётные числа и вернуть их в '
                    'прежнем порядке; в v остаются нечётные (тоже в прежнем порядке). Копировать элементы не '
                    'нужно: числа просто переезжают.',
       'starter': 'fn take_evens(v: &mut Vec<i32>) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![1, 2, 3, 4, 5, 6, 8];\n'
                 '    let e = take_evens(&mut v);\n'
                 '    println!("{:?} {:?}", e, v);\n'
                 '    let mut w: Vec<i32> = vec![];\n'
                 '    println!("{:?} {:?}", take_evens(&mut w), w);\n'
                 '}\n',
       'hint': 'drain(..) выдаёт элементы с владением; partition делит их на два вектора по условию.',
       'expected': ['[2, 4, 6, 8] [1, 3, 5]', '[] []']},
      {'id': 'r18-pascal',
       'mode': 'rust',
       'title': 'Vec<Vec<>>: треугольник Паскаля',
       'statement': 'pascal(n) → Vec<Vec<u64>>: первые n строк треугольника Паскаля (в первой строке одна '
                    'единица). Каждая строка строится из предыдущей.',
       'starter': 'fn pascal(n: usize) -> Vec<Vec<u64>> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for row in pascal(6) {\n'
                 '        println!("{:?}", row);\n'
                 '    }\n'
                 '    println!("{}", pascal(0).len());\n'
                 '    println!("{}", pascal(60)[59][30]);\n'
                 '}\n',
       'hint': 'Внутренний элемент равен сумме двух элементов предыдущей строки: rows[i-1][j-1] + '
               'rows[i-1][j].',
       'expected': ['[1]',
                    '[1, 1]',
                    '[1, 2, 1]',
                    '[1, 3, 3, 1]',
                    '[1, 4, 6, 4, 1]',
                    '[1, 5, 10, 10, 5, 1]',
                    '0',
                    '59132290782430712']},
      {'id': 'r18-iter-pipeline',
       'mode': 'rust',
       'title': 'Итераторы вместо циклов',
       'statement': 'sum_sq_odd(v) → i32 — сумма квадратов нечётных; dot(a, b) → i32 — скалярное '
                    'произведение (zip); running_max(v) → Vec<i32> — максимум на каждом префиксе (scan). '
                    'Слово for в коде использовать нельзя — только адаптеры итераторов.',
       'starter': 'fn sum_sq_odd(v: &[i32]) -> i32 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn dot(a: &[i32], b: &[i32]) -> i32 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn running_max(v: &[i32]) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!("fo", "r ")).count();\n'
                 '    println!("{}", sum_sq_odd(&[1, 2, 3, 4, 5]));\n'
                 '    println!("{}", dot(&[1, 2, 3], &[4, 5, 6]));\n'
                 '    println!("{:?}", running_max(&[3, 1, 4, 1, 5, 2, 6]));\n'
                 '    println!("{} {:?}", dot(&[1, 2], &[3]), running_max(&[]));\n'
                 '    println!("loops: {}", bad0);\n'
                 '}\n',
       'hint': 'scan(начальное, |состояние, элемент| …) хранит изменяемое состояние между шагами и '
               'возвращает Some(следующее значение).',
       'expected': ['35', '32', '[3, 3, 4, 4, 5, 5, 6]', '3 []', 'loops: 0']},
      {'id': 'r18-closure-capture',
       'mode': 'rust',
       'title': 'Замыкания и захват',
       'statement': 'count_above(v, threshold) → usize: сколько элементов больше порога (порог захватывается '
                    'замыканием). running_total(v) → Vec<i32>: нарастающие суммы; замыкание изменяет '
                    'захваченную переменную sum. apply_n(f: fn(i32) -> i32, n, x) → i32: применить функцию n '
                    'раз.',
       'starter': 'fn count_above(v: &[i32], threshold: i32) -> usize {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn running_total(v: &[i32]) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn apply_n(f: fn(i32) -> i32, n: u32, x: i32) -> i32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn double(x: i32) -> i32 {\n'
                 '    x * 2\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    println!("{} {}", count_above(&[1, 5, 10, 15], 5), count_above(&[], 0));\n'
                 '    println!("{:?}", running_total(&[1, 2, 3, 4]));\n'
                 '    println!("{} {}", apply_n(double, 5, 1), apply_n(|x| x - 1, 3, 10));\n'
                 '}\n',
       'hint': 'Замыкание |&x| sum += x … изменяет внешнюю sum — она должна быть mut; функция принимается '
               'как fn(i32) -> i32, и обычное замыкание без захвата подходит.',
       'expected': ['2 0', '[1, 3, 6, 10]', '32 7']},
      {'id': 'r18-fix-collect',
       'mode': 'rust',
       'title': 'Исправьте: collect без типа',
       'statement': 'squares_sum возводит элементы в квадрат, собирает их и суммирует. Компилятор не может '
                    'определить, в какую коллекцию собирать. Исправьте одной правкой.',
       'starter': 'fn squares_sum(v: &[i32]) -> i32 {\n'
                  '    let squares = v.iter().map(|x| x * x).collect();\n'
                  '    squares.iter().sum()\n'
                  '}\n',
       'driver': 'fn main() {\n    println!("{} {}", squares_sum(&[1, 2, 3]), squares_sum(&[]));\n}\n',
       'hint': 'collect::<Vec<i32>>() или тип у переменной: let squares: Vec<i32> = ….',
       'expected': ['14 0']},
      {'id': 'r18-caesar',
       'mode': 'rust',
       'title': 'String: шифр Цезаря',
       'statement': 'caesar(s: &str, k: u8) → String: сдвинуть каждую латинскую букву на k вперёд по кругу '
                    '(0 ≤ k ≤ 25), регистр сохранить; остальные символы (в том числе кириллицу) оставить как '
                    'есть.',
       'starter': 'fn caesar(s: &str, k: u8) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", caesar("Hello, World!", 3));\n'
                 '    println!("{}", caesar("xyz XYZ", 3));\n'
                 '    println!("{}", caesar("привет abc", 1));\n'
                 '    println!("{}", caesar(&caesar("Round trip", 7), 19));\n'
                 '}\n',
       'hint': "c as u8 - b'a' + k даёт позицию в алфавите; % 26 заворачивает по кругу; collect() из "
               'итератора char в String.',
       'expected': ['Khoor, Zruog!', 'abc ABC', 'привет bcd', 'Round trip']},
      {'id': 'r18-utf8-stats',
       'mode': 'rust',
       'title': 'Символы и байты',
       'statement': 'char_stats(s) → (usize, usize): число символов и число байт. is_palindrome(s) → bool: '
                    'палиндром, если игнорировать регистр и все символы, кроме букв и цифр. reverse_words(s) '
                    '→ String: слова в обратном порядке, через один пробел.',
       'starter': 'fn char_stats(s: &str) -> (usize, usize) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn is_palindrome(s: &str) -> bool {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn reverse_words(s: &str) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?} {:?}", char_stats("привет"), char_stats("abc"));\n'
                 '    println!("{} {}", is_palindrome("А роза упала на лапу Азора"), is_palindrome("не '
                 'палиндром"));\n'
                 '    println!("{}", is_palindrome("A man, a plan, a canal: Panama"));\n'
                 '    println!("{:?}", reverse_words("  один  два три "));\n'
                 '}\n',
       'hint': 'Соберите Vec<char> из букв и цифр в нижнем регистре и сравните его с самим собой в обратном '
               'порядке.',
       'expected': ['(6, 12) (3, 3)', 'true false', 'true', '"три два один"']},
      {'id': 'r18-title-case',
       'mode': 'rust',
       'title': 'Первая буква заглавная',
       'statement': 'title_case(s) → String: каждое слово с заглавной буквы, остальные буквы строчные '
                    '(работает и с кириллицей); слова разделяются в результате ровно одним пробелом.',
       'starter': 'fn title_case(s: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", title_case("hELLO   wORLD"));\n'
                 '    println!("{}", title_case("привет мир"));\n'
                 '    println!("{:?}", title_case("   "));\n'
                 '    println!("{}", title_case("rust"));\n'
                 '}\n',
       'hint': 'chars() даёт первую букву, а остаток — cs.as_str(); to_uppercase() возвращает итератор, '
               'соберите его в String.',
       'expected': ['Hello World', 'Привет Мир', '""', 'Rust']},
      {'id': 'r18-fix-string-add',
       'mode': 'rust',
       'title': 'Исправьте: + забрал строку',
       'statement': 'join3 склеивает три строки и дописывает «(из a b c)». Оператор + забирает левый '
                    'операнд, и a после него использовать нельзя. Исправьте, чтобы функция вернула, '
                    'например, «xyz (из x y z)».',
       'starter': 'fn join3(a: String, b: String, c: String) -> String {\n'
                  '    let ab = a + &b;\n'
                  '    let abc = ab + &c;\n'
                  '    format!("{abc} (из {a} {b} {c})")\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", join3("x".into(), "y".into(), "z".into()));\n'
                 '    println!("{}", join3("при".into(), "вет".into(), "!".into()));\n'
                 '}\n',
       'hint': 'format! не забирает аргументы, поэтому после него строки остаются доступны.',
       'expected': ['xyz (из x y z)', 'привет! (из при вет !)']},
      {'id': 'r18-word-count',
       'mode': 'rust',
       'title': 'HashMap и entry: частоты слов',
       'statement': 'word_count(text) → Vec<(String, usize)>: слова (последовательности букв; всё остальное '
                    '— разделители; регистр не важен) с количеством вхождений, отсортированные по убыванию '
                    'количества, затем по алфавиту. Подсчёт — через entry.',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn word_count(text: &str) -> Vec<(String, usize)> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let r = word_count("The fox, the DOG; the end. Fox? dog!");\n'
                 '    println!("{:?}", r);\n'
                 '    println!("{:?}", word_count("Привет, привет, мир!"));\n'
                 '    println!("{:?}", word_count("...  "));\n'
                 '}\n',
       'hint': 'split(|c: char| !c.is_alphabetic()) разбивает по небуквам; *m.entry(слово).or_insert(0) += 1 '
               'считает; сортировка — sort_by с then.',
       'expected': ['[("the", 3), ("dog", 2), ("fox", 2), ("end", 1)]', '[("привет", 2), ("мир", 1)]', '[]']},
      {'id': 'r18-group-by-len',
       'mode': 'rust',
       'title': 'Группировка по длине',
       'statement': 'group_by_len(words: &[&str]) → BTreeMap<usize, Vec<String>>: ключ — длина слова в '
                    'символах, значение — слова этой длины в порядке появления. Используйте '
                    'entry(…).or_insert_with(Vec::new).',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn group_by_len(words: &[&str]) -> BTreeMap<usize, Vec<String>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let m = group_by_len(&["a", "bb", "cc", "d", "привет", "eee", "мир", "ё"]);\n'
                 '    println!("{:?}", m);\n'
                 '    println!("{}", group_by_len(&[]).len());\n'
                 '}\n',
       'hint': 'or_insert_with(Vec::new) создаёт пустой вектор только если ключа ещё нет; push вызывается на '
               'возвращённой &mut.',
       'expected': ['{1: ["a", "d", "ё"], 2: ["bb", "cc"], 3: ["eee", "мир"], 6: ["привет"]}', '0']},
      {'id': 'r18-two-sum',
       'mode': 'rust',
       'title': 'Два числа за один проход: HashMap',
       'statement': 'two_sum(v: &[i64], target) → Option<(usize, usize)>: индексы i < j с v[i] + v[j] = '
                    'target; из всех пар нужна та, у которой j наименьшее (при равных j — наименьшее i). '
                    'Входы большие, поэтому двойной цикл не уложится в лимит: используйте HashMap «значение '
                    '→ индекс» и один проход.',
       'starter': 'fn two_sum(v: &[i64], target: i64) -> Option<(usize, usize)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", two_sum(&[2, 7, 11, 15], 9));\n'
                 '    println!("{:?}", two_sum(&[3, 3], 6));\n'
                 '    println!("{:?}", two_sum(&[1, 2, 3], 100));\n'
                 '    let n = 400_000usize;\n'
                 '    let v: Vec<i64> = (0..n as i64).map(|i| i * 3 + 1).collect();\n'
                 '    let target = v[n - 2] + v[n - 1];\n'
                 '    println!("{:?}", two_sum(&v, target));\n'
                 '}\n',
       'hint': 'Идите по элементам; для текущего x проверьте, есть ли в таблице target - x, и только потом '
               'кладите x в таблицу.',
       'expected': ['Some((0, 1))', 'Some((0, 1))', 'None', 'Some((399998, 399999))']},
      {'id': 'r18-anagrams',
       'mode': 'rust',
       'title': 'Анаграммы: ключ из отсортированных букв',
       'statement': 'anagram_groups(words: &[&str]) → Vec<Vec<String>>: сгруппируйте слова-анаграммы '
                    '(регистр не важен, но слова сохраняются как есть). Верните только группы из двух и '
                    'более слов; слова внутри группы — в порядке появления; группы — в порядке возрастания '
                    'ключа (букв слова по алфавиту).',
       'starter': 'fn anagram_groups(words: &[&str]) -> Vec<Vec<String>> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", anagram_groups(&["listen", "silent", "enlist", "google", "gogole", '
                 '"cat", "act", "Tac", "dog"]));\n'
                 '    println!("{:?}", anagram_groups(&["один", "два"]));\n'
                 '    println!("{:?}", anagram_groups(&[]));\n'
                 '}\n',
       'hint': 'Ключ группы — слово, у которого буквы отсортированы; BTreeMap сам упорядочит группы по '
               'ключу.',
       'expected': ['[["cat", "act", "Tac"], ["google", "gogole"], ["listen", "silent", "enlist"]]',
                    '[]',
                    '[]']},
      {'id': 'r18-merge-counts',
       'mode': 'rust',
       'title': 'Слияние словарей с владением',
       'statement': 'merge_counts(a, b) → BTreeMap<String, i32>: объединить два словаря счётчиков, складывая '
                    'значения для общих ключей. Оба словаря передаются по значению: ключи-строки должны '
                    'переехать, а не копироваться.',
       'starter': 'use std::collections::{BTreeMap, HashMap};\n'
                  '\n'
                  'fn merge_counts(a: HashMap<String, i32>, b: HashMap<String, i32>) -> BTreeMap<String, '
                  'i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                 '    let mut a = HashMap::new();\n'
                 '    a.insert(String::from("x"), 1);\n'
                 '    a.insert(String::from("y"), 2);\n'
                 '    let mut b = HashMap::new();\n'
                 '    b.insert(String::from("y"), 10);\n'
                 '    b.insert(String::from("z"), 5);\n'
                 '    println!("{:?}", merge_counts(a, b));\n'
                 '    println!("{:?}", merge_counts(HashMap::new(), HashMap::new()));\n'
                 '    println!("clones: {}", bad0);\n'
                 '}\n',
       'hint': 'into_iter() у HashMap отдаёт пары (String, i32) с владением; chain соединяет два итератора.',
       'expected': ['{"x": 1, "y": 12, "z": 5}', '{}', 'clones: 0']},
      {'id': 'r18-fix-key-move',
       'mode': 'rust',
       'title': 'Исправьте: ключ переехал в таблицу',
       'statement': 'index(words) → (HashMap<String, usize>, usize): отображение «слово → последний индекс» '
                    'и суммарная длина всех слов в байтах. Код не собирается: w переезжает в insert, а затем '
                    'читается. Исправьте минимальной правкой.',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn index(words: Vec<String>) -> (HashMap<String, usize>, usize) {\n'
                  '    let mut m = HashMap::new();\n'
                  '    let mut total = 0;\n'
                  '    for (i, w) in words.into_iter().enumerate() {\n'
                  '        m.insert(w, i);\n'
                  '        total += w.len();\n'
                  '    }\n'
                  '    (m, total)\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                 '    let (m, total) = index(vec!["aa".into(), "b".into(), "aa".into(), "привет".into()]);\n'
                 '    let mut items: Vec<_> = m.iter().collect();\n'
                 '    items.sort();\n'
                 '    println!("{:?} {}", items, total);\n'
                 '    println!("clones: {}", bad0);\n'
                 '}\n',
       'hint': 'Прочитайте w.len() до insert: после insert строка принадлежит таблице. Клонировать не нужно.',
       'expected': ['[("aa", 2), ("b", 1), ("привет", 3)] 17', 'clones: 0']},
      {'id': 'r18-parse-age',
       'mode': 'rust',
       'title': 'Result<u8, String> и виды ошибок разбора',
       'statement': 'parse_age(s) → Result<u8, String>: разберите строку как u8 и верните понятное '
                    'сообщение: пустая строка → "пусто"; не число (в том числе отрицательное) → "не число"; '
                    'больше 255 → "слишком велико"; число больше 150 → "нереальный возраст". Вид ошибки '
                    'узнают через e.kind() и IntErrorKind.',
       'starter': 'use std::num::IntErrorKind;\n'
                  '\n'
                  'fn parse_age(s: &str) -> Result<u8, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    for s in ["42", "", "abc", "-5", "300", "200", "150", "0"] {\n'
                 '        println!("{:?} -> {:?}", s, parse_age(s));\n'
                 '    }\n'
                 '}\n',
       'hint': 'Охрана в match: Ok(n) if n > 150 => …; для ошибок — match e.kind() { IntErrorKind::Empty => '
               '…, … }.',
       'expected': ['"42" -> Ok(42)',
                    '"" -> Err("пусто")',
                    '"abc" -> Err("не число")',
                    '"-5" -> Err("не число")',
                    '"300" -> Err("слишком велико")',
                    '"200" -> Err("нереальный возраст")',
                    '"150" -> Ok(150)',
                    '"0" -> Ok(0)']},
      {'id': 'r18-question-mark',
       'mode': 'rust',
       'title': 'Оператор ?: цепочка разборов',
       'statement': 'sum_strs(a, b) → Result<i32, ParseIntError>: разобрать обе строки и сложить; '
                    'average(items: &[&str]) → Result<f64, ParseIntError>: среднее значение чисел (пустой '
                    'набор → 0.0). Оператор ? обязателен.',
       'starter': 'use std::num::ParseIntError;\n'
                  '\n'
                  'fn sum_strs(a: &str, b: &str) -> Result<i32, ParseIntError> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn average(items: &[&str]) -> Result<f64, ParseIntError> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", sum_strs("3", " 4 "));\n'
                 '    match sum_strs("3", "x") {\n'
                 '        Ok(v) => println!("{v}"),\n'
                 '        Err(e) => println!("ошибка: {e}"),\n'
                 '    }\n'
                 '    println!("{:?}", average(&["1", "2", "4"]));\n'
                 '    println!("{:?} {}", average(&[]), average(&["1", ""]).is_err());\n'
                 '    match average(&["99999999999"]) {\n'
                 '        Ok(v) => println!("{v}"),\n'
                 '        Err(e) => println!("ошибка: {e}"),\n'
                 '    }\n'
                 '}\n',
       'hint': 'let x: i32 = a.trim().parse()?; — при ошибке функция сразу вернёт Err.',
       'expected': ['Ok(7)',
                    'ошибка: invalid digit found in string',
                    'Ok(2.3333333333333335)',
                    'Ok(0.0) true',
                    'ошибка: number too large to fit in target type']},
      {'id': 'r18-custom-error',
       'mode': 'rust',
       'title': 'Своя ошибка: enum, Display, From',
       'statement': 'AppError — Empty, Parse(ParseIntError), Negative(i32). Реализуйте Display («пустая '
                    'строка» / «не число: <причина>» / «отрицательное: N»), std::error::Error и '
                    'From<ParseIntError>, затем parse_positive(s) → Result<u32, AppError>: строка с '
                    'обрезанными пробелами; пустая → Empty; не число → Parse (через ?); меньше нуля → '
                    'Negative.',
       'starter': 'use std::fmt;\n'
                  'use std::num::ParseIntError;\n'
                  '\n'
                  '#[derive(Debug)]\n'
                  'enum AppError {\n'
                  '    Empty,\n'
                  '    Parse(ParseIntError),\n'
                  '    Negative(i32),\n'
                  '}\n'
                  '\n'
                  'impl fmt::Display for AppError {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn parse_positive(s: &str) -> Result<u32, AppError> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    for s in ["17", "  ", "x1", "-3", " 0 "] {\n'
                 '        match parse_positive(s) {\n'
                 '            Ok(n) => println!("ok {n}"),\n'
                 '            Err(e) => println!("{e}"),\n'
                 '        }\n'
                 '    }\n'
                 '    let e: Box<dyn std::error::Error> = Box::new(AppError::Negative(-1));\n'
                 '    println!("{e}");\n'
                 '    println!("{:?}", parse_positive(""));\n'
                 '}\n',
       'hint': 'impl From<ParseIntError> for AppError { fn from(e) -> AppError { AppError::Parse(e) } } — '
               'тогда ? преобразует ошибку сам.',
       'expected': ['ok 17',
                    'пустая строка',
                    'не число: invalid digit found in string',
                    'отрицательное: -3',
                    'ok 0',
                    'отрицательное: -1',
                    'Err(Empty)']},
      {'id': 'r18-box-dyn-error',
       'mode': 'rust',
       'title': 'Box<dyn Error>: любая ошибка',
       'statement': 'run(a, b) → Result<i32, Box<dyn Error>>: разобрать оба аргумента как i32 (ошибка '
                    'разбора пробрасывается через ?) и разделить a на b; при b == 0 вернуть собственную '
                    'ошибку «деление на ноль» (строку можно превратить в Box<dyn Error> через .into()).',
       'starter': 'use std::error::Error;\n'
                  '\n'
                  'fn run(a: &str, b: &str) -> Result<i32, Box<dyn Error>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    for (a, b) in [("84", "2"), ("1", "0"), ("x", "1"), ("5", ""), ("-9", "3")] {\n'
                 '        match run(a, b) {\n'
                 '            Ok(v) => println!("{v}"),\n'
                 '            Err(e) => println!("ошибка: {e}"),\n'
                 '        }\n'
                 '    }\n'
                 '}\n',
       'hint': 'Err("текст".into()) строит Box<dyn Error> из строки; ? сам упаковывает ParseIntError.',
       'expected': ['42',
                    'ошибка: деление на ноль',
                    'ошибка: invalid digit found in string',
                    'ошибка: cannot parse integer from empty string',
                    '-3']},
      {'id': 'r18-map-err',
       'mode': 'rust',
       'title': 'map_err: понятное сообщение',
       'statement': 'read_port(s) → Result<u16, String>: порт из строки. Ошибка разбора превращается в «bad '
                    "port '<s>': <причина>» через map_err, а значение 0 — в «port 0 reserved». Допустимые "
                    'значения: 1..=65535.',
       'starter': 'fn read_port(s: &str) -> Result<u16, String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for s in ["8080", "0", "70000", "http", " 443 ", ""] {\n'
                 '        println!("{:?}", read_port(s));\n'
                 '    }\n'
                 '}\n',
       'hint': 'map_err(|e| format!(…)) меняет только ошибку; после него ? пробрасывает уже String.',
       'expected': ['Ok(8080)',
                    'Err("port 0 reserved")',
                    'Err("bad port \'70000\': number too large to fit in target type")',
                    'Err("bad port \'http\': invalid digit found in string")',
                    'Ok(443)',
                    'Err("bad port \'\': cannot parse integer from empty string")']},
      {'id': 'r18-collect-result',
       'mode': 'rust',
       'title': 'collect в Result<Vec<_>, _>',
       'statement': 'parse_all(items) → Result<Vec<i32>, ParseIntError>: разобрать все строки; при первой '
                    'ошибке вернуть её (один collect). sum_valid(items) → i32: сумма только корректных '
                    'чисел, ошибки пропускаются (filter_map + ok).',
       'starter': 'use std::num::ParseIntError;\n'
                  '\n'
                  'fn parse_all(items: &[&str]) -> Result<Vec<i32>, ParseIntError> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn sum_valid(items: &[&str]) -> i32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", parse_all(&["1", " 2 ", "3"]));\n'
                 '    println!("{:?}", parse_all(&["1", "x", "3", "y"]));\n'
                 '    println!("{:?}", parse_all(&[]));\n'
                 '    println!("{} {}", sum_valid(&["1", "x", "30", ""]), sum_valid(&[]));\n'
                 '}\n',
       'hint': 'collect() в Result<Vec<_>, _> берёт итератор из Result и останавливается на первой ошибке; '
               'ok() превращает Result в Option.',
       'expected': ['Ok([1, 2, 3])', 'Err(ParseIntError { kind: InvalidDigit })', 'Ok([])', '31 0']},
      {'id': 'r18-ok-or',
       'mode': 'rust',
       'title': 'ok_or: из Option в Result',
       'statement': 'lookup(m: &HashMap<&str, i32>, key) → Result<i32, String>: значение по ключу или ошибка '
                    '«нет ключа <key>» (ok_or_else). first_digit(s) → Result<u32, String>: значение первой '
                    'цифры строки или ошибка «нет цифр» (используйте chars, find и to_digit).',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn lookup(m: &HashMap<&str, i32>, key: &str) -> Result<i32, String> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn first_digit(s: &str) -> Result<u32, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut m = HashMap::new();\n'
                 '    m.insert("a", 1);\n'
                 '    m.insert("b", 2);\n'
                 '    println!("{:?} {:?}", lookup(&m, "a"), lookup(&m, "z"));\n'
                 '    println!("{:?} {:?} {:?}", first_digit("abc7x9"), first_digit("none"), '
                 'first_digit(""));\n'
                 '}\n',
       'hint': 'get возвращает Option<&i32>; copied() даёт Option<i32>; ok_or_else(|| …) превращает None в '
               'Err.',
       'expected': ['Ok(1) Err("нет ключа z")', 'Ok(7) Err("нет цифр") Err("нет цифр")']},
      {'id': 'r18-fix-question-mark',
       'mode': 'rust',
       'title': 'Исправьте: ? в функции без Result',
       'statement': 'double разбирает строку и удваивает число. Оператор ? использован в функции, которая '
                    'возвращает просто i32 — компилятор отвечает ошибкой. Исправьте сигнатуру (результат — '
                    'Result<i32, ParseIntError>), тело меняется минимально.',
       'starter': 'use std::num::ParseIntError;\n'
                  '\n'
                  'fn double(s: &str) -> i32 {\n'
                  '    let n: i32 = s.trim().parse()?;\n'
                  '    n * 2\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?} {:?}", double("21"), double(" -4 "));\n'
                 '    println!("{}", double("z").is_err());\n'
                 '}\n',
       'hint': 'Тип функции — Result<i32, ParseIntError>, последнее выражение — Ok(n * 2).',
       'expected': ['Ok(42) Ok(-8)', 'true']},
      {'id': 'r18-unwind-drop',
       'mode': 'rust',
       'title': 'Паника разматывает стек и вызывает drop',
       'statement': 'Guard печатает «drop g» при уничтожении. Напишите risky(): создайте Guard и затем '
                    'вызовите panic!("boom"). Драйвер перехватит панику через catch_unwind и покажет, что '
                    'Guard всё равно был уничтожен: сначала выведется «drop g», затем «caught».',
       'starter': "struct Guard(&'static str);\n"
                  '\n'
                  'impl Drop for Guard {\n'
                  '    fn drop(&mut self) {\n'
                  '        println!("drop {}", self.0);\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn risky() {\n'
                  '    // создайте Guard и вызовите panic!\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    std::panic::set_hook(Box::new(|_| {}));\n'
                 '    let r = std::panic::catch_unwind(|| risky());\n'
                 '    println!("{}", if r.is_err() { "caught" } else { "no panic" });\n'
                 '}\n',
       'hint': 'let _g = Guard("g"); — привязка с именем живёт до конца функции, и при панике drop '
               'вызывается во время размотки.',
       'expected': ['drop g', 'caught']},
      {'id': 'r18-retry',
       'mode': 'rust',
       'title': 'Повторные попытки: замыкание FnMut',
       'statement': 'retry(n, f) → Result<i32, String>: вызывайте f(попытка) для попыток 1, 2, …, n, пока не '
                    'получите Ok; верните первый Ok или последнюю ошибку (n = 0 → «нет попыток»). f — '
                    'замыкание FnMut(u32) -> Result<i32, String>, оно может менять захваченные переменные.',
       'starter': 'fn retry(n: u32, mut f: impl FnMut(u32) -> Result<i32, String>) -> Result<i32, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut calls = 0;\n'
                 '    let r = retry(5, |k| {\n'
                 '        calls += 1;\n'
                 '        if k < 3 { Err(format!("fail {k}")) } else { Ok(k as i32 * 10) }\n'
                 '    });\n'
                 '    println!("{:?} calls={}", r, calls);\n'
                 '    println!("{:?}", retry(3, |k| Err(format!("fail {k}"))));\n'
                 '    println!("{:?}", retry(0, |_| Ok(1)));\n'
                 '}\n',
       'hint': 'Храните последнюю ошибку в переменной и возвращайте её после цикла; Ok — сразу через return.',
       'expected': ['Ok(30) calls=3', 'Err("fail 3")', 'Err("нет попыток")']},
      {'id': 'r18-config-parser',
       'mode': 'rust',
       'title': 'Разбор конфигурации с номерами строк',
       'statement': 'parse_config(text) → Result<BTreeMap<String, String>, String>: строки «ключ = '
                    'значение»; пустые строки и строки, начинающиеся с «#», пропускаются; пробелы по краям '
                    "ключа и значения обрезаются. Первая же ошибка: «line N: нет '='», «line N: пустой ключ» "
                    'или «line N: дубликат ключа K» (N — номер строки с единицы).',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn parse_config(text: &str) -> Result<BTreeMap<String, String>, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", parse_config("# comment\\nname = app\\n\\nport=8080\\nmode =  fast = '
                 'yes\\n"));\n'
                 '    println!("{:?}", parse_config("a=1\\nbroken\\nb=2"));\n'
                 '    println!("{:?}", parse_config("a=1\\n = 5"));\n'
                 '    println!("{:?}", parse_config("x=1\\ny=2\\nx=3"));\n'
                 '    println!("{:?}", parse_config(""));\n'
                 '}\n',
       'hint': "lines().enumerate() даёт индекс с нуля — добавьте 1; split_once('=') делит по первому знаку "
               'равенства.',
       'expected': ['Ok({"mode": "fast = yes", "name": "app", "port": "8080"})',
                    'Err("line 2: нет \'=\'")',
                    'Err("line 2: пустой ключ")',
                    'Err("line 3: дубликат ключа x")',
                    'Ok({})']}]}
