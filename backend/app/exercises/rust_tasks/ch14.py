"""Задачи книги «Изучаем Rust»: глава 14 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {14: [{'id': 'r14-word-count',
       'mode': 'rust',
       'title': 'Counter',
       'statement': 'Python: Counter(words). Напишите count_words(text: &str) -> Vec<(String, usize)>: '
                    'частоты слов (split_whitespace, в нижнем регистре), по убыванию частоты, при равных — '
                    'по алфавиту.',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn count_words(text: &str) -> Vec<(String, usize)> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", count_words("a b A c b a"));\n'
                 '    println!("{:?}", count_words(""));\n'
                 '}\n',
       'hint': 'entry().or_insert(0) и сортировка пар.',
       'expected': ['[("a", 3), ("b", 2), ("c", 1)]', '[]']},
      {'id': 'r14-get-default',
       'mode': 'rust',
       'title': 'd.get(k, default)',
       'statement': 'Python: d.get(k, 0). Напишите lookup(m: &HashMap<String, i32>, k: &str) -> i32 — '
                    'значение по ключу или 0.',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn lookup(m: &HashMap<String, i32>, k: &str) -> i32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut m = HashMap::new();\n'
                 '    m.insert(String::from("a"), 5);\n'
                 '    println!("{}", lookup(&m, "a"));\n'
                 '    println!("{}", lookup(&m, "z"));\n'
                 '}\n',
       'hint': 'get(k).copied().unwrap_or(0)',
       'expected': ['5', '0']},
      {'id': 'r14-invert',
       'mode': 'rust',
       'title': 'Инвертировать словарь',
       'statement': 'Python: {v: k for k, v in d.items()}. Напишите invert(m: &HashMap<String, i32>) -> '
                    'HashMap<i32, String> (значения уникальны).',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn invert(m: &HashMap<String, i32>) -> HashMap<i32, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut m = HashMap::new();\n'
                 '    m.insert(String::from("a"), 1);\n'
                 '    m.insert(String::from("b"), 2);\n'
                 '    let r = invert(&m);\n'
                 '    println!("{} {} {}", r.len(), r[&1], r[&2]);\n'
                 '}\n',
       'hint': 'iter().map(|(k, v)| (*v, k.clone())).collect()',
       'expected': ['2 a b']},
      {'id': 'r14-group-by-len',
       'mode': 'rust',
       'title': 'Группировка по длине',
       'statement': 'Python: defaultdict(list). Напишите group_by_len(words: &[&str]) -> BTreeMap<usize, '
                    'Vec<String>>: слова по длине в символах (внутри — в исходном порядке).',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn group_by_len(words: &[&str]) -> BTreeMap<usize, Vec<String>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", group_by_len(&["a", "bb", "c", "dd", "eee"]));\n'
                 '    println!("{:?}", group_by_len(&[]));\n'
                 '}\n',
       'hint': 'entry(len).or_default().push(…)',
       'expected': ['{1: ["a", "c"], 2: ["bb", "dd"], 3: ["eee"]}', '{}']},
      {'id': 'r14-anagram-groups',
       'mode': 'rust',
       'title': 'Группы анаграмм',
       'statement': 'Напишите group_anagrams(words: &[&str]) -> Vec<Vec<String>>: слова-анаграммы вместе; '
                    'группы отсортированы по первому слову, слова внутри групп — в исходном порядке. Ключ — '
                    'отсортированные буквы.',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn group_anagrams(words: &[&str]) -> Vec<Vec<String>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", group_anagrams(&["tea", "eat", "tan", "ate", "nat", "bat"]));\n'
                 '}\n',
       'hint': 'Ключ Vec<char> — подходит: Vec реализует Hash.',
       'expected': ['[["bat"], ["tan", "nat"], ["tea", "eat", "ate"]]']},
      {'id': 'r14-two-sum-map',
       'mode': 'rust',
       'title': 'Два числа за один проход',
       'statement': 'Напишите two_sum(v: &[i32], target: i32) -> Option<(usize, usize)>: индексы (i, j), i < '
                    'j, с v[i] + v[j] = target, за один проход с HashMap «значение → индекс». Для первой '
                    'найденной при проходе j пары.',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn two_sum(v: &[i32], target: i32) -> Option<(usize, usize)> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", two_sum(&[2, 7, 11, 15], 9));\n'
                 '    println!("{:?}", two_sum(&[3, 2, 4], 6));\n'
                 '    println!("{:?}", two_sum(&[1, 2], 10));\n'
                 '    let big: Vec<i32> = (0..200000).collect();\n'
                 '    println!("{:?}", two_sum(&big, 399997));\n'
                 '}\n',
       'hint': 'Для каждого x ищем target - x среди уже просмотренных.',
       'expected': ['Some((0, 1))', 'Some((1, 2))', 'None', 'Some((199998, 199999))']},
      {'id': 'r14-merge-sum',
       'mode': 'rust',
       'title': 'Слияние со сложением',
       'statement': 'Python: Counter(a) + Counter(b). Напишите merge_sum(a: &HashMap<String, i32>, b: '
                    '&HashMap<String, i32>) -> BTreeMap<String, i32>: ключи объединяются, значения при '
                    'совпадении складываются.',
       'starter': 'use std::collections::{BTreeMap, HashMap};\n'
                  '\n'
                  'fn merge_sum(a: &HashMap<String, i32>, b: &HashMap<String, i32>) -> BTreeMap<String, i32> '
                  '{\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut a = HashMap::new();\n'
                 '    a.insert(String::from("x"), 1);\n'
                 '    a.insert(String::from("y"), 2);\n'
                 '    let mut b = HashMap::new();\n'
                 '    b.insert(String::from("y"), 10);\n'
                 '    b.insert(String::from("z"), 5);\n'
                 '    println!("{:?}", merge_sum(&a, &b));\n'
                 '}\n',
       'hint': 'Обойдите обе карты и накапливайте в одну.',
       'expected': ['{"x": 1, "y": 12, "z": 5}']},
      {'id': 'r14-dict-from-zip',
       'mode': 'rust',
       'title': 'dict(zip(k, v))',
       'statement': 'Напишите zip_map(keys: &[&str], vals: &[i32]) -> BTreeMap<String, i32> — пары по '
                    'короткому из двух срезов.',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn zip_map(keys: &[&str], vals: &[i32]) -> BTreeMap<String, i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", zip_map(&["a", "b", "c"], &[1, 2]));\n'
                 '    println!("{:?}", zip_map(&[], &[1]));\n'
                 '}\n',
       'hint': 'zip + collect в BTreeMap.',
       'expected': ['{"a": 1, "b": 2}', '{}']},
      {'id': 'r14-top-n',
       'mode': 'rust',
       'title': 'Топ слов',
       'statement': 'Напишите top_words(text: &str, n: usize) -> Vec<String>: n самых частых слов (в нижнем '
                    'регистре); при равных частотах — по алфавиту.',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn top_words(text: &str, n: usize) -> Vec<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", top_words("the cat and the dog and the bird", 2));\n'
                 '    println!("{:?}", top_words("a b c", 5));\n'
                 '    println!("{:?}", top_words("", 3));\n'
                 '}\n',
       'hint': 'Сначала счёт, затем sort_by и take(n).',
       'expected': ['["the", "and"]', '["a", "b", "c"]', '[]']},
      {'id': 'r14-entry-and-modify',
       'mode': 'rust',
       'title': 'and_modify',
       'statement': 'Напишите apply(events: &[(&str, i32)]) -> BTreeMap<String, i32>: для каждого события '
                    '(ключ, значение) — если ключ уже есть, прибавить значение, иначе поставить его '
                    '(and_modify + or_insert).',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn apply(events: &[(&str, i32)]) -> BTreeMap<String, i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", apply(&[("a", 1), ("b", 2), ("a", 10)]));\n'
                 '    println!("{:?}", apply(&[]));\n'
                 '}\n',
       'hint': 'm.entry(k).and_modify(|e| *e += v).or_insert(v)',
       'expected': ['{"a": 11, "b": 2}', '{}']},
      {'id': 'r14-btree-range',
       'mode': 'rust',
       'title': 'Диапазон ключей',
       'statement': 'Напишите between(m: &BTreeMap<i32, String>, lo: i32, hi: i32) -> Vec<String>: значения '
                    'для ключей из [lo, hi] по возрастанию ключа (метод range).',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn between(m: &BTreeMap<i32, String>, lo: i32, hi: i32) -> Vec<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut m = BTreeMap::new();\n'
                 '    for (k, v) in [(5, "e"), (1, "a"), (3, "c"), (4, "d"), (2, "b")] {\n'
                 '        m.insert(k, v.to_string());\n'
                 '    }\n'
                 '    println!("{:?}", between(&m, 2, 4));\n'
                 '    println!("{:?}", between(&m, 6, 9));\n'
                 '    println!("{:?}", between(&m, 0, 1));\n'
                 '}\n',
       'hint': 'm.range(lo..=hi)',
       'expected': ['["b", "c", "d"]', '[]', '["a"]']},
      {'id': 'r14-first-last',
       'mode': 'rust',
       'title': 'Минимальный и максимальный ключ',
       'statement': 'Напишите extremes(m: &BTreeMap<i32, i32>) -> Option<(i32, i32)>: (наименьший ключ, '
                    'наибольший ключ) или None для пустой карты (first_key_value, last_key_value).',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn extremes(m: &BTreeMap<i32, i32>) -> Option<(i32, i32)> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut m = BTreeMap::new();\n'
                 '    println!("{:?}", extremes(&m));\n'
                 '    m.insert(5, 0);\n'
                 '    m.insert(-2, 1);\n'
                 '    m.insert(9, 2);\n'
                 '    println!("{:?}", extremes(&m));\n'
                 '}\n',
       'hint': 'first_key_value() возвращает Option<(&K, &V)>.',
       'expected': ['None', 'Some((-2, 9))']},
      {'id': 'r14-set-ops',
       'mode': 'rust',
       'title': 'Операции над множествами',
       'statement': 'Напишите set_ops(a: &[i32], b: &[i32]) -> (Vec<i32>, Vec<i32>, Vec<i32>): объединение, '
                    'пересечение и разность a − b, каждый результат отсортирован по возрастанию.',
       'starter': 'use std::collections::HashSet;\n'
                  '\n'
                  'fn set_ops(a: &[i32], b: &[i32]) -> (Vec<i32>, Vec<i32>, Vec<i32>) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", set_ops(&[1, 2, 3, 3], &[3, 4, 5]));\n'
                 '    println!("{:?}", set_ops(&[], &[1]));\n'
                 '}\n',
       'hint': 'union, intersection, difference — итераторы; соберите в Vec и отсортируйте.',
       'expected': ['([1, 2, 3, 4, 5], [3], [1, 2])', '([1], [], [])']},
      {'id': 'r14-unique-count',
       'mode': 'rust',
       'title': 'Сколько различных',
       'statement': 'Python: len(set(l)). Напишите distinct(v: &[i32]) -> usize.',
       'starter': 'use std::collections::HashSet;\n\nfn distinct(v: &[i32]) -> usize {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", distinct(&[1, 2, 2, 3, 3, 3]));\n'
                 '    println!("{}", distinct(&[]));\n'
                 '    let big: Vec<i32> = (0..300000).map(|x| x % 1000).collect();\n'
                 '    println!("{}", distinct(&big));\n'
                 '}\n',
       'hint': 'collect в HashSet и len().',
       'expected': ['3', '0', '1000']},
      {'id': 'r14-has-duplicates',
       'mode': 'rust',
       'title': 'Есть ли дубликаты',
       'statement': 'Напишите has_duplicates(v: &[i32]) -> bool за линейное время: HashSet и ранний выход '
                    'при повторе (insert возвращает false).',
       'starter': 'use std::collections::HashSet;\n'
                  '\n'
                  'fn has_duplicates(v: &[i32]) -> bool {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", has_duplicates(&[1, 2, 3]));\n'
                 '    println!("{}", has_duplicates(&[1, 2, 1]));\n'
                 '    let big: Vec<i32> = (0..500000).collect();\n'
                 '    println!("{}", has_duplicates(&big));\n'
                 '}\n',
       'hint': 'if !seen.insert(x) { return true; }',
       'expected': ['false', 'true', 'false']},
      {'id': 'r14-common-chars',
       'mode': 'rust',
       'title': 'Общие буквы',
       'statement': 'Напишите common(a: &str, b: &str) -> String: буквы, которые есть в обеих строках (без '
                    'повторов), по алфавиту.',
       'starter': 'use std::collections::HashSet;\n'
                  '\n'
                  'fn common(a: &str, b: &str) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", common("hello", "world"));\n'
                 '    println!("[{}]", common("abc", "xyz"));\n'
                 '    println!("{}", common("привет", "тире"));\n'
                 '}\n',
       'hint': 'Пересечение двух HashSet<char>.',
       'expected': ['lo', '[]', 'еирт']},
      {'id': 'r14-pangram',
       'mode': 'rust',
       'title': 'Панграмма',
       'statement': 'Напишите is_pangram(s: &str) -> bool: содержит ли строка все 26 букв латиницы (регистр '
                    'не важен).',
       'starter': 'use std::collections::HashSet;\n\nfn is_pangram(s: &str) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", is_pangram("The quick brown fox jumps over the lazy dog"));\n'
                 '    println!("{}", is_pangram("hello world"));\n'
                 '    println!("{}", is_pangram(""));\n'
                 '}\n',
       'hint': 'Соберите множество букв и проверьте размер.',
       'expected': ['true', 'false', 'false']},
      {'id': 'r14-lru-like',
       'mode': 'rust',
       'title': 'Первый неповторяющийся',
       'statement': 'Python: Counter + проход. Напишите first_unique(v: &[i32]) -> Option<i32>: первый '
                    'элемент, встречающийся ровно один раз.',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn first_unique(v: &[i32]) -> Option<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", first_unique(&[4, 5, 4, 6, 5, 7]));\n'
                 '    println!("{:?}", first_unique(&[1, 1]));\n'
                 '    println!("{:?}", first_unique(&[]));\n'
                 '}\n',
       'hint': 'Первый проход считает, второй ищет count == 1.',
       'expected': ['Some(6)', 'None', 'None']},
      {'id': 'r14-char-histogram',
       'mode': 'rust',
       'title': 'Гистограмма символов',
       'statement': 'Напишите histogram(s: &str) -> BTreeMap<char, usize>: сколько раз встречается каждый '
                    'символ (без пробелов).',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn histogram(s: &str) -> BTreeMap<char, usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", histogram("hello world"));\n'
                 '    println!("{:?}", histogram(""));\n'
                 '}\n',
       'hint': 'BTreeMap хранит ключи отсортированными.',
       'expected': ["{'d': 1, 'e': 1, 'h': 1, 'l': 3, 'o': 2, 'r': 1, 'w': 1}", '{}']},
      {'id': 'r14-inventory',
       'mode': 'rust',
       'title': 'Склад',
       'statement': 'Напишите update_stock(stock: &mut HashMap<String, u32>, op: &str, item: &str, n: u32) '
                    '-> Result<(), String>: «add» увеличивает остаток; «take» уменьшает (Err("нет товара"), '
                    'если ключа нет, и Err("мало"), если остаток меньше n; при остатке 0 ключ удаляется); '
                    'иные операции — Err("операция").',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn update_stock(stock: &mut HashMap<String, u32>, op: &str, item: &str, n: u32) -> '
                  'Result<(), String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut s = HashMap::new();\n'
                 '    println!("{:?}", update_stock(&mut s, "add", "гвозди", 10));\n'
                 '    println!("{:?}", update_stock(&mut s, "take", "гвозди", 4));\n'
                 '    println!("{:?}", update_stock(&mut s, "take", "гвозди", 7));\n'
                 '    println!("{:?}", update_stock(&mut s, "take", "болты", 1));\n'
                 '    println!("{:?}", update_stock(&mut s, "take", "гвозди", 6));\n'
                 '    println!("{}", s.len());\n'
                 '    println!("{:?}", update_stock(&mut s, "sell", "x", 1));\n'
                 '}\n',
       'hint': 'get_mut даёт &mut значения; remove при нуле.',
       'expected': ['Ok(())',
                    'Ok(())',
                    'Err("мало")',
                    'Err("нет товара")',
                    'Ok(())',
                    '0',
                    'Err("операция")']},
      {'id': 'r14-index',
       'mode': 'rust',
       'title': 'Индекс слов',
       'statement': 'Напишите build_index(docs: &[&str]) -> BTreeMap<String, Vec<usize>>: для каждого слова '
                    '(в нижнем регистре) — номера документов (с 0, без повторов, по возрастанию), где оно '
                    'встречается.',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn build_index(docs: &[&str]) -> BTreeMap<String, Vec<usize>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", build_index(&["Rust is fast", "rust is safe", "Go is fast fast"]));\n'
                 '}\n',
       'hint': 'Проверьте last() перед push, чтобы не дублировать номер.',
       'expected': ['{"fast": [0, 2], "go": [2], "is": [0, 1, 2], "rust": [0, 1], "safe": [1]}']},
      {'id': 'r14-memo-fib',
       'mode': 'rust',
       'title': 'Мемоизация',
       'statement': 'Напишите fib(n: u64, memo: &mut HashMap<u64, u64>) -> u64 с мемоизацией (аналог '
                    '@lru_cache): fib(0)=0, fib(1)=1. Для n = 90 вычисление мгновенно.',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn fib(n: u64, memo: &mut HashMap<u64, u64>) -> u64 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut memo = HashMap::new();\n'
                 '    println!("{}", fib(10, &mut memo));\n'
                 '    println!("{}", fib(90, &mut memo));\n'
                 '    println!("{}", memo.len());\n'
                 '}\n',
       'hint': 'Сначала смотрим в memo, потом считаем и сохраняем.',
       'expected': ['55', '2880067194370816120', '89']},
      {'id': 'r14-lookup-table',
       'mode': 'rust',
       'title': 'Таблица соответствий',
       'statement': 'Напишите roman_to_int(s: &str) -> u32: римское число в обычное (I=1, V=5, X=10, L=50, '
                    'C=100, D=500, M=1000; меньшая цифра перед большей вычитается). Используйте '
                    'HashMap<char, u32> или match.',
       'starter': 'use std::collections::HashMap;\n\nfn roman_to_int(s: &str) -> u32 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for s in ["III", "IV", "IX", "LVIII", "MCMXCIV", "MMXXVI"] {\n'
                 '        println!("{} {}", s, roman_to_int(s));\n'
                 '    }\n'
                 '}\n',
       'hint': 'Если следующая цифра больше, текущую вычитаем.',
       'expected': ['III 3', 'IV 4', 'IX 9', 'LVIII 58', 'MCMXCIV 1994', 'MMXXVI 2026']},
      {'id': 'r14-cache',
       'mode': 'rust',
       'title': 'Кэш с лимитом',
       'statement': 'Реализуйте структуру Cache с полями map: HashMap<String, i32>, order: Vec<String>, cap: '
                    'usize. Функция new(cap) создаёт пустой кэш; put(&mut self, k: &str, v: i32) добавляет '
                    'пару и при превышении cap вытесняет самый старый ключ (FIFO); при обновлении '
                    'существующего ключа порядок не меняется; get(&self, k: &str) -> Option<i32>.',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'struct Cache {\n'
                  '    map: HashMap<String, i32>,\n'
                  '    order: Vec<String>,\n'
                  '    cap: usize,\n'
                  '}\n'
                  '\n'
                  'impl Cache {\n'
                  '    fn new(cap: usize) -> Cache {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn put(&mut self, k: &str, v: i32) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn get(&self, k: &str) -> Option<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut c = Cache::new(2);\n'
                 '    c.put("a", 1);\n'
                 '    c.put("b", 2);\n'
                 '    c.put("a", 10);\n'
                 '    c.put("c", 3);\n'
                 '    println!("{:?} {:?} {:?}", c.get("a"), c.get("b"), c.get("c"));\n'
                 '}\n',
       'hint': 'При вытеснении удалите первый элемент order и его ключ в map.',
       'expected': ['None Some(2) Some(3)']},
      {'id': 'r14-bimap',
       'mode': 'rust',
       'title': 'Двунаправленное соответствие',
       'statement': 'Напишите is_isomorphic(a: &str, b: &str) -> bool: можно ли заменить буквы a на буквы b '
                    'так, чтобы получить b (каждая буква отображается в одну и ту же, разные — в разные; '
                    'строки одной длины).',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn is_isomorphic(a: &str, b: &str) -> bool {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", is_isomorphic("egg", "add"));\n'
                 '    println!("{}", is_isomorphic("foo", "bar"));\n'
                 '    println!("{}", is_isomorphic("paper", "title"));\n'
                 '    println!("{}", is_isomorphic("ab", "aa"));\n'
                 '    println!("{}", is_isomorphic("", ""));\n'
                 '}\n',
       'hint': 'Две карты: a → b и b → a.',
       'expected': ['true', 'false', 'true', 'false', 'true']},
      {'id': 'r14-graph-degrees',
       'mode': 'rust',
       'title': 'Степени вершин графа',
       'statement': 'Напишите degrees(edges: &[(u32, u32)]) -> BTreeMap<u32, usize>: степень каждой вершины '
                    'неориентированного графа (каждое ребро увеличивает степень обоих концов; петля (v, v) '
                    'считается дважды).',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn degrees(edges: &[(u32, u32)]) -> BTreeMap<u32, usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", degrees(&[(1, 2), (2, 3), (3, 1), (3, 4)]));\n'
                 '    println!("{:?}", degrees(&[(5, 5)]));\n'
                 '    println!("{:?}", degrees(&[]));\n'
                 '}\n',
       'hint': 'Два entry на ребро.',
       'expected': ['{1: 2, 2: 2, 3: 3, 4: 1}', '{5: 2}', '{}']},
      {'id': 'r14-adjacency',
       'mode': 'rust',
       'title': 'Список смежности',
       'statement': 'Напишите adjacency(edges: &[(u32, u32)]) -> BTreeMap<u32, Vec<u32>>: для каждой вершины '
                    '— отсортированный список соседей неориентированного графа без повторов.',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn adjacency(edges: &[(u32, u32)]) -> BTreeMap<u32, Vec<u32>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", adjacency(&[(1, 2), (1, 3), (2, 3), (1, 2)]));\n'
                 '    println!("{:?}", adjacency(&[]));\n'
                 '}\n',
       'hint': 'or_default().push в обе стороны; потом sort и dedup.',
       'expected': ['{1: [2, 3], 2: [1, 3], 3: [1, 2]}', '{}']},
      {'id': 'r14-sorted-by-value',
       'mode': 'rust',
       'title': 'Сортировка по значению',
       'statement': 'Python: sorted(d.items(), key=lambda kv: kv[1]). Напишите by_value(m: &HashMap<String, '
                    'i32>) -> Vec<(String, i32)>: пары по возрастанию значения, при равных — по ключу.',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'fn by_value(m: &HashMap<String, i32>) -> Vec<(String, i32)> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut m = HashMap::new();\n'
                 '    m.insert(String::from("b"), 2);\n'
                 '    m.insert(String::from("a"), 2);\n'
                 '    m.insert(String::from("c"), -1);\n'
                 '    println!("{:?}", by_value(&m));\n'
                 '}\n',
       'hint': 'sort_by с then для разрешения равенства.',
       'expected': ['[("c", -1), ("a", 2), ("b", 2)]']},
      {'id': 'r14-struct-key',
       'mode': 'rust',
       'title': 'Структура как ключ',
       'statement': 'Добавьте структуре Pos { x: i32, y: i32 } нужные derive (Hash, PartialEq, Eq, Clone, '
                    'Copy, Debug) и напишите visited(path: &[(i32, i32)]) -> usize: сколько различных клеток '
                    'посещено (HashSet<Pos>).',
       'starter': 'use std::collections::HashSet;\n'
                  '\n'
                  'struct Pos {\n'
                  '    x: i32,\n'
                  '    y: i32,\n'
                  '}\n'
                  '\n'
                  'fn visited(path: &[(i32, i32)]) -> usize {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", visited(&[(0, 0), (1, 0), (1, 1), (0, 0), (1, 0)]));\n'
                 '    println!("{}", visited(&[]));\n'
                 '}\n',
       'hint': '#[derive(Hash, PartialEq, Eq)] делает структуру пригодной как ключ.',
       'expected': ['3', '0']},
      {'id': 'r14-sym-diff',
       'mode': 'rust',
       'title': 'Что изменилось',
       'statement': 'Напишите changed(old: &[&str], new: &[&str]) -> Vec<String>: слова, которые есть ровно '
                    'в одном из списков (симметрическая разность), по алфавиту.',
       'starter': 'use std::collections::HashSet;\n'
                  '\n'
                  'fn changed(old: &[&str], new: &[&str]) -> Vec<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", changed(&["a", "b", "c"], &["b", "c", "d"]));\n'
                 '    println!("{:?}", changed(&["x"], &["x"]));\n'
                 '}\n',
       'hint': 'symmetric_difference возвращает итератор.',
       'expected': ['["a", "d"]', '[]']}]}
