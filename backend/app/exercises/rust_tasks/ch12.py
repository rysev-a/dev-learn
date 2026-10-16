"""Задачи книги «Изучаем Rust»: глава 12 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {12: [{'id': 'r12-last-neg',
       'mode': 'rust',
       'title': 'Отрицательные индексы',
       'statement': 'Python: l[-k]. Напишите from_end(v: &[i32], k: usize) -> Option<i32>: k-й элемент с '
                    'конца (k = 1 — последний). Для k = 0 или k > len — None.',
       'starter': 'fn from_end(v: &[i32], k: usize) -> Option<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let v = [10, 20, 30, 40];\n'
                 '    println!("{:?}", from_end(&v, 1));\n'
                 '    println!("{:?}", from_end(&v, 4));\n'
                 '    println!("{:?}", from_end(&v, 5));\n'
                 '    println!("{:?}", from_end(&v, 0));\n'
                 '}\n',
       'hint': 'Индекс — v.len() - k.',
       'expected': ['Some(40)', 'Some(10)', 'None', 'None']},
      {'id': 'r12-rotate',
       'mode': 'rust',
       'title': 'Циклический сдвиг',
       'statement': 'Python: l[k:] + l[:k]. Напишите rotate_left(v: &[i32], k: usize) -> Vec<i32>: сдвиг '
                    'влево на k (k может быть больше длины).',
       'starter': 'fn rotate_left(v: &[i32], k: usize) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", rotate_left(&[1, 2, 3, 4, 5], 2));\n'
                 '    println!("{:?}", rotate_left(&[1, 2, 3], 7));\n'
                 '    println!("{:?}", rotate_left(&[], 3));\n'
                 '}\n',
       'hint': 'Сначала k %= len, потом склейте два среза.',
       'expected': ['[3, 4, 5, 1, 2]', '[2, 3, 1]', '[]']},
      {'id': 'r12-step',
       'mode': 'rust',
       'title': 'Срез с шагом',
       'statement': 'Python: l[::2]. Напишите every_other(v: &[i32]) -> Vec<i32>: элементы с чётными '
                    'индексами 0, 2, 4, …',
       'starter': 'fn every_other(v: &[i32]) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", every_other(&[1, 2, 3, 4, 5]));\n'
                 '    println!("{:?}", every_other(&[7]));\n'
                 '    println!("{:?}", every_other(&[]));\n'
                 '}\n',
       'hint': 'iter().step_by(2).copied().collect()',
       'expected': ['[1, 3, 5]', '[7]', '[]']},
      {'id': 'r12-remove-value',
       'mode': 'rust',
       'title': 'list.remove(x)',
       'statement': 'Python: l.remove(x) удаляет первое вхождение и бросает ValueError, если нет. Напишите '
                    'remove_first(v: &mut Vec<i32>, x: i32) -> bool: true, если удалили.',
       'starter': 'fn remove_first(v: &mut Vec<i32>, x: i32) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![1, 2, 3, 2];\n'
                 '    println!("{}", remove_first(&mut v, 2));\n'
                 '    println!("{:?}", v);\n'
                 '    println!("{}", remove_first(&mut v, 9));\n'
                 '    println!("{:?}", v);\n'
                 '}\n',
       'hint': 'position даёт индекс первого, remove(i) удаляет его.',
       'expected': ['true', '[1, 3, 2]', 'false', '[1, 3, 2]']},
      {'id': 'r12-remove-all',
       'mode': 'rust',
       'title': 'Удалить все',
       'statement': 'Python: [x for x in l if x != v]. Напишите remove_all(v: &mut Vec<i32>, x: i32) — '
                    'удалить все вхождения за один проход, используя retain.',
       'starter': 'fn remove_all(v: &mut Vec<i32>, x: i32) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![1, 2, 3, 2, 2, 4];\n'
                 '    remove_all(&mut v, 2);\n'
                 '    println!("{:?}", v);\n'
                 '    remove_all(&mut v, 9);\n'
                 '    println!("{:?}", v);\n'
                 '}\n',
       'hint': 'v.retain(|&e| e != x)',
       'expected': ['[1, 3, 4]', '[1, 3, 4]']},
      {'id': 'r12-dedup-order',
       'mode': 'rust',
       'title': 'Уникальные с порядком',
       'statement': 'Python: list(dict.fromkeys(l)). Напишите unique(v: &[i32]) -> Vec<i32>: убрать повторы, '
                    'сохранив порядок первых вхождений. Без HashSet (только вектор и contains).',
       'starter': 'fn unique(v: &[i32]) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", unique(&[3, 1, 3, 2, 1, 2]));\n'
                 '    println!("{:?}", unique(&[]));\n'
                 '    println!("{:?}", unique(&[5, 5, 5]));\n'
                 '}\n',
       'hint': 'Проверяйте out.contains(&x) перед push.',
       'expected': ['[3, 1, 2]', '[]', '[5]']},
      {'id': 'r12-chunks',
       'mode': 'rust',
       'title': 'Пачки',
       'statement': 'Напишите batches(v: &[i32], n: usize) -> Vec<Vec<i32>>: разбейте на пачки по n '
                    'элементов (последняя может быть короче), n > 0. Используйте chunks.',
       'starter': 'fn batches(v: &[i32], n: usize) -> Vec<Vec<i32>> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", batches(&[1, 2, 3, 4, 5, 6, 7], 3));\n'
                 '    println!("{:?}", batches(&[1, 2], 5));\n'
                 '    println!("{:?}", batches(&[], 2));\n'
                 '}\n',
       'hint': 'v.chunks(n).map(|c| c.to_vec()).collect()',
       'expected': ['[[1, 2, 3], [4, 5, 6], [7]]', '[[1, 2]]', '[]']},
      {'id': 'r12-windows',
       'mode': 'rust',
       'title': 'Скользящее окно',
       'statement': 'Напишите moving_sums(v: &[i32], k: usize) -> Vec<i32>: суммы всех окон из k подряд '
                    'идущих элементов (k > 0). Используйте windows.',
       'starter': 'fn moving_sums(v: &[i32], k: usize) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", moving_sums(&[1, 2, 3, 4, 5], 3));\n'
                 '    println!("{:?}", moving_sums(&[1, 2], 3));\n'
                 '    println!("{:?}", moving_sums(&[4], 1));\n'
                 '}\n',
       'hint': 'windows(k) выдаёт срезы длины k.',
       'expected': ['[6, 9, 12]', '[]', '[4]']},
      {'id': 'r12-is-sorted',
       'mode': 'rust',
       'title': 'Отсортирован ли',
       'statement': 'Напишите is_sorted(v: &[i32]) -> bool: элементы не убывают. Используйте windows(2).',
       'starter': 'fn is_sorted(v: &[i32]) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", is_sorted(&[1, 2, 2, 5]));\n'
                 '    println!("{}", is_sorted(&[1, 3, 2]));\n'
                 '    println!("{}", is_sorted(&[]));\n'
                 '    println!("{}", is_sorted(&[9]));\n'
                 '}\n',
       'hint': 'all для пустой последовательности — true.',
       'expected': ['true', 'false', 'true', 'true']},
      {'id': 'r12-sort-desc',
       'mode': 'rust',
       'title': 'sorted(reverse=True)',
       'statement': 'Python: sorted(l, reverse=True). Напишите sorted_desc(v: &[i32]) -> Vec<i32> — '
                    'отсортированная копия по убыванию; исходный срез не меняется.',
       'starter': 'fn sorted_desc(v: &[i32]) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let a = [3, 1, 4, 1, 5];\n'
                 '    println!("{:?}", sorted_desc(&a));\n'
                 '    println!("{:?}", a);\n'
                 '}\n',
       'hint': 'to_vec() и sort_by(|a, b| b.cmp(a))',
       'expected': ['[5, 4, 3, 1, 1]', '[3, 1, 4, 1, 5]']},
      {'id': 'r12-sort-key',
       'mode': 'rust',
       'title': 'key=len',
       'statement': 'Python: sorted(words, key=len). Напишите by_len(words: &[&str]) -> Vec<String>: слова '
                    'по возрастанию длины в символах; при равной длине — в исходном порядке.',
       'starter': 'fn by_len(words: &[&str]) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", by_len(&["ccc", "a", "bb", "dd", "e"]));\n'
                 '    println!("{:?}", by_len(&["привет", "мир", "я"]));\n'
                 '}\n',
       'hint': 'sort_by_key устойчива.',
       'expected': ['["a", "e", "bb", "dd", "ccc"]', '["я", "мир", "привет"]']},
      {'id': 'r12-top-k',
       'mode': 'rust',
       'title': 'Топ-k',
       'statement': 'Python: sorted(l, reverse=True)[:k]. Напишите top_k(v: &[i32], k: usize) -> Vec<i32>: k '
                    'наибольших по убыванию (если элементов меньше — все).',
       'starter': 'fn top_k(v: &[i32], k: usize) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", top_k(&[5, 1, 9, 3, 7], 3));\n'
                 '    println!("{:?}", top_k(&[2, 1], 5));\n'
                 '    println!("{:?}", top_k(&[4, 4, 1], 2));\n'
                 '}\n',
       'hint': 'sort_by, затем truncate(k).',
       'expected': ['[9, 7, 5]', '[2, 1]', '[4, 4]']},
      {'id': 'r12-binary-search',
       'mode': 'rust',
       'title': 'bisect',
       'statement': 'Python: bisect.bisect_left(l, x). Напишите insert_pos(v: &[i32], x: i32) -> usize: '
                    'позиция, куда вставить x, чтобы сохранить порядок (слева от равных). Срез отсортирован. '
                    'Используйте partition_point.',
       'starter': 'fn insert_pos(v: &[i32], x: i32) -> usize {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let v = [1, 3, 3, 5, 8];\n'
                 '    println!("{}", insert_pos(&v, 0));\n'
                 '    println!("{}", insert_pos(&v, 3));\n'
                 '    println!("{}", insert_pos(&v, 4));\n'
                 '    println!("{}", insert_pos(&v, 9));\n'
                 '}\n',
       'hint': 'partition_point(|&e| e < x)',
       'expected': ['0', '1', '3', '5']},
      {'id': 'r12-zip-pairs',
       'mode': 'rust',
       'title': 'zip',
       'statement': 'Python: list(zip(a, b)). Напишите pairs(a: &[i32], b: &[&str]) -> Vec<(i32, String)>: '
                    'пары по короткому из двух срезов.',
       'starter': 'fn pairs(a: &[i32], b: &[&str]) -> Vec<(i32, String)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", pairs(&[1, 2, 3], &["a", "b"]));\n'
                 '    println!("{:?}", pairs(&[], &["a"]));\n'
                 '}\n',
       'hint': 'a.iter().zip(b.iter())',
       'expected': ['[(1, "a"), (2, "b")]', '[]']},
      {'id': 'r12-enumerate-rev',
       'mode': 'rust',
       'title': 'Индексы с конца',
       'statement': 'Напишите last_index_of(v: &[i32], x: i32) -> Option<usize>: индекс последнего вхождения '
                    'x или None. Используйте iter().rposition.',
       'starter': 'fn last_index_of(v: &[i32], x: i32) -> Option<usize> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", last_index_of(&[1, 2, 3, 2, 1], 2));\n'
                 '    println!("{:?}", last_index_of(&[1, 2], 5));\n'
                 '    println!("{:?}", last_index_of(&[], 1));\n'
                 '}\n',
       'hint': 'rposition ищет с конца.',
       'expected': ['Some(3)', 'None', 'None']},
      {'id': 'r12-flatten',
       'mode': 'rust',
       'title': 'Склеить списки',
       'statement': 'Python: [x for row in rows for x in row]. Напишите flatten(rows: &[Vec<i32>]) -> '
                    'Vec<i32>.',
       'starter': 'fn flatten(rows: &[Vec<i32>]) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", flatten(&[vec![1, 2], vec![], vec![3]]));\n'
                 '    println!("{:?}", flatten(&[]));\n'
                 '}\n',
       'hint': 'rows.iter().flatten().copied().collect()',
       'expected': ['[1, 2, 3]', '[]']},
      {'id': 'r12-transpose',
       'mode': 'rust',
       'title': 'Транспонирование',
       'statement': 'Python: list(zip(*m)). Напишите transpose(m: &[Vec<i32>]) -> Vec<Vec<i32>> для '
                    'прямоугольной матрицы (все строки одной длины; пустая матрица → пустая).',
       'starter': 'fn transpose(m: &[Vec<i32>]) -> Vec<Vec<i32>> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", transpose(&[vec![1, 2, 3], vec![4, 5, 6]]));\n'
                 '    println!("{:?}", transpose(&[vec![7]]));\n'
                 '    println!("{:?}", transpose(&[]));\n'
                 '}\n',
       'hint': 't[j][i] = m[i][j]',
       'expected': ['[[1, 4], [2, 5], [3, 6]]', '[[7]]', '[]']},
      {'id': 'r12-grid-trap',
       'mode': 'rust',
       'title': 'Ловушка [[0]*n]*m',
       'statement': 'Напишите make_grid(rows: usize, cols: usize) -> Vec<Vec<i32>>, заполненную нулями; '
                    'строки независимы. После вызова driver меняет ячейку, и меняется только одна строка.',
       'starter': 'fn make_grid(rows: usize, cols: usize) -> Vec<Vec<i32>> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut g = make_grid(2, 3);\n'
                 '    g[0][1] = 7;\n'
                 '    println!("{:?}", g);\n'
                 '    println!("{:?}", make_grid(0, 5));\n'
                 '}\n',
       'hint': 'vec![vec![0; cols]; rows]',
       'expected': ['[[0, 7, 0], [0, 0, 0]]', '[]']},
      {'id': 'r12-flat-index',
       'mode': 'rust',
       'title': 'Плоская матрица',
       'statement': 'Матрица хранится одним вектором построчно, ширина w. Напишите get(m: &[i32], w: usize, '
                    'row: usize, col: usize) -> Option<i32>: элемент или None, если вне границ (col ≥ w или '
                    'индекс за концом).',
       'starter': 'fn get(m: &[i32], w: usize, row: usize, col: usize) -> Option<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let m = [1, 2, 3, 4, 5, 6];\n'
                 '    println!("{:?}", get(&m, 3, 1, 2));\n'
                 '    println!("{:?}", get(&m, 3, 2, 0));\n'
                 '    println!("{:?}", get(&m, 3, 0, 3));\n'
                 '    println!("{:?}", get(&m, 3, 0, 0));\n'
                 '}\n',
       'hint': 'Индекс row * w + col; проверьте col < w отдельно.',
       'expected': ['Some(6)', 'None', 'None', 'Some(1)']},
      {'id': 'r12-stack-brackets',
       'mode': 'rust',
       'title': 'Стек скобок',
       'statement': 'Напишите balanced(s: &str) -> bool: правильна ли расстановка скобок ()[]{} (Vec как '
                    'стек).',
       'starter': 'fn balanced(s: &str) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for s in ["([]{})", "([)]", "((", "", "a(b)c", ")("] {\n'
                 '        println!("{:?} {}", s, balanced(s));\n'
                 '    }\n'
                 '}\n',
       'hint': 'push открывающих, pop и сравнение при закрывающих.',
       'expected': ['"([]{})" true', '"([)]" false', '"((" false', '"" true', '"a(b)c" true', '")(" false']},
      {'id': 'r12-queue',
       'mode': 'rust',
       'title': 'Очередь на VecDeque',
       'statement': 'Напишите josephus(n: usize, k: usize) -> usize: задача Иосифа Флавия — n человек по '
                    'кругу, каждый k-й выбывает; вернуть номер (с 1) последнего оставшегося. Используйте '
                    'VecDeque.',
       'starter': 'fn josephus(n: usize, k: usize) -> usize {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", josephus(7, 3));\n'
                 '    println!("{}", josephus(1, 5));\n'
                 '    println!("{}", josephus(10, 2));\n'
                 '    println!("{}", josephus(5000, 7));\n'
                 '}\n',
       'hint': 'k - 1 раз переносим из начала в конец, затем удаляем.',
       'expected': ['4', '1', '5', '4173']},
      {'id': 'r12-bfs-grid',
       'mode': 'rust',
       'title': 'Кратчайший путь по сетке',
       'statement': "Напишите shortest(grid: &[&str]) -> Option<usize>: длина кратчайшего пути из 'S' в 'E' "
                    "по клеткам '.' (вверх, вниз, влево, вправо), '#' — стена. None, если пути нет. Поиск в "
                    'ширину на VecDeque.',
       'starter': 'fn shortest(grid: &[&str]) -> Option<usize> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", shortest(&["S.#", "..#", "#.E"]));\n'
                 '    println!("{:?}", shortest(&["S#E"]));\n'
                 '    println!("{:?}", shortest(&["SE"]));\n'
                 '}\n',
       'hint': 'dist хранит расстояния; очередь VecDeque из клеток.',
       'expected': ['Some(4)', 'None', 'Some(1)']},
      {'id': 'r12-heap-kth',
       'mode': 'rust',
       'title': 'k-е по величине',
       'statement': 'Python: heapq.nlargest(k, l)[-1]. Напишите kth_largest(v: &[i32], k: usize) -> '
                    'Option<i32>: k-е по величине (k = 1 — наибольшее) через BinaryHeap. None, если k = 0 '
                    'или k > len.',
       'starter': 'fn kth_largest(v: &[i32], k: usize) -> Option<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", kth_largest(&[3, 1, 4, 1, 5, 9, 2, 6], 3));\n'
                 '    println!("{:?}", kth_largest(&[1], 2));\n'
                 '    println!("{:?}", kth_largest(&[5, 5], 2));\n'
                 '}\n',
       'hint': 'BinaryHeap — куча-максимум; pop даёт наибольшее.',
       'expected': ['Some(5)', 'None', 'Some(5)']},
      {'id': 'r12-capacity',
       'mode': 'rust',
       'title': 'Ёмкость вектора',
       'statement': 'Напишите growth(n: usize) -> Vec<usize>: создайте пустой Vec<u8>, добавьте n элементов '
                    'и запишите в результат значение capacity() каждый раз, когда оно меняется (без повторов '
                    'подряд). Для первых n = 20 результат будет строго возрастающим.',
       'starter': 'fn growth(n: usize) -> Vec<usize> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let g = growth(100);\n'
                 '    println!("{}", g.windows(2).all(|w| w[0] < w[1]));\n'
                 '    println!("{}", g[0] >= 1);\n'
                 '    println!("{}", *g.last().unwrap() >= 100);\n'
                 '}\n',
       'hint': 'Запоминайте capacity после каждого push и сравнивайте с последним.',
       'expected': ['true', 'true', 'true']},
      {'id': 'r12-split-at',
       'mode': 'rust',
       'title': 'Разделить пополам',
       'statement': 'Напишите halves(v: &[i32]) -> (Vec<i32>, Vec<i32>): левая половина (длина len / 2) и '
                    'правая (остальное). Используйте split_at.',
       'starter': 'fn halves(v: &[i32]) -> (Vec<i32>, Vec<i32>) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", halves(&[1, 2, 3, 4, 5]));\n'
                 '    println!("{:?}", halves(&[1, 2]));\n'
                 '    println!("{:?}", halves(&[]));\n'
                 '}\n',
       'hint': 'split_at(mid) возвращает два среза.',
       'expected': ['([1, 2], [3, 4, 5])', '([1], [2])', '([], [])']},
      {'id': 'r12-drain',
       'mode': 'rust',
       'title': 'Вынуть диапазон',
       'statement': 'Напишите cut(v: &mut Vec<i32>, a: usize, b: usize) -> Vec<i32>: удалить элементы a..b '
                    'из v и вернуть их (drain).',
       'starter': 'fn cut(v: &mut Vec<i32>, a: usize, b: usize) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![0, 1, 2, 3, 4, 5];\n'
                 '    let d = cut(&mut v, 1, 4);\n'
                 '    println!("{:?} {:?}", d, v);\n'
                 '    let e = cut(&mut v, 0, 0);\n'
                 '    println!("{:?} {:?}", e, v);\n'
                 '}\n',
       'hint': 'v.drain(a..b).collect()',
       'expected': ['[1, 2, 3] [0, 4, 5]', '[] [0, 4, 5]']},
      {'id': 'r12-argmax',
       'mode': 'rust',
       'title': 'Индекс максимума',
       'statement': 'Python: l.index(max(l)). Напишите argmax(v: &[i32]) -> Option<usize>: индекс первого '
                    'наибольшего элемента или None для пустого среза.',
       'starter': 'fn argmax(v: &[i32]) -> Option<usize> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", argmax(&[3, 9, 2, 9]));\n'
                 '    println!("{:?}", argmax(&[-5]));\n'
                 '    println!("{:?}", argmax(&[]));\n'
                 '}\n',
       'hint': 'Строгое сравнение сохранит индекс первого.',
       'expected': ['Some(1)', 'Some(0)', 'None']},
      {'id': 'r12-prefix-sums',
       'mode': 'rust',
       'title': 'Префиксные суммы',
       'statement': 'Python: list(itertools.accumulate(l)). Напишите prefix_sums(v: &[i32]) -> Vec<i32>: '
                    'частичные суммы (i-й элемент — сумма первых i + 1).',
       'starter': 'fn prefix_sums(v: &[i32]) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", prefix_sums(&[1, 2, 3, 4]));\n'
                 '    println!("{:?}", prefix_sums(&[5, -5, 5]));\n'
                 '    println!("{:?}", prefix_sums(&[]));\n'
                 '}\n',
       'hint': 'Замыкание может менять внешнюю переменную s.',
       'expected': ['[1, 3, 6, 10]', '[5, 0, 5]', '[]']},
      {'id': 'r12-two-sum',
       'mode': 'rust',
       'title': 'Два числа с суммой',
       'statement': 'Напишите two_sum(v: &[i32], target: i32) -> Option<(usize, usize)>: индексы i < j, для '
                    'которых v[i] + v[j] = target (первая найденная пара при переборе i, затем j).',
       'starter': 'fn two_sum(v: &[i32], target: i32) -> Option<(usize, usize)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", two_sum(&[2, 7, 11, 15], 9));\n'
                 '    println!("{:?}", two_sum(&[3, 2, 4], 6));\n'
                 '    println!("{:?}", two_sum(&[1, 2], 10));\n'
                 '}\n',
       'hint': 'Два вложенных цикла, j начинается с i + 1.',
       'expected': ['Some((0, 1))', 'Some((1, 2))', 'None']},
      {'id': 'r12-merge',
       'mode': 'rust',
       'title': 'Слияние отсортированных',
       'statement': 'Напишите merge(a: &[i32], b: &[i32]) -> Vec<i32>: слейте два отсортированных среза в '
                    'один отсортированный вектор за линейное время (двумя индексами).',
       'starter': 'fn merge(a: &[i32], b: &[i32]) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", merge(&[1, 3, 5], &[2, 4, 6, 8]));\n'
                 '    println!("{:?}", merge(&[], &[1]));\n'
                 '    println!("{:?}", merge(&[1, 1], &[1]));\n'
                 '}\n',
       'hint': 'После цикла допишите хвосты обоих срезов.',
       'expected': ['[1, 2, 3, 4, 5, 6, 8]', '[1]', '[1, 1, 1]']}]}
