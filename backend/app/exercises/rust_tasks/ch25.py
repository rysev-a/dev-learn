"""Задачи книги «Изучаем Rust»: глава 25 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {25: [{'id': 'r25-swap-remove',
       'mode': 'rust',
       'title': 'swap_remove',
       'statement': 'Напишите remove_all_even(v: &mut Vec<i32>): удалить все чётные числа за линейное время '
                    'без сохранения порядка, с помощью swap_remove. (Проверка — по сумме и количеству '
                    'оставшихся.)',
       'starter': 'fn remove_all_even(v: &mut Vec<i32>) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v: Vec<i32> = (1..=10).collect();\n'
                 '    remove_all_even(&mut v);\n'
                 '    v.sort();\n'
                 '    println!("{:?}", v);\n'
                 '    let mut big: Vec<i32> = (0..400000).collect();\n'
                 '    remove_all_even(&mut big);\n'
                 '    println!("{} {}", big.len(), big.iter().map(|&x| x as i64).sum::<i64>());\n'
                 '}\n',
       'hint': 'Не увеличивайте i после swap_remove — на месте уже новый элемент.',
       'expected': ['[1, 3, 5, 7, 9]', '200000 40000000000']},
      {'id': 'r25-split-off',
       'mode': 'rust',
       'title': 'split_off',
       'statement': 'Напишите split_at_value(v: &mut Vec<i32>, x: i32) -> Vec<i32>: отрежьте от v хвост '
                    'начиная с первого элемента, равного x (если x нет — вернуть пустой вектор), и верните '
                    'его.',
       'starter': 'fn split_at_value(v: &mut Vec<i32>, x: i32) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![1, 2, 3, 4, 5];\n'
                 '    let t = split_at_value(&mut v, 3);\n'
                 '    println!("{:?} {:?}", v, t);\n'
                 '    let t2 = split_at_value(&mut v, 9);\n'
                 '    println!("{:?} {:?}", v, t2);\n'
                 '}\n',
       'hint': 'v.split_off(i) оставляет в v первые i элементов.',
       'expected': ['[1, 2] [3, 4, 5]', '[1, 2] []']},
      {'id': 'r25-dedup-by-key',
       'mode': 'rust',
       'title': 'dedup_by_key',
       'statement': 'Напишите unique_by_len(words: &mut Vec<String>): оставить только первое слово из каждой '
                    'подряд идущей группы слов одной длины в символах (dedup_by_key).',
       'starter': 'fn unique_by_len(words: &mut Vec<String>) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut w: Vec<String> = ["aa", "bb", "ccc", "d", "e", "ff"].iter().map(|s| '
                 's.to_string()).collect();\n'
                 '    unique_by_len(&mut w);\n'
                 '    println!("{:?}", w);\n'
                 '}\n',
       'hint': 'dedup_by_key убирает соседние элементы с одинаковым ключом.',
       'expected': ['["aa", "ccc", "d", "ff"]']},
      {'id': 'r25-drain-filter',
       'mode': 'rust',
       'title': 'Вынуть по условию',
       'statement': 'Напишите take_evens(v: &mut Vec<i32>) -> Vec<i32>: вернуть все чётные (в исходном '
                    'порядке) и удалить их из v. Используйте retain и накопление в отдельный вектор.',
       'starter': 'fn take_evens(v: &mut Vec<i32>) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![1, 2, 3, 4, 5, 6];\n'
                 '    let e = take_evens(&mut v);\n'
                 '    println!("{:?} {:?}", e, v);\n'
                 '}\n',
       'hint': 'retain вызывает замыкание по порядку — в нём можно копить.',
       'expected': ['[2, 4, 6] [1, 3, 5]']},
      {'id': 'r25-rotate',
       'mode': 'rust',
       'title': 'Поворот среза',
       'statement': 'Напишите rotate(v: &mut [i32], k: usize): циклический сдвиг вправо на k позиций на '
                    'месте (rotate_right, k может быть больше длины).',
       'starter': 'fn rotate(v: &mut [i32], k: usize) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = [1, 2, 3, 4, 5];\n'
                 '    rotate(&mut v, 2);\n'
                 '    println!("{:?}", v);\n'
                 '    rotate(&mut v, 12);\n'
                 '    println!("{:?}", v);\n'
                 '    let mut e: [i32; 0] = [];\n'
                 '    rotate(&mut e, 3);\n'
                 '}\n',
       'hint': 'rotate_right паникует при k > len, поэтому берите k % len.',
       'expected': ['[4, 5, 1, 2, 3]', '[2, 3, 4, 5, 1]']},
      {'id': 'r25-windows-max',
       'mode': 'rust',
       'title': 'Максимум в окне',
       'statement': 'Напишите window_max(v: &[i32], k: usize) -> Vec<i32>: максимум в каждом окне из k '
                    'подряд идущих элементов (k > 0; если k > len — пустой). За линейное время (VecDeque '
                    'хранит индексы кандидатов), на 200000 элементов.',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn window_max(v: &[i32], k: usize) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", window_max(&[1, 3, -1, -3, 5, 3, 6, 7], 3));\n'
                 '    println!("{:?}", window_max(&[4], 1));\n'
                 '    println!("{:?}", window_max(&[1, 2], 5));\n'
                 '    let big: Vec<i32> = (0..200000i64).map(|x| ((x * 7919) % 10007) as i32).collect();\n'
                 '    let r = window_max(&big, 1000);\n'
                 '    println!("{} {}", r.len(), r.iter().map(|&x| x as i64).sum::<i64>());\n'
                 '}\n',
       'hint': 'Очередь убывающих значений: хвост выбрасываем, если он не больше нового.',
       'expected': ['[3, 3, 5, 5, 6, 7]', '[4]', '[]', '199001 1990276864']},
      {'id': 'r25-josephus-deque',
       'mode': 'rust',
       'title': 'Считалка на колоде',
       'statement': 'Напишите last_standing(names: &[&str], k: usize) -> String: по кругу выбывает каждый '
                    'k-й, вернуть имя последнего. Используйте VecDeque и rotate_left.',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn last_standing(names: &[&str], k: usize) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", last_standing(&["А", "Б", "В", "Г", "Д"], 2));\n'
                 '    println!("{}", last_standing(&["Один"], 7));\n'
                 '    println!("{}", last_standing(&["А", "Б", "В"], 3));\n'
                 '}\n',
       'hint': 'q.rotate_left(k - 1), затем pop_front.',
       'expected': ['В', 'Один', 'Б']},
      {'id': 'r25-round-robin',
       'mode': 'rust',
       'title': 'Круговой планировщик',
       'statement': 'Напишите round_robin(tasks: &[(&str, u32)], quantum: u32) -> Vec<String>: каждой задаче '
                    'по очереди выделяют quantum единиц; порядок завершения (имена) вернуть списком. '
                    'VecDeque.',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn round_robin(tasks: &[(&str, u32)], quantum: u32) -> Vec<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", round_robin(&[("a", 5), ("b", 2), ("c", 7)], 3));\n'
                 '    println!("{:?}", round_robin(&[], 3));\n'
                 '}\n',
       'hint': 'Не закончила — в конец очереди с остатком.',
       'expected': ['["b", "a", "c"]', '[]']},
      {'id': 'r25-hash-two-sets',
       'mode': 'rust',
       'title': 'Общие элементы',
       'statement': 'Напишите common_sorted(a: &[i32], b: &[i32]) -> Vec<i32>: пересечение a и b без '
                    'повторов по возрастанию (HashSet).',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn common_sorted(a: &[i32], b: &[i32]) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", common_sorted(&[1, 2, 2, 3, 4], &[2, 4, 4, 6]));\n'
                 '    println!("{:?}", common_sorted(&[], &[1]));\n'
                 '}\n',
       'hint': 'Два множества и intersection.',
       'expected': ['[2, 4]', '[]']},
      {'id': 'r25-subset',
       'mode': 'rust',
       'title': 'Подмножество',
       'statement': 'Напишите can_make(note: &str, magazine: &str) -> bool: хватит ли букв из magazine, '
                    'чтобы вырезать note (каждая буква один раз; сравнивать как есть, пробелы игнорировать). '
                    'HashMap счётчиков.',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn can_make(note: &str, magazine: &str) -> bool {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", can_make("aab", "baa x"));\n'
                 '    println!("{}", can_make("aaa", "aab"));\n'
                 '    println!("{}", can_make("", ""));\n'
                 '}\n',
       'hint': 'Счётчики букв магазина уменьшаются при вырезании.',
       'expected': ['true', 'false', 'true']},
      {'id': 'r25-btree-ranks',
       'mode': 'rust',
       'title': 'Ранги по возрастанию',
       'statement': 'Напишите ranks(v: &[i32]) -> Vec<usize>: для каждого элемента — его номер (с 0) среди '
                    'различных значений по возрастанию (сжатие координат): [10, 5, 10, 7] → [2, 0, 2, 1]. '
                    'Используйте BTreeSet.',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn ranks(v: &[i32]) -> Vec<usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", ranks(&[10, 5, 10, 7]));\n'
                 '    println!("{:?}", ranks(&[]));\n'
                 '    println!("{:?}", ranks(&[3, 3, 3]));\n'
                 '}\n',
       'hint': 'BTreeSet даёт отсортированные уникальные значения; binary_search — номер.',
       'expected': ['[2, 0, 2, 1]', '[]', '[0, 0, 0]']},
      {'id': 'r25-btree-range',
       'mode': 'rust',
       'title': 'Ближайшие значения',
       'statement': 'Напишите nearest(sorted: &BTreeSet<i32>, x: i32) -> (Option<i32>, Option<i32>): '
                    'наибольшее значение не больше x и наименьшее не меньше x (методы range).',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn nearest(sorted: &BTreeSet<i32>, x: i32) -> (Option<i32>, Option<i32>) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let s: BTreeSet<i32> = [10, 20, 30, 40].into_iter().collect();\n'
                 '    println!("{:?}", nearest(&s, 25));\n'
                 '    println!("{:?}", nearest(&s, 5));\n'
                 '    println!("{:?}", nearest(&s, 50));\n'
                 '    println!("{:?}", nearest(&s, 30));\n'
                 '}\n',
       'hint': 'range(..=x).next_back() и range(x..).next()',
       'expected': ['(Some(20), Some(30))', '(None, Some(10))', '(Some(40), None)', '(Some(30), Some(30))']},
      {'id': 'r25-btree-intervals',
       'mode': 'rust',
       'title': 'События по порядку',
       'statement': 'Напишите timeline(events: &[(u32, &str)]) -> Vec<String>: события (время, название) '
                    'выведите в порядке времени; при одинаковом времени названия через «/» в порядке '
                    'добавления. Строки вида «5: a/b». BTreeMap.',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn timeline(events: &[(u32, &str)]) -> Vec<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    for l in timeline(&[(5, "a"), (2, "b"), (5, "c"), (9, "d")]) {\n'
                 '        println!("{}", l);\n'
                 '    }\n'
                 '}\n',
       'hint': 'entry(t).or_default().push(n); BTreeMap обходит по возрастанию.',
       'expected': ['2: b', '5: a/c', '9: d']},
      {'id': 'r25-btree-pop',
       'mode': 'rust',
       'title': 'Приоритетные задачи',
       'statement': 'Напишите process(tasks: &[(u32, &str)]) -> Vec<String>: задачи (приоритет, имя) '
                    'выполняются от наименьшего приоритета (число) к наибольшему; при равных — в порядке '
                    'добавления. Используйте BTreeMap<u32, VecDeque<String>> и pop_first.',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn process(tasks: &[(u32, &str)]) -> Vec<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", process(&[(3, "c"), (1, "a"), (3, "d"), (2, "b"), (1, "e")]));\n'
                 '    println!("{:?}", process(&[]));\n'
                 '}\n',
       'hint': 'pop_first даёт пару с наименьшим ключом.',
       'expected': ['["a", "e", "b", "c", "d"]', '[]']},
      {'id': 'r25-heap-topk',
       'mode': 'rust',
       'title': 'Топ-k кучей',
       'statement': 'Напишите top_k(v: &[i32], k: usize) -> Vec<i32>: k наибольших по убыванию, используя '
                    'кучу-минимум размера k (BinaryHeap<Reverse<i32>>) — для 300000 элементов и k = 5.',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn top_k(v: &[i32], k: usize) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", top_k(&[5, 1, 9, 3, 7, 7], 3));\n'
                 '    println!("{:?}", top_k(&[2], 5));\n'
                 '    println!("{:?}", top_k(&[2], 0));\n'
                 '    let big: Vec<i32> = (0..300000i64).map(|x| ((x * 7919) % 100003) as i32).collect();\n'
                 '    println!("{:?}", top_k(&big, 5));\n'
                 '}\n',
       'hint': 'Если в куче больше k — удаляем наименьшее.',
       'expected': ['[9, 7, 7]', '[2]', '[]', '[100002, 100002, 100002, 100001, 100001]']},
      {'id': 'r25-heap-merge',
       'mode': 'rust',
       'title': 'Слияние k списков',
       'statement': 'Напишите merge_k(lists: &[Vec<i32>]) -> Vec<i32>: слить отсортированные списки в один '
                    'отсортированный, используя BinaryHeap<Reverse<(i32, usize, usize)>> (значение, номер '
                    'списка, индекс).',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn merge_k(lists: &[Vec<i32>]) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", merge_k(&[vec![1, 4, 7], vec![2, 5], vec![], vec![3, 6, 9]]));\n'
                 '    println!("{:?}", merge_k(&[]));\n'
                 '}\n',
       'hint': 'В куче всегда по одному кандидату из каждого списка.',
       'expected': ['[1, 2, 3, 4, 5, 6, 7, 9]', '[]']},
      {'id': 'r25-heap-median',
       'mode': 'rust',
       'title': 'Бегущая медиана',
       'statement': 'Напишите running_median(v: &[i32]) -> Vec<f64>: после каждого элемента — медиана всех '
                    'прочитанных (две кучи: нижняя — максимум, верхняя — минимум).',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn running_median(v: &[i32]) -> Vec<f64> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", running_median(&[5, 15, 1, 3]));\n'
                 '    println!("{:?}", running_median(&[2]));\n'
                 '    println!("{:?}", running_median(&[]));\n'
                 '}\n',
       'hint': 'Размеры куч отличаются не больше чем на один.',
       'expected': ['[5.0, 10.0, 5.0, 4.0]', '[2.0]', '[]']},
      {'id': 'r25-dijkstra',
       'mode': 'rust',
       'title': 'Дейкстра на куче',
       'statement': 'Напишите dijkstra(n: usize, edges: &[(usize, usize, u32)], src: usize) -> '
                    'Vec<Option<u32>>: кратчайшие расстояния от src в ориентированном графе из n вершин; '
                    'недостижимые — None. Куча-минимум; граф на 20000 вершин.',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn dijkstra(n: usize, edges: &[(usize, usize, u32)], src: usize) -> Vec<Option<u32>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", dijkstra(5, &[(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5)], '
                 '0));\n'
                 '    let n = 20000;\n'
                 '    let edges: Vec<(usize, usize, u32)> = (0..n - 1).map(|i| (i, i + 1, 1)).chain((0..n - '
                 '2).map(|i| (i, i + 2, 3))).collect();\n'
                 '    let d = dijkstra(n, &edges, 0);\n'
                 '    println!("{:?} {:?}", d[n - 1], d[1]);\n'
                 '}\n',
       'hint': 'Пропускайте устаревшие записи в куче: d > dist[u].',
       'expected': ['[Some(0), Some(3), Some(1), Some(4), None]', 'Some(19999) Some(1)']},
      {'id': 'r25-deque-palindrome',
       'mode': 'rust',
       'title': 'Палиндром колодой',
       'statement': 'Напишите is_pal(s: &str) -> bool: палиндром ли строка (только буквы и цифры, без учёта '
                    'регистра), сравнивая символы с обоих концов VecDeque.',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn is_pal(s: &str) -> bool {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", is_pal("А роза упала на лапу Азора"));\n'
                 '    println!("{}", is_pal("Rust"));\n'
                 '    println!("{}", is_pal(""));\n'
                 '    println!("{}", is_pal("A man, a plan, a canal: Panama"));\n'
                 '}\n',
       'hint': 'pop_front и pop_back сравниваем парами.',
       'expected': ['true', 'false', 'true', 'true']},
      {'id': 'r25-lru',
       'mode': 'rust',
       'title': 'Мини-LRU',
       'statement': 'Структура Lru { cap: usize, order: VecDeque<String>, map: HashMap<String, i32> }. '
                    'Реализуйте new(cap), get(&mut self, k: &str) -> Option<i32> (обращение делает ключ '
                    'самым свежим) и put(&mut self, k: &str, v: i32) (обновление ключа тоже делает его '
                    'свежим; при переполнении удаляется самый старый).',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'struct Lru {\n'
                  '    cap: usize,\n'
                  '    order: VecDeque<String>,\n'
                  '    map: HashMap<String, i32>,\n'
                  '}\n'
                  '\n'
                  'impl Lru {\n'
                  '    fn new(cap: usize) -> Lru {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn touch(&mut self, k: &str) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn get(&mut self, k: &str) -> Option<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn put(&mut self, k: &str, v: i32) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut c = Lru::new(2);\n'
                 '    c.put("a", 1);\n'
                 '    c.put("b", 2);\n'
                 '    println!("{:?}", c.get("a"));\n'
                 '    c.put("c", 3);\n'
                 '    println!("{:?} {:?} {:?}", c.get("a"), c.get("b"), c.get("c"));\n'
                 '}\n',
       'hint': 'touch переносит ключ в конец порядка; самый старый — в начале.',
       'expected': ['Some(1)', 'Some(1) None Some(3)']},
      {'id': 'r25-hash-pair-sum',
       'mode': 'rust',
       'title': 'Пары с суммой',
       'statement': 'Напишите count_pairs(v: &[i32], target: i32) -> usize: сколько пар индексов i < j имеют '
                    'v[i] + v[j] = target (HashMap частот, один проход) — на 200000 элементов.',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn count_pairs(v: &[i32], target: i32) -> usize {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", count_pairs(&[1, 5, 7, -1, 5], 6));\n'
                 '    println!("{}", count_pairs(&[1, 1, 1], 2));\n'
                 '    println!("{}", count_pairs(&[], 0));\n'
                 '    let big: Vec<i32> = (0..200000).map(|x| x % 1000).collect();\n'
                 '    println!("{}", count_pairs(&big, 999));\n'
                 '}\n',
       'hint': 'Перед добавлением x в карту ищем его пару.',
       'expected': ['3', '3', '0', '20000000']},
      {'id': 'r25-lcp',
       'mode': 'rust',
       'title': 'Общий префикс',
       'statement': 'Напишите group_by_first(words: &[&str]) -> BTreeMap<char, Vec<String>>: слова по первой '
                    'букве (в нижнем регистре); пустые строки пропускаются; внутри групп — по возрастанию.',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn group_by_first(words: &[&str]) -> BTreeMap<char, Vec<String>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", group_by_first(&["яблоко", "Арбуз", "ананас", "", "Ёж", '
                 '"ежевика"]));\n'
                 '}\n',
       'hint': 'entry(буква).or_default().push(…); потом sort.',
       'expected': ['{\'а\': ["Арбуз", "ананас"], \'е\': ["ежевика"], \'я\': ["яблоко"], \'ё\': ["Ёж"]}']},
      {'id': 'r25-histogram-top',
       'mode': 'rust',
       'title': 'Самые частые',
       'statement': 'Напишите most_common(v: &[i32]) -> Option<i32>: самое частое значение; при равенстве — '
                    'наименьшее. Для пустого — None. HashMap и один проход по карте.',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn most_common(v: &[i32]) -> Option<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", most_common(&[1, 2, 2, 3, 3]));\n'
                 '    println!("{:?}", most_common(&[5]));\n'
                 '    println!("{:?}", most_common(&[]));\n'
                 '}\n',
       'hint': 'max_by с тем же сравнением по ключу в обратном порядке.',
       'expected': ['Some(2)', 'Some(5)', 'None']},
      {'id': 'r25-vec-capacity',
       'mode': 'rust',
       'title': 'Не перевыделять',
       'statement': 'Напишите squares(n: usize) -> Vec<u64>: квадраты 0…n−1, предварительно зарезервировав '
                    'память (with_capacity) — после заполнения capacity() должна быть равна n.',
       'starter': 'fn squares(n: usize) -> Vec<u64> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let v = squares(5);\n'
                 '    println!("{:?} {}", v, v.capacity() == 5);\n'
                 '    let w = squares(100000);\n'
                 '    println!("{} {}", w.len(), w.capacity() == 100000);\n'
                 '}\n',
       'hint': 'Vec::with_capacity(n)',
       'expected': ['[0, 1, 4, 9, 16] true', '100000 true']},
      {'id': 'r25-concat-join',
       'mode': 'rust',
       'title': 'concat и join',
       'statement': 'Напишите flatten_join(rows: &[Vec<&str>]) -> String: строки каждой подгруппы склеить '
                    'пробелами, группы разделить « | » (метод join у среза).',
       'starter': 'fn flatten_join(rows: &[Vec<&str>]) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", flatten_join(&[vec!["a", "b"], vec!["c"], vec![]]));\n'
                 '    println!("[{}]", flatten_join(&[]));\n'
                 '}\n',
       'hint': 'Два join: внутренний и внешний.',
       'expected': ['a b | c |', '[]']},
      {'id': 'r25-binary-search-by',
       'mode': 'rust',
       'title': 'binary_search_by',
       'statement': 'Напишите find_user(users: &[(u32, &str)], id: u32) -> Option<&str>: users отсортирован '
                    'по id; найти имя бинарным поиском (binary_search_by_key).',
       'starter': "fn find_user<'a>(users: &[(u32, &'a str)], id: u32) -> Option<&'a str> {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let u = [(1, "аня"), (4, "боря"), (9, "вера")];\n'
                 '    println!("{:?} {:?} {:?}", find_user(&u, 4), find_user(&u, 5), find_user(&[], 1));\n'
                 '}\n',
       'hint': 'binary_search_by_key(&id, |&(i, _)| i)',
       'expected': ['Some("боря") None None']},
      {'id': 'r25-vec-of-vec-sort',
       'mode': 'rust',
       'title': 'Сортировка строк матрицы',
       'statement': 'Напишите sort_rows(m: &mut Vec<Vec<i32>>): отсортировать каждую строку по возрастанию, '
                    'а затем строки между собой лексикографически.',
       'starter': 'fn sort_rows(m: &mut Vec<Vec<i32>>) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut m = vec![vec![3, 1, 2], vec![0, 9], vec![1, 0, 5], vec![]];\n'
                 '    sort_rows(&mut m);\n'
                 '    println!("{:?}", m);\n'
                 '}\n',
       'hint': 'Vec<Vec<i32>> сам умеет сравниваться лексикографически.',
       'expected': ['[[], [0, 1, 5], [0, 9], [1, 2, 3]]']},
      {'id': 'r25-set-visited',
       'mode': 'rust',
       'title': 'Посещённые состояния',
       'statement': 'Напишите steps_to_cycle(start: u32) -> usize: последовательность x → (x·x + 1) mod '
                    '1000; сколько шагов до первого повтора значения (HashSet посещённых; start считается '
                    'посещённым в момент 0).',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn steps_to_cycle(start: u32) -> usize {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", steps_to_cycle(0));\n'
                 '    println!("{}", steps_to_cycle(1));\n'
                 '    println!("{}", steps_to_cycle(500));\n'
                 '}\n',
       'hint': 'insert возвращает false, когда значение уже было.',
       'expected': ['10', '9', '10']},
      {'id': 'r25-reverse-heap-sorted',
       'mode': 'rust',
       'title': 'Сортировка кучей',
       'statement': 'Напишите heap_sort(v: &[i32]) -> Vec<i32>: отсортируйте по возрастанию через BinaryHeap '
                    '(from + into_sorted_vec).',
       'starter': 'use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};\n'
                  'use std::cmp::Reverse;\n'
                  '\n'
                  'fn heap_sort(v: &[i32]) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", heap_sort(&[5, 2, 9, 1, 5, 6]));\n'
                 '    println!("{:?}", heap_sort(&[]));\n'
                 '    let big: Vec<i32> = (0..100000i64).map(|x| ((x * 31337) % 10007) as i32).collect();\n'
                 '    let s = heap_sort(&big);\n'
                 '    println!("{} {}", s[0], s[s.len() - 1]);\n'
                 '}\n',
       'hint': 'into_sorted_vec возвращает по возрастанию.',
       'expected': ['[1, 2, 5, 5, 6, 9]', '[]', '0 10006']},
      {'id': 'r25-linked-list-note',
       'mode': 'rust',
       'title': 'Когда список, а когда вектор',
       'statement': 'Напишите move_front(v: &mut Vec<i32>, i: usize): перенести элемент с индексом i в '
                    'начало вектора, сохранив порядок остальных (remove + insert, либо rotate_right на срезе '
                    '0..=i).',
       'starter': 'fn move_front(v: &mut Vec<i32>, i: usize) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![1, 2, 3, 4, 5];\n'
                 '    move_front(&mut v, 3);\n'
                 '    println!("{:?}", v);\n'
                 '    move_front(&mut v, 0);\n'
                 '    println!("{:?}", v);\n'
                 '}\n',
       'hint': 'v[..=i].rotate_right(1) без копирования всего вектора.',
       'expected': ['[4, 1, 2, 3, 5]', '[4, 1, 2, 3, 5]']}]}
