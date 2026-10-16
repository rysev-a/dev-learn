"""Задачи книги «Изучаем Rust»: глава 20 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {20: [{'id': 'r20-compose',
       'mode': 'rust',
       'title': 'Композиция функций',
       'statement': 'compose(f, g) → impl Fn(A) → C: возвращает функцию «сначала f, затем g». Работает для '
                    'любых типов: числа → строки → длины. Результат — замыкание, которое владеет обеими '
                    'функциями.',
       'starter': 'fn compose<A, B, C>(f: impl Fn(A) -> B, g: impl Fn(B) -> C) -> impl Fn(A) -> C {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let inc_then_double = compose(|x: i32| x + 1, |x: i32| x * 2);\n'
                 '    println!("{}", inc_then_double(4));\n'
                 '    let to_len = compose(|n: i32| n.to_string(), |s: String| s.len());\n'
                 '    println!("{} {}", to_len(12345), to_len(-7));\n'
                 '    let shout = compose(|s: &str| s.to_uppercase(), |s: String| s + "!");\n'
                 '    println!("{}", shout("привет"));\n'
                 '}\n',
       'hint': 'Верните move |x| g(f(x)): move нужен, чтобы замыкание забрало f и g — иначе оно переживёт '
               'их.',
       'expected': ['10', '5 2', 'ПРИВЕТ!']},
      {'id': 'r20-make-adder',
       'mode': 'rust',
       'title': 'Фабрики замыканий',
       'statement': 'make_adder(n) → impl Fn(i32) → i32 прибавляет n; make_counter() → impl FnMut() → u32 '
                    'при каждом вызове возвращает 1, 2, 3, …; make_accumulator(start) → impl FnMut(i32) → '
                    'i32 добавляет число к сумме и возвращает её.',
       'starter': 'fn make_adder(n: i32) -> impl Fn(i32) -> i32 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn make_counter() -> impl FnMut() -> u32 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn make_accumulator(start: i32) -> impl FnMut(i32) -> i32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let add5 = make_adder(5);\n'
                 '    println!("{} {}", add5(1), add5(-5));\n'
                 '    let mut c = make_counter();\n'
                 '    let mut d = make_counter();\n'
                 '    println!("{} {} {} {}", c(), c(), d(), c());\n'
                 '    let mut acc = make_accumulator(100);\n'
                 '    println!("{} {} {}", acc(1), acc(10), acc(-111));\n'
                 '}\n',
       'hint': 'Захваченную переменную замыкание держит внутри себя: каждое созданное замыкание — со своей '
               'копией счётчика.',
       'expected': ['6 0', '1 2 1 3', '101 111 0']},
      {'id': 'r20-apply-n',
       'mode': 'rust',
       'title': 'Функции высшего порядка',
       'statement': 'apply_n(f, n, x) — применить Fn(i32) → i32 к x ровно n раз. twice(f) → impl Fn(i32) → '
                    'i32 — «f дважды». iterate_until(f, x, limit) → Vec<i32> — значения x, f(x), f(f(x)), … '
                    'пока они меньше limit.',
       'starter': 'fn apply_n<F: Fn(i32) -> i32>(f: F, n: u32, x: i32) -> i32 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn twice(f: impl Fn(i32) -> i32) -> impl Fn(i32) -> i32 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn iterate_until(f: impl Fn(i32) -> i32, x: i32, limit: i32) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", apply_n(|x| x * 2, 10, 1));\n'
                 '    println!("{}", apply_n(|x| x + 3, 0, 7));\n'
                 '    let add10 = twice(|x| x + 5);\n'
                 '    println!("{} {}", add10(1), twice(twice(|x| x * 3))(1));\n'
                 '    println!("{:?}", iterate_until(|x| x * 2 + 1, 1, 100));\n'
                 '    println!("{:?}", iterate_until(|x| x + 1, 50, 10));\n'
                 '}\n',
       'hint': 'apply_n — свёртка по диапазону (0..n): fold(x, |acc, _| f(acc)).',
       'expected': ['1024', '7', '11 81', '[1, 3, 7, 15, 31, 63]', '[]']},
      {'id': 'r20-fix-move',
       'mode': 'rust',
       'title': 'Исправьте: замыкание переживёт функцию',
       'statement': 'make_greeter возвращает замыкание, которое здоровается по имени. Компилятор отвечает: '
                    'замыкание может пережить локальную переменную, на которую ссылается. Исправьте одним '
                    'словом.',
       'starter': 'fn make_greeter(name: String) -> impl Fn() -> String {\n'
                  '    || format!("Привет, {name}!")\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let g = make_greeter(String::from("Аня"));\n'
                 '    println!("{}", g());\n'
                 '    println!("{}", g());\n'
                 '    let h = make_greeter("Борис".to_string());\n'
                 '    println!("{}", h());\n'
                 '}\n',
       'hint': 'Слово move перед вертикальными чертами: name переедет в замыкание.',
       'expected': ['Привет, Аня!', 'Привет, Аня!', 'Привет, Борис!']},
      {'id': 'r20-fix-fnonce',
       'mode': 'rust',
       'title': 'Исправьте: замыкание вызывается один раз',
       'statement': 'run_once вызывает переданное замыкание единственный раз, но объявлено как F: Fn. '
                    'Замыкание из драйвера потребляет строку (FnOnce), и сборка падает. Исправьте '
                    'ограничение трейта.',
       'starter': 'fn run_once<F: Fn() -> String>(f: F) -> String {\n    f()\n}\n',
       'driver': 'fn main() {\n'
                 '    let s = String::from("уникальная строка");\n'
                 '    println!("{}", run_once(move || s));\n'
                 '    println!("{}", run_once(|| String::from("статическая")));\n'
                 '    let v = vec![1, 2, 3];\n'
                 '    println!("{}", run_once(move || format!("{:?}", v)));\n'
                 '}\n',
       'hint': 'FnOnce — самый слабый трейт: подходит и замыканию, которое отдаёт захваченное значение.',
       'expected': ['уникальная строка', 'статическая', '[1, 2, 3]']},
      {'id': 'r20-repeat-call',
       'mode': 'rust',
       'title': 'FnMut: повторять действие',
       'statement': 'repeat_call(n, f: impl FnMut()) вызывает f ровно n раз. times_table(n, f: impl '
                    'FnMut(u32, u32)) вызывает f(i, j) для всех 1 ≤ i ≤ j ≤ n в порядке (1,1), (1,2), …, '
                    '(2,2), …. Накопление результата выполняет замыкание вызывающего.',
       'starter': 'fn repeat_call(n: u32, mut f: impl FnMut()) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn times_table(n: u32, mut f: impl FnMut(u32, u32)) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut count = 0;\n'
                 '    repeat_call(5, || count += 2);\n'
                 '    println!("{}", count);\n'
                 '    let mut log = Vec::new();\n'
                 '    repeat_call(3, || log.push("tick"));\n'
                 '    println!("{:?}", log);\n'
                 '    let mut pairs = String::new();\n'
                 '    times_table(3, |i, j| pairs.push_str(&format!("{}x{}={} ", i, j, i * j)));\n'
                 '    println!("{}", pairs.trim_end());\n'
                 '    let mut sum = 0;\n'
                 '    times_table(10, |i, j| sum += i * j);\n'
                 '    println!("{}", sum);\n'
                 '}\n',
       'hint': 'Параметр f объявлен mut, чтобы его можно было вызывать: FnMut меняет своё состояние при '
               'каждом вызове.',
       'expected': ['10', '["tick", "tick", "tick"]', '1x1=1 1x2=2 1x3=3 2x2=4 2x3=6 3x3=9', '1705']},
      {'id': 'r20-sort-closures',
       'mode': 'rust',
       'title': 'Сортировка с замыканиями',
       'statement': 'sort_words(v: &mut Vec<String>) — по длине, при равенстве по алфавиту. sort_scores(v: '
                    '&mut Vec<(String, i32)>) — по убыванию очков, при равенстве по имени. sort_floats(v: '
                    '&mut Vec<f64>) — по возрастанию через partial_cmp (NaN нет).',
       'starter': 'fn sort_words(v: &mut Vec<String>) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn sort_scores(v: &mut Vec<(String, i32)>) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn sort_floats(v: &mut Vec<f64>) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut w: Vec<String> = ["pear", "fig", "apple", "kiwi", "date"].iter().map(|s| '
                 's.to_string()).collect();\n'
                 '    sort_words(&mut w);\n'
                 '    println!("{:?}", w);\n'
                 '    let mut s = vec![("bob".to_string(), 5), ("ann".to_string(), 9), ("cat".to_string(), '
                 '5)];\n'
                 '    sort_scores(&mut s);\n'
                 '    println!("{:?}", s);\n'
                 '    let mut f = vec![2.5, -1.0, 3.25, 0.0];\n'
                 '    sort_floats(&mut f);\n'
                 '    println!("{:?}", f);\n'
                 '}\n',
       'hint': 'Для вторичного порядка используйте .then_with(|| …) после первого cmp.',
       'expected': ['["fig", "date", "kiwi", "pear", "apple"]',
                    '[("ann", 9), ("bob", 5), ("cat", 5)]',
                    '[-1.0, 0.0, 2.5, 3.25]']},
      {'id': 'r20-keep-if',
       'mode': 'rust',
       'title': 'Обобщённый фильтр с замыканием',
       'statement': 'keep_if<T>(v: Vec<T>, pred: impl Fn(&T) → bool) → Vec<T> — оставить подходящие '
                    '(элементы переезжают, без клонирования). split_by<T>(v: Vec<T>, pred: impl Fn(&T) → '
                    'bool) → (Vec<T>, Vec<T>) — подходящие и остальные.',
       'starter': 'fn keep_if<T>(v: Vec<T>, pred: impl Fn(&T) -> bool) -> Vec<T> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn split_by<T>(v: Vec<T>, pred: impl Fn(&T) -> bool) -> (Vec<T>, Vec<T>) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                 '    println!("{:?}", keep_if(vec![1, 2, 3, 4, 5, 6], |x| x % 3 == 0));\n'
                 '    println!("{:?}", keep_if(vec!["a".to_string(), "bb".to_string(), "c".to_string()], |s| '
                 's.len() == 1));\n'
                 '    let (short, long) = split_by(vec!["tree", "a", "forest", "ox"], |s| s.len() <= 2);\n'
                 '    println!("{:?} {:?}", short, long);\n'
                 '    println!("clones: {}", bad0);\n'
                 '}\n',
       'hint': 'into_iter() забирает элементы; filter получает &&T, но pred(x) принимает &T — раст '
               'разыменует сам.',
       'expected': ['[3, 6]', '["a", "c"]', '["a", "ox"] ["tree", "forest"]', 'clones: 0']},
      {'id': 'r20-memo',
       'mode': 'rust',
       'title': 'Кеш вычислений: Memo<F>',
       'statement': 'Memo<F: Fn(u64) → u64> хранит функцию и HashMap результатов. new(f); get(&mut self, x) '
                    '→ u64 вызывает f только при первом запросе значения; hits() → u32 — сколько раз ответ '
                    'взят из кеша. Драйвер считает вызовы f сам.',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'struct Memo<F: Fn(u64) -> u64> {\n'
                  '    f: F,\n'
                  '    cache: HashMap<u64, u64>,\n'
                  '    hits: u32,\n'
                  '}\n'
                  '\n'
                  'impl<F: Fn(u64) -> u64> Memo<F> {\n'
                  '    fn new(f: F) -> Memo<F> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn get(&mut self, x: u64) -> u64 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn hits(&self) -> u32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'use std::cell::Cell;\n'
                 '\n'
                 'fn main() {\n'
                 '    let calls = Cell::new(0);\n'
                 '    let mut m = Memo::new(|x| {\n'
                 '        calls.set(calls.get() + 1);\n'
                 '        x * x\n'
                 '    });\n'
                 '    println!("{} {} {}", m.get(4), m.get(4), m.get(5));\n'
                 '    println!("{} {}", m.get(4), m.get(5));\n'
                 '    println!("calls={} hits={}", calls.get(), m.hits());\n'
                 '}\n',
       'hint': 'Вызов поля-замыкания пишут в скобках: (self.f)(x), иначе раст ищет метод f.',
       'expected': ['16 16 25', '16 25', 'calls=2 hits=3']},
      {'id': 'r20-lazy-calls',
       'mode': 'rust',
       'title': 'Ленивость: считаем вызовы',
       'statement': 'lazy_calls() → (usize, usize): создайте итератор (0..100).map(g), где g увеличивает '
                    'внешний счётчик и возвращает число × 2. Верните число вызовов g, когда итератор только '
                    'построен (ничего не запрошено), и после take(3).collect().',
       'starter': 'use std::cell::Cell;\n'
                  '\n'
                  'fn lazy_calls() -> (usize, usize) {\n'
                  '    let calls = Cell::new(0usize);\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n    println!("{:?}", lazy_calls());\n}\n',
       'hint': 'Cell позволяет менять значение через общую ссылку: calls.set(calls.get() + 1) внутри '
               'замыкания.',
       'expected': ['(0, 3)']},
      {'id': 'r20-scan-windows',
       'mode': 'rust',
       'title': 'Нарастающие суммы и разности',
       'statement': 'prefix_sums(v) → Vec<i32> — нарастающие суммы (scan). diffs(v) → Vec<i32> — разности '
                    'соседних (windows(2)). running_max(v) → Vec<i32> — максимум на каждом префиксе. '
                    'is_sorted_asc(v) → bool — через windows.',
       'starter': 'fn prefix_sums(v: &[i32]) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn diffs(v: &[i32]) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn running_max(v: &[i32]) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn is_sorted_asc(v: &[i32]) -> bool {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!("fo", "r ")).count();\n'
                 '    println!("{:?}", prefix_sums(&[1, 2, 3, 4]));\n'
                 '    println!("{:?}", diffs(&[1, 4, 9, 16]));\n'
                 '    println!("{:?}", running_max(&[3, 1, 4, 1, 5, 2]));\n'
                 '    println!("{} {} {}", is_sorted_asc(&[1, 2, 2, 5]), is_sorted_asc(&[1, 0]), '
                 'is_sorted_asc(&[]));\n'
                 '    println!("{:?} {:?}", prefix_sums(&[]), diffs(&[7]));\n'
                 '    println!("loops: {}", bad0);\n'
                 '}\n',
       'hint': 'scan(начальное_состояние, |состояние, &x| { …; Some(значение) }); windows(2) даёт срезы по '
               'два соседних элемента.',
       'expected': ['[1, 3, 6, 10]',
                    '[3, 5, 7]',
                    '[3, 3, 4, 4, 5, 5]',
                    'true false true',
                    '[] []',
                    'loops: 0']},
      {'id': 'r20-flat-map',
       'mode': 'rust',
       'title': 'flat_map: раскрыть вложенное',
       'statement': 'all_chars(words) → String — все символы слов подряд. pairs(n) → Vec<(i32, i32)> — все '
                    'пары (i, j) с 1 ≤ i < j ≤ n в лексикографическом порядке. unique_letters(words) → '
                    'String — все различные буквы в алфавитном порядке.',
       'starter': 'fn all_chars(words: &[&str]) -> String {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn pairs(n: i32) -> Vec<(i32, i32)> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn unique_letters(words: &[&str]) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", all_chars(&["ab", "", "cde"]));\n'
                 '    println!("{:?}", pairs(4));\n'
                 '    println!("{:?}", pairs(1));\n'
                 '    println!("{}", unique_letters(&["banana", "bandana"]));\n'
                 '    println!("{}", unique_letters(&[]).len());\n'
                 '}\n',
       'hint': 'Во внутреннем замыкании move |j| (i, j) забирает i; без move i останется ссылкой на внешнюю '
               'переменную.',
       'expected': ['abcde', '[(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]', '[]', 'abdn', '0']},
      {'id': 'r20-zip-dot',
       'mode': 'rust',
       'title': 'zip: скалярное произведение и пары',
       'statement': 'dot(a, b) → i64 — скалярное произведение (до длины короче). pairwise_max(a, b) → '
                    'Vec<i32> — максимум в каждой позиции. unzip_sum(pairs) → (i32, i32) — суммы первых и '
                    'вторых элементов (unzip).',
       'starter': 'fn dot(a: &[i32], b: &[i32]) -> i64 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn pairwise_max(a: &[i32], b: &[i32]) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn unzip_sum(pairs: &[(i32, i32)]) -> (i32, i32) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{} {}", dot(&[1, 2, 3], &[4, 5, 6]), dot(&[1, 2], &[10]));\n'
                 '    println!("{}", dot(&[i32::MAX, i32::MAX], &[2, 2]));\n'
                 '    println!("{:?}", pairwise_max(&[1, 9, 3], &[4, 2, 8, 100]));\n'
                 '    println!("{:?}", unzip_sum(&[(1, 10), (2, 20), (3, 30)]));\n'
                 '    println!("{:?}", unzip_sum(&[]));\n'
                 '}\n',
       'hint': 'zip остановится на более коротком; произведение считайте в i64, чтобы не переполнить i32.',
       'expected': ['32 10', '8589934588', '[4, 9, 8]', '(6, 60)', '(0, 0)']},
      {'id': 'r20-chunks-windows',
       'mode': 'rust',
       'title': 'chunks и windows',
       'statement': 'chunk_sums(v, k) → Vec<i32> — суммы подряд идущих кусков по k (последний может быть '
                    'короче). moving_average(v, k) → Vec<f64> — среднее каждого окна из k элементов. '
                    'peaks(v) → Vec<usize> — индексы пиков: элементов строго больше обоих соседей.',
       'starter': 'fn chunk_sums(v: &[i32], k: usize) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn moving_average(v: &[i32], k: usize) -> Vec<f64> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn peaks(v: &[i32]) -> Vec<usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", chunk_sums(&[1, 2, 3, 4, 5, 6, 7], 3));\n'
                 '    println!("{:?}", moving_average(&[1, 2, 3, 4, 5], 2));\n'
                 '    println!("{:?}", moving_average(&[10, 20], 3));\n'
                 '    println!("{:?}", peaks(&[1, 3, 2, 5, 5, 4, 6, 1]));\n'
                 '    println!("{:?}", peaks(&[1, 2]));\n'
                 '}\n',
       'hint': 'У windows(3) индекс пика на единицу больше номера окна: .map(|(i, _)| i + 1).',
       'expected': ['[6, 15, 7]', '[1.5, 2.5, 3.5, 4.5]', '[]', '[1, 6]', '[]']},
      {'id': 'r20-partition-runs',
       'mode': 'rust',
       'title': 'Разбиения и серии',
       'statement': 'partition_parity(v) → (Vec<i32>, Vec<i32>) — чётные и нечётные. run_lengths(v) → '
                    'Vec<(i32, usize)> — серии одинаковых подряд идущих значений. split_runs(v) → '
                    'Vec<Vec<i32>> — те же серии как подмассивы.',
       'starter': 'fn partition_parity(v: &[i32]) -> (Vec<i32>, Vec<i32>) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn run_lengths(v: &[i32]) -> Vec<(i32, usize)> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn split_runs(v: &[i32]) -> Vec<Vec<i32>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", partition_parity(&[1, 2, 3, 4, 5, 6]));\n'
                 '    println!("{:?}", run_lengths(&[1, 1, 2, 2, 2, 1, 3]));\n'
                 '    println!("{:?}", split_runs(&[5, 5, 7, 5]));\n'
                 '    println!("{:?} {:?}", run_lengths(&[]), split_runs(&[]));\n'
                 '}\n',
       'hint': 'В fold накопитель — вектор пар; последнюю пару можно изменить через last_mut().',
       'expected': ['([2, 4, 6], [1, 3, 5])',
                    '[(1, 2), (2, 3), (1, 1), (3, 1)]',
                    '[[5, 5], [7], [5]]',
                    '[] []']},
      {'id': 'r20-find-any',
       'mode': 'rust',
       'title': 'Поиск: any, all, find, position',
       'statement': 'all_distinct(v) → bool; first_negative_index(v) → Option<usize>; first_number(words: '
                    '&[&str]) → Option<i64> — первое слово, которое парсится как число (find_map); '
                    'position_of_max(v) → Option<usize> — индекс первого максимума.',
       'starter': 'fn all_distinct(v: &[i32]) -> bool {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn first_negative_index(v: &[i32]) -> Option<usize> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn first_number(words: &[&str]) -> Option<i64> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn position_of_max(v: &[i32]) -> Option<usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{} {} {}", all_distinct(&[3, 1, 2]), all_distinct(&[1, 2, 1]), '
                 'all_distinct(&[]));\n'
                 '    println!("{:?} {:?}", first_negative_index(&[4, 0, -2, -5]), first_negative_index(&[1, '
                 '2]));\n'
                 '    println!("{:?} {:?}", first_number(&["abc", "x1", "42", "7"]), first_number(&["a", '
                 '"b"]));\n'
                 '    println!("{:?} {:?}", position_of_max(&[2, 9, 1, 9]), position_of_max(&[]));\n'
                 '}\n',
       'hint': 'find_map объединяет поиск и преобразование: возвращает первое Some.',
       'expected': ['true false true', 'Some(2) None', 'Some(42) None', 'Some(1) None']},
      {'id': 'r20-min-max-by',
       'mode': 'rust',
       'title': 'min_by, max_by_key, partial_cmp',
       'statement': 'longest_word(words) → Option<&str> — первое самое длинное. closest_to(v: &[f64], '
                    'target) → Option<f64> — ближайшее к target значение (при равенстве — первое). '
                    'youngest(people: &[(&str, u32)]) → Option<&str> — имя самого молодого (первого).',
       'starter': "fn longest_word<'a>(words: &[&'a str]) -> Option<&'a str> {\n"
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn closest_to(v: &[f64], target: f64) -> Option<f64> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  "fn youngest<'a>(people: &[(&'a str, u32)]) -> Option<&'a str> {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", longest_word(&["aa", "bbb", "ccc", "d"]));\n'
                 '    println!("{:?}", longest_word(&[]));\n'
                 '    println!("{:?} {:?}", closest_to(&[1.0, 4.5, 3.9, 10.0], 4.0), closest_to(&[], 1.0));\n'
                 '    println!("{:?}", closest_to(&[2.0, 4.0], 3.0));\n'
                 '    println!("{:?}", youngest(&[("ann", 31), ("bob", 22), ("cat", 22)]));\n'
                 '}\n',
       'hint': 'max_by_key при равенстве возвращает ПОСЛЕДНИЙ, min_by_key — первый: для «первого самого '
               'длинного» удобнее fold.',
       'expected': ['Some("bbb")', 'None', 'Some(3.9) None', 'Some(2.0)', 'Some("bob")']},
      {'id': 'r20-fold-counts',
       'mode': 'rust',
       'title': 'fold: частоты и гистограмма',
       'statement': 'char_counts(s) → BTreeMap<char, usize> — сколько раз встречается каждый символ (через '
                    'fold). length_histogram(words) → Vec<usize> — количество слов каждой длины, начиная с '
                    'длины 1 до максимальной (пропущенные длины — нули).',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn char_counts(s: &str) -> BTreeMap<char, usize> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn length_histogram(words: &[&str]) -> Vec<usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", char_counts("hello"));\n'
                 '    println!("{:?}", char_counts("привет мир"));\n'
                 '    println!("{:?}", char_counts(""));\n'
                 '    println!("{:?}", length_histogram(&["a", "bb", "cc", "dddd", "e"]));\n'
                 '    println!("{:?}", length_histogram(&[]));\n'
                 '}\n',
       'hint': 'fold(начальный_контейнер, |mut acc, x| { …; acc }): накопитель объявляется mut и '
               'возвращается в конце.',
       'expected': ["{'e': 1, 'h': 1, 'l': 2, 'o': 1}",
                    "{' ': 1, 'в': 1, 'е': 1, 'и': 2, 'м': 1, 'п': 1, 'р': 2, 'т': 1}",
                    '{}',
                    '[2, 2, 0, 1]',
                    '[]']},
      {'id': 'r20-collect-result',
       'mode': 'rust',
       'title': 'collect в Option и Result',
       'statement': 'parse_list(s) → Result<Vec<i32>, ParseIntError> — числа из «1,2,3» (первая ошибка '
                    'прерывает). all_some(v: &[Option<i32>]) → Option<Vec<i32>> — Some, только если все '
                    'Some. sum_ok(items: &[&str]) → i32 — сумма разобравшихся чисел, остальные пропускаются.',
       'starter': 'use std::num::ParseIntError;\n'
                  '\n'
                  'fn parse_list(s: &str) -> Result<Vec<i32>, ParseIntError> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn all_some(v: &[Option<i32>]) -> Option<Vec<i32>> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn sum_ok(items: &[&str]) -> i32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", parse_list("1, 2,3"));\n'
                 '    println!("{:?}", parse_list("1,x,3"));\n'
                 '    println!("{:?}", parse_list(""));\n'
                 '    println!("{:?}", all_some(&[Some(1), Some(2)]));\n'
                 '    println!("{:?}", all_some(&[Some(1), None]));\n'
                 '    println!("{} {}", sum_ok(&["1", "x", "20"]), sum_ok(&[]));\n'
                 '}\n',
       'hint': 'collect() умеет собирать Result<Vec<_>, _> и Option<Vec<_>> — остановится на первой неудаче.',
       'expected': ['Ok([1, 2, 3])',
                    'Err(ParseIntError { kind: InvalidDigit })',
                    'Err(ParseIntError { kind: Empty })',
                    'Some([1, 2])',
                    'None',
                    '21 0']},
      {'id': 'r20-collect-maps',
       'mode': 'rust',
       'title': 'collect в String и HashMap',
       'statement': 'acronym(s) → String — первые буквы слов заглавными. index_by_len(words) → '
                    'BTreeMap<usize, Vec<&str>> — слова по длине (в порядке появления). to_lookup(pairs: '
                    '&[(&str, i32)]) → HashMap<&str, i32> — при повторах побеждает последнее значение.',
       'starter': 'use std::collections::{BTreeMap, HashMap};\n'
                  '\n'
                  'fn acronym(s: &str) -> String {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  "fn index_by_len<'a>(words: &[&'a str]) -> BTreeMap<usize, Vec<&'a str>> {\n"
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  "fn to_lookup<'a>(pairs: &[(&'a str, i32)]) -> HashMap<&'a str, i32> {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", acronym("portable network graphics"));\n'
                 '    println!("{} {:?}", acronym("  по  умолчанию "), acronym(""));\n'
                 '    println!("{:?}", index_by_len(&["a", "bb", "c", "dd", "eee"]));\n'
                 '    let m = to_lookup(&[("x", 1), ("y", 2), ("x", 3)]);\n'
                 '    let mut items: Vec<_> = m.iter().collect();\n'
                 '    items.sort();\n'
                 '    println!("{:?}", items);\n'
                 '}\n',
       'hint': 'Итератор пар (K, V) собирается в HashMap, а позже пара с тем же ключом затирает прежнюю.',
       'expected': ['PNG', 'ПУ ""', '{1: ["a", "c"], 2: ["bb", "dd"], 3: ["eee"]}', '[("x", 3), ("y", 2)]']},
      {'id': 'r20-peekable-tokens',
       'mode': 'rust',
       'title': 'peekable: разбор выражения на токены',
       'statement': "Token — Num(i64) или Op(char) (+ - * /, скобки '(' и ')' тоже Op). tokenize(s) → "
                    'Result<Vec<Token>, String>: числа из нескольких цифр, пробелы пропускаются; '
                    'недопустимый символ → Err("bad char X"). Используйте peekable, чтобы дочитать число до '
                    'конца.',
       'starter': '#[derive(Debug, PartialEq)]\n'
                  'enum Token {\n'
                  '    Num(i64),\n'
                  '    Op(char),\n'
                  '}\n'
                  '\n'
                  'fn tokenize(s: &str) -> Result<Vec<Token>, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", tokenize("12 + 3*(40-5)"));\n'
                 '    println!("{:?}", tokenize(""));\n'
                 '    println!("{:?}", tokenize("7 $ 3"));\n'
                 '    println!("{:?}", tokenize("007"));\n'
                 '}\n',
       'hint': 'peek() не забирает символ: пока следующий — цифра, копите число и вызывайте next().',
       'expected': ["Ok([Num(12), Op('+'), Num(3), Op('*'), Op('('), Num(40), Op('-'), Num(5), Op(')')])",
                    'Ok([])',
                    'Err("bad char $")',
                    'Ok([Num(7)])']},
      {'id': 'r20-rle',
       'mode': 'rust',
       'title': 'Кодирование серий (RLE)',
       'statement': 'rle(s) → String: «aaabcc» → «a3b1c2» (символ и длина серии). unrle(s) → Option<String> '
                    '— обратное преобразование; None, если формат неверен (после символа нет цифр). Серии '
                    'могут быть длиннее 9: «x12».',
       'starter': 'fn rle(s: &str) -> String {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn unrle(s: &str) -> Option<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", rle("aaabcc"));\n'
                 '    println!("{:?}", rle(""));\n'
                 '    println!("{}", rle("ppppppppppppq"));\n'
                 '    println!("{:?}", unrle("a3b1c2"));\n'
                 '    println!("{:?}", unrle("x12"));\n'
                 '    println!("{:?} {:?}", unrle("ab"), unrle("3a"));\n'
                 '    println!("{}", unrle(&rle("привет миииир")).unwrap());\n'
                 '}\n',
       'hint': 'В rle после символа продолжайте читать, пока peek() равен тому же символу; в unrle длину '
               'читайте цифрами.',
       'expected': ['a3b1c2',
                    '""',
                    'p12q1',
                    'Some("aaabcc")',
                    'Some("xxxxxxxxxxxx")',
                    'None None',
                    'привет миииир']},
      {'id': 'r20-successors',
       'mode': 'rust',
       'title': 'successors: ряды по правилу',
       'statement': 'collatz(n) → Vec<u64> — последовательность Коллатца от n до 1 включительно (чётное /2, '
                    'нечётное 3n+1). powers_of_two_below(limit) → Vec<u64> — 1, 2, 4, … меньше limit. '
                    'digits(n: u64) → Vec<u8> — цифры числа слева направо (через successors и деление на '
                    '10).',
       'starter': 'fn collatz(n: u64) -> Vec<u64> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn powers_of_two_below(limit: u64) -> Vec<u64> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn digits(n: u64) -> Vec<u8> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", collatz(6));\n'
                 '    println!("{:?}", collatz(1));\n'
                 '    println!("{}", collatz(27).len());\n'
                 '    println!("{:?}", powers_of_two_below(100));\n'
                 '    println!("{}", powers_of_two_below(u64::MAX).len());\n'
                 '    println!("{:?} {:?}", digits(9071), digits(0));\n'
                 '}\n',
       'hint': 'successors(Some(начало), |&x| правило) — когда правило вернёт None, ряд заканчивается.',
       'expected': ['[6, 3, 10, 5, 16, 8, 4, 2, 1]',
                    '[1]',
                    '112',
                    '[1, 2, 4, 8, 16, 32, 64]',
                    '64',
                    '[9, 0, 7, 1] [0]']},
      {'id': 'r20-from-fn',
       'mode': 'rust',
       'title': 'from_fn, repeat и cycle',
       'statement': 'fibs(n) → Vec<u64> — первые n чисел Фибоначчи (std::iter::from_fn с состоянием). '
                    'round_robin(items, n) → Vec<String> — n элементов по кругу (cycle().take). every_kth(v, '
                    'k) → Vec<i32> — элементы с индексами 0, k, 2k, … (step_by).',
       'starter': 'fn fibs(n: usize) -> Vec<u64> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn round_robin(items: &[&str], n: usize) -> Vec<String> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn every_kth(v: &[i32], k: usize) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", fibs(10));\n'
                 '    println!("{:?}", fibs(0));\n'
                 '    println!("{:?}", round_robin(&["a", "b", "c"], 7));\n'
                 '    println!("{:?}", round_robin(&[], 3));\n'
                 '    println!("{:?}", every_kth(&[1, 2, 3, 4, 5, 6, 7], 3));\n'
                 '}\n',
       'hint': 'В from_fn состояние держит замыкание: объявите его снаружи и перенесите внутрь через move.',
       'expected': ['[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]',
                    '[]',
                    '["a", "b", "c", "a", "b", "c", "a"]',
                    '[]',
                    '[1, 4, 7]']},
      {'id': 'r20-between-markers',
       'mode': 'rust',
       'title': 'skip_while и take_while',
       'statement': 'between(lines: &[&str], start: &str, end: &str) → Vec<&str> — строки между первой '
                    'строкой start и следующей за ней end (сами маркеры не входят; если start нет — пусто; '
                    'если end нет — до конца). last_n<T: Clone>(v: &[T], n) → Vec<T> — последние n элементов '
                    'в исходном порядке (через rev и take).',
       'starter': "fn between<'a>(lines: &[&'a str], start: &str, end: &str) -> Vec<&'a str> {\n"
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn last_n<T: Clone>(v: &[T], n: usize) -> Vec<T> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let log = ["x", "BEGIN", "a", "b", "END", "c", "BEGIN"];\n'
                 '    println!("{:?}", between(&log, "BEGIN", "END"));\n'
                 '    println!("{:?}", between(&log, "NONE", "END"));\n'
                 '    println!("{:?}", between(&["BEGIN", "q"], "BEGIN", "END"));\n'
                 '    println!("{:?} {:?}", last_n(&[1, 2, 3, 4, 5], 2), last_n(&[1, 2], 5));\n'
                 '    println!("{:?}", last_n::<i32>(&[], 3));\n'
                 '}\n',
       'hint': 'skip_while пропускает до маркера включительно не пропуская его самого — поэтому после него '
               'нужен skip(1).',
       'expected': ['["a", "b"]', '[]', '["q"]', '[4, 5] [1, 2]', '[]']},
      {'id': 'r20-event-bus',
       'mode': 'rust',
       'title': 'Обработчики: Vec<Box<dyn FnMut>>',
       'statement': 'Bus хранит обработчики Box<dyn FnMut(&str) → String>. on(&mut self, h) добавляет '
                    'обработчик; emit(&mut self, event: &str) → Vec<String> вызывает все по порядку и '
                    'собирает их ответы. Обработчики могут иметь своё изменяемое состояние (счётчик, '
                    'накопитель).',
       'starter': 'struct Bus {\n'
                  '    handlers: Vec<Box<dyn FnMut(&str) -> String>>,\n'
                  '}\n'
                  '\n'
                  'impl Bus {\n'
                  '    fn new() -> Bus {\n'
                  '        todo!()\n'
                  '    }\n'
                  "    fn on(&mut self, h: impl FnMut(&str) -> String + 'static) {\n"
                  '        todo!()\n'
                  '    }\n'
                  '    fn emit(&mut self, event: &str) -> Vec<String> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut bus = Bus::new();\n'
                 '    let mut n = 0;\n'
                 '    bus.on(move |e| {\n'
                 '        n += 1;\n'
                 '        format!("#{n} {e}")\n'
                 '    });\n'
                 '    bus.on(|e| e.to_uppercase());\n'
                 '    let mut seen: Vec<String> = Vec::new();\n'
                 '    bus.on(move |e| {\n'
                 '        seen.push(e.to_string());\n'
                 '        seen.join("+")\n'
                 '    });\n'
                 '    println!("{:?}", bus.emit("start"));\n'
                 '    println!("{:?}", bus.emit("stop"));\n'
                 '    println!("{:?}", Bus::new().emit("nobody"));\n'
                 '}\n',
       'hint': 'Box::new(h) превращает замыкание в Box<dyn FnMut>; вызывать через iter_mut(), потому что '
               'состояние меняется.',
       'expected': ['["#1 start", "START", "start"]', '["#2 stop", "STOP", "start+stop"]', '[]']},
      {'id': 'r20-fn-table',
       'mode': 'rust',
       'title': 'Таблица функций: fn-указатели',
       'statement': 'apply_all(fs: &[fn(f64) → f64], x) → Vec<f64> — результаты всех функций. op_for(name: '
                    '&str) → Option<fn(f64, f64) → f64> — «add», «sub», «mul», «div» (деление обычное, a / '
                    'b), иначе None. calc(expr: &str) → Option<f64>: «3 add 4» → 7 (число, имя операции, '
                    'число); любая ошибка формата → None.',
       'starter': 'fn apply_all(fs: &[fn(f64) -> f64], x: f64) -> Vec<f64> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn op_for(name: &str) -> Option<fn(f64, f64) -> f64> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn calc(expr: &str) -> Option<f64> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let fs: [fn(f64) -> f64; 3] = [f64::sqrt, f64::abs, |x| x * 10.0];\n'
                 '    println!("{:?}", apply_all(&fs, 16.0));\n'
                 '    println!("{:?}", apply_all(&[], 1.0));\n'
                 '    println!("{:?} {:?}", calc("3 add 4"), calc("10 div 4"));\n'
                 '    println!("{:?} {:?} {:?}", calc("2 pow 3"), calc("x add 1"), calc("1 add"));\n'
                 '    println!("{}", std::mem::size_of::<fn(f64) -> f64>());\n'
                 '}\n',
       'hint': 'Указатель fn получается из имени функции: Some(add); замыкание без захвата тоже приводится к '
               'fn.',
       'expected': ['[4.0, 16.0, 160.0]', '[]', 'Some(7.0) Some(2.5)', 'None None None', '8']},
      {'id': 'r20-boxed-predicates',
       'mode': 'rust',
       'title': 'Комбинаторы предикатов: Box<dyn Fn>',
       'statement': 'in_range(lo, hi) → Box<dyn Fn(i32) → bool>; not(p) → Box<dyn Fn(i32) → bool>; '
                    'all_of(ps: Vec<Box<dyn Fn(i32) → bool>>) → Box<dyn Fn(i32) → bool> — истина, если все '
                    'предикаты истинны; any_of — если хотя бы один. Замыкания владеют захваченными '
                    'значениями.',
       'starter': 'fn in_range(lo: i32, hi: i32) -> Box<dyn Fn(i32) -> bool> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn not(p: Box<dyn Fn(i32) -> bool>) -> Box<dyn Fn(i32) -> bool> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn all_of(ps: Vec<Box<dyn Fn(i32) -> bool>>) -> Box<dyn Fn(i32) -> bool> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn any_of(ps: Vec<Box<dyn Fn(i32) -> bool>>) -> Box<dyn Fn(i32) -> bool> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let teen = in_range(13, 19);\n'
                 '    println!("{} {}", teen(15), teen(20));\n'
                 '    let not_teen = not(in_range(13, 19));\n'
                 '    println!("{} {}", not_teen(15), not_teen(20));\n'
                 '    let both = all_of(vec![in_range(0, 100), not(in_range(40, 60))]);\n'
                 '    println!("{} {} {}", both(10), both(50), both(200));\n'
                 '    let either = any_of(vec![in_range(0, 5), in_range(100, 105)]);\n'
                 '    println!("{} {} {}", either(3), either(50), either(101));\n'
                 '    println!("{} {}", all_of(vec![])(1), any_of(vec![])(1));\n'
                 '}\n',
       'hint': 'Каждый комбинатор возвращает Box::new(move |x| …): move забирает предикаты внутрь замыкания.',
       'expected': ['true false', 'false true', 'true false false', 'true false true', 'true false']},
      {'id': 'r20-log-summary',
       'mode': 'rust',
       'title': 'Конвейер без циклов: сводка журнала',
       'statement': 'summarize(log: &str) → Vec<(String, usize)>: строки вида «LEVEL текст», пустые и без '
                    'пробела пропускаются; результат — уровни с числом строк, по убыванию числа, при '
                    'равенстве по алфавиту. Слово for в коде использовать нельзя — только адаптеры и '
                    'потребители.',
       'starter': 'fn summarize(log: &str) -> Vec<(String, usize)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!("fo", "r ")).count();\n'
                 '    let log = "INFO started\\nWARN disk 91%\\n\\nINFO ready\\nERROR boom\\nbare\\nINFO '
                 'x\\nWARN y";\n'
                 '    println!("{:?}", summarize(log));\n'
                 '    println!("{:?}", summarize(""));\n'
                 '    println!("loops: {}", bad0);\n'
                 '}\n',
       'hint': 'lines().filter_map(...) отбросит строки без пробела; подсчёт — fold с HashMap, затем '
               'сортировка.',
       'expected': ['[("INFO", 3), ("WARN", 2), ("ERROR", 1)]', '[]', 'loops: 0']},
      {'id': 'r20-closure-sizes',
       'mode': 'rust',
       'title': 'Размер замыкания = размер захваченного',
       'statement': 'closure_sizes() → [usize; 4]: создайте четыре замыкания и верните size_of_val каждого: '
                    '(1) ничего не захватывает; (2) move || n + 1 с захватом i32 n; (3) || s.len() — без '
                    'move, берёт ссылку на String s; (4) move-замыкание, владеющее клоном строки s. '
                    'Замыкание — это структура с захваченными значениями.',
       'starter': 'fn closure_sizes() -> [usize; 4] {\n'
                  '    let n = 7i32;\n'
                  '    let s = String::from("hi");\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n    println!("{:?}", closure_sizes());\n}\n',
       'hint': 'size_of_val(&замыкание); ссылка занимает 8 байт, String — 24, i32 — 4, пустое замыкание — 0.',
       'expected': ['[0, 4, 8, 24]']}]}
