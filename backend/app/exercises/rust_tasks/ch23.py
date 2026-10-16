"""Задачи книги «Изучаем Rust»: глава 23 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {23: [{'id': 'r23-par-sum',
       'mode': 'rust',
       'title': 'Параллельная сумма: scope и chunks',
       'statement': 'par_sum(v: &[i64], parts: usize) → i64: разрежьте срез на parts кусков (последний может '
                    'быть короче; parts ≥ 1), в thread::scope запустите по потоку на кусок, каждый считает '
                    'свою сумму, затем сложите результаты. Данные не копируются: потоки берут ссылки на '
                    'куски.',
       'starter': 'use std::thread;\n\nfn par_sum(v: &[i64], parts: usize) -> i64 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let v: Vec<i64> = (1..=100_000).collect();\n'
                 '    println!("{}", par_sum(&v, 4));\n'
                 '    println!("{}", par_sum(&v, 7));\n'
                 '    println!("{}", par_sum(&v[..10], 100));\n'
                 '    println!("{}", par_sum(&[], 3));\n'
                 '    println!("{}", par_sum(&[5], 1));\n'
                 '}\n',
       'hint': 'chunks(size) даёт срезы; s.spawn(move || …) в scope может брать срез напрямую; '
               'h.join().unwrap() возвращает сумму куска.',
       'expected': ['5000050000', '5000050000', '55', '0', '5']},
      {'id': 'r23-spawn-join-results',
       'mode': 'rust',
       'title': 'spawn и join: результаты по порядку',
       'statement': 'squares_in_threads(n) → Vec<u64>: для каждого i от 1 до n запустите поток, который '
                    'возвращает i², и соберите результаты В ПОРЯДКЕ i (дождитесь потоков по очереди через '
                    'JoinHandle). word_lengths(words: Vec<String>) → Vec<usize> — каждое слово '
                    'обрабатывается в своём потоке (слова переезжают в потоки).',
       'starter': 'use std::thread;\n'
                  '\n'
                  'fn squares_in_threads(n: u64) -> Vec<u64> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn word_lengths(words: Vec<String>) -> Vec<usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", squares_in_threads(8));\n'
                 '    println!("{:?}", squares_in_threads(0));\n'
                 '    println!("{:?}", word_lengths(vec!["привет".into(), "мир".into(), "".into(), '
                 '"rust".into()]));\n'
                 '}\n',
       'hint': 'Сначала запустите ВСЕ потоки (collect в вектор хэндлов), только потом join: иначе потоки '
               'пойдут по очереди.',
       'expected': ['[1, 4, 9, 16, 25, 36, 49, 64]', '[]', '[6, 3, 0, 4]']},
      {'id': 'r23-fix-move',
       'mode': 'rust',
       'title': 'Исправьте: замыкание заимствует локальное',
       'statement': 'sum_in_thread запускает поток, который суммирует вектор, но замыкание берёт v по '
                    'ссылке, а поток может пережить функцию (E0373). Исправьте одним словом.',
       'starter': 'use std::thread;\n'
                  '\n'
                  'fn sum_in_thread(v: Vec<i32>) -> i32 {\n'
                  '    let h = thread::spawn(|| v.iter().sum::<i32>());\n'
                  '    h.join().unwrap()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", sum_in_thread(vec![1, 2, 3, 4]));\n'
                 '    println!("{}", sum_in_thread(vec![]));\n'
                 '}\n',
       'hint': 'move передаст вектор потоку целиком.',
       'expected': ['10', '0']},
      {'id': 'r23-fix-rc',
       'mode': 'rust',
       'title': 'Исправьте: Rc не Send',
       'statement': 'len_in_thread оборачивает строку в Rc и отправляет в поток — компилятор не пускает (Rc '
                    'не реализует Send). Замените Rc на Arc, остальное оставьте.',
       'starter': 'use std::rc::Rc;\n'
                  'use std::thread;\n'
                  '\n'
                  'fn len_in_thread(s: &str) -> usize {\n'
                  '    let shared = Rc::new(s.to_string());\n'
                  '    let for_thread = Rc::clone(&shared);\n'
                  '    let h = thread::spawn(move || for_thread.len());\n'
                  '    let n = h.join().unwrap();\n'
                  '    n + Rc::strong_count(&shared) - 1\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", len_in_thread("привет"));\n'
                 '    println!("{}", len_in_thread(""));\n'
                 '}\n',
       'hint': 'Arc имеет те же методы new, clone и strong_count — подставьте его вместо Rc и подключите '
               'std::sync::Arc.',
       'expected': ['12', '0']},
      {'id': 'r23-counter-mutex',
       'mode': 'rust',
       'title': 'Общий счётчик: Arc<Mutex<u64>>',
       'statement': 'count_parallel(threads: usize, per_thread: u64) → u64: запустите threads потоков, '
                    'каждый увеличивает общий счётчик (Arc<Mutex<u64>>) per_thread раз по единице; верните '
                    'итог. contended(threads, per_thread) → u64 — то же, но каждый поток сначала считает '
                    'локально и один раз прибавляет к общему.',
       'starter': 'use std::sync::{Arc, Mutex};\n'
                  'use std::thread;\n'
                  '\n'
                  'fn count_parallel(threads: usize, per_thread: u64) -> u64 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn contended(threads: usize, per_thread: u64) -> u64 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{} {}", count_parallel(8, 10_000), contended(8, 10_000));\n'
                 '    println!("{} {}", count_parallel(1, 5), contended(3, 0));\n'
                 '    println!("{}", count_parallel(0, 100));\n'
                 '}\n',
       'hint': 'Каждому потоку — свой клон Arc; замок берётся на одну операцию: *c.lock().unwrap() += 1.',
       'expected': ['80000 80000', '5 0', '0']},
      {'id': 'r23-bank-transfers',
       'mode': 'rust',
       'title': 'Переводы без взаимных блокировок',
       'statement': 'transfer_all(accounts: &[Arc<Mutex<i64>>], transfers: &[(usize, usize, i64)]) → '
                    'Vec<i64>: каждый перевод (from, to, сумма) выполняется в своём потоке одновременно с '
                    'остальными. Чтобы не получить deadlock, всегда захватывайте счета в порядке возрастания '
                    'номера. from == to — ничего не делать. Верните итоговые балансы (отрицательные '
                    'допустимы).',
       'starter': 'use std::sync::{Arc, Mutex};\n'
                  'use std::thread;\n'
                  '\n'
                  'fn transfer_all(accounts: &[Arc<Mutex<i64>>], transfers: &[(usize, usize, i64)]) -> '
                  'Vec<i64> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let accs: Vec<Arc<Mutex<i64>>> = (0..4).map(|_| Arc::new(Mutex::new(100))).collect();\n'
                 '    let mut transfers = Vec::new();\n'
                 '    for i in 0..200usize {\n'
                 '        transfers.push((i % 4, (i * 3 + 1) % 4, (i as i64 % 7) + 1));\n'
                 '    }\n'
                 '    let res = transfer_all(&accs, &transfers);\n'
                 '    println!("{:?} total={}", res, res.iter().sum::<i64>());\n'
                 '    let expected: Vec<i64> = {\n'
                 '        let mut e = vec![100i64; 4];\n'
                 '        for &(f, t, a) in &transfers {\n'
                 '            if f != t {\n'
                 '                e[f] -= a;\n'
                 '                e[t] += a;\n'
                 '            }\n'
                 '        }\n'
                 '        e\n'
                 '    };\n'
                 '    println!("{}", res == expected);\n'
                 '    println!("{:?}", transfer_all(&[], &[]));\n'
                 '}\n',
       'hint': 'Всегда блокируйте сначала счёт с меньшим номером: так цикл ожидания невозможен.',
       'expected': ['[101, 99, 101, 99] total=400', 'true', '[]']},
      {'id': 'r23-rwlock-cache',
       'mode': 'rust',
       'title': 'Кеш на RwLock',
       'statement': 'Cache хранит RwLock<HashMap<u64, u64>> и AtomicUsize числа реальных вычислений. '
                    'get(&self, x, f: fn(u64) → u64) → u64: читает под read-замком; если нет — берёт '
                    'write-замок, проверяет ещё раз и вычисляет (вычисление считается). computations(&self) '
                    '→ usize. Из нескольких потоков одно значение должно вычисляться ровно один раз.',
       'starter': 'use std::collections::HashMap;\n'
                  'use std::sync::atomic::{AtomicUsize, Ordering};\n'
                  'use std::sync::RwLock;\n'
                  '\n'
                  'struct Cache {\n'
                  '    map: RwLock<HashMap<u64, u64>>,\n'
                  '    computed: AtomicUsize,\n'
                  '}\n'
                  '\n'
                  'impl Cache {\n'
                  '    fn new() -> Cache {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn get(&self, x: u64, f: fn(u64) -> u64) -> u64 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn computations(&self) -> usize {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'use std::sync::Arc;\n'
                 'use std::thread;\n'
                 '\n'
                 'fn slow_square(x: u64) -> u64 {\n'
                 '    x * x\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    let c = Arc::new(Cache::new());\n'
                 '    let hs: Vec<_> = (0..8)\n'
                 '        .map(|t| {\n'
                 '            let c = Arc::clone(&c);\n'
                 '            thread::spawn(move || (0..50u64).map(|i| c.get((i + t) % 10, '
                 'slow_square)).sum::<u64>())\n'
                 '        })\n'
                 '        .collect();\n'
                 '    let total: u64 = hs.into_iter().map(|h| h.join().unwrap()).sum();\n'
                 '    println!("{} {}", total, c.computations());\n'
                 '    println!("{}", c.get(3, slow_square));\n'
                 '    println!("{}", c.computations());\n'
                 '}\n',
       'hint': 'После получения write-замка проверьте ключ ещё раз: пока вы ждали, другой поток мог его '
               'вычислить.',
       'expected': ['11400 10', '9', '10']},
      {'id': 'r23-word-count-par',
       'mode': 'rust',
       'title': 'Параллельный подсчёт слов',
       'statement': 'word_count_par(text: &str, parts: usize) → BTreeMap<String, usize>: разделите строки '
                    'текста между parts потоками (по порядку блоками), каждый считает слова (в нижнем '
                    'регистре, слова — буквы и цифры) в своём HashMap, затем слейте результаты. Результат не '
                    'должен зависеть от parts.',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn word_count_par(text: &str, parts: usize) -> BTreeMap<String, usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let text = "the quick brown fox\\njumps over the lazy dog\\nThe DOG barks, the fox '
                 'runs\\n\\nfox fox";\n'
                 '    let a = word_count_par(text, 1);\n'
                 '    let b = word_count_par(text, 3);\n'
                 '    let c = word_count_par(text, 10);\n'
                 '    println!("{:?}", a);\n'
                 '    println!("{}", a == b && b == c);\n'
                 '    println!("{:?}", word_count_par("", 4));\n'
                 '    println!("{:?}", word_count_par("Привет, привет! мир", 2));\n'
                 '}\n',
       'hint': 'Каждый поток возвращает свой HashMap; общий результат собирается уже в главном потоке — без '
               'блокировок.',
       'expected': ['{"barks": 1, "brown": 1, "dog": 2, "fox": 4, "jumps": 1, "lazy": 1, "over": 1, "quick": '
                    '1, "runs": 1, "the": 4}',
                    'true',
                    '{}',
                    '{"мир": 1, "привет": 2}']},
      {'id': 'r23-par-map',
       'mode': 'rust',
       'title': 'par_map: параллельное преобразование',
       'statement': 'par_map<T, U, F>(v: &[T], parts: usize, f: F) → Vec<U> where T: Sync, U: Send, F: '
                    'Fn(&T) → U + Sync: применить f ко всем элементам, разбив срез на parts кусков по '
                    'потокам; результат в исходном порядке.',
       'starter': 'use std::thread;\n'
                  '\n'
                  'fn par_map<T, U, F>(v: &[T], parts: usize, f: F) -> Vec<U>\n'
                  'where\n'
                  '    T: Sync,\n'
                  '    U: Send,\n'
                  '    F: Fn(&T) -> U + Sync,\n'
                  '{\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let v: Vec<u64> = (1..=20).collect();\n'
                 '    println!("{:?}", par_map(&v, 3, |x| x * x));\n'
                 '    println!("{:?}", par_map(&["a", "bb", "ccc"], 2, |s| s.len()));\n'
                 '    println!("{:?}", par_map(&[] as &[i32], 4, |x| x + 1));\n'
                 '    let words = vec![String::from("раз"), String::from("два"), String::from("три")];\n'
                 '    println!("{:?}", par_map(&words, 3, |w| w.to_uppercase()));\n'
                 '    let k = 10;\n'
                 '    println!("{:?}", par_map(&[1, 2, 3], 2, |x| x * k));\n'
                 '}\n',
       'hint': 'Замыкание f вызывается из нескольких потоков по общей ссылке: поэтому F: Sync; берите &f и '
               'копируйте ссылку в потоки.',
       'expected': ['[1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, '
                    '400]',
                    '[1, 2, 3]',
                    '[]',
                    '["РАЗ", "ДВА", "ТРИ"]',
                    '[10, 20, 30]']},
      {'id': 'r23-pipeline-channels',
       'mode': 'rust',
       'title': 'Конвейер из потоков и каналов',
       'statement': 'pipeline(n: u64) → Vec<u64>: три стадии в трёх потоках, соединённые каналами mpsc: (1) '
                    'генератор шлёт числа 1..=n; (2) возводит в квадрат; (3) фильтр оставляет квадраты, '
                    'делящиеся на 3. Главный поток собирает результат (порядок сохраняется).',
       'starter': 'use std::sync::mpsc;\n'
                  'use std::thread;\n'
                  '\n'
                  'fn pipeline(n: u64) -> Vec<u64> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", pipeline(12));\n'
                 '    println!("{:?}", pipeline(0));\n'
                 '    println!("{}", pipeline(1000).len());\n'
                 '}\n',
       'hint': 'Каждая стадия владеет своим tx; когда стадия закончилась, её tx закрывается — следующая '
               'стадия выходит из цикла по rx.',
       'expected': ['[9, 36, 81, 144]', '[]', '333']},
      {'id': 'r23-fan-in',
       'mode': 'rust',
       'title': 'Несколько производителей, один получатель',
       'statement': 'fan_in(producers: usize, items: usize) → Vec<(usize, usize)>: запустите producers '
                    'потоков; поток p шлёт в общий канал пары (p, 0), (p, 1), …, (p, items-1). Главный поток '
                    'собирает ВСЕ сообщения и возвращает их отсортированными. Для этого клонируйте '
                    'отправителя и не забудьте закрыть исходного.',
       'starter': 'use std::sync::mpsc;\n'
                  'use std::thread;\n'
                  '\n'
                  'fn fan_in(producers: usize, items: usize) -> Vec<(usize, usize)> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", fan_in(3, 2));\n'
                 '    println!("{}", fan_in(10, 100).len());\n'
                 '    println!("{:?}", fan_in(0, 5));\n'
                 '    println!("{:?}", fan_in(2, 0));\n'
                 '}\n',
       'hint': 'drop(tx) в главном потоке закрывает исходный отправитель: иначе rx.iter() никогда не '
               'закончится.',
       'expected': ['[(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]', '1000', '[]', '[]']},
      {'id': 'r23-ping-pong',
       'mode': 'rust',
       'title': 'Пинг-понг через два канала',
       'statement': 'ping_pong(rounds: u32) → Vec<String>: два потока обмениваются сообщениями через два '
                    'канала: «ping» от первого второму, «pong» обратно, rounds раз. Каждый поток записывает '
                    'в общий журнал (отдельный канал или значение, возвращаемое из join) события в порядке '
                    '«ping 1», «pong 1», «ping 2», …',
       'starter': 'use std::sync::mpsc;\n'
                  'use std::thread;\n'
                  '\n'
                  'fn ping_pong(rounds: u32) -> Vec<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", ping_pong(3));\n'
                 '    println!("{:?}", ping_pong(0));\n'
                 '    println!("{}", ping_pong(500).len());\n'
                 '}\n',
       'hint': 'Пинг ждёт ответа recv() после каждого send(): так события выстраиваются строго по очереди.',
       'expected': ['["ping 1", "pong 1", "ping 2", "pong 2", "ping 3", "pong 3"]', '[]', '1000']},
      {'id': 'r23-sync-channel',
       'mode': 'rust',
       'title': 'Ограниченный канал: давление назад',
       'statement': 'bounded_sum(items: u64, capacity: usize) → (u64, bool): производитель в потоке шлёт '
                    'числа 1..=items в sync_channel(capacity); потребитель в главном потоке суммирует. '
                    'Второе значение — истина, если потребитель получил числа строго по порядку 1, 2, 3, …',
       'starter': 'use std::sync::mpsc;\n'
                  'use std::thread;\n'
                  '\n'
                  'fn bounded_sum(items: u64, capacity: usize) -> (u64, bool) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", bounded_sum(10, 2));\n'
                 '    println!("{:?}", bounded_sum(10_000, 1));\n'
                 '    println!("{:?}", bounded_sum(100, 0));\n'
                 '    println!("{:?}", bounded_sum(0, 4));\n'
                 '}\n',
       'hint': 'sync_channel(0) — «рандеву»: send ждёт, пока получатель не заберёт значение.',
       'expected': ['(55, true)', '(50005000, true)', '(5050, true)', '(0, true)']},
      {'id': 'r23-condvar-queue',
       'mode': 'rust',
       'title': 'Ограниченная очередь на Mutex и Condvar',
       'statement': 'BoundedQueue<T> { Mutex<VecDeque<T>>, Condvar not_empty, Condvar not_full, capacity }: '
                    'push(&self, x) ждёт, пока есть место; pop(&self) → T ждёт, пока появится элемент. '
                    'Проверка: производители и потребители в разных потоках, сумма всех элементов совпадает.',
       'starter': 'use std::collections::VecDeque;\n'
                  'use std::sync::{Condvar, Mutex};\n'
                  '\n'
                  'struct BoundedQueue<T> {\n'
                  '    items: Mutex<VecDeque<T>>,\n'
                  '    not_empty: Condvar,\n'
                  '    not_full: Condvar,\n'
                  '    capacity: usize,\n'
                  '}\n'
                  '\n'
                  'impl<T> BoundedQueue<T> {\n'
                  '    fn new(capacity: usize) -> BoundedQueue<T> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn push(&self, x: T) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn pop(&self) -> T {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'use std::sync::Arc;\n'
                 'use std::thread;\n'
                 '\n'
                 'fn main() {\n'
                 '    let q = Arc::new(BoundedQueue::new(3));\n'
                 '    let producers: Vec<_> = (0..4u64)\n'
                 '        .map(|p| {\n'
                 '            let q = Arc::clone(&q);\n'
                 '            thread::spawn(move || {\n'
                 '                for i in 0..50 {\n'
                 '                    q.push(p * 1000 + i);\n'
                 '                }\n'
                 '            })\n'
                 '        })\n'
                 '        .collect();\n'
                 '    let consumers: Vec<_> = (0..2)\n'
                 '        .map(|_| {\n'
                 '            let q = Arc::clone(&q);\n'
                 '            thread::spawn(move || (0..100).map(|_| q.pop()).sum::<u64>())\n'
                 '        })\n'
                 '        .collect();\n'
                 '    for p in producers {\n'
                 '        p.join().unwrap();\n'
                 '    }\n'
                 '    let total: u64 = consumers.into_iter().map(|c| c.join().unwrap()).sum();\n'
                 '    let expected: u64 = (0..4u64).map(|p| (0..50).map(|i| p * 1000 + '
                 'i).sum::<u64>()).sum();\n'
                 '    println!("{} {}", total, total == expected);\n'
                 '    let single: BoundedQueue<i32> = BoundedQueue::new(1);\n'
                 '    single.push(7);\n'
                 '    println!("{}", single.pop());\n'
                 '}\n',
       'hint': 'Ожидание условия — всегда в цикле while: после пробуждения условие нужно проверить ещё раз.',
       'expected': ['304900 true', '7']},
      {'id': 'r23-barrier-phases',
       'mode': 'rust',
       'title': 'Barrier: две фазы',
       'statement': 'phases(n: usize) → Vec<u64>: n потоков; в фазе 1 поток i записывает в общий вектор слот '
                    'i значение (i+1)²; после Barrier в фазе 2 каждый поток читает сумму всех слотов и '
                    'возвращает её. Благодаря барьеру все n результатов одинаковы.',
       'starter': 'use std::sync::{Arc, Barrier, Mutex};\n'
                  'use std::thread;\n'
                  '\n'
                  'fn phases(n: usize) -> Vec<u64> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", phases(4));\n'
                 '    println!("{:?}", phases(1));\n'
                 '    let r = phases(12);\n'
                 '    println!("{} {}", r.len(), r.iter().all(|&x| x == r[0]));\n'
                 '    println!("{:?}", phases(0));\n'
                 '}\n',
       'hint': 'barrier.wait() блокирует поток, пока не придут все n; только после него безопасно читать '
               'чужие слоты.',
       'expected': ['[30, 30, 30, 30]', '[1]', '12 true', '[]']},
      {'id': 'r23-atomic-counter',
       'mode': 'rust',
       'title': 'Атомики: fetch_add и fetch_max',
       'statement': 'atomic_stats(threads: usize, per_thread: usize) → (usize, usize, usize). Поток с '
                    'номером id (0..threads): per_thread раз увеличивает общий счётчик hits (fetch_add); '
                    'записывает свой id в biggest через fetch_max; пытается занять флаг first через '
                    'compare_exchange(0, id + 1) — это удаётся ровно одному потоку. Верните (hits, '
                    'наибольший id, число потоков, занявших флаг).',
       'starter': 'use std::sync::atomic::{AtomicUsize, Ordering};\n'
                  'use std::sync::Arc;\n'
                  'use std::thread;\n'
                  '\n'
                  'fn atomic_stats(threads: usize, per_thread: usize) -> (usize, usize, usize) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", atomic_stats(8, 10_000));\n'
                 '    println!("{:?}", atomic_stats(1, 3));\n'
                 '    println!("{:?}", atomic_stats(16, 0));\n'
                 '    println!("{:?}", atomic_stats(0, 5));\n'
                 '}\n',
       'hint': 'compare_exchange(0, id+1, …) удаётся ровно одному потоку — победитель один независимо от '
               'порядка запуска.',
       'expected': ['(80000, 7, 1)', '(3, 0, 1)', '(0, 15, 1)', '(0, 0, 0)']},
      {'id': 'r23-spinlock',
       'mode': 'rust',
       'title': 'Спинлок на AtomicBool',
       'statement': 'SpinLock { locked: AtomicBool }: lock(&self) крутится, пока compare_exchange(false, '
                    'true, Acquire, Relaxed) не удастся (std::hint::spin_loop() в цикле); unlock(&self) '
                    'пишет false (Release). Драйвер проверяет, что внутри критической секции одновременно '
                    'находится не больше одного потока.',
       'starter': 'use std::sync::atomic::{AtomicBool, Ordering};\n'
                  '\n'
                  'struct SpinLock {\n'
                  '    locked: AtomicBool,\n'
                  '}\n'
                  '\n'
                  'impl SpinLock {\n'
                  '    fn new() -> SpinLock {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn lock(&self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn unlock(&self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'use std::sync::atomic::{AtomicUsize, Ordering};\n'
                 'use std::sync::Arc;\n'
                 'use std::thread;\n'
                 '\n'
                 'fn main() {\n'
                 '    let lock = Arc::new(SpinLock::new());\n'
                 '    let inside = Arc::new(AtomicUsize::new(0));\n'
                 '    let max_inside = Arc::new(AtomicUsize::new(0));\n'
                 '    let entries = Arc::new(AtomicUsize::new(0));\n'
                 '    let hs: Vec<_> = (0..4)\n'
                 '        .map(|_| {\n'
                 '            let (lock, inside, max_inside, entries) = (lock.clone(), inside.clone(), '
                 'max_inside.clone(), entries.clone());\n'
                 '            thread::spawn(move || {\n'
                 '                for _ in 0..2000 {\n'
                 '                    lock.lock();\n'
                 '                    let now = inside.fetch_add(1, Ordering::SeqCst) + 1;\n'
                 '                    max_inside.fetch_max(now, Ordering::SeqCst);\n'
                 '                    entries.fetch_add(1, Ordering::SeqCst);\n'
                 '                    inside.fetch_sub(1, Ordering::SeqCst);\n'
                 '                    lock.unlock();\n'
                 '                }\n'
                 '            })\n'
                 '        })\n'
                 '        .collect();\n'
                 '    for h in hs {\n'
                 '        h.join().unwrap();\n'
                 '    }\n'
                 '    println!("max_inside={} entries={}", max_inside.load(Ordering::SeqCst), '
                 'entries.load(Ordering::SeqCst));\n'
                 '}\n',
       'hint': 'Успешный compare_exchange(false, true) означает «я взял замок»; Acquire при взятии и Release '
               'при отпускании связывают секции.',
       'expected': ['max_inside=1 entries=8000']},
      {'id': 'r23-once-flag',
       'mode': 'rust',
       'title': 'Выполнить ровно один раз',
       'statement': 'Once { done: AtomicBool }: run(&self, f: impl FnOnce()) → bool: выполняет f только если '
                    'никто ещё не начал (compare_exchange на флаге); возвращает true тому, кто выполнил. '
                    'Драйвер запускает 16 потоков: f должна сработать ровно один раз.',
       'starter': 'use std::sync::atomic::{AtomicBool, Ordering};\n'
                  '\n'
                  'struct Once {\n'
                  '    done: AtomicBool,\n'
                  '}\n'
                  '\n'
                  'impl Once {\n'
                  '    fn new() -> Once {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn run(&self, f: impl FnOnce()) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'use std::sync::atomic::{AtomicUsize, Ordering};\n'
                 'use std::sync::Arc;\n'
                 'use std::thread;\n'
                 '\n'
                 'fn main() {\n'
                 '    let once = Arc::new(Once::new());\n'
                 '    let calls = Arc::new(AtomicUsize::new(0));\n'
                 '    let winners = Arc::new(AtomicUsize::new(0));\n'
                 '    let hs: Vec<_> = (0..16)\n'
                 '        .map(|_| {\n'
                 '            let (once, calls, winners) = (once.clone(), calls.clone(), winners.clone());\n'
                 '            thread::spawn(move || {\n'
                 '                if once.run(|| {\n'
                 '                    calls.fetch_add(1, Ordering::SeqCst);\n'
                 '                }) {\n'
                 '                    winners.fetch_add(1, Ordering::SeqCst);\n'
                 '                }\n'
                 '            })\n'
                 '        })\n'
                 '        .collect();\n'
                 '    for h in hs {\n'
                 '        h.join().unwrap();\n'
                 '    }\n'
                 '    println!("calls={} winners={}", calls.load(Ordering::SeqCst), '
                 'winners.load(Ordering::SeqCst));\n'
                 '    println!("{}", once.run(|| {}));\n'
                 '}\n',
       'hint': 'Только один compare_exchange(false, true) окажется успешным — он и вызывает f.',
       'expected': ['calls=1 winners=1', 'false']},
      {'id': 'r23-thread-pool',
       'mode': 'rust',
       'title': 'Свой пул потоков',
       'statement': 'ThreadPool::new(n) запускает n рабочих; execute(&self, job: impl FnOnce() + Send + '
                    "'static) кладёт задачу в канал; shutdown(self) закрывает канал и дожидается рабочих "
                    '(все поставленные задачи выполнены). Рабочие достают задачи из общего '
                    'Arc<Mutex<Receiver<Job>>>.',
       'starter': 'use std::sync::mpsc;\n'
                  'use std::sync::{Arc, Mutex};\n'
                  'use std::thread::{self, JoinHandle};\n'
                  '\n'
                  "type Job = Box<dyn FnOnce() + Send + 'static>;\n"
                  '\n'
                  'struct ThreadPool {\n'
                  '    workers: Vec<JoinHandle<()>>,\n'
                  '    sender: Option<mpsc::Sender<Job>>,\n'
                  '}\n'
                  '\n'
                  'impl ThreadPool {\n'
                  '    fn new(n: usize) -> ThreadPool {\n'
                  '        todo!()\n'
                  '    }\n'
                  "    fn execute(&self, job: impl FnOnce() + Send + 'static) {\n"
                  '        todo!()\n'
                  '    }\n'
                  '    fn shutdown(mut self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'use std::sync::atomic::{AtomicU64, Ordering};\n'
                 'use std::sync::Arc;\n'
                 '\n'
                 'fn main() {\n'
                 '    let pool = ThreadPool::new(4);\n'
                 '    let total = Arc::new(AtomicU64::new(0));\n'
                 '    for i in 1..=100u64 {\n'
                 '        let total = Arc::clone(&total);\n'
                 '        pool.execute(move || {\n'
                 '            total.fetch_add(i * i, Ordering::SeqCst);\n'
                 '        });\n'
                 '    }\n'
                 '    pool.shutdown();\n'
                 '    println!("{}", total.load(Ordering::SeqCst));\n'
                 '    let empty = ThreadPool::new(2);\n'
                 '    empty.shutdown();\n'
                 '    println!("ok");\n'
                 '}\n',
       'hint': 'Рабочий: loop { let job = rx.lock().unwrap().recv(); … } — замок держится только на время '
               'recv; закрытый канал → Err → выходим.',
       'expected': ['338350', 'ok']},
      {'id': 'r23-par-double',
       'mode': 'rust',
       'title': 'chunks_mut: изменить на месте параллельно',
       'statement': 'par_scale(v: &mut [i64], k: i64, parts: usize): умножьте каждый элемент на k, разделив '
                    'срез на parts непересекающихся изменяемых кусков (chunks_mut) и запустив поток на '
                    'каждый. par_prefix_marks(v: &mut [i64]) — каждый элемент заменить на его индекс × '
                    'значение (потоки получают смещение куска).',
       'starter': 'use std::thread;\n'
                  '\n'
                  'fn par_scale(v: &mut [i64], k: i64, parts: usize) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn par_prefix_marks(v: &mut [i64]) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut v: Vec<i64> = (1..=10).collect();\n'
                 '    par_scale(&mut v, 3, 4);\n'
                 '    println!("{:?}", v);\n'
                 '    let mut w = vec![5; 10];\n'
                 '    par_prefix_marks(&mut w);\n'
                 '    println!("{:?}", w);\n'
                 '    let mut e: Vec<i64> = vec![];\n'
                 '    par_scale(&mut e, 2, 3);\n'
                 '    println!("{:?}", e);\n'
                 '}\n',
       'hint': 'chunks_mut даёт непересекающиеся &mut [T]: каждый кусок можно отдать своему потоку без '
               'блокировок.',
       'expected': ['[3, 6, 9, 12, 15, 18, 21, 24, 27, 30]', '[0, 5, 10, 15, 20, 25, 30, 35, 40, 45]', '[]']},
      {'id': 'r23-sieve-par',
       'mode': 'rust',
       'title': 'Простые числа: сегменты по потокам',
       'statement': 'count_primes(n: u64, parts: usize) → usize: сколько простых меньше n. Диапазон 2..n '
                    'делится на parts сегментов; каждый поток проверяет числа своего сегмента пробным '
                    'делением. Результат не зависит от parts. Для n до 200 000 работа должна уложиться в '
                    'лимит.',
       'starter': 'use std::thread;\n\nfn count_primes(n: u64, parts: usize) -> usize {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{} {} {}", count_primes(100, 1), count_primes(100, 4), count_primes(100, '
                 '9));\n'
                 '    println!("{} {}", count_primes(2, 3), count_primes(3, 5));\n'
                 '    println!("{}", count_primes(200_000, 8));\n'
                 '}\n',
       'hint': 'Сегмент [lo, hi): lo = 2 + p·size, hi = min(lo + size, n); поток возвращает количество '
               'простых в нём.',
       'expected': ['25 25 25', '0 1', '17984']},
      {'id': 'r23-matrix-rows',
       'mode': 'rust',
       'title': 'Матрица: строки по потокам',
       'statement': 'matmul(a: &[Vec<i64>], b: &[Vec<i64>]) → Vec<Vec<i64>>: произведение матриц (размеры '
                    'согласованы). Каждая строка результата вычисляется в отдельном потоке внутри scope; '
                    'результат должен совпасть с последовательным вычислением.',
       'starter': 'use std::thread;\n'
                  '\n'
                  'fn matmul(a: &[Vec<i64>], b: &[Vec<i64>]) -> Vec<Vec<i64>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a = vec![vec![1, 2, 3], vec![4, 5, 6]];\n'
                 '    let b = vec![vec![7, 8], vec![9, 10], vec![11, 12]];\n'
                 '    println!("{:?}", matmul(&a, &b));\n'
                 '    let n = 60;\n'
                 '    let big: Vec<Vec<i64>> = (0..n).map(|i| (0..n).map(|j| ((i * 7 + j * 3) % 10) as '
                 'i64).collect()).collect();\n'
                 '    let r = matmul(&big, &big);\n'
                 '    let mut seq = vec![vec![0i64; n]; n];\n'
                 '    for i in 0..n {\n'
                 '        for j in 0..n {\n'
                 '            for k in 0..n {\n'
                 '                seq[i][j] += big[i][k] * big[k][j];\n'
                 '            }\n'
                 '        }\n'
                 '    }\n'
                 '    println!("{} {}", r == seq, r[5][7]);\n'
                 '    println!("{:?}", matmul(&[], &[]));\n'
                 '}\n',
       'hint': 'Каждая строка результата зависит только от строки a и всей b — потоки не пересекаются; b '
               'берётся по общей ссылке.',
       'expected': ['[[58, 64], [139, 154]]', 'true 1350', '[]']},
      {'id': 'r23-merge-sort-par',
       'mode': 'rust',
       'title': 'Параллельная сортировка слиянием',
       'statement': 'par_sort(v: Vec<i64>) → Vec<i64>: сортировка слиянием; половины сортируются в разных '
                    'потоках (thread::scope), пока длина больше 1000, ниже — обычная sort. Результат '
                    'совпадает с v.sort().',
       'starter': 'fn par_sort(v: Vec<i64>) -> Vec<i64> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut x: u64 = 12345;\n'
                 '    let v: Vec<i64> = (0..50_000)\n'
                 '        .map(|_| {\n'
                 '            x = x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n'
                 '            ((x >> 33) % 100_000) as i64 - 50_000\n'
                 '        })\n'
                 '        .collect();\n'
                 '    let mut want = v.clone();\n'
                 '    want.sort();\n'
                 '    let got = par_sort(v);\n'
                 '    println!("{} {} {}", got == want, got[0], got[got.len() - 1]);\n'
                 '    println!("{:?} {:?}", par_sort(vec![]), par_sort(vec![3, 1, 2]));\n'
                 '}\n',
       'hint': 'Поток получает правую половину целиком (split_off), левая сортируется в текущем потоке; '
               'потом merge двух отсортированных векторов.',
       'expected': ['true -49999 49999', '[] [1, 2, 3]']},
      {'id': 'r23-histogram-par',
       'mode': 'rust',
       'title': 'Гистограмма: у каждого потока своя копия',
       'statement': 'histogram(data: &[u8], parts: usize) → [usize; 16]: частота значений data[i] % 16. '
                    'Каждый поток заполняет СВОЙ массив [usize; 16] по своему куску, затем массивы '
                    'складываются. Никаких общих счётчиков внутри цикла.',
       'starter': 'use std::thread;\n'
                  '\n'
                  'fn histogram(data: &[u8], parts: usize) -> [usize; 16] {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let data: Vec<u8> = (0..100_000u32).map(|i| (i.wrapping_mul(2654435761) >> 24) as '
                 'u8).collect();\n'
                 '    let h1 = histogram(&data, 1);\n'
                 '    let h8 = histogram(&data, 8);\n'
                 '    println!("{}", h1 == h8);\n'
                 '    println!("{} {:?}", h1.iter().sum::<usize>(), &h1[..4]);\n'
                 '    println!("{:?}", histogram(&[], 3));\n'
                 '    println!("{:?}", histogram(&[1, 17, 33, 2], 2));\n'
                 '}\n',
       'hint': 'Массив [usize; 16] — копируемый тип, его удобно вернуть из потока; суммируйте поэлементно.',
       'expected': ['true',
                    '100000 [6246, 6250, 6251, 6247]',
                    '[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]',
                    '[0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]']},
      {'id': 'r23-poison-recovery',
       'mode': 'rust',
       'title': 'Отравленный мьютекс',
       'statement': 'poison_demo() → (bool, i32, bool): создайте Arc<Mutex<i32>> со значением 10; поток '
                    'берёт замок, делает +5 и паникует; затем: (1) is_poisoned() замка, (2) значение, '
                    'полученное через lock().unwrap_or_else(|e| e.into_inner()), (3) удастся ли после '
                    'clear_poison() обычный lock().is_ok().',
       'starter': 'use std::sync::{Arc, Mutex};\n'
                  'use std::thread;\n'
                  '\n'
                  'fn poison_demo() -> (bool, i32, bool) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    std::panic::set_hook(Box::new(|_| {}));\n'
                 '    println!("{:?}", poison_demo());\n'
                 '}\n',
       'hint': 'PoisonError::into_inner отдаёт охранника даже у отравленного мьютекса; clear_poison снимает '
               'пометку.',
       'expected': ['(true, 15, true)']},
      {'id': 'r23-try-lock',
       'mode': 'rust',
       'title': 'try_lock: без ожидания',
       'statement': 'try_lock_demo() → Vec<bool>: замок Mutex<i32>. Запишите is_ok() последовательности: '
                    'try_lock() на свободном; на занятом (охранник жив в этом же потоке) — в другом потоке '
                    'через scope; в этом потоке после отпускания; затем RwLock: try_write() при живом '
                    'читателе; try_read() при живом читателе.',
       'starter': 'use std::sync::{Mutex, RwLock};\n'
                  'use std::thread;\n'
                  '\n'
                  'fn try_lock_demo() -> Vec<bool> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n    println!("{:?}", try_lock_demo());\n}\n',
       'hint': 'try_lock возвращает Err(WouldBlock), если замок занят; живой охранник — это переменная, не '
               'вызов-выражение.',
       'expected': ['[true, false, true, false, true]']},
      {'id': 'r23-cancel-flag',
       'mode': 'rust',
       'title': 'Отмена потока флагом',
       'statement': 'cancel_demo() → (bool, bool): worker в цикле увеличивает общий AtomicU64 и проверяет '
                    'Arc<AtomicBool> «stop». Главный поток дожидается, пока счётчик станет ≥ 1000, ставит '
                    'stop, join-ит рабочего. Верните (поток завершился, счётчик на момент join ≥ 1000).',
       'starter': 'use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};\n'
                  'use std::sync::Arc;\n'
                  'use std::thread;\n'
                  '\n'
                  'fn cancel_demo() -> (bool, bool) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", cancel_demo());\n'
                 '    println!("{:?}", cancel_demo());\n'
                 '}\n',
       'hint': 'Флаг отмены — AtomicBool в Arc: рабочий читает его в цикле, главный потом выставляет true.',
       'expected': ['(true, true)', '(true, true)']},
      {'id': 'r23-send-bounds',
       'mode': 'rust',
       'title': "Границы Send и 'static",
       'statement': 'run_in_thread<R, F>(f: F) → R запускает замыкание в новом потоке и возвращает результат '
                    "(join). Напишите правильные ограничения: F: FnOnce() → R + Send + 'static, R: Send + "
                    "'static. run_all<R, F>(jobs: Vec<F>) → Vec<R> запускает все параллельно и возвращает "
                    'результаты по порядку.',
       'starter': 'use std::thread;\n'
                  '\n'
                  'fn run_in_thread<R, F>(f: F) -> R {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn run_all<R, F>(jobs: Vec<F>) -> Vec<R> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", run_in_thread(|| 6 * 7));\n'
                 '    let s = String::from("владение");\n'
                 '    println!("{}", run_in_thread(move || s.to_uppercase()));\n'
                 '    println!("{:?}", run_all((1..=5).map(|i| move || i * i).collect()));\n'
                 '    let v = vec![1, 2, 3];\n'
                 '    println!("{:?}", run_all(vec![move || v.iter().sum::<i32>()]));\n'
                 '    println!("{:?}", run_all(Vec::<fn() -> u8>::new()));\n'
                 '}\n',
       'hint': "thread::spawn требует Send + 'static от замыкания и Send + 'static от результата — повторите "
               'эти границы в where.',
       'expected': ['42', 'ВЛАДЕНИЕ', '[1, 4, 9, 16, 25]', '[6]', '[]']},
      {'id': 'r23-named-threads',
       'mode': 'rust',
       'title': 'Именованные потоки и thread_local',
       'statement': 'named_work(n: usize) → Vec<(String, u32)>: запустите n потоков через thread::Builder с '
                    'именами «worker-0», «worker-1», …; в каждом thread_local-счётчик (Cell<u32>) '
                    'увеличивается (i+1) раз; поток возвращает (своё имя через thread::current().name(), '
                    'значение локального счётчика). Результаты — по порядку запуска.',
       'starter': 'use std::cell::Cell;\n'
                  'use std::thread;\n'
                  '\n'
                  'thread_local! {\n'
                  '    static LOCAL: Cell<u32> = Cell::new(0);\n'
                  '}\n'
                  '\n'
                  'fn named_work(n: usize) -> Vec<(String, u32)> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", named_work(4));\n'
                 '    LOCAL.with(|c| c.set(100));\n'
                 '    println!("{:?}", named_work(2));\n'
                 '    println!("{}", LOCAL.with(|c| c.get()));\n'
                 '}\n',
       'hint': 'thread_local даёт каждому потоку собственную копию: изменения в рабочих не видны главному '
               'потоку.',
       'expected': ['[("worker-0", 1), ("worker-1", 2), ("worker-2", 3), ("worker-3", 4)]',
                    '[("worker-0", 1), ("worker-1", 2)]',
                    '100']},
      {'id': 'r23-dining-philosophers',
       'mode': 'rust',
       'title': 'Обедающие философы',
       'statement': 'philosophers(n: usize, meals: usize) → Vec<usize>: n философов за круглым столом, n '
                    'вилок (Mutex<()>). Философ i берёт вилки i и (i+1)%n — НО всегда сначала с меньшим '
                    'номером, чтобы не было deadlock. Каждый «ест» meals раз (увеличивает свой счётчик). '
                    'Верните число приёмов пищи каждого.',
       'starter': 'use std::sync::{Arc, Mutex};\n'
                  'use std::thread;\n'
                  '\n'
                  'fn philosophers(n: usize, meals: usize) -> Vec<usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", philosophers(5, 100));\n'
                 '    println!("{:?}", philosophers(2, 3));\n'
                 '    println!("{:?}", philosophers(1, 4));\n'
                 '    println!("{:?}", philosophers(0, 5));\n'
                 '}\n',
       'hint': 'Сначала вилка с меньшим номером — все философы выстраивают захват в одном порядке, цикла '
               'ожидания нет; при n = 1 обе вилки совпадают.',
       'expected': ['[100, 100, 100, 100, 100]', '[3, 3]', '[4]', '[]']}]}
