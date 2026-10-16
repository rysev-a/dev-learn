"""Задачи книги «Изучаем Rust»: глава 38 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {38: [{'id': 'r38-binary-search',
       'mode': 'rust',
       'title': 'Бинарный поиск со счётчиком шагов',
       'statement': 'Напишите binary_search(v: &[i32], x: i32) -> (Option<usize>, u32): индекс значения в '
                    'отсортированном срезе (любой из подходящих при повторах) и число выполненных сравнений. '
                    'Проверка подаёт миллион элементов и требует не больше 21 шага.',
       'starter': 'fn binary_search(v: &[i32], x: i32) -> (Option<usize>, u32) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?} {:?}", binary_search(&[], 5).0, binary_search(&[5], 5).0);\n'
                 '    let v: Vec<i32> = (0..1_000_000).map(|x| x * 2).collect();\n'
                 '    let mut worst = 0;\n'
                 '    let mut found = 0;\n'
                 '    for x in (0..2_000_000).step_by(7919) {\n'
                 '        let (idx, steps) = binary_search(&v, x);\n'
                 '        worst = worst.max(steps);\n'
                 '        if let Some(i) = idx {\n'
                 '            assert_eq!(v[i], x);\n'
                 '            found += 1;\n'
                 '        }\n'
                 '    }\n'
                 '    println!("{} {}", found, worst <= 21);\n'
                 '    println!("{:?}", binary_search(&v, -1).0);\n'
                 '}\n',
       'expected': ['None Some(0)', '127 true', 'None'],
       'hint': 'Сравнивайте v[mid] с x и сдвигайте границы lo / hi; считайте каждую итерацию цикла.'},
      {'id': 'r38-merge-sort',
       'mode': 'rust',
       'title': 'Сортировка слиянием',
       'statement': 'Напишите merge_sort(v: &[i64]) -> Vec<i64> — устойчивая сортировка слиянием за O(n log '
                    'n). Проверка подаёт 300 000 чисел.',
       'starter': 'fn merge_sort(v: &[i64]) -> Vec<i64> {\n    todo!()\n}\n',
       'driver': 'struct Lcg(u64);\n'
                 'impl Lcg {\n'
                 '    fn next(&mut self) -> u64 {\n'
                 '        self.0 = '
                 'self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n'
                 '        self.0 >> 33\n'
                 '    }\n'
                 '}\n'
                 'fn main() {\n'
                 '    println!("{:?} {:?}", merge_sort(&[]), merge_sort(&[3, 1, 2, 1, -5]));\n'
                 '    let mut rng = Lcg(42);\n'
                 '    let v: Vec<i64> = (0..300_000).map(|_| (rng.next() % 1_000_000) as i64 - '
                 '500_000).collect();\n'
                 '    let sorted = merge_sort(&v);\n'
                 '    let mut expected = v.clone();\n'
                 '    expected.sort();\n'
                 '    println!("{} {}", sorted == expected, sorted.len());\n'
                 '}\n',
       'expected': ['[] [-5, 1, 1, 2, 3]', 'true 300000'],
       'hint': 'split_at делит срез на две части; слияние — два индекса; рекурсия до длины 1.'},
      {'id': 'r38-kth-largest',
       'mode': 'rust',
       'title': 'k-й по величине через кучу',
       'statement': 'Напишите kth_largest(v: &[i32], k: usize) -> Option<i32>: k-й по величине элемент (k = '
                    '1 — максимум; повторы считаются отдельно); None, если k = 0 или k > длины. Память O(k): '
                    'проверка подаёт 2 миллиона чисел.',
       'starter': 'fn kth_largest(v: &[i32], k: usize) -> Option<i32> {\n    todo!()\n}\n',
       'driver': 'struct Lcg(u64);\n'
                 'impl Lcg {\n'
                 '    fn next(&mut self) -> u64 {\n'
                 '        self.0 = '
                 'self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n'
                 '        self.0 >> 33\n'
                 '    }\n'
                 '}\n'
                 'fn main() {\n'
                 '    println!("{:?} {:?} {:?}", kth_largest(&[3, 1, 4, 1, 5, 9, 2, 6], 1), kth_largest(&[3, '
                 '1, 4, 1, 5, 9, 2, 6], 3), kth_largest(&[3, 1, 4, 1, 5, 9, 2, 6], 8));\n'
                 '    println!("{:?} {:?} {:?}", kth_largest(&[1, 2], 0), kth_largest(&[1, 2], 3), '
                 'kth_largest(&[], 1));\n'
                 '    let mut rng = Lcg(7);\n'
                 '    let v: Vec<i32> = (0..2_000_000).map(|_| (rng.next() % 1_000_000_000) as '
                 'i32).collect();\n'
                 '    let mut sorted = v.clone();\n'
                 '    sorted.sort_by(|a, b| b.cmp(a));\n'
                 '    println!("{} {}", kth_largest(&v, 10) == Some(sorted[9]), kth_largest(&v, 1000) == '
                 'Some(sorted[999]));\n'
                 '}\n',
       'expected': ['Some(9) Some(5) Some(1)', 'None None None', 'true true'],
       'hint': 'Куча на k элементов с обёрткой Reverse: после просмотра всех элементов на вершине — k-й по '
               'величине.'},
      {'id': 'r38-grid-bfs',
       'mode': 'rust',
       'title': 'Кратчайший путь в лабиринте',
       'statement': 'Напишите shortest_path(grid: &[&str], start: (usize, usize), goal: (usize, usize)) -> '
                    "Option<usize>: число шагов по клеткам (вверх, вниз, влево, вправо) из start в goal; '#' "
                    "— стена, '.' — свободно. Если пути нет или start/goal — стены — None. Проверка подаёт "
                    'поле 1000×1000.',
       'starter': 'fn shortest_path(grid: &[&str], start: (usize, usize), goal: (usize, usize)) -> '
                  'Option<usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let maze = ["..#....", ".##.##.", "....#..", ".##...#", "...#..."];\n'
                 '    println!("{:?}", shortest_path(&maze, (0, 0), (4, 6)));\n'
                 '    println!("{:?}", shortest_path(&maze, (0, 0), (0, 3)));\n'
                 '    println!("{:?}", shortest_path(&maze, (0, 0), (0, 2)));\n'
                 '    println!("{:?}", shortest_path(&["."], (0, 0), (0, 0)));\n'
                 '    let open: Vec<String> = (0..1000).map(|_| ".".repeat(1000)).collect();\n'
                 '    let refs: Vec<&str> = open.iter().map(|s| s.as_str()).collect();\n'
                 '    println!("{:?}", shortest_path(&refs, (0, 0), (999, 999)));\n'
                 '}\n',
       'expected': ['Some(10)', 'Some(7)', 'None', 'Some(0)', 'Some(1998)'],
       'hint': 'BFS по клеткам: dist — таблица расстояний, usize::MAX — «не посещена»; соседей вычисляйте '
               'осторожно, чтобы не вычесть из нуля.'},
      {'id': 'r38-dijkstra',
       'mode': 'rust',
       'title': 'Дейкстра на большом графе',
       'statement': 'Напишите dijkstra(n: usize, edges: &[(usize, usize, u64)], s: usize) -> '
                    'Vec<Option<u64>>: ориентированные взвешенные рёбра (от, к, вес); расстояния от s (None '
                    '— недостижима). Проверка подаёт 100 000 вершин и 500 000 рёбер.',
       'starter': 'fn dijkstra(n: usize, edges: &[(usize, usize, u64)], s: usize) -> Vec<Option<u64>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'struct Lcg(u64);\n'
                 'impl Lcg {\n'
                 '    fn next(&mut self) -> u64 {\n'
                 '        self.0 = '
                 'self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n'
                 '        self.0 >> 33\n'
                 '    }\n'
                 '}\n'
                 'fn main() {\n'
                 '    let e = [(0, 1, 7), (0, 2, 2), (2, 1, 3), (1, 3, 1), (2, 3, 8)];\n'
                 '    println!("{:?}", dijkstra(5, &e, 0));\n'
                 '    println!("{:?}", dijkstra(1, &[], 0));\n'
                 '    let mut rng = Lcg(99);\n'
                 '    let n = 100_000;\n'
                 '    let edges: Vec<(usize, usize, u64)> = (0..500_000)\n'
                 '        .map(|_| ((rng.next() % n as u64) as usize, (rng.next() % n as u64) as usize, '
                 'rng.next() % 1000 + 1))\n'
                 '        .collect();\n'
                 '    let d = dijkstra(n, &edges, 0);\n'
                 '    let reachable = d.iter().filter(|x| x.is_some()).count();\n'
                 '    let sum: u64 = d.iter().flatten().sum();\n'
                 '    println!("{} {}", reachable, sum);\n'
                 '}\n',
       'expected': ['[Some(0), Some(5), Some(2), Some(6), None]', '[Some(0)]', '99374 206257411'],
       'hint': 'Список смежности + BinaryHeap<Reverse<(u64, usize)>>; устаревшие записи пропускайте при '
               'извлечении.'},
      {'id': 'r38-lcs',
       'mode': 'rust',
       'title': 'LCS на длинных строках',
       'statement': 'Напишите lcs(a: &str, b: &str) -> usize: длина наибольшей общей подпоследовательности '
                    '(по символам). Проверка подаёт две строки по 4000 символов — таблица во всю длину не '
                    'нужна.',
       'starter': 'fn lcs(a: &str, b: &str) -> usize {\n    todo!()\n}\n',
       'driver': 'struct Lcg(u64);\n'
                 'impl Lcg {\n'
                 '    fn next(&mut self) -> u64 {\n'
                 '        self.0 = '
                 'self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n'
                 '        self.0 >> 33\n'
                 '    }\n'
                 '}\n'
                 'fn main() {\n'
                 '    println!("{} {} {}", lcs("abcde", "ace"), lcs("abc", "xyz"), lcs("", "abc"));\n'
                 '    println!("{}", lcs("привет мир", "превед медвед"));\n'
                 '    let mut rng = Lcg(5);\n'
                 "    let a: String = (0..4000).map(|_| (b'a' + (rng.next() % 4) as u8) as char).collect();\n"
                 "    let b: String = (0..4000).map(|_| (b'a' + (rng.next() % 4) as u8) as char).collect();\n"
                 '    println!("{} {}", lcs(&a, &a), lcs(&a, &b));\n'
                 '}\n',
       'expected': ['3 0 0', '6', '4000 2591'],
       'hint': 'Две строки таблицы (prev, cur); строки превратите в Vec<char>, чтобы индексировать символы.'},
      {'id': 'r38-components',
       'mode': 'rust',
       'title': 'Компоненты связности',
       'statement': 'Напишите count_components(n: usize, edges: &[(usize, usize)]) -> usize: число компонент '
                    'связности неориентированного графа (изолированные вершины — отдельные компоненты). '
                    'Проверка: миллион вершин и миллион рёбер.',
       'starter': 'fn count_components(n: usize, edges: &[(usize, usize)]) -> usize {\n    todo!()\n}\n',
       'driver': 'struct Lcg(u64);\n'
                 'impl Lcg {\n'
                 '    fn next(&mut self) -> u64 {\n'
                 '        self.0 = '
                 'self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n'
                 '        self.0 >> 33\n'
                 '    }\n'
                 '}\n'
                 'fn main() {\n'
                 '    println!("{} {} {}", count_components(5, &[(0, 1), (1, 2), (3, 4)]), '
                 'count_components(3, &[]), count_components(0, &[]));\n'
                 '    println!("{}", count_components(4, &[(0, 0), (1, 1)]));\n'
                 '    let mut rng = Lcg(3);\n'
                 '    let n = 1_000_000;\n'
                 '    let edges: Vec<(usize, usize)> = (0..1_000_000).map(|_| ((rng.next() % n as u64) as '
                 'usize, (rng.next() % n as u64) as usize)).collect();\n'
                 '    println!("{}", count_components(n, &edges));\n'
                 '}\n',
       'expected': ['2 3 0', '4', '161915'],
       'hint': 'Union-Find с сжатием путей (итеративным, чтобы не переполнить стек на длинных цепочках).'},
      {'id': 'r38-kruskal',
       'mode': 'rust',
       'title': 'Минимальное остовное дерево',
       'statement': 'Напишите mst_weight(n: usize, edges: &[(usize, usize, u64)]) -> Option<u64>: суммарный '
                    'вес минимального остовного дерева (Краскал) или None, если граф несвязен. n = 0 или 1 — '
                    'вес 0.',
       'starter': 'fn mst_weight(n: usize, edges: &[(usize, usize, u64)]) -> Option<u64> {\n    todo!()\n}\n',
       'driver': 'struct Lcg(u64);\n'
                 'impl Lcg {\n'
                 '    fn next(&mut self) -> u64 {\n'
                 '        self.0 = '
                 'self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n'
                 '        self.0 >> 33\n'
                 '    }\n'
                 '}\n'
                 'fn main() {\n'
                 '    let e = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8)];\n'
                 '    println!("{:?} {:?} {:?}", mst_weight(4, &e), mst_weight(5, &e), mst_weight(1, &[]));\n'
                 '    println!("{:?}", mst_weight(0, &[]));\n'
                 '    let mut rng = Lcg(11);\n'
                 '    let n = 50_000;\n'
                 '    let mut edges: Vec<(usize, usize, u64)> = (1..n).map(|i| (i - 1, i, rng.next() % 1000 '
                 '+ 1)).collect();\n'
                 '    for _ in 0..300_000 {\n'
                 '        edges.push(((rng.next() % n as u64) as usize, (rng.next() % n as u64) as usize, '
                 'rng.next() % 1000 + 1));\n'
                 '    }\n'
                 '    println!("{:?}", mst_weight(n, &edges));\n'
                 '}\n',
       'expected': ['Some(8) None Some(0)', 'Some(0)', 'Some(4271456)'],
       'hint': 'Отсортируйте рёбра по весу и добавляйте те, что соединяют разные компоненты; в остове ровно '
               'n − 1 ребро.'},
      {'id': 'r38-topo',
       'mode': 'rust',
       'title': 'Топологическая сортировка',
       'statement': 'Напишите topo_order(n: usize, edges: &[(usize, usize)]) -> Option<Vec<usize>>: порядок '
                    'вершин 0..n так, чтобы для каждого ребра (a, b) вершина a стояла раньше b; из доступных '
                    'всегда берите вершину с наименьшим номером. При цикле — None.',
       'starter': 'fn topo_order(n: usize, edges: &[(usize, usize)]) -> Option<Vec<usize>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", topo_order(6, &[(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]));\n'
                 '    println!("{:?}", topo_order(3, &[(0, 1), (1, 2), (2, 0)]));\n'
                 '    println!("{:?} {:?}", topo_order(0, &[]), topo_order(3, &[]));\n'
                 '    let n = 200_000;\n'
                 '    let chain: Vec<(usize, usize)> = (1..n).map(|i| (i, i - 1)).collect();\n'
                 '    let r = topo_order(n, &chain).unwrap();\n'
                 '    println!("{} {} {}", r.len(), r[0], r[n - 1]);\n'
                 '}\n',
       'expected': ['Some([4, 5, 0, 2, 3, 1])', 'None', 'Some([]) Some([0, 1, 2])', '200000 199999 0'],
       'hint': 'Алгоритм Кана: степени входа + куча готовых вершин (наименьший номер первым).'},
      {'id': 'r38-safe-arith',
       'mode': 'rust',
       'title': 'Осторожная арифметика',
       'statement': 'Напишите safe_factorial(n: u32) -> Option<u64> (None при переполнении u64), mean_u8(v: '
                    '&[u8]) -> Option<u8> (среднее с округлением вниз, без переполнения; None для пустого) и '
                    'distance(a: usize, b: usize) -> usize (|a − b| без паники).',
       'starter': 'fn safe_factorial(n: u32) -> Option<u64> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn mean_u8(v: &[u8]) -> Option<u8> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn distance(a: usize, b: usize) -> usize {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?} {:?} {:?} {:?}", safe_factorial(0), safe_factorial(5), '
                 'safe_factorial(20), safe_factorial(21));\n'
                 '    println!("{:?} {:?} {:?}", mean_u8(&[255, 255, 254]), mean_u8(&[]), mean_u8(&[1, '
                 '2]));\n'
                 '    println!("{} {} {}", distance(3, 10), distance(10, 3), distance(0, 0));\n'
                 '}\n',
       'expected': ['Some(1) Some(120) Some(2432902008176640000) None', 'Some(254) None Some(1)', '7 7 0'],
       'hint': 'checked_mul возвращает None при переполнении, оператор ? прерывает функцию; сумму u8 копите '
               'в более широком типе.'}]}
