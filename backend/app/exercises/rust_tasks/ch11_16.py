"""Задачи книги «Изучаем Rust»: главы 11–16."""

TASKS: dict[int, list[dict]] = {
    11: [
        {
            "id": "rs11-binary-search",
            "mode": "rust",
            "title": "Бинарный поиск со счётчиком шагов",
            "statement": (
                "Напишите binary_search(v: &[i32], x: i32) -> (Option<usize>, u32): "
                "индекс значения в отсортированном срезе (любой из подходящих при "
                "повторах) и число выполненных сравнений. Проверка подаёт миллион "
                "элементов и требует не больше 21 шага."
            ),
            "starter": "fn binary_search(v: &[i32], x: i32) -> (Option<usize>, u32) {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?} {:?}\", binary_search(&[], 5).0, binary_search(&[5], 5).0);\n"
                "    let v: Vec<i32> = (0..1_000_000).map(|x| x * 2).collect();\n"
                "    let mut worst = 0;\n"
                "    let mut found = 0;\n"
                "    for x in (0..2_000_000).step_by(7919) {\n"
                "        let (idx, steps) = binary_search(&v, x);\n"
                "        worst = worst.max(steps);\n"
                "        if let Some(i) = idx {\n"
                "            assert_eq!(v[i], x);\n"
                "            found += 1;\n"
                "        }\n"
                "    }\n"
                "    println!(\"{} {}\", found, worst <= 21);\n"
                "    println!(\"{:?}\", binary_search(&v, -1).0);\n"
                "}\n"
            ),
            "expected": ["None Some(0)", "127 true", "None"],
            "hint": "Сравнивайте v[mid] с x и сдвигайте границы lo / hi; считайте каждую итерацию цикла.",
        },
        {
            "id": "rs11-merge-sort",
            "mode": "rust",
            "title": "Сортировка слиянием",
            "statement": (
                "Напишите merge_sort(v: &[i64]) -> Vec<i64> — устойчивая сортировка "
                "слиянием за O(n log n). Проверка подаёт 300 000 чисел."
            ),
            "starter": "fn merge_sort(v: &[i64]) -> Vec<i64> {\n    todo!()\n}\n",
            "driver": (
                "struct Lcg(u64);\n"
                "impl Lcg {\n"
                "    fn next(&mut self) -> u64 {\n"
                "        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n"
                "        self.0 >> 33\n"
                "    }\n"
                "}\n"
                "fn main() {\n"
                "    println!(\"{:?} {:?}\", merge_sort(&[]), merge_sort(&[3, 1, 2, 1, -5]));\n"
                "    let mut rng = Lcg(42);\n"
                "    let v: Vec<i64> = (0..300_000).map(|_| (rng.next() % 1_000_000) as i64 - 500_000).collect();\n"
                "    let sorted = merge_sort(&v);\n"
                "    let mut expected = v.clone();\n"
                "    expected.sort();\n"
                "    println!(\"{} {}\", sorted == expected, sorted.len());\n"
                "}\n"
            ),
            "expected": ["[] [-5, 1, 1, 2, 3]", "true 300000"],
            "hint": "split_at делит срез на две части; слияние — два индекса; рекурсия до длины 1.",
        },
        {
            "id": "rs11-kth-largest",
            "mode": "rust",
            "title": "k-й по величине через кучу",
            "statement": (
                "Напишите kth_largest(v: &[i32], k: usize) -> Option<i32>: k-й по "
                "величине элемент (k = 1 — максимум; повторы считаются отдельно); "
                "None, если k = 0 или k > длины. Память O(k): проверка подаёт 2 "
                "миллиона чисел."
            ),
            "starter": "fn kth_largest(v: &[i32], k: usize) -> Option<i32> {\n    todo!()\n}\n",
            "driver": (
                "struct Lcg(u64);\n"
                "impl Lcg {\n"
                "    fn next(&mut self) -> u64 {\n"
                "        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n"
                "        self.0 >> 33\n"
                "    }\n"
                "}\n"
                "fn main() {\n"
                "    println!(\"{:?} {:?} {:?}\", kth_largest(&[3, 1, 4, 1, 5, 9, 2, 6], 1), kth_largest(&[3, 1, 4, 1, 5, 9, 2, 6], 3), kth_largest(&[3, 1, 4, 1, 5, 9, 2, 6], 8));\n"
                "    println!(\"{:?} {:?} {:?}\", kth_largest(&[1, 2], 0), kth_largest(&[1, 2], 3), kth_largest(&[], 1));\n"
                "    let mut rng = Lcg(7);\n"
                "    let v: Vec<i32> = (0..2_000_000).map(|_| (rng.next() % 1_000_000_000) as i32).collect();\n"
                "    let mut sorted = v.clone();\n"
                "    sorted.sort_by(|a, b| b.cmp(a));\n"
                "    println!(\"{} {}\", kth_largest(&v, 10) == Some(sorted[9]), kth_largest(&v, 1000) == Some(sorted[999]));\n"
                "}\n"
            ),
            "expected": ["Some(9) Some(5) Some(1)", "None None None", "true true"],
            "hint": "Куча на k элементов с обёрткой Reverse: после просмотра всех элементов на вершине — k-й по величине.",
        },
        {
            "id": "rs11-grid-bfs",
            "mode": "rust",
            "title": "Кратчайший путь в лабиринте",
            "statement": (
                "Напишите shortest_path(grid: &[&str], start: (usize, usize), goal: "
                "(usize, usize)) -> Option<usize>: число шагов по клеткам (вверх, "
                "вниз, влево, вправо) из start в goal; '#' — стена, '.' — свободно. "
                "Если пути нет или start/goal — стены — None. Проверка подаёт поле "
                "1000×1000."
            ),
            "starter": "fn shortest_path(grid: &[&str], start: (usize, usize), goal: (usize, usize)) -> Option<usize> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let maze = [\"..#....\", \".##.##.\", \"....#..\", \".##...#\", \"...#...\"];\n"
                "    println!(\"{:?}\", shortest_path(&maze, (0, 0), (4, 6)));\n"
                "    println!(\"{:?}\", shortest_path(&maze, (0, 0), (0, 3)));\n"
                "    println!(\"{:?}\", shortest_path(&maze, (0, 0), (0, 2)));\n"
                "    println!(\"{:?}\", shortest_path(&[\".\"], (0, 0), (0, 0)));\n"
                "    let open: Vec<String> = (0..1000).map(|_| \".\".repeat(1000)).collect();\n"
                "    let refs: Vec<&str> = open.iter().map(|s| s.as_str()).collect();\n"
                "    println!(\"{:?}\", shortest_path(&refs, (0, 0), (999, 999)));\n"
                "}\n"
            ),
            "expected": ["Some(10)", "Some(7)", "None", "Some(0)", "Some(1998)"],
            "hint": "BFS по клеткам: dist — таблица расстояний, usize::MAX — «не посещена»; соседей вычисляйте осторожно, чтобы не вычесть из нуля.",
        },
        {
            "id": "rs11-dijkstra",
            "mode": "rust",
            "title": "Дейкстра на большом графе",
            "statement": (
                "Напишите dijkstra(n: usize, edges: &[(usize, usize, u64)], s: "
                "usize) -> Vec<Option<u64>>: ориентированные взвешенные рёбра (от, "
                "к, вес); расстояния от s (None — недостижима). Проверка подаёт 100 "
                "000 вершин и 500 000 рёбер."
            ),
            "starter": "fn dijkstra(n: usize, edges: &[(usize, usize, u64)], s: usize) -> Vec<Option<u64>> {\n    todo!()\n}\n",
            "driver": (
                "struct Lcg(u64);\n"
                "impl Lcg {\n"
                "    fn next(&mut self) -> u64 {\n"
                "        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n"
                "        self.0 >> 33\n"
                "    }\n"
                "}\n"
                "fn main() {\n"
                "    let e = [(0, 1, 7), (0, 2, 2), (2, 1, 3), (1, 3, 1), (2, 3, 8)];\n"
                "    println!(\"{:?}\", dijkstra(5, &e, 0));\n"
                "    println!(\"{:?}\", dijkstra(1, &[], 0));\n"
                "    let mut rng = Lcg(99);\n"
                "    let n = 100_000;\n"
                "    let edges: Vec<(usize, usize, u64)> = (0..500_000)\n"
                "        .map(|_| ((rng.next() % n as u64) as usize, (rng.next() % n as u64) as usize, rng.next() % 1000 + 1))\n"
                "        .collect();\n"
                "    let d = dijkstra(n, &edges, 0);\n"
                "    let reachable = d.iter().filter(|x| x.is_some()).count();\n"
                "    let sum: u64 = d.iter().flatten().sum();\n"
                "    println!(\"{} {}\", reachable, sum);\n"
                "}\n"
            ),
            "expected": ["[Some(0), Some(5), Some(2), Some(6), None]", "[Some(0)]", "99374 206257411"],
            "hint": "Список смежности + BinaryHeap<Reverse<(u64, usize)>>; устаревшие записи пропускайте при извлечении.",
        },
        {
            "id": "rs11-lcs",
            "mode": "rust",
            "title": "LCS на длинных строках",
            "statement": (
                "Напишите lcs(a: &str, b: &str) -> usize: длина наибольшей общей "
                "подпоследовательности (по символам). Проверка подаёт две строки по "
                "4000 символов — таблица во всю длину не нужна."
            ),
            "starter": "fn lcs(a: &str, b: &str) -> usize {\n    todo!()\n}\n",
            "driver": (
                "struct Lcg(u64);\n"
                "impl Lcg {\n"
                "    fn next(&mut self) -> u64 {\n"
                "        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n"
                "        self.0 >> 33\n"
                "    }\n"
                "}\n"
                "fn main() {\n"
                "    println!(\"{} {} {}\", lcs(\"abcde\", \"ace\"), lcs(\"abc\", \"xyz\"), lcs(\"\", \"abc\"));\n"
                "    println!(\"{}\", lcs(\"привет мир\", \"превед медвед\"));\n"
                "    let mut rng = Lcg(5);\n"
                "    let a: String = (0..4000).map(|_| (b'a' + (rng.next() % 4) as u8) as char).collect();\n"
                "    let b: String = (0..4000).map(|_| (b'a' + (rng.next() % 4) as u8) as char).collect();\n"
                "    println!(\"{} {}\", lcs(&a, &a), lcs(&a, &b));\n"
                "}\n"
            ),
            "expected": ["3 0 0", "6", "4000 2591"],
            "hint": "Две строки таблицы (prev, cur); строки превратите в Vec<char>, чтобы индексировать символы.",
        },
        {
            "id": "rs11-components",
            "mode": "rust",
            "title": "Компоненты связности",
            "statement": (
                "Напишите count_components(n: usize, edges: &[(usize, usize)]) -> "
                "usize: число компонент связности неориентированного графа "
                "(изолированные вершины — отдельные компоненты). Проверка: миллион "
                "вершин и миллион рёбер."
            ),
            "starter": "fn count_components(n: usize, edges: &[(usize, usize)]) -> usize {\n    todo!()\n}\n",
            "driver": (
                "struct Lcg(u64);\n"
                "impl Lcg {\n"
                "    fn next(&mut self) -> u64 {\n"
                "        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n"
                "        self.0 >> 33\n"
                "    }\n"
                "}\n"
                "fn main() {\n"
                "    println!(\"{} {} {}\", count_components(5, &[(0, 1), (1, 2), (3, 4)]), count_components(3, &[]), count_components(0, &[]));\n"
                "    println!(\"{}\", count_components(4, &[(0, 0), (1, 1)]));\n"
                "    let mut rng = Lcg(3);\n"
                "    let n = 1_000_000;\n"
                "    let edges: Vec<(usize, usize)> = (0..1_000_000).map(|_| ((rng.next() % n as u64) as usize, (rng.next() % n as u64) as usize)).collect();\n"
                "    println!(\"{}\", count_components(n, &edges));\n"
                "}\n"
            ),
            "expected": ["2 3 0", "4", "161915"],
            "hint": "Union-Find с сжатием путей (итеративным, чтобы не переполнить стек на длинных цепочках).",
        },
        {
            "id": "rs11-kruskal",
            "mode": "rust",
            "title": "Минимальное остовное дерево",
            "statement": (
                "Напишите mst_weight(n: usize, edges: &[(usize, usize, u64)]) -> "
                "Option<u64>: суммарный вес минимального остовного дерева (Краскал) "
                "или None, если граф несвязен. n = 0 или 1 — вес 0."
            ),
            "starter": "fn mst_weight(n: usize, edges: &[(usize, usize, u64)]) -> Option<u64> {\n    todo!()\n}\n",
            "driver": (
                "struct Lcg(u64);\n"
                "impl Lcg {\n"
                "    fn next(&mut self) -> u64 {\n"
                "        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n"
                "        self.0 >> 33\n"
                "    }\n"
                "}\n"
                "fn main() {\n"
                "    let e = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8)];\n"
                "    println!(\"{:?} {:?} {:?}\", mst_weight(4, &e), mst_weight(5, &e), mst_weight(1, &[]));\n"
                "    println!(\"{:?}\", mst_weight(0, &[]));\n"
                "    let mut rng = Lcg(11);\n"
                "    let n = 50_000;\n"
                "    let mut edges: Vec<(usize, usize, u64)> = (1..n).map(|i| (i - 1, i, rng.next() % 1000 + 1)).collect();\n"
                "    for _ in 0..300_000 {\n"
                "        edges.push(((rng.next() % n as u64) as usize, (rng.next() % n as u64) as usize, rng.next() % 1000 + 1));\n"
                "    }\n"
                "    println!(\"{:?}\", mst_weight(n, &edges));\n"
                "}\n"
            ),
            "expected": ["Some(8) None Some(0)", "Some(0)", "Some(4271456)"],
            "hint": "Отсортируйте рёбра по весу и добавляйте те, что соединяют разные компоненты; в остове ровно n − 1 ребро.",
        },
        {
            "id": "rs11-topo",
            "mode": "rust",
            "title": "Топологическая сортировка",
            "statement": (
                "Напишите topo_order(n: usize, edges: &[(usize, usize)]) -> "
                "Option<Vec<usize>>: порядок вершин 0..n так, чтобы для каждого "
                "ребра (a, b) вершина a стояла раньше b; из доступных всегда берите "
                "вершину с наименьшим номером. При цикле — None."
            ),
            "starter": "fn topo_order(n: usize, edges: &[(usize, usize)]) -> Option<Vec<usize>> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", topo_order(6, &[(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]));\n"
                "    println!(\"{:?}\", topo_order(3, &[(0, 1), (1, 2), (2, 0)]));\n"
                "    println!(\"{:?} {:?}\", topo_order(0, &[]), topo_order(3, &[]));\n"
                "    let n = 200_000;\n"
                "    let chain: Vec<(usize, usize)> = (1..n).map(|i| (i, i - 1)).collect();\n"
                "    let r = topo_order(n, &chain).unwrap();\n"
                "    println!(\"{} {} {}\", r.len(), r[0], r[n - 1]);\n"
                "}\n"
            ),
            "expected": ["Some([4, 5, 0, 2, 3, 1])", "None", "Some([]) Some([0, 1, 2])", "200000 199999 0"],
            "hint": "Алгоритм Кана: степени входа + куча готовых вершин (наименьший номер первым).",
        },
        {
            "id": "rs11-safe-arith",
            "mode": "rust",
            "title": "Осторожная арифметика",
            "statement": (
                "Напишите safe_factorial(n: u32) -> Option<u64> (None при "
                "переполнении u64), mean_u8(v: &[u8]) -> Option<u8> (среднее с "
                "округлением вниз, без переполнения; None для пустого) и "
                "distance(a: usize, b: usize) -> usize (|a − b| без паники)."
            ),
            "starter": "fn safe_factorial(n: u32) -> Option<u64> {\n    todo!()\n}\n\nfn mean_u8(v: &[u8]) -> Option<u8> {\n    todo!()\n}\n\nfn distance(a: usize, b: usize) -> usize {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?} {:?} {:?} {:?}\", safe_factorial(0), safe_factorial(5), safe_factorial(20), safe_factorial(21));\n"
                "    println!(\"{:?} {:?} {:?}\", mean_u8(&[255, 255, 254]), mean_u8(&[]), mean_u8(&[1, 2]));\n"
                "    println!(\"{} {} {}\", distance(3, 10), distance(10, 3), distance(0, 0));\n"
                "}\n"
            ),
            "expected": ["Some(1) Some(120) Some(2432902008176640000) None", "Some(254) None Some(1)", "7 7 0"],
            "hint": "checked_mul возвращает None при переполнении, оператор ? прерывает функцию; сумму u8 копите в более широком типе.",
        },
    ],
    12: [
        {
            "id": "rs12-bit-tricks",
            "mode": "rust",
            "title": "Битовые трюки",
            "statement": (
                "Напишите без готовых методов count_ones, is_power_of_two и "
                "reverse_bits: lowest_set_bit(n: u32) -> u32 (само младшее "
                "«горящее» значение, 0 для 0), is_pow2(n: u64) -> bool (0 — нет), "
                "parity(n: u32) -> bool (число единичных битов нечётно) и "
                "reverse8(n: u8) -> u8 (биты в обратном порядке)."
            ),
            "starter": "fn lowest_set_bit(n: u32) -> u32 {\n    todo!()\n}\n\nfn is_pow2(n: u64) -> bool {\n    todo!()\n}\n\nfn parity(n: u32) -> bool {\n    todo!()\n}\n\nfn reverse8(n: u8) -> u8 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{} {} {} {}\", lowest_set_bit(0), lowest_set_bit(12), lowest_set_bit(0x8000_0000), lowest_set_bit(7));\n"
                "    println!(\"{} {} {} {}\", is_pow2(0), is_pow2(1), is_pow2(1 << 40), is_pow2(96));\n"
                "    println!(\"{} {} {} {}\", parity(0), parity(1), parity(3), parity(0b1011_0000));\n"
                "    println!(\"{:08b} {:08b} {:08b}\", reverse8(0b0000_0001), reverse8(0b1011_0000), reverse8(0xFF));\n"
                "}\n"
            ),
            "expected": ["0 4 2147483648 1", "false true true false", "false true false true", "10000000 00001101 11111111"],
            "hint": "n & n.wrapping_neg() выделяет младшую единицу; n & (n - 1) сбрасывает её.",
        },
        {
            "id": "rs12-header",
            "mode": "rust",
            "title": "Разбор двоичного заголовка",
            "statement": (
                "Формат заголовка (8 байт): магическое число 0xCAFE (u16, старший "
                "байт первым), версия (u8), длина данных (u32, младший байт "
                "первым), флаги (u8). Напишите parse_header(b: &[u8]) -> "
                "Option<(u8, u32, u8)> (версия, длина, флаги; None — если байтов "
                "меньше 8 или магия не совпала) и build_header(version: u8, len: "
                "u32, flags: u8) -> [u8; 8]."
            ),
            "starter": "fn parse_header(b: &[u8]) -> Option<(u8, u32, u8)> {\n    todo!()\n}\n\nfn build_header(version: u8, len: u32, flags: u8) -> [u8; 8] {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let h = build_header(2, 0x0001_0203, 0b101);\n"
                "    println!(\"{:02x?}\", h);\n"
                "    println!(\"{:?}\", parse_header(&h));\n"
                "    println!(\"{:?} {:?}\", parse_header(&h[..7]), parse_header(&[0xCA, 0xFF, 1, 0, 0, 0, 0, 0]));\n"
                "    let mut longer = h.to_vec();\n"
                "    longer.extend_from_slice(&[9, 9, 9]);\n"
                "    println!(\"{:?}\", parse_header(&longer));\n"
                "}\n"
            ),
            "expected": ["[ca, fe, 02, 03, 02, 01, 00, 05]", "Some((2, 66051, 5))", "None None", "Some((2, 66051, 5))"],
            "hint": "u16::from_be_bytes([b[0], b[1]]), u32::from_le_bytes([...4 байта...]); массив байтов собирайте из to_be_bytes / to_le_bytes.",
        },
        {
            "id": "rs12-varint",
            "mode": "rust",
            "title": "Varint с проверкой ошибок",
            "statement": (
                "Напишите varint_encode(n: u64) -> Vec<u8> и varint_decode(b: "
                "&[u8]) -> Result<(u64, usize), &'static str>: число и сколько "
                "байтов прочитано. Ошибки: пустой вход или оборвавшаяся запись (все "
                "байты с признаком продолжения) → \"truncated\"; запись длиннее 10 "
                "байтов или не помещающаяся в u64 → \"overflow\"."
            ),
            "starter": "fn varint_encode(n: u64) -> Vec<u8> {\n    todo!()\n}\n\nfn varint_decode(b: &[u8]) -> Result<(u64, usize), &'static str> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for n in [0u64, 1, 127, 128, 300, 16384, u32::MAX as u64, u64::MAX] {\n"
                "        let e = varint_encode(n);\n"
                "        println!(\"{} {} {:?}\", n, e.len(), varint_decode(&e) == Ok((n, e.len())));\n"
                "    }\n"
                "    println!(\"{:?} {:?}\", varint_decode(&[]), varint_decode(&[0x80, 0x80]));\n"
                "    println!(\"{:?}\", varint_decode(&[0xff; 11]));\n"
                "    println!(\"{:?}\", varint_decode(&[0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x02]));\n"
                "    println!(\"{:?}\", varint_decode(&[0xac, 0x02, 0xff]));\n"
                "}\n"
            ),
            "expected": ["0 1 true", "1 1 true", "127 1 true", "128 2 true", "300 2 true", "16384 3 true", "4294967295 5 true", "18446744073709551615 10 true", "Err(\"truncated\") Err(\"truncated\")", "Err(\"overflow\")", "Err(\"overflow\")", "Ok((300, 2))"],
            "hint": "Каждый байт даёт 7 бит со сдвигом 7·i; десятый байт может нести только один значащий бит.",
        },
        {
            "id": "rs12-crc32",
            "mode": "rust",
            "title": "CRC-32 по таблице",
            "statement": (
                "Напишите crc32(data: &[u8]) -> u32 (многочлен 0xEDB88320 в "
                "отражённом виде, начальное значение 0xFFFFFFFF, итог "
                "инвертируется) — как zlib.crc32 в питоне. Проверка подаёт 8 МБ "
                "данных."
            ),
            "starter": "fn crc32(data: &[u8]) -> u32 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:08x} {:08x} {:08x}\", crc32(b\"\"), crc32(b\"hello\"), crc32(b\"123456789\"));\n"
                "    let big: Vec<u8> = (0..8_000_000u32).map(|i| (i % 251) as u8).collect();\n"
                "    println!(\"{:08x}\", crc32(&big));\n"
                "}\n"
            ),
            "expected": ["00000000 3610a686 cbf43926", "37ac4d4a"],
            "hint": "Таблицу из 256 значений считайте один раз перед циклом по данным.",
        },
        {
            "id": "rs12-base64",
            "mode": "rust",
            "title": "Base64",
            "statement": (
                "Напишите base64_encode(data: &[u8]) -> String (алфавит A–Z a–z 0–9 "
                "+ /, добивка '=') и base64_decode(s: &str) -> Option<Vec<u8>> "
                "(None при недопустимом символе или неверной длине)."
            ),
            "starter": "fn base64_encode(data: &[u8]) -> String {\n    todo!()\n}\n\nfn base64_decode(s: &str) -> Option<Vec<u8>> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for s in [\"\", \"f\", \"fo\", \"foo\", \"foob\", \"fooba\", \"foobar\", \"Привет\"] {\n"
                "        let e = base64_encode(s.as_bytes());\n"
                "        let d = base64_decode(&e).unwrap();\n"
                "        println!(\"{:?} {} {}\", s, e, d == s.as_bytes());\n"
                "    }\n"
                "    println!(\"{:?} {:?} {:?}\", base64_decode(\"Zm9v!\"), base64_decode(\"Zm9\"), base64_decode(\"Zg=A\"));\n"
                "    println!(\"{}\", base64_encode(&[0xff, 0xfe, 0xfd]));\n"
                "}\n"
            ),
            "expected": ["\"\"  true", "\"f\" Zg== true", "\"fo\" Zm8= true", "\"foo\" Zm9v true", "\"foob\" Zm9vYg== true", "\"fooba\" Zm9vYmE= true", "\"foobar\" Zm9vYmFy true", "\"Привет\" 0J/RgNC40LLQtdGC true", "None None None", "//79"],
            "hint": "Три байта = 24 бита = четыре шестибитных индекса в алфавите; недостающие байты — нули, а в выводе знаки '='.",
        },
        {
            "id": "rs12-bitset",
            "mode": "rust",
            "title": "Битовое множество и решето",
            "statement": (
                "Дополните BitSet: new(len), set(i), clear(i), get(i), count() -> "
                "u32, ones() -> Vec<usize> (номера единиц по возрастанию), "
                "union_with(&mut self, other: &BitSet). Затем напишите "
                "primes_below(n: usize) -> Vec<usize> — решето Эратосфена на BitSet "
                "(проверка: n = 20 миллионов)."
            ),
            "starter": "struct BitSet {\n    words: Vec<u64>,\n    len: usize,\n}\n\nimpl BitSet {\n    fn new(len: usize) -> BitSet {\n        todo!()\n    }\n    fn set(&mut self, i: usize) {\n        todo!()\n    }\n    fn clear(&mut self, i: usize) {\n        todo!()\n    }\n    fn get(&self, i: usize) -> bool {\n        todo!()\n    }\n    fn count(&self) -> u32 {\n        todo!()\n    }\n    fn ones(&self) -> Vec<usize> {\n        todo!()\n    }\n    fn union_with(&mut self, other: &BitSet) {\n        todo!()\n    }\n}\n\nfn primes_below(n: usize) -> Vec<usize> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let mut a = BitSet::new(130);\n"
                "    for i in [0, 5, 64, 129] {\n"
                "        a.set(i);\n"
                "    }\n"
                "    let mut b = BitSet::new(130);\n"
                "    b.set(5);\n"
                "    b.set(100);\n"
                "    a.union_with(&b);\n"
                "    a.clear(0);\n"
                "    println!(\"{:?} {} {} {}\", a.ones(), a.count(), a.get(100), a.get(0));\n"
                "    println!(\"{:?} {}\", primes_below(30), primes_below(2).len());\n"
                "    let p = primes_below(20_000_000);\n"
                "    println!(\"{} {:?}\", p.len(), p.last());\n"
                "}\n"
            ),
            "expected": ["[5, 64, 100, 129] 4 true false", "[2, 3, 5, 7, 11, 13, 17, 19, 23, 29] 0", "1270607 Some(19999999)"],
            "hint": "trailing_zeros() + w &= w - 1 перебирают единичные биты слова; решето: пометьте кратные i, начиная с i·i.",
        },
        {
            "id": "rs12-cpu",
            "mode": "rust",
            "title": "Эмулятор процессора",
            "statement": (
                "Реализуйте run(prog: &[Instr], limit: u32) -> Result<Cpu, Trap>. "
                "Процессор: регистры regs: [u8; 4], память mem: [u8; 16], pc, zero, "
                "steps. Команды: Ldi(r, v), Mov(a, b), Add(a, b), Sub(a, b) "
                "(оборачивающие, обновляют флаг zero по результату), Ld(r, addr), "
                "St(r, addr), Jmp(t), Jz(t), Jnz(t), Hlt (останавливает; тоже "
                "считается шагом). Ловушки: адрес памяти ≥ 16 → "
                "Trap::BadAddress(addr), pc ≥ длины программы без Hlt → "
                "Trap::PcOutOfRange(pc), больше limit шагов → Trap::Timeout. Каждое "
                "выполнение команды увеличивает steps."
            ),
            "starter": "#[derive(Debug, Clone, Copy)]\nenum Instr {\n    Ldi(usize, u8),\n    Mov(usize, usize),\n    Add(usize, usize),\n    Sub(usize, usize),\n    Ld(usize, usize),\n    St(usize, usize),\n    Jmp(usize),\n    Jz(usize),\n    Jnz(usize),\n    Hlt,\n}\n\n#[derive(Debug, PartialEq)]\nenum Trap {\n    BadAddress(usize),\n    PcOutOfRange(usize),\n    Timeout,\n}\n\n#[derive(Debug)]\nstruct Cpu {\n    regs: [u8; 4],\n    mem: [u8; 16],\n    pc: usize,\n    zero: bool,\n    steps: u32,\n}\n\nfn run(prog: &[Instr], limit: u32) -> Result<Cpu, Trap> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    use Instr::*;\n"
                "    let sum = [Ldi(0, 0), Ldi(1, 5), Ldi(2, 1), Add(0, 1), Sub(1, 2), Jnz(3), Hlt];\n"
                "    let c = run(&sum, 1000).unwrap();\n"
                "    println!(\"{:?} {} {}\", c.regs, c.steps, c.zero);\n"
                "    let mem = [Ldi(0, 42), St(0, 3), Ldi(0, 0), Ld(1, 3), Hlt];\n"
                "    let c = run(&mem, 100).unwrap();\n"
                "    println!(\"{:?} {:?}\", c.regs, &c.mem[..5]);\n"
                "    println!(\"{:?}\", run(&[Ldi(0, 1), St(0, 16)], 100).err());\n"
                "    println!(\"{:?}\", run(&[Ldi(0, 1)], 100).err());\n"
                "    println!(\"{:?}\", run(&[Jmp(0)], 50).err());\n"
                "    println!(\"{:?}\", run(&[Ldi(0, 250), Ldi(1, 10), Add(0, 1), Hlt], 10).map(|c| (c.regs[0], c.zero)));\n"
                "    println!(\"{:?}\", run(&[Jmp(7)], 10).err());\n"
                "}\n"
            ),
            "expected": ["[15, 0, 1, 0] 19 true", "[0, 42, 0, 0] [0, 0, 0, 42, 0]", "Some(BadAddress(16))", "Some(PcOutOfRange(1))", "Some(Timeout)", "Ok((4, false))", "Some(PcOutOfRange(7))"],
            "hint": "Проверяйте pc перед чтением команды; ?-оператор вместе с ok_or превращает выход за массив в Trap.",
        },
        {
            "id": "rs12-encode-instr",
            "mode": "rust",
            "title": "Машинный код команд",
            "statement": (
                "Кодируйте команды в два байта: байт 0 = код операции << 4 | a << 2 "
                "| b, байт 1 = число или адрес (0, если нет). Коды: Hlt 0, Ldi 1, "
                "Mov 2, Add 3, Sub 4, Ld 5, St 6, Jmp 7, Jz 8, Jnz 9. Для Ldi(r, "
                "v): a = r, байт 1 = v; для Mov/Add/Sub(a, b): a, b; для Ld(r, "
                "addr) и St(r, addr): a = r, байт 1 = addr (адрес ≤ 255); для "
                "переходов: байт 1 = цель. Напишите encode(i: &Instr) -> [u8; 2] и "
                "decode(b: [u8; 2]) -> Option<Instr> (None для неизвестного кода "
                "операции)."
            ),
            "starter": "#[derive(Debug, Clone, Copy, PartialEq)]\nenum Instr {\n    Ldi(usize, u8),\n    Mov(usize, usize),\n    Add(usize, usize),\n    Sub(usize, usize),\n    Ld(usize, usize),\n    St(usize, usize),\n    Jmp(usize),\n    Jz(usize),\n    Jnz(usize),\n    Hlt,\n}\n\nfn encode(i: &Instr) -> [u8; 2] {\n    todo!()\n}\n\nfn decode(b: [u8; 2]) -> Option<Instr> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    use Instr::*;\n"
                "    let prog = [Ldi(1, 5), Add(0, 1), Sub(1, 2), Jnz(3), Ld(2, 200), St(3, 17), Mov(3, 0), Jz(9), Jmp(0), Hlt];\n"
                "    for i in &prog {\n"
                "        let e = encode(i);\n"
                "        println!(\"{:02x} {:02x} {}\", e[0], e[1], decode(e) == Some(*i));\n"
                "    }\n"
                "    println!(\"{:?} {:?}\", decode([0xA0, 0]), decode([0xF3, 9]));\n"
                "}\n"
            ),
            "expected": ["14 05 true", "31 00 true", "46 00 true", "90 03 true", "58 c8 true", "6c 11 true", "2c 00 true", "80 09 true", "70 00 true", "00 00 true", "None None"],
            "hint": "Поля байта 0 собираются сдвигами: op << 4 | a << 2 | b; разбор — обратными сдвигами и маской 3.",
        },
        {
            "id": "rs12-cache",
            "mode": "rust",
            "title": "Симулятор кэша",
            "statement": (
                "Напишите cache_sim(trace: &[u64], lines: usize, line_size: u64) -> "
                "(u64, u64): кэш с прямым отображением (как в курсе по "
                "архитектуре): блок = адрес / line_size, строка = блок % lines, тег "
                "= блок / lines; верните (попадания, промахи). Проверка: 5 "
                "миллионов обращений."
            ),
            "starter": "fn cache_sim(trace: &[u64], lines: usize, line_size: u64) -> (u64, u64) {\n    todo!()\n}\n",
            "driver": (
                "struct Lcg(u64);\n"
                "impl Lcg {\n"
                "    fn next(&mut self) -> u64 {\n"
                "        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n"
                "        self.0 >> 33\n"
                "    }\n"
                "}\n"
                "fn main() {\n"
                "    println!(\"{:?}\", cache_sim(&[0, 4, 8, 16, 0, 64, 0], 4, 16));\n"
                "    println!(\"{:?} {:?}\", cache_sim(&[], 4, 16), cache_sim(&[0, 0, 0], 4, 16));\n"
                "    let seq: Vec<u64> = (0..1_000_000u64).map(|i| i * 4).collect();\n"
                "    println!(\"{:?}\", cache_sim(&seq, 64, 64));\n"
                "    let mut rng = Lcg(1);\n"
                "    let rnd: Vec<u64> = (0..5_000_000).map(|_| rng.next() % 100_000).collect();\n"
                "    let (h, m) = cache_sim(&rnd, 1024, 64);\n"
                "    println!(\"{}\", h + m);\n"
                "}\n"
            ),
            "expected": ["(3, 4)", "(0, 0) (2, 1)", "(937500, 62500)", "5000000"],
            "hint": "Таблица тегов Vec<Option<u64>>; сравнивайте tags[idx] с Some(tag).",
        },
        {
            "id": "rs12-alu-flags",
            "mode": "rust",
            "title": "АЛУ с флагами",
            "statement": (
                "Напишите alu(op: &str, a: u8, b: u8) -> (u8, bool, bool, bool, "
                "bool): op — \"ADD\" или \"SUB\"; результат и флаги (zero, negative, "
                "carry, overflow). carry — перенос при сложении или заём (a < b) "
                "при вычитании; overflow — знаковое переполнение (операнды как "
                "числа в дополнительном коде)."
            ),
            "starter": "fn alu(op: &str, a: u8, b: u8) -> (u8, bool, bool, bool, bool) {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for (op, a, b) in [(\"ADD\", 100, 100), (\"ADD\", 255, 1), (\"ADD\", 127, 1), (\"ADD\", 128, 128), (\"SUB\", 5, 7), (\"SUB\", 128, 1), (\"SUB\", 0, 0), (\"SUB\", 127, 255)] {\n"
                "        println!(\"{} {} {} {:?}\", op, a, b, alu(op, a, b));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["ADD 100 100 (200, false, true, false, true)", "ADD 255 1 (0, true, false, true, false)", "ADD 127 1 (128, false, true, false, true)", "ADD 128 128 (0, true, false, true, true)", "SUB 5 7 (254, false, true, true, false)", "SUB 128 1 (127, false, false, false, true)", "SUB 0 0 (0, true, false, false, false)", "SUB 127 255 (128, false, true, true, true)"],
            "hint": "overflowing_add/sub возвращают (результат, признак); для знакового переполнения выполните ту же операцию над i8.",
        },
    ],
    13: [
        {
            "id": "rs13-wc",
            "mode": "rust",
            "title": "wc: строки, слова, байты",
            "statement": (
                "Напишите count_stats<R: std::io::Read>(r: R) -> "
                "std::io::Result<(usize, usize, usize)>: число строк (символов '\\n' "
                "плюс последняя строка без перевода), слов (по пробельным символам) "
                "и байтов. Читайте буферизованно: проверка подаёт 20 МБ."
            ),
            "starter": "use std::io::Read;\n\nfn count_stats<R: Read>(r: R) -> std::io::Result<(usize, usize, usize)> {\n    todo!()\n}\n",
            "driver": (
                "use std::io::Cursor;\n"
                "\n"
                "fn main() {\n"
                "    println!(\"{:?}\", count_stats(Cursor::new(\"one two\\nthree\\n\\nfour five six\")).unwrap());\n"
                "    println!(\"{:?} {:?}\", count_stats(Cursor::new(\"\")).unwrap(), count_stats(Cursor::new(\"\\n\")).unwrap());\n"
                "    println!(\"{:?}\", count_stats(Cursor::new(\"привет мир\\n\")).unwrap());\n"
                "    let big = \"lorem ipsum dolor sit amet\\n\".repeat(750_000);\n"
                "    println!(\"{:?}\", count_stats(Cursor::new(big)).unwrap());\n"
                "}\n"
            ),
            "expected": ["(4, 6, 28)", "(0, 0, 0) (1, 0, 1)", "(1, 2, 20)", "(750000, 3750000, 20250000)"],
            "hint": "read_until(b'\\n', &mut buf) читает строку вместе с переводом; считайте байты по числу прочитанного.",
        },
        {
            "id": "rs13-paths",
            "mode": "rust",
            "title": "Лексический разбор путей",
            "statement": (
                "Напишите без обращения к файловой системе: normalize(path: &str) "
                "-> String (как в курсе по ОС: убрать '.', повторные '/', "
                "обработать '..', результат абсолютный; для относительного пути "
                "'..' выше начала сохраняются) и ext_of(path: &str) -> "
                "Option<String> (расширение без точки; None для имён без точки или "
                "вида '.bashrc')."
            ),
            "starter": "fn normalize(path: &str) -> String {\n    todo!()\n}\n\nfn ext_of(path: &str) -> Option<String> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for p in [\"/usr/./bin/../lib//x/\", \"/\", \"/../..\", \"a/b/../../c\", \"../x/./y\", \"a/..\", \"\", \"./\", \"../../a/../b\"] {\n"
                "        println!(\"{:?} -> {:?}\", p, normalize(p));\n"
                "    }\n"
                "    for p in [\"/a/report.final.txt\", \"Makefile\", \"/a/.bashrc\", \"archive.tar.gz\", \"dir.d/file\", \"trailing.\"] {\n"
                "        println!(\"{:?} {:?}\", p, ext_of(p));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["\"/usr/./bin/../lib//x/\" -> \"/usr/lib/x\"", "\"/\" -> \"/\"", "\"/../..\" -> \"/\"", "\"a/b/../../c\" -> \"c\"", "\"../x/./y\" -> \"../x/y\"", "\"a/..\" -> \".\"", "\"\" -> \".\"", "\"./\" -> \".\"", "\"../../a/../b\" -> \"../../b\"", "\"/a/report.final.txt\" Some(\"txt\")", "\"Makefile\" None", "\"/a/.bashrc\" None", "\"archive.tar.gz\" Some(\"gz\")", "\"dir.d/file\" None", "\"trailing.\" None"],
            "hint": "Стек компонентов; '..' снимает предыдущий компонент, но не другой '..'; в абсолютном пути выше корня подняться нельзя.",
        },
        {
            "id": "rs13-list-tree",
            "mode": "rust",
            "title": "Дерево каталогов",
            "statement": (
                "Напишите list_tree(root: &Path) -> io::Result<Vec<String>>: "
                "относительные пути всех файлов и каталогов внутри root (каталоги — "
                "с '/' на конце), отсортированные по полному пути как строке."
            ),
            "starter": "use std::io;\nuse std::path::Path;\n\nfn list_tree(root: &Path) -> io::Result<Vec<String>> {\n    todo!()\n}\n",
            "driver": (
                "fn tmp_dir(name: &str) -> std::path::PathBuf {\n"
                "    let d = std::env::temp_dir().join(format!(\"say13-{}-{}\", name, std::process::id()));\n"
                "    let _ = std::fs::remove_dir_all(&d);\n"
                "    std::fs::create_dir_all(&d).unwrap();\n"
                "    d\n"
                "}\n"
                "use std::fs;\n"
                "\n"
                "fn main() {\n"
                "    let root = tmp_dir(\"tree\");\n"
                "    fs::create_dir_all(root.join(\"src/util\")).unwrap();\n"
                "    fs::create_dir_all(root.join(\"empty\")).unwrap();\n"
                "    fs::write(root.join(\"Cargo.toml\"), \"x\").unwrap();\n"
                "    fs::write(root.join(\"src/main.rs\"), \"m\").unwrap();\n"
                "    fs::write(root.join(\"src/util/mod.rs\"), \"\").unwrap();\n"
                "    println!(\"{:?}\", list_tree(&root).unwrap());\n"
                "    println!(\"{:?}\", list_tree(&root.join(\"empty\")).unwrap());\n"
                "    println!(\"{:?}\", list_tree(&root.join(\"nope\")).map_err(|e| e.kind()));\n"
                "    fs::remove_dir_all(&root).unwrap();\n"
                "}\n"
            ),
            "expected": ["[\"Cargo.toml\", \"empty/\", \"src/\", \"src/main.rs\", \"src/util/\", \"src/util/mod.rs\"]", "[]", "Err(NotFound)"],
            "hint": "Рекурсия с префиксом пути; тип записи — e.file_type()?.is_dir(); в конце sort().",
        },
        {
            "id": "rs13-dir-size",
            "mode": "rust",
            "title": "Размер каталога",
            "statement": (
                "Напишите dir_size(root: &Path) -> io::Result<u64>: суммарный "
                "размер всех обычных файлов внутри root (рекурсивно). Символические "
                "ссылки не разыменовывайте (не заходите и не считайте)."
            ),
            "starter": "use std::io;\nuse std::path::Path;\n\nfn dir_size(root: &Path) -> io::Result<u64> {\n    todo!()\n}\n",
            "driver": (
                "fn tmp_dir(name: &str) -> std::path::PathBuf {\n"
                "    let d = std::env::temp_dir().join(format!(\"say13-{}-{}\", name, std::process::id()));\n"
                "    let _ = std::fs::remove_dir_all(&d);\n"
                "    std::fs::create_dir_all(&d).unwrap();\n"
                "    d\n"
                "}\n"
                "use std::fs;\n"
                "\n"
                "fn main() {\n"
                "    let root = tmp_dir(\"size\");\n"
                "    fs::create_dir_all(root.join(\"a/b\")).unwrap();\n"
                "    fs::write(root.join(\"one\"), vec![0u8; 100]).unwrap();\n"
                "    fs::write(root.join(\"a/two\"), vec![0u8; 2000]).unwrap();\n"
                "    fs::write(root.join(\"a/b/three\"), vec![1u8; 30]).unwrap();\n"
                "    #[cfg(unix)]\n"
                "    std::os::unix::fs::symlink(&root, root.join(\"a/loop\")).unwrap();\n"
                "    println!(\"{}\", dir_size(&root).unwrap());\n"
                "    println!(\"{}\", dir_size(&root.join(\"a/b\")).unwrap());\n"
                "    println!(\"{:?}\", dir_size(&root.join(\"zzz\")).map_err(|e| e.kind()));\n"
                "    fs::remove_dir_all(&root).unwrap();\n"
                "}\n"
            ),
            "expected": ["2130", "30", "Err(NotFound)"],
            "hint": "e.file_type() не следует по ссылкам (в отличие от fs::metadata): is_file / is_dir у ссылки ложны.",
        },
        {
            "id": "rs13-grep-file",
            "mode": "rust",
            "title": "grep по файлу",
            "statement": (
                "Напишите grep_file(path: &Path, needle: &str) -> "
                "io::Result<Vec<(usize, String)>>: пары (номер строки с единицы, "
                "строка), содержащие подстроку needle. Читайте построчно через "
                "BufReader."
            ),
            "starter": "use std::io;\nuse std::path::Path;\n\nfn grep_file(path: &Path, needle: &str) -> io::Result<Vec<(usize, String)>> {\n    todo!()\n}\n",
            "driver": (
                "fn tmp_dir(name: &str) -> std::path::PathBuf {\n"
                "    let d = std::env::temp_dir().join(format!(\"say13-{}-{}\", name, std::process::id()));\n"
                "    let _ = std::fs::remove_dir_all(&d);\n"
                "    std::fs::create_dir_all(&d).unwrap();\n"
                "    d\n"
                "}\n"
                "use std::fs;\n"
                "\n"
                "fn main() {\n"
                "    let dir = tmp_dir(\"grep\");\n"
                "    let f = dir.join(\"log.txt\");\n"
                "    fs::write(&f, \"start\\nERROR disk full\\nok\\nERROR timeout\\n\\nend ERROR\").unwrap();\n"
                "    println!(\"{:?}\", grep_file(&f, \"ERROR\").unwrap());\n"
                "    println!(\"{:?} {:?}\", grep_file(&f, \"nothing\").unwrap(), grep_file(&f, \"\").unwrap().len());\n"
                "    println!(\"{:?}\", grep_file(&dir.join(\"missing\"), \"x\").map_err(|e| e.kind()));\n"
                "    fs::remove_dir_all(&dir).unwrap();\n"
                "}\n"
            ),
            "expected": ["[(2, \"ERROR disk full\"), (4, \"ERROR timeout\"), (6, \"end ERROR\")]", "[] 6", "Err(NotFound)"],
            "hint": "lines() даёт Result<String>; enumerate() — номера с нуля, прибавьте единицу.",
        },
        {
            "id": "rs13-copy-filtered",
            "mode": "rust",
            "title": "Копирование с фильтром",
            "statement": (
                "Напишите copy_filtered(src: &Path, dst: &Path, keep: impl Fn(&str) "
                "-> bool) -> io::Result<usize>: читает src построчно, записывает в "
                "dst (через BufWriter, каждая строка заканчивается '\\n') только "
                "строки, для которых keep вернул true; возвращает число записанных "
                "строк."
            ),
            "starter": "use std::io;\nuse std::path::Path;\n\nfn copy_filtered(src: &Path, dst: &Path, keep: impl Fn(&str) -> bool) -> io::Result<usize> {\n    todo!()\n}\n",
            "driver": (
                "fn tmp_dir(name: &str) -> std::path::PathBuf {\n"
                "    let d = std::env::temp_dir().join(format!(\"say13-{}-{}\", name, std::process::id()));\n"
                "    let _ = std::fs::remove_dir_all(&d);\n"
                "    std::fs::create_dir_all(&d).unwrap();\n"
                "    d\n"
                "}\n"
                "use std::fs;\n"
                "\n"
                "fn main() {\n"
                "    let dir = tmp_dir(\"copy\");\n"
                "    let (a, b) = (dir.join(\"in.txt\"), dir.join(\"out.txt\"));\n"
                "    fs::write(&a, \"# comment\\nkey=1\\n\\nkey=2\\n# other\\nlast\").unwrap();\n"
                "    let n = copy_filtered(&a, &b, |l| !l.is_empty() && !l.starts_with('#')).unwrap();\n"
                "    println!(\"{} {:?}\", n, fs::read_to_string(&b).unwrap());\n"
                "    println!(\"{:?}\", copy_filtered(&dir.join(\"none\"), &b, |_| true).map_err(|e| e.kind()));\n"
                "    let big = dir.join(\"big.txt\");\n"
                "    fs::write(&big, \"line\\n\".repeat(300_000)).unwrap();\n"
                "    println!(\"{}\", copy_filtered(&big, &dir.join(\"big2.txt\"), |_| true).unwrap());\n"
                "    fs::remove_dir_all(&dir).unwrap();\n"
                "}\n"
            ),
            "expected": ["3 \"key=1\\nkey=2\\nlast\\n\"", "Err(NotFound)", "300000"],
            "hint": "BufWriter сам сбросится при уничтожении, но flush() явно возвращает ошибку записи — лучше вызвать его.",
        },
        {
            "id": "rs13-run-capture",
            "mode": "rust",
            "title": "Запуск программы с отчётом",
            "statement": (
                "Напишите run_capture(cmd: &str, args: &[&str]) -> Result<(String, "
                "i32), String>: запускает программу и возвращает (stdout без "
                "перевода строки в конце, код возврата). Если программы нет — "
                "Err(\"not found: <cmd>\"); если процесс убит сигналом (кода нет) — "
                "код −1; другие ошибки запуска — Err(текст ошибки)."
            ),
            "starter": "use std::process::Command;\n\nfn run_capture(cmd: &str, args: &[&str]) -> Result<(String, i32), String> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", run_capture(\"echo\", &[\"hi\", \"there\"]));\n"
                "    println!(\"{:?}\", run_capture(\"sh\", &[\"-c\", \"echo partial; exit 4\"]));\n"
                "    println!(\"{:?}\", run_capture(\"sh\", &[\"-c\", \"kill -9 $$\"]));\n"
                "    println!(\"{:?}\", run_capture(\"no-such-program-xyz\", &[]));\n"
                "    println!(\"{:?}\", run_capture(\"printf\", &[\"a\\\\nb\\\\n\\\\n\"]));\n"
                "}\n"
            ),
            "expected": ["Ok((\"hi there\", 0))", "Ok((\"partial\", 4))", "Ok((\"\", -1))", "Err(\"not found: no-such-program-xyz\")", "Ok((\"a\\nb\", 0))"],
            "hint": "output() возвращает Err, только если процесс не удалось запустить; ненулевой код — это Ok со статусом.",
        },
        {
            "id": "rs13-sort-process",
            "mode": "rust",
            "title": "Сортировка внешней программой",
            "statement": (
                "Напишите sort_with_process(lines: &[&str]) -> "
                "io::Result<Vec<String>>: отправьте строки на стандартный ввод "
                "программы sort, закройте ввод и верните строки её вывода."
            ),
            "starter": "use std::io;\n\nfn sort_with_process(lines: &[&str]) -> io::Result<Vec<String>> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", sort_with_process(&[\"pear\", \"apple\", \"fig\", \"banana\"]).unwrap());\n"
                "    println!(\"{:?}\", sort_with_process(&[]).unwrap());\n"
                "    let many: Vec<String> = (0..50_000).map(|i| format!(\"{:06}\", (i * 7919) % 50_000)).collect();\n"
                "    let refs: Vec<&str> = many.iter().map(|s| s.as_str()).collect();\n"
                "    let r = sort_with_process(&refs).unwrap();\n"
                "    println!(\"{} {} {}\", r.len(), r[0], r[r.len() - 1]);\n"
                "}\n"
            ),
            "expected": ["[\"apple\", \"banana\", \"fig\", \"pear\"]", "[]", "50000 000000 049999"],
            "hint": "Стандартный ввод дочернего процесса нужно закрыть (уничтожить владельца) до wait_with_output.",
        },
        {
            "id": "rs13-kv-server",
            "mode": "rust",
            "title": "Сервер ключ-значение",
            "statement": (
                "Напишите handle_kv(stream: TcpStream, store: "
                "Arc<Mutex<HashMap<String, String>>>) -> io::Result<()>: читает "
                "команды по одной в строке и отвечает строкой: 'SET k v' (v — "
                "остаток строки, может содержать пробелы) → 'OK'; 'GET k' → "
                "значение или 'NIL'; 'DEL k' → 'OK' или 'NIL' (если ключа не было); "
                "'INCR k' → новое число (отсутствующий ключ — 0, значение не число "
                "— 'ERR'); всё остальное → 'ERR'. Заканчивайте, когда клиент закрыл "
                "соединение."
            ),
            "starter": "use std::collections::HashMap;\nuse std::io;\nuse std::net::TcpStream;\nuse std::sync::{Arc, Mutex};\n\nfn handle_kv(stream: TcpStream, store: Arc<Mutex<HashMap<String, String>>>) -> io::Result<()> {\n    todo!()\n}\n",
            "driver": (
                "use std::io::{BufRead, BufReader, Write};\n"
                "use std::net::{TcpListener, TcpStream};\n"
                "use std::thread;\n"
                "\n"
                "fn session(addr: std::net::SocketAddr, cmds: &[&str]) -> Vec<String> {\n"
                "    let mut c = TcpStream::connect(addr).unwrap();\n"
                "    let mut r = BufReader::new(c.try_clone().unwrap());\n"
                "    let mut out = Vec::new();\n"
                "    for cmd in cmds {\n"
                "        writeln!(c, \"{}\", cmd).unwrap();\n"
                "        let mut line = String::new();\n"
                "        r.read_line(&mut line).unwrap();\n"
                "        out.push(line.trim_end().to_string());\n"
                "    }\n"
                "    out\n"
                "}\n"
                "\n"
                "fn main() {\n"
                "    let listener = TcpListener::bind(\"127.0.0.1:0\").unwrap();\n"
                "    let addr = listener.local_addr().unwrap();\n"
                "    let store = Arc::new(Mutex::new(HashMap::new()));\n"
                "    let st = Arc::clone(&store);\n"
                "    let server = thread::spawn(move || {\n"
                "        for _ in 0..2 {\n"
                "            let (s, _) = listener.accept().unwrap();\n"
                "            handle_kv(s, Arc::clone(&st)).unwrap();\n"
                "        }\n"
                "    });\n"
                "    println!(\"{:?}\", session(addr, &[\"SET greeting hello big world\", \"GET greeting\", \"GET x\", \"INCR n\", \"INCR n\", \"SET s abc\", \"INCR s\", \"DEL n\", \"DEL n\", \"FOO\", \"SET onlykey\"]));\n"
                "    println!(\"{:?}\", session(addr, &[\"GET greeting\", \"GET n\"]));\n"
                "    server.join().unwrap();\n"
                "    println!(\"{}\", store.lock().unwrap().len());\n"
                "}\n"
            ),
            "expected": ["[\"OK\", \"hello big world\", \"NIL\", \"1\", \"2\", \"OK\", \"ERR\", \"OK\", \"NIL\", \"ERR\", \"ERR\"]", "[\"hello big world\", \"NIL\"]", "2"],
            "hint": "Один Mutex на всю обработку команды — просто и корректно; клиент закрывает соединение, и lines() заканчивается.",
        },
        {
            "id": "rs13-udp-reverse",
            "mode": "rust",
            "title": "UDP: ответ задом наперёд",
            "statement": (
                "Напишите udp_reverse_once(sock: &UdpSocket) -> io::Result<usize>: "
                "принять одну дейтаграмму (до 1024 байт), отправить обратно "
                "отправителю те же байты в обратном порядке и вернуть длину. Если "
                "за 500 мс ничего не пришло — вернуть ошибку вида TimedOut или "
                "WouldBlock (установите таймаут чтения на сокете)."
            ),
            "starter": "use std::io;\nuse std::net::UdpSocket;\n\nfn udp_reverse_once(sock: &UdpSocket) -> io::Result<usize> {\n    todo!()\n}\n",
            "driver": (
                "use std::net::UdpSocket;\n"
                "use std::thread;\n"
                "use std::time::Duration;\n"
                "\n"
                "fn main() {\n"
                "    let server = UdpSocket::bind(\"127.0.0.1:0\").unwrap();\n"
                "    let addr = server.local_addr().unwrap();\n"
                "    let h = thread::spawn(move || {\n"
                "        let a = udp_reverse_once(&server).map_err(|e| e.kind());\n"
                "        let b = udp_reverse_once(&server).map_err(|e| e.kind());\n"
                "        let kind_ok = matches!(b, Err(std::io::ErrorKind::TimedOut) | Err(std::io::ErrorKind::WouldBlock));\n"
                "        (a, kind_ok)\n"
                "    });\n"
                "    let c = UdpSocket::bind(\"127.0.0.1:0\").unwrap();\n"
                "    c.set_read_timeout(Some(Duration::from_secs(2))).unwrap();\n"
                "    c.send_to(b\"abc123\", addr).unwrap();\n"
                "    let mut buf = [0u8; 64];\n"
                "    let (n, _) = c.recv_from(&mut buf).unwrap();\n"
                "    println!(\"{}\", String::from_utf8_lossy(&buf[..n]));\n"
                "    println!(\"{:?}\", h.join().unwrap());\n"
                "}\n"
            ),
            "expected": ["321cba", "(Ok(6), true)"],
            "hint": "recv_from возвращает размер и адрес отправителя; send_to ему же.",
        },
    ],
    14: [
        {
            "id": "rs14-parse-request",
            "mode": "rust",
            "title": "Разбор HTTP-запроса целиком",
            "statement": (
                "Напишите parse_request(raw: &str) -> Result<Request, String> "
                "(структура Request дана): стартовая строка (3 части, иначе "
                "Err(\"bad request line\")), заголовки (ключ → значение; имена в "
                "нижнем регистре, значения без пробелов по краям; строка без ':' — "
                "Err(\"bad header\")), параметры из query после '?' (без "
                "декодирования: пары 'a=b', без '=' — значение пустое), тело — всё "
                "после пустой строки; Content-Length должен быть числом (иначе "
                "Err(\"bad content-length\")) и не больше длины тела в байтах (иначе "
                "Err(\"incomplete body\")); тело обрезается до этой длины."
            ),
            "starter": "use std::collections::BTreeMap;\n\n#[derive(Debug, PartialEq)]\nstruct Request {\n    method: String,\n    path: String,\n    query: BTreeMap<String, String>,\n    headers: BTreeMap<String, String>,\n    body: String,\n}\n\nfn parse_request(raw: &str) -> Result<Request, String> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let r = parse_request(\"POST /items?id=7&flag&x= HTTP/1.1\\r\\nHost: Example\\r\\nContent-Length: 5\\r\\n\\r\\nhello EXTRA\").unwrap();\n"
                "    println!(\"{} {} {:?} {:?} {:?}\", r.method, r.path, r.query, r.headers, r.body);\n"
                "    println!(\"{:?}\", parse_request(\"GET / HTTP/1.1\\r\\n\\r\\n\").map(|r| (r.path, r.body)));\n"
                "    for raw in [\"GET /\\r\\n\\r\\n\", \"GET / HTTP/1.1\\r\\nbroken\\r\\n\\r\\n\", \"POST / HTTP/1.1\\r\\nContent-Length: x\\r\\n\\r\\n\", \"POST / HTTP/1.1\\r\\nContent-Length: 9\\r\\n\\r\\nshort\", \"\"] {\n"
                "        println!(\"{:?}\", parse_request(raw).err());\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["POST /items {\"flag\": \"\", \"id\": \"7\", \"x\": \"\"} {\"content-length\": \"5\", \"host\": \"Example\"} \"hello\"", "Ok((\"/\", \"\"))", "Some(\"bad request line\")", "Some(\"bad header\")", "Some(\"bad content-length\")", "Some(\"incomplete body\")", "Some(\"bad request line\")"],
            "hint": "Начните с split_once(\"\\r\\n\\r\\n\"); проверки делайте в порядке: стартовая строка, заголовки, длина тела.",
        },
        {
            "id": "rs14-percent",
            "mode": "rust",
            "title": "Процентное кодирование",
            "statement": (
                "Напишите percent_encode(s: &str) -> String: байты A–Z a–z 0–9 - _ "
                ". ~ остаются, остальные байты UTF-8 заменяются на %XX (заглавные "
                "цифры); и percent_decode(s: &str) -> String: '+' → пробел, %XX → "
                "байт; некорректная последовательность (нет двух шестнадцатеричных "
                "цифр) остаётся как есть; итог собирается из байтов с заменой "
                "недопустимых UTF-8 последовательностей (from_utf8_lossy)."
            ),
            "starter": "fn percent_encode(s: &str) -> String {\n    todo!()\n}\n\nfn percent_decode(s: &str) -> String {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for s in [\"hello world\", \"a/b?c=d&e\", \"Москва\", \"safe-_.~\", \"100%\", \"\"] {\n"
                "        let e = percent_encode(s);\n"
                "        println!(\"{:?} -> {} -> {}\", s, e, percent_decode(&e) == s);\n"
                "    }\n"
                "    println!(\"{:?} {:?} {:?}\", percent_decode(\"a+b%20c\"), percent_decode(\"%zz%4\"), percent_decode(\"%D0%9F\"));\n"
                "}\n"
            ),
            "expected": ["\"hello world\" -> hello%20world -> true", "\"a/b?c=d&e\" -> a%2Fb%3Fc%3Dd%26e -> true", "\"Москва\" -> %D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0 -> true", "\"safe-_.~\" -> safe-_.~ -> true", "\"100%\" -> 100%25 -> true", "\"\" ->  -> true", "\"a b c\" \"%zz%4\" \"П\""],
            "hint": "Кодируйте по байтам (s.as_bytes()), формат {:02X}; при декодировании накапливайте Vec<u8> и только в конце превращайте в строку.",
        },
        {
            "id": "rs14-build-response",
            "mode": "rust",
            "title": "Сборка ответа",
            "statement": (
                "Напишите build_response(status: u16, headers: &[(&str, &str)], "
                "body: &[u8]) -> Vec<u8>: стартовая строка 'HTTP/1.1 КОД ПОЯСНЕНИЕ' "
                "(пояснения: 200 OK, 201 Created, 204 No Content, 400 Bad Request, "
                "404 Not Found, 405 Method Not Allowed, 413 Payload Too Large, 500 "
                "Internal Server Error; для прочих кодов — 'Unknown'), переданные "
                "заголовки в порядке, затем автоматически 'Content-Length: N' (N — "
                "байты тела) и 'Connection: close', пустая строка и тело. Концы "
                "строк — \\r\\n."
            ),
            "starter": "fn build_response(status: u16, headers: &[(&str, &str)], body: &[u8]) -> Vec<u8> {\n    todo!()\n}\n",
            "driver": (
                "fn show(b: &[u8]) -> String {\n"
                "    String::from_utf8_lossy(b).replace(\"\\r\\n\", \"|\")\n"
                "}\n"
                "\n"
                "fn main() {\n"
                "    println!(\"{}\", show(&build_response(200, &[(\"Content-Type\", \"text/plain\")], \"привет\".as_bytes())));\n"
                "    println!(\"{}\", show(&build_response(404, &[], b\"\")));\n"
                "    println!(\"{}\", show(&build_response(418, &[(\"X-A\", \"1\"), (\"X-B\", \"2\")], b\"tea\")));\n"
                "    println!(\"{}\", build_response(204, &[], b\"\").len());\n"
                "}\n"
            ),
            "expected": ["HTTP/1.1 200 OK|Content-Type: text/plain|Content-Length: 12|Connection: close||привет", "HTTP/1.1 404 Not Found|Content-Length: 0|Connection: close||", "HTTP/1.1 418 Unknown|X-A: 1|X-B: 2|Content-Length: 3|Connection: close||tea", "65"],
            "hint": "body.len() — байты; собирайте заголовок строкой, потом превращайте в байты и дописывайте тело.",
        },
        {
            "id": "rs14-json-encode",
            "mode": "rust",
            "title": "Кодирование JSON",
            "statement": (
                "Для enum Json { Null, Bool(bool), Num(f64), Str(String), "
                "Arr(Vec<Json>), Obj(Vec<(String, Json)>) } напишите to_json(v: "
                "&Json) -> String (компактно, без пробелов, порядок ключей как в "
                "Vec). Числа: целые значения без дробной части (3.0 → 3), иначе "
                "стандартный вывод {}; строки экранируются: \\\" \\\\ \\n \\r \\t, прочие "
                "управляющие символы (< 0x20) — \\u00XX строчными шестнадцатеричными "
                "цифрами."
            ),
            "starter": "enum Json {\n    Null,\n    Bool(bool),\n    Num(f64),\n    Str(String),\n    Arr(Vec<Json>),\n    Obj(Vec<(String, Json)>),\n}\n\nfn to_json(v: &Json) -> String {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let v = Json::Obj(vec![\n"
                "        (\"name\".to_string(), Json::Str(\"Ann \\\"A\\\"\\nLee\\t\\u{1}\".to_string())),\n"
                "        (\"age\".to_string(), Json::Num(31.0)),\n"
                "        (\"score\".to_string(), Json::Num(4.5)),\n"
                "        (\"tags\".to_string(), Json::Arr(vec![Json::Str(\"a\\\\b\".to_string()), Json::Null, Json::Bool(true)])),\n"
                "        (\"nested\".to_string(), Json::Obj(vec![(\"empty\".to_string(), Json::Arr(vec![]))])),\n"
                "        (\"neg\".to_string(), Json::Num(-0.25)),\n"
                "    ]);\n"
                "    println!(\"{}\", to_json(&v));\n"
                "    println!(\"{} {}\", to_json(&Json::Null), to_json(&Json::Obj(vec![])));\n"
                "}\n"
            ),
            "expected": ["{\"name\":\"Ann \\\"A\\\"\\nLee\\t\\u0001\",\"age\":31,\"score\":4.5,\"tags\":[\"a\\\\b\",null,true],\"nested\":{\"empty\":[]},\"neg\":-0.25}", "null {}"],
            "hint": "Рекурсия по вариантам; целое число — через as i64, чтобы не печатать «31.0».",
        },
        {
            "id": "rs14-json-parse",
            "mode": "rust",
            "title": "Разбор JSON",
            "statement": (
                "Напишите parse_json(s: &str) -> Result<Json, String> (enum Json "
                "дан): null, true/false, числа (как у f64::from_str; без ведущих "
                "плюсов), строки с экранированием \\\" \\\\ \\/ \\n \\r \\t \\uXXXX (только "
                "базовая плоскость), массивы и объекты; пробелы между элементами "
                "игнорируются. Любая ошибка синтаксиса или лишние символы после "
                "значения — Err(\"parse error\"). Глубина вложенности в тестах "
                "небольшая."
            ),
            "starter": "#[derive(Debug, PartialEq)]\nenum Json {\n    Null,\n    Bool(bool),\n    Num(f64),\n    Str(String),\n    Arr(Vec<Json>),\n    Obj(Vec<(String, Json)>),\n}\n\nfn parse_json(s: &str) -> Result<Json, String> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", parse_json(r#\"{\"a\": 1, \"b\": [true, null, \"x\\ny\"], \"c\": {\"d\": -2.5e1}}\"#));\n"
                "    println!(\"{:?} {:?}\", parse_json(\"  [ ]  \"), parse_json(\"{}\"));\n"
                "    println!(\"{:?}\", parse_json(r#\"\"Aé \\\"q\\\" \\/\"\"#));\n"
                "    for bad in [\"\", \"[1,\", \"{\\\"a\\\" 1}\", \"tru\", \"[1] x\", \"\\\"abc\", \"+1\", \"{'a':1}\", \"[1 2]\"] {\n"
                "        println!(\"{:?} {:?}\", bad, parse_json(bad));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["Ok(Obj([(\"a\", Num(1.0)), (\"b\", Arr([Bool(true), Null, Str(\"x\\ny\")])), (\"c\", Obj([(\"d\", Num(-25.0))]))]))", "Ok(Arr([])) Ok(Obj([]))", "Ok(Str(\"Aé \\\"q\\\" /\"))", "\"\" Err(\"parse error\")", "\"[1,\" Err(\"parse error\")", "\"{\\\"a\\\" 1}\" Err(\"parse error\")", "\"tru\" Err(\"parse error\")", "\"[1] x\" Err(\"parse error\")", "\"\\\"abc\" Err(\"parse error\")", "\"+1\" Err(\"parse error\")", "\"{'a':1}\" Err(\"parse error\")", "\"[1 2]\" Err(\"parse error\")"],
            "hint": "Рекурсивный спуск: структура с позицией i; value() смотрит на первый байт и выбирает ветку; после значения останутся только пробелы.",
        },
        {
            "id": "rs14-safe-path",
            "mode": "rust",
            "title": "Безопасный путь и тип содержимого",
            "statement": (
                "Напишите safe_join(root: &str, url_path: &str) -> Option<String>: "
                "путь из запроса (без query) присоединяется к корню; допустимы "
                "только обычные компоненты, пустые и '.' пропускаются, любой '..' "
                "или обратная косая черта в компоненте — None; процентное "
                "кодирование НЕ декодируется (но компонент '%2e%2e' — тоже None). "
                "Результат — root + '/' + компоненты через '/'. И mime(path: &str) "
                "-> &'static str: html → text/html; css → text/css; js → "
                "text/javascript; json → application/json; png → image/png; txt → "
                "text/plain; прочее — application/octet-stream (регистр расширения "
                "не важен)."
            ),
            "starter": "fn safe_join(root: &str, url_path: &str) -> Option<String> {\n    todo!()\n}\n\nfn mime(path: &str) -> &'static str {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for p in [\"/index.html\", \"/a/./b//c.css\", \"/\", \"/../etc/passwd\", \"/a/../../x\", \"/a\\\\..\\\\b\", \"/%2E%2e/x\", \"/ok/..hidden\"] {\n"
                "        println!(\"{:?} -> {:?}\", p, safe_join(\"/srv/www/\", p));\n"
                "    }\n"
                "    for f in [\"a.HTML\", \"x/y.js\", \"data.json\", \"logo.PNG\", \"README\", \"archive.tar.gz\", \".txt\", \"a.b/c\"] {\n"
                "        println!(\"{} {}\", f, mime(f));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["\"/index.html\" -> Some(\"/srv/www/index.html\")", "\"/a/./b//c.css\" -> Some(\"/srv/www/a/b/c.css\")", "\"/\" -> Some(\"/srv/www\")", "\"/../etc/passwd\" -> None", "\"/a/../../x\" -> None", "\"/a\\\\..\\\\b\" -> None", "\"/%2E%2e/x\" -> None", "\"/ok/..hidden\" -> Some(\"/srv/www/ok/..hidden\")", "a.HTML text/html", "x/y.js text/javascript", "data.json application/json", "logo.PNG image/png", "README application/octet-stream", "archive.tar.gz application/octet-stream", ".txt text/plain", "a.b/c application/octet-stream"],
            "hint": "Проверяйте каждый компонент отдельно; «..» запрещён всегда, даже если в итоге не выходит за корень.",
        },
        {
            "id": "rs14-range",
            "mode": "rust",
            "title": "Заголовок Range",
            "statement": (
                "Напишите parse_range(header: &str, size: u64) -> Option<(u64, "
                "u64)>: значение 'bytes=START-END' для файла размером size → "
                "включительные границы (первый, последний). 'bytes=500-' — до конца "
                "файла; 'bytes=-100' — последние 100 байт (если файл короче — весь "
                "файл); END больше размера обрезается до size − 1; None — если "
                "формат неверный, START ≥ size, START > END, size = 0 или "
                "диапазонов несколько (запятая)."
            ),
            "starter": "fn parse_range(header: &str, size: u64) -> Option<(u64, u64)> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for h in [\"bytes=0-99\", \"bytes=500-\", \"bytes=-100\", \"bytes=-5000\", \"bytes=900-2000\", \"bytes=1000-1005\", \"bytes=50-10\", \"bytes=0-1,5-6\", \"items=0-1\", \"bytes=\", \"bytes=a-b\", \"bytes=-0\", \"bytes=-\"] {\n"
                "        println!(\"{} {:?}\", h, parse_range(h, 1000));\n"
                "    }\n"
                "    println!(\"{:?}\", parse_range(\"bytes=0-0\", 0));\n"
                "}\n"
            ),
            "expected": ["bytes=0-99 Some((0, 99))", "bytes=500- Some((500, 999))", "bytes=-100 Some((900, 999))", "bytes=-5000 Some((0, 999))", "bytes=900-2000 Some((900, 999))", "bytes=1000-1005 None", "bytes=50-10 None", "bytes=0-1,5-6 None", "items=0-1 None", "bytes= None", "bytes=a-b None", "bytes=-0 None", "bytes=- None", "None"],
            "hint": "Три формы: «a-b», «a-» и «-n»; последнюю считайте через saturating_sub.",
        },
        {
            "id": "rs14-cookies",
            "mode": "rust",
            "title": "Cookie",
            "statement": (
                "Напишите parse_cookies(header: &str) -> BTreeMap<String, String> "
                "(формат 'a=1; b=two; flag'; пробелы вокруг имён и значений "
                "обрезаются; пара без '=' — пустое значение; пустые части "
                "пропускаются; при повторе побеждает последнее) и set_cookie(name: "
                "&str, value: &str, max_age: Option<u32>, http_only: bool) -> "
                "String: 'name=value' + '; Max-Age=N' (если задан) + '; HttpOnly' "
                "(если нужно) + всегда '; Path=/'. Порядок частей: Max-Age, Path, "
                "HttpOnly."
            ),
            "starter": "use std::collections::BTreeMap;\n\nfn parse_cookies(header: &str) -> BTreeMap<String, String> {\n    todo!()\n}\n\nfn set_cookie(name: &str, value: &str, max_age: Option<u32>, http_only: bool) -> String {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", parse_cookies(\"a=1; b = two ;flag; ; a=3; c=x=y\"));\n"
                "    println!(\"{:?} {:?}\", parse_cookies(\"\"), parse_cookies(\" ; \"));\n"
                "    println!(\"{}\", set_cookie(\"sid\", \"abc123\", Some(3600), true));\n"
                "    println!(\"{}\", set_cookie(\"theme\", \"dark\", None, false));\n"
                "}\n"
            ),
            "expected": ["{\"a\": \"3\", \"b\": \"two\", \"c\": \"x=y\", \"flag\": \"\"}", "{} {}", "sid=abc123; Max-Age=3600; Path=/; HttpOnly", "theme=dark; Path=/"],
            "hint": "split(';'), trim, split_once('=') — значение может содержать '=' (берётся всё после первого).",
        },
        {
            "id": "rs14-serve-one",
            "mode": "rust",
            "title": "Мини-сервер: один запрос",
            "statement": (
                "Напишите serve_one(stream: TcpStream) -> io::Result<()>: "
                "прочитайте один HTTP/1.1-запрос (заголовки до пустой строки, тело "
                "по Content-Length), отправьте ответ и закройте соединение "
                "(Connection: close; Content-Length в байтах). Маршруты: GET "
                "/hello?name=X → 200 text/plain \"Hello, X!\" (X без декодирования; "
                "без параметра — \"Hello, world!\"); POST /echo → 200 с телом "
                "запроса; любой другой путь → 404 \"not found\"; для /hello и /echo с "
                "неверным методом → 405 \"method not allowed\"; неразборчивая "
                "стартовая строка → 400 \"bad request\". Тело ответа — текст."
            ),
            "starter": "use std::io;\nuse std::net::TcpStream;\n\nfn serve_one(stream: TcpStream) -> io::Result<()> {\n    todo!()\n}\n",
            "driver": (
                "use std::io::{Read, Write};\n"
                "use std::net::{TcpListener, TcpStream};\n"
                "use std::thread;\n"
                "\n"
                "fn call(addr: std::net::SocketAddr, raw: &str) -> (String, String) {\n"
                "    let mut c = TcpStream::connect(addr).unwrap();\n"
                "    for chunk in raw.as_bytes().chunks(7) {\n"
                "        c.write_all(chunk).unwrap();\n"
                "        c.flush().unwrap();\n"
                "    }\n"
                "    let mut out = String::new();\n"
                "    c.read_to_string(&mut out).unwrap();\n"
                "    let (head, body) = out.split_once(\"\\r\\n\\r\\n\").unwrap();\n"
                "    let status = head.lines().next().unwrap().to_string();\n"
                "    let clen: usize = head.lines().find_map(|l| l.strip_prefix(\"Content-Length: \")).unwrap().parse().unwrap();\n"
                "    assert_eq!(clen, body.len());\n"
                "    (status, body.to_string())\n"
                "}\n"
                "\n"
                "fn main() {\n"
                "    let l = TcpListener::bind(\"127.0.0.1:0\").unwrap();\n"
                "    let addr = l.local_addr().unwrap();\n"
                "    let reqs = [\n"
                "        \"GET /hello?name=Ann HTTP/1.1\\r\\nHost: x\\r\\n\\r\\n\",\n"
                "        \"GET /hello HTTP/1.1\\r\\nHost: x\\r\\n\\r\\n\",\n"
                "        \"POST /echo HTTP/1.1\\r\\nHost: x\\r\\nContent-Length: 21\\r\\n\\r\\nпривет, мир\\n\",\n"
                "        \"DELETE /echo HTTP/1.1\\r\\n\\r\\n\",\n"
                "        \"GET /nope HTTP/1.1\\r\\n\\r\\n\",\n"
                "        \"BROKEN\\r\\n\\r\\n\",\n"
                "    ];\n"
                "    let n = reqs.len();\n"
                "    let srv = thread::spawn(move || {\n"
                "        for s in l.incoming().take(n) {\n"
                "            serve_one(s.unwrap()).unwrap();\n"
                "        }\n"
                "    });\n"
                "    for r in reqs {\n"
                "        println!(\"{:?}\", call(addr, r));\n"
                "    }\n"
                "    srv.join().unwrap();\n"
                "}\n"
            ),
            "expected": ["(\"HTTP/1.1 200 OK\", \"Hello, Ann!\")", "(\"HTTP/1.1 200 OK\", \"Hello, world!\")", "(\"HTTP/1.1 200 OK\", \"привет, мир\\n\")", "(\"HTTP/1.1 405 Method Not Allowed\", \"method not allowed\")", "(\"HTTP/1.1 404 Not Found\", \"not found\")", "(\"HTTP/1.1 400 Bad Request\", \"bad request\")"],
            "hint": "Читайте через BufReader: read_line для стартовой строки и заголовков, read_exact для тела; ответ собирайте одной строкой и пишите write!.",
        },
    ],
    15: [
        {
            "id": "rs15-match-route",
            "mode": "rust",
            "title": "Сопоставление маршрута",
            "statement": (
                "Напишите match_route(pattern: &str, path: &str) -> "
                "Option<BTreeMap<String, String>>: сегменты через '/', ведущие и "
                "хвостовые '/' игнорируются. Сегмент шаблона ':имя' захватывает "
                "один сегмент пути; последний сегмент '*имя' захватывает весь "
                "остаток пути (сегменты через '/', может быть пустым); остальные "
                "сегменты должны совпасть дословно. Число сегментов без '*' должно "
                "совпасть."
            ),
            "starter": "use std::collections::BTreeMap;\n\nfn match_route(pattern: &str, path: &str) -> Option<BTreeMap<String, String>> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", match_route(\"/users/:id/posts/:post\", \"/users/42/posts/7/\"));\n"
                "    println!(\"{:?} {:?}\", match_route(\"/users/:id\", \"/users\"), match_route(\"/users/:id\", \"/accounts/5\"));\n"
                "    println!(\"{:?} {:?}\", match_route(\"/\", \"/\"), match_route(\"/\", \"/x\"));\n"
                "    println!(\"{:?}\", match_route(\"/static/*path\", \"/static/css/site/main.css\"));\n"
                "    println!(\"{:?} {:?}\", match_route(\"/static/*path\", \"/static\"), match_route(\"/static/*path\", \"/other/a\"));\n"
                "    println!(\"{:?}\", match_route(\"/a/:x/*rest\", \"/a/1/b/c\"));\n"
                "}\n"
            ),
            "expected": ["Some({\"id\": \"42\", \"post\": \"7\"})", "None None", "Some({}) None", "Some({\"path\": \"css/site/main.css\"})", "Some({\"path\": \"\"}) None", "Some({\"rest\": \"b/c\", \"x\": \"1\"})"],
            "hint": "Разберите оба пути на сегменты и идите по шаблону: ':' — захват, '*' — хвост (return), иначе — равенство.",
        },
        {
            "id": "rs15-router",
            "mode": "rust",
            "title": "Маршрутизатор с 404 и 405",
            "statement": (
                "Дополните Router: new(), add(&mut self, method, pattern, handler) "
                "и handle(&self, method, path) -> (u16, String): первая запись, у "
                "которой совпали метод и шаблон, вызывает обработчик с параметрами "
                "и возвращает (200, результат). Если ни одна не подошла, но шаблон "
                "совпал для другого метода — (405, \"method not allowed\"); если "
                "шаблон не совпал нигде — (404, \"not found\"). Функция match_route "
                "уже написана."
            ),
            "starter": "use std::collections::BTreeMap;\n\ntype Params = BTreeMap<String, String>;\ntype Handler = Box<dyn Fn(&Params) -> String>;\n\nfn match_route(pattern: &str, path: &str) -> Option<Params> {\n    let segs = |s: &str| -> Vec<String> { s.split('/').filter(|x| !x.is_empty()).map(|x| x.to_string()).collect() };\n    let (p, q) = (segs(pattern), segs(path));\n    if p.len() != q.len() {\n        return None;\n    }\n    let mut params = Params::new();\n    for (a, b) in p.iter().zip(q.iter()) {\n        if let Some(name) = a.strip_prefix(':') {\n            params.insert(name.to_string(), b.clone());\n        } else if a != b {\n            return None;\n        }\n    }\n    Some(params)\n}\n\nstruct Router {\n    routes: Vec<(String, String, Handler)>,\n}\n\nimpl Router {\n    fn new() -> Router {\n        todo!()\n    }\n    fn add(&mut self, method: &str, pattern: &str, h: Handler) {\n        todo!()\n    }\n    fn handle(&self, method: &str, path: &str) -> (u16, String) {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let mut r = Router::new();\n"
                "    r.add(\"GET\", \"/users/new\", Box::new(|_| \"new form\".to_string()));\n"
                "    r.add(\"GET\", \"/users/:id\", Box::new(|p| format!(\"user {}\", p[\"id\"])));\n"
                "    r.add(\"DELETE\", \"/users/:id\", Box::new(|p| format!(\"deleted {}\", p[\"id\"])));\n"
                "    r.add(\"GET\", \"/\", Box::new(|_| \"home\".to_string()));\n"
                "    for (m, p) in [(\"GET\", \"/users/new\"), (\"GET\", \"/users/42\"), (\"DELETE\", \"/users/7\"), (\"POST\", \"/users/7\"), (\"GET\", \"/nope\"), (\"GET\", \"/\"), (\"PUT\", \"/\")] {\n"
                "        println!(\"{} {} -> {:?}\", m, p, r.handle(m, p));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["GET /users/new -> (200, \"new form\")", "GET /users/42 -> (200, \"user 42\")", "DELETE /users/7 -> (200, \"deleted 7\")", "POST /users/7 -> (405, \"method not allowed\")", "GET /nope -> (404, \"not found\")", "GET / -> (200, \"home\")", "PUT / -> (405, \"method not allowed\")"],
            "hint": "Один проход: запоминайте, совпал ли шаблон при другом методе; результат — после цикла.",
        },
        {
            "id": "rs15-middleware",
            "mode": "rust",
            "title": "Цепочка слоёв",
            "statement": (
                "Типы: Handler = Rc<dyn Fn(&Request) -> Response>, Layer = Rc<dyn "
                "Fn(&Request, &Handler) -> Response> (слой получает запрос и "
                "«следующий» обработчик). Напишите compose(layers: Vec<Layer>, "
                "endpoint: Handler) -> Handler: первый слой в списке — самый "
                "внешний (вызывается первым), последний вызывает endpoint."
            ),
            "starter": "use std::rc::Rc;\n\nstruct Request {\n    path: String,\n    auth: Option<String>,\n}\n\n#[derive(Debug, PartialEq)]\nstruct Response {\n    status: u16,\n    body: String,\n}\n\ntype Handler = Rc<dyn Fn(&Request) -> Response>;\ntype Layer = Rc<dyn Fn(&Request, &Handler) -> Response>;\n\nfn compose(layers: Vec<Layer>, endpoint: Handler) -> Handler {\n    todo!()\n}\n",
            "driver": (
                "use std::cell::RefCell;\n"
                "\n"
                "fn main() {\n"
                "    let log: Rc<RefCell<Vec<String>>> = Rc::new(RefCell::new(Vec::new()));\n"
                "    let l1 = Rc::clone(&log);\n"
                "    let logging: Layer = Rc::new(move |req, next| {\n"
                "        l1.borrow_mut().push(format!(\"in {}\", req.path));\n"
                "        let r = next(req);\n"
                "        l1.borrow_mut().push(format!(\"out {}\", r.status));\n"
                "        r\n"
                "    });\n"
                "    let auth: Layer = Rc::new(|req, next| {\n"
                "        if req.auth.as_deref() == Some(\"secret\") {\n"
                "            next(req)\n"
                "        } else {\n"
                "            Response { status: 401, body: \"unauthorized\".to_string() }\n"
                "        }\n"
                "    });\n"
                "    let l2 = Rc::clone(&log);\n"
                "    let tag: Layer = Rc::new(move |req, next| {\n"
                "        l2.borrow_mut().push(\"tag\".to_string());\n"
                "        let mut r = next(req);\n"
                "        r.body.push('!');\n"
                "        r\n"
                "    });\n"
                "    let endpoint: Handler = Rc::new(|req| Response { status: 200, body: format!(\"hello {}\", req.path) });\n"
                "    let app = compose(vec![logging, auth, tag], endpoint);\n"
                "    println!(\"{:?}\", app(&Request { path: \"/a\".into(), auth: Some(\"secret\".into()) }));\n"
                "    println!(\"{:?}\", app(&Request { path: \"/b\".into(), auth: None }));\n"
                "    println!(\"{:?}\", log.borrow());\n"
                "    let bare = compose(vec![], Rc::new(|_| Response { status: 204, body: String::new() }));\n"
                "    println!(\"{:?}\", bare(&Request { path: \"/\".into(), auth: None }));\n"
                "}\n"
            ),
            "expected": ["Response { status: 200, body: \"hello /a!\" }", "Response { status: 401, body: \"unauthorized\" }", "[\"in /a\", \"tag\", \"out 200\", \"in /b\", \"out 401\"]", "Response { status: 204, body: \"\" }"],
            "hint": "Оборачивайте с конца: последний слой — вокруг endpoint, предпоследний — вокруг получившегося и так далее; layer и next перемещаются в замыкание.",
        },
        {
            "id": "rs15-todo-api",
            "mode": "rust",
            "title": "REST-интерфейс списка дел",
            "statement": (
                "Хранилище Store уже написано. Напишите handle(store: "
                "&Mutex<Store>, method: &str, path: &str, body: &str) -> (u16, "
                "String): GET /todos → (200, JSON-массив по возрастанию id: "
                "[{\"id\":1,\"title\":\"a\",\"done\":false}], пустой — []); POST /todos "
                "(тело — название без кавычек, обрезается; пустое → (400, \"empty "
                "title\")) → (201, {\"id\":N}); GET /todos/ID → (200, объект) или "
                "(404, \"not found\"); нечисловой ID → (400, \"bad id\"); PUT "
                "/todos/ID/done → (200, \"done\") или 404; DELETE /todos/ID → (204, "
                "\"\") или 404. Известный путь с другим методом — (405, \"method not "
                "allowed\"); неизвестный путь — (404, \"not found\")."
            ),
            "starter": "use std::collections::BTreeMap;\nuse std::sync::Mutex;\n\nstruct Todo {\n    title: String,\n    done: bool,\n}\n\nstruct Store {\n    next: u32,\n    items: BTreeMap<u32, Todo>,\n}\n\nimpl Store {\n    fn new() -> Store {\n        Store { next: 1, items: BTreeMap::new() }\n    }\n    fn create(&mut self, title: &str) -> u32 {\n        let id = self.next;\n        self.next += 1;\n        self.items.insert(id, Todo { title: title.to_string(), done: false });\n        id\n    }\n}\n\nfn handle(store: &Mutex<Store>, method: &str, path: &str, body: &str) -> (u16, String) {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let s = Mutex::new(Store::new());\n"
                "    for (m, p, b) in [\n"
                "        (\"GET\", \"/todos\", \"\"),\n"
                "        (\"POST\", \"/todos\", \"  write chapter \"),\n"
                "        (\"POST\", \"/todos\", \"test server\"),\n"
                "        (\"POST\", \"/todos\", \"   \"),\n"
                "        (\"GET\", \"/todos/1\", \"\"),\n"
                "        (\"PUT\", \"/todos/1/done\", \"\"),\n"
                "        (\"GET\", \"/todos\", \"\"),\n"
                "        (\"GET\", \"/todos/9\", \"\"),\n"
                "        (\"GET\", \"/todos/abc\", \"\"),\n"
                "        (\"DELETE\", \"/todos/2\", \"\"),\n"
                "        (\"DELETE\", \"/todos/2\", \"\"),\n"
                "        (\"PATCH\", \"/todos\", \"\"),\n"
                "        (\"GET\", \"/todos/1/done\", \"\"),\n"
                "        (\"GET\", \"/nope\", \"\"),\n"
                "    ] {\n"
                "        println!(\"{} {} -> {:?}\", m, p, handle(&s, m, p, b));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["GET /todos -> (200, \"[]\")", "POST /todos -> (201, \"{\\\"id\\\":1}\")", "POST /todos -> (201, \"{\\\"id\\\":2}\")", "POST /todos -> (400, \"empty title\")", "GET /todos/1 -> (200, \"{\\\"id\\\":1,\\\"title\\\":\\\"write chapter\\\",\\\"done\\\":false}\")", "PUT /todos/1/done -> (200, \"done\")", "GET /todos -> (200, \"[{\\\"id\\\":1,\\\"title\\\":\\\"write chapter\\\",\\\"done\\\":true},{\\\"id\\\":2,\\\"title\\\":\\\"test server\\\",\\\"done\\\":false}]\")", "GET /todos/9 -> (404, \"not found\")", "GET /todos/abc -> (400, \"bad id\")", "DELETE /todos/2 -> (204, \"\")", "DELETE /todos/2 -> (404, \"not found\")", "PATCH /todos -> (405, \"method not allowed\")", "GET /todos/1/done -> (405, \"method not allowed\")", "GET /nope -> (404, \"not found\")"],
            "hint": "Разбейте путь на сегменты и сопоставляйте срез: [\"todos\"], [\"todos\", id], [\"todos\", id, \"done\"]; блокировку берите один раз в начале.",
        },
        {
            "id": "rs15-thread-pool",
            "mode": "rust",
            "title": "Пул потоков",
            "statement": (
                "Реализуйте ThreadPool: new(n) запускает n рабочих потоков, "
                "execute(&self, f) отправляет задание (FnOnce + Send + 'static) в "
                "общую очередь, а Drop закрывает очередь и дожидается всех рабочих "
                "(принятые задания выполняются до конца)."
            ),
            "starter": "use std::sync::{mpsc, Arc, Mutex};\nuse std::thread;\n\ntype Job = Box<dyn FnOnce() + Send + 'static>;\n\nstruct ThreadPool {\n    workers: Vec<thread::JoinHandle<()>>,\n    tx: Option<mpsc::Sender<Job>>,\n}\n\nimpl ThreadPool {\n    fn new(n: usize) -> ThreadPool {\n        todo!()\n    }\n    fn execute<F: FnOnce() + Send + 'static>(&self, f: F) {\n        todo!()\n    }\n}\n\nimpl Drop for ThreadPool {\n    fn drop(&mut self) {\n        todo!()\n    }\n}\n",
            "driver": (
                "use std::sync::atomic::{AtomicUsize, Ordering};\n"
                "\n"
                "fn main() {\n"
                "    let done = Arc::new(AtomicUsize::new(0));\n"
                "    let running = Arc::new(AtomicUsize::new(0));\n"
                "    let peak = Arc::new(AtomicUsize::new(0));\n"
                "    {\n"
                "        let pool = ThreadPool::new(4);\n"
                "        for _ in 0..40 {\n"
                "            let (d, r, p) = (Arc::clone(&done), Arc::clone(&running), Arc::clone(&peak));\n"
                "            pool.execute(move || {\n"
                "                let now = r.fetch_add(1, Ordering::SeqCst) + 1;\n"
                "                p.fetch_max(now, Ordering::SeqCst);\n"
                "                std::thread::sleep(std::time::Duration::from_millis(5));\n"
                "                r.fetch_sub(1, Ordering::SeqCst);\n"
                "                d.fetch_add(1, Ordering::SeqCst);\n"
                "            });\n"
                "        }\n"
                "    }\n"
                "    println!(\"{} {}\", done.load(Ordering::SeqCst), peak.load(Ordering::SeqCst) <= 4);\n"
                "    let empty = ThreadPool::new(2);\n"
                "    drop(empty);\n"
                "    println!(\"ok\");\n"
                "}\n"
            ),
            "expected": ["40 true", "ok"],
            "hint": "Приёмник один — оберните его в Arc<Mutex<_>>; в Drop сначала закройте канал (take + drop), потом join.",
        },
        {
            "id": "rs15-serve-until",
            "mode": "rust",
            "title": "Сервер с мягкой остановкой",
            "statement": (
                "Напишите serve_until(listener: TcpListener, stop: Arc<AtomicBool>, "
                "handler: fn(TcpStream)) -> usize: переведите сокет в неблокирующий "
                "режим и, пока флаг stop не поднят, принимайте соединения (каждое "
                "передаётся в handler в этом же потоке); если принимать нечего — "
                "спите 2 мс. Верните число обработанных соединений."
            ),
            "starter": "use std::net::{TcpListener, TcpStream};\nuse std::sync::atomic::AtomicBool;\nuse std::sync::Arc;\n\nfn serve_until(listener: TcpListener, stop: Arc<AtomicBool>, handler: fn(TcpStream)) -> usize {\n    todo!()\n}\n",
            "driver": (
                "use std::io::{Read, Write};\n"
                "use std::net::{TcpListener, TcpStream};\n"
                "use std::sync::atomic::{AtomicBool, Ordering};\n"
                "use std::sync::Arc;\n"
                "use std::thread;\n"
                "use std::time::Duration;\n"
                "\n"
                "fn upper(mut s: TcpStream) {\n"
                "    let mut buf = [0u8; 64];\n"
                "    let n = s.read(&mut buf).unwrap();\n"
                "    s.write_all(&buf[..n].to_ascii_uppercase()).unwrap();\n"
                "}\n"
                "\n"
                "fn main() {\n"
                "    let listener = TcpListener::bind(\"127.0.0.1:0\").unwrap();\n"
                "    let addr = listener.local_addr().unwrap();\n"
                "    let stop = Arc::new(AtomicBool::new(false));\n"
                "    let flag = Arc::clone(&stop);\n"
                "    let server = thread::spawn(move || serve_until(listener, flag, upper));\n"
                "    for word in [\"alpha\", \"beta\", \"gamma\"] {\n"
                "        let mut c = TcpStream::connect(addr).unwrap();\n"
                "        c.write_all(word.as_bytes()).unwrap();\n"
                "        let mut reply = String::new();\n"
                "        c.read_to_string(&mut reply).unwrap();\n"
                "        println!(\"{}\", reply);\n"
                "    }\n"
                "    thread::sleep(Duration::from_millis(20));\n"
                "    stop.store(true, Ordering::SeqCst);\n"
                "    println!(\"handled {}\", server.join().unwrap());\n"
                "    let l2 = TcpListener::bind(\"127.0.0.1:0\").unwrap();\n"
                "    let stopped = Arc::new(AtomicBool::new(true));\n"
                "    println!(\"handled {}\", serve_until(l2, stopped, upper));\n"
                "}\n"
            ),
            "expected": ["ALPHA", "BETA", "GAMMA", "handled 3", "handled 0"],
            "hint": "accept() неблокирующего сокета возвращает ошибку WouldBlock, если соединений нет; принятому потоку верните блокирующий режим.",
        },
        {
            "id": "rs15-rate-limiter",
            "mode": "rust",
            "title": "Ограничитель по клиентам",
            "statement": (
                "Реализуйте RateLimiter: new(capacity: f64, rate: f64) (у каждого "
                "нового ключа ведро полное; last = момент первого обращения) и "
                "allow(&mut self, key: &str, now: f64) -> bool: ведро пополняется "
                "на (now − last) · rate, не больше capacity; запрос стоит один "
                "жетон. Клиенты не влияют друг на друга. Время приходит неубывающим "
                "для одного ключа."
            ),
            "starter": "use std::collections::HashMap;\n\nstruct RateLimiter {\n    capacity: f64,\n    rate: f64,\n    buckets: HashMap<String, (f64, f64)>,\n}\n\nimpl RateLimiter {\n    fn new(capacity: f64, rate: f64) -> RateLimiter {\n        todo!()\n    }\n    fn allow(&mut self, key: &str, now: f64) -> bool {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let mut rl = RateLimiter::new(2.0, 0.5);\n"
                "    let calls = [(\"a\", 0.0), (\"a\", 0.0), (\"a\", 0.0), (\"b\", 0.0), (\"a\", 1.0), (\"a\", 2.0), (\"a\", 2.0), (\"b\", 0.5), (\"b\", 4.0), (\"b\", 4.0), (\"b\", 4.0)];\n"
                "    let r: Vec<String> = calls.iter().map(|&(k, t)| format!(\"{}@{}={}\", k, t, rl.allow(k, t))).collect();\n"
                "    println!(\"{}\", r.join(\" \"));\n"
                "    let mut hot = RateLimiter::new(1.0, 1000.0);\n"
                "    let allowed = (0..100_000).filter(|&i| hot.allow(&format!(\"c{}\", i % 10), i as f64 / 1000.0)).count();\n"
                "    println!(\"{}\", allowed);\n"
                "}\n"
            ),
            "expected": ["a@0=true a@0=true a@0=false b@0=true a@1=false a@2=true a@2=false b@0.5=true b@4=true b@4=true b@4=false", "100000"],
            "hint": "Состояние ключа — пара (жетоны, последнее время); обновляйте её и при отказе (жетоны пополнились).",
        },
        {
            "id": "rs15-histogram",
            "mode": "rust",
            "title": "Гистограмма задержек",
            "statement": (
                "Реализуйте Histogram::new(bounds: &[u64]) (верхние границы корзин "
                "в мс по возрастанию), observe(&mut self, ms: u64) и render(&self, "
                "name: &str) -> String в стиле Prometheus: для каждой границы "
                "строка name_bucket{le=\"B\"} N, где N — число наблюдений ≤ B "
                "(накопительно); затем name_bucket{le=\"+Inf\"} (все наблюдения), "
                "name_count и name_sum. Строки разделены \\n, без завершающего."
            ),
            "starter": "struct Histogram {\n    bounds: Vec<u64>,\n    counts: Vec<u64>,\n    total: u64,\n    sum: u64,\n}\n\nimpl Histogram {\n    fn new(bounds: &[u64]) -> Histogram {\n        todo!()\n    }\n    fn observe(&mut self, ms: u64) {\n        todo!()\n    }\n    fn render(&self, name: &str) -> String {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let mut h = Histogram::new(&[10, 50, 100]);\n"
                "    for ms in [3, 10, 11, 49, 50, 99, 250, 1000] {\n"
                "        h.observe(ms);\n"
                "    }\n"
                "    println!(\"{}\", h.render(\"latency_ms\"));\n"
                "    println!(\"{}\", Histogram::new(&[]).render(\"x\"));\n"
                "}\n"
            ),
            "expected": ["latency_ms_bucket{le=\"10\"} 2", "latency_ms_bucket{le=\"50\"} 5", "latency_ms_bucket{le=\"100\"} 6", "latency_ms_bucket{le=\"+Inf\"} 8", "latency_ms_count 8", "latency_ms_sum 1472", "x_bucket{le=\"+Inf\"} 0", "x_count 0", "x_sum 0"],
            "hint": "Накопительные корзины: наблюдение увеличивает счётчик каждой границы, которая не меньше значения.",
        },
        {
            "id": "rs15-parse-args",
            "mode": "rust",
            "title": "Разбор командной строки",
            "statement": (
                "Напишите parse_args(args: &[&str]) -> Result<Options, String> "
                "(Options дана): '--name=value' и '--name value' → options[name] = "
                "value; '--flag' без значения (следующий элемент начинается с '-' "
                "или это конец списка) → flags содержит flag; '-v', '-vv', '-vvv' → "
                "verbose += число букв v; '--' — всё остальное позиционные "
                "аргументы; прочее — позиционные. Ошибки: '-x' с буквой, не v → "
                "Err(\"unknown option -x\"); '--=v' → Err(\"empty option name\")."
            ),
            "starter": "use std::collections::BTreeMap;\n\n#[derive(Debug, Default, PartialEq)]\nstruct Options {\n    options: BTreeMap<String, String>,\n    flags: Vec<String>,\n    verbose: u32,\n    positional: Vec<String>,\n}\n\nfn parse_args(args: &[&str]) -> Result<Options, String> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", parse_args(&[\"--port=8080\", \"--host\", \"localhost\", \"-vv\", \"--debug\", \"file.txt\", \"-v\", \"--\", \"--not-an-option\", \"-x\"]));\n"
                "    println!(\"{:?}\", parse_args(&[]));\n"
                "    println!(\"{:?}\", parse_args(&[\"--a\", \"--b\", \"val\", \"pos\"]));\n"
                "    println!(\"{:?} {:?} {:?}\", parse_args(&[\"-x\"]), parse_args(&[\"--=v\"]), parse_args(&[\"--\"]));\n"
                "    println!(\"{:?}\", parse_args(&[\"-\"]));\n"
                "}\n"
            ),
            "expected": ["Ok(Options { options: {\"debug\": \"file.txt\", \"host\": \"localhost\", \"port\": \"8080\"}, flags: [], verbose: 3, positional: [\"--not-an-option\", \"-x\"] })", "Ok(Options { options: {}, flags: [], verbose: 0, positional: [] })", "Ok(Options { options: {\"b\": \"val\"}, flags: [\"a\"], verbose: 0, positional: [\"pos\"] })", "Err(\"unknown option -x\") Err(\"empty option name\") Ok(Options { options: {}, flags: [], verbose: 0, positional: [] })", "Ok(Options { options: {}, flags: [], verbose: 0, positional: [\"-\"] })"],
            "hint": "Один цикл с индексом: у «--имя» значение берётся из следующего элемента, если он не начинается с '-'.",
        },
    ],
    16: [
        {
            "id": "rs16-encode-messages",
            "mode": "rust",
            "title": "Сообщения клиента Postgres",
            "statement": (
                "Напишите startup_message(params: &[(&str, &str)]) -> Vec<u8> "
                "(длина i32 включая себя; версия протокола 196608 (3.0) как i32; "
                "затем пары 'имя\\0значение\\0'; в конце ещё один нулевой байт), "
                "query_message(sql: &str) -> Vec<u8> ('Q', длина i32 = 4 + байты "
                "sql + 1, текст, нулевой байт), terminate_message() -> Vec<u8> "
                "('X', длина 4) и password_message(pw: &str) -> Vec<u8> ('p', "
                "длина, пароль и нулевой байт). Все числа — старшим байтом вперёд."
            ),
            "starter": "fn startup_message(params: &[(&str, &str)]) -> Vec<u8> {\n    todo!()\n}\n\nfn query_message(sql: &str) -> Vec<u8> {\n    todo!()\n}\n\nfn terminate_message() -> Vec<u8> {\n    todo!()\n}\n\nfn password_message(pw: &str) -> Vec<u8> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let s = startup_message(&[(\"user\", \"app\"), (\"database\", \"shop\")]);\n"
                "    println!(\"{} {:?}\", s.len(), &s[..8]);\n"
                "    println!(\"{:?}\", String::from_utf8_lossy(&s[8..]).replace('\\0', \"|\"));\n"
                "    println!(\"{:?}\", startup_message(&[]));\n"
                "    println!(\"{:?}\", query_message(\"SELECT 1\"));\n"
                "    println!(\"{:?} {:?}\", terminate_message(), password_message(\"pw\"));\n"
                "    let q = query_message(\"SELECT 'привет'\");\n"
                "    println!(\"{} {}\", q.len(), u32::from_be_bytes([q[1], q[2], q[3], q[4]]));\n"
                "}\n"
            ),
            "expected": ["32 [0, 0, 0, 32, 0, 3, 0, 0]", "\"user|app|database|shop||\"", "[0, 0, 0, 9, 0, 3, 0, 0, 0]", "[81, 0, 0, 0, 13, 83, 69, 76, 69, 67, 84, 32, 49, 0]", "[88, 0, 0, 0, 4] [112, 0, 0, 0, 7, 112, 119, 0]", "27 26"],
            "hint": "Общий помощник: метка + (длина тела + 4) как u32::to_be_bytes + тело.",
        },
        {
            "id": "rs16-decode-messages",
            "mode": "rust",
            "title": "Сообщения сервера Postgres",
            "statement": (
                "Напишите read_message(buf: &[u8]) -> Option<(u8, Vec<u8>, usize)> "
                "(метка, содержимое, сколько байтов занято; None — если сообщение "
                "неполное), data_row(payload: &[u8]) -> Result<Vec<Option<String>>, "
                "String> (число колонок i16, для каждой длина i32 и байты; −1 — "
                "NULL; ошибка \"truncated\", если данных не хватает) и "
                "error_fields(payload: &[u8]) -> BTreeMap<char, String> "
                "(ErrorResponse: пары 'метка-байт, строка с нулём', завершается "
                "нулевым байтом)."
            ),
            "starter": "use std::collections::BTreeMap;\n\nfn read_message(buf: &[u8]) -> Option<(u8, Vec<u8>, usize)> {\n    todo!()\n}\n\nfn data_row(payload: &[u8]) -> Result<Vec<Option<String>>, String> {\n    todo!()\n}\n\nfn error_fields(payload: &[u8]) -> BTreeMap<char, String> {\n    todo!()\n}\n",
            "driver": (
                "fn msg(tag: u8, payload: &[u8]) -> Vec<u8> {\n"
                "    let mut m = vec![tag];\n"
                "    m.extend_from_slice(&((payload.len() + 4) as u32).to_be_bytes());\n"
                "    m.extend_from_slice(payload);\n"
                "    m\n"
                "}\n"
                "\n"
                "fn main() {\n"
                "    let mut row = vec![0, 3];\n"
                "    for c in [Some(\"42\"), None, Some(\"привет\")] {\n"
                "        match c {\n"
                "            Some(s) => {\n"
                "                row.extend_from_slice(&(s.len() as i32).to_be_bytes());\n"
                "                row.extend_from_slice(s.as_bytes());\n"
                "            }\n"
                "            None => row.extend_from_slice(&(-1i32).to_be_bytes()),\n"
                "        }\n"
                "    }\n"
                "    let mut stream = msg(b'D', &row);\n"
                "    stream.extend(msg(b'C', b\"SELECT 1\\0\"));\n"
                "    stream.extend(msg(b'Z', b\"I\"));\n"
                "    let mut off = 0;\n"
                "    while let Some((tag, payload, used)) = read_message(&stream[off..]) {\n"
                "        println!(\"{} {} {}\", tag as char, payload.len(), used);\n"
                "        off += used;\n"
                "    }\n"
                "    println!(\"{}\", off == stream.len());\n"
                "    let (_, p, _) = read_message(&stream).unwrap();\n"
                "    println!(\"{:?}\", data_row(&p));\n"
                "    println!(\"{:?} {:?}\", data_row(&p[..10]), data_row(&[0, 1, 0, 0, 0, 9, 1]));\n"
                "    println!(\"{:?} {:?}\", read_message(&stream[..4]), read_message(&stream[..8]).map(|m| m.0));\n"
                "    let err = b\"SERROR\\0C42P01\\0Mrelation \\\"users\\\" does not exist\\0\\0\";\n"
                "    println!(\"{:?}\", error_fields(err));\n"
                "}\n"
            ),
            "expected": ["D 28 33", "C 9 14", "Z 1 6", "true", "Ok([Some(\"42\"), None, Some(\"привет\")])", "Err(\"truncated\") Err(\"truncated\")", "None None", "{'C': \"42P01\", 'M': \"relation \\\"users\\\" does not exist\", 'S': \"ERROR\"}"],
            "hint": "Проверяйте границы всегда через get(..) — неполные данные не должны вызывать панику.",
        },
        {
            "id": "rs16-from-column",
            "mode": "rust",
            "title": "Отображение колонок в типы",
            "statement": (
                "Трейт FromColumn с методом from_col(c: Option<&str>) -> "
                "Result<Self, String> дан. Реализуйте его для i32 (NULL → "
                "Err(\"NULL\"), нечисло → Err(\"bad int: ТЕКСТ\")), f64 (аналогично "
                "\"bad float: ТЕКСТ\"), bool ('t'/'f'; иное — Err(\"bad bool: "
                "ТЕКСТ\")), String и Option<T> (для любого T: FromColumn; None → "
                "Ok(None)). Затем напишите product_from_row(row: &[Option<&str>]) "
                "-> Result<Product, String>; ошибки колонки оформляются как \"column "
                "N: ошибка\" (N с нуля)."
            ),
            "starter": "trait FromColumn: Sized {\n    fn from_col(c: Option<&str>) -> Result<Self, String>;\n}\n\n#[derive(Debug, PartialEq)]\nstruct Product {\n    id: i32,\n    title: String,\n    price: f64,\n    in_stock: bool,\n    discount: Option<f64>,\n}\n\n// impl FromColumn for i32, f64, bool, String, Option<T> ...\n\nfn product_from_row(row: &[Option<&str>]) -> Result<Product, String> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", product_from_row(&[Some(\"1\"), Some(\"Laptop\"), Some(\"999.5\"), Some(\"t\"), None]));\n"
                "    println!(\"{:?}\", product_from_row(&[Some(\"2\"), Some(\"Mouse\"), Some(\"15\"), Some(\"f\"), Some(\"0.1\")]));\n"
                "    println!(\"{:?}\", product_from_row(&[Some(\"x\"), Some(\"A\"), Some(\"1\"), Some(\"t\"), None]));\n"
                "    println!(\"{:?}\", product_from_row(&[Some(\"3\"), None, Some(\"1\"), Some(\"t\"), None]));\n"
                "    println!(\"{:?}\", product_from_row(&[Some(\"3\"), Some(\"B\"), Some(\"1.x\"), Some(\"t\"), None]));\n"
                "    println!(\"{:?}\", product_from_row(&[Some(\"3\"), Some(\"B\"), Some(\"1\"), Some(\"yes\"), None]));\n"
                "    println!(\"{:?}\", product_from_row(&[Some(\"3\"), Some(\"B\"), Some(\"1\"), Some(\"t\"), Some(\"zz\")]));\n"
                "    println!(\"{:?}\", product_from_row(&[Some(\"3\")]));\n"
                "}\n"
            ),
            "expected": ["Ok(Product { id: 1, title: \"Laptop\", price: 999.5, in_stock: true, discount: None })", "Ok(Product { id: 2, title: \"Mouse\", price: 15.0, in_stock: false, discount: Some(0.1) })", "Err(\"column 0: bad int: x\")", "Err(\"column 1: NULL\")", "Err(\"column 2: bad float: 1.x\")", "Err(\"column 3: bad bool: yes\")", "Err(\"column 4: bad float: zz\")", "Err(\"column 1: NULL\")"],
            "hint": "Вспомогательная обобщённая функция col::<T>(row, i) собирает префикс «column N: » к любой ошибке.",
        },
        {
            "id": "rs16-render-query",
            "mode": "rust",
            "title": "Подстановка параметров для журнала",
            "statement": (
                "Для лога запросов напишите quote_literal(s: &str) -> String "
                "(кавычки вокруг, внутренние ' удваиваются) и render_query(sql: "
                "&str, params: &[Option<&str>]) -> String: каждое $N (N — число из "
                "одной или нескольких цифр, нумерация с единицы) заменяется на NULL "
                "для None и quote_literal для Some; $N с номером вне списка и "
                "одиночный '$' остаются как есть. Внутри строковых литералов в sql "
                "замен не делайте (текст между одинарными кавычками копируется без "
                "изменений; '' внутри — экранированная кавычка)."
            ),
            "starter": "fn quote_literal(s: &str) -> String {\n    todo!()\n}\n\nfn render_query(sql: &str, params: &[Option<&str>]) -> String {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{}\", quote_literal(\"O'Brien\"));\n"
                "    println!(\"{}\", render_query(\"SELECT * FROM u WHERE name = $1 AND age > $2 AND note IS NOT DISTINCT FROM $3\", &[Some(\"x' OR '1'='1\"), Some(\"18\"), None]));\n"
                "    println!(\"{}\", render_query(\"SELECT $1, $10, $2, '$1 stays', $5, $\", &[Some(\"a\"), Some(\"b\")]));\n"
                "    let many: Vec<String> = (1..=10).map(|i| format!(\"v{}\", i)).collect();\n"
                "    let refs: Vec<Option<&str>> = many.iter().map(|s| Some(s.as_str())).collect();\n"
                "    println!(\"{}\", render_query(\"$1 $10 $2\", &refs));\n"
                "    println!(\"{}\", render_query(\"SELECT 'it''s $1' || $1\", &[Some(\"z\")]));\n"
                "}\n"
            ),
            "expected": ["'O''Brien'", "SELECT * FROM u WHERE name = 'x'' OR ''1''=''1' AND age > '18' AND note IS NOT DISTINCT FROM NULL", "SELECT 'a', $10, 'b', '$1 stays', $5, $", "'v1' 'v10' 'v2'", "SELECT 'it''s $1' || 'z'"],
            "hint": "Идите по символам, помните, внутри ли вы строкового литерала; число после '$' читайте до конца цифр, чтобы $10 не превратился в $1 и '0'.",
        },
        {
            "id": "rs16-select-builder",
            "mode": "rust",
            "title": "Построитель SELECT",
            "statement": (
                "Реализуйте Select: from(table), filter(mut self, col, op, value) "
                "(добавляет «col op $N»), filter_in(mut self, col, values: &[&str]) "
                "(«col IN ($N, $N+1, …)»; пустой список — условие «FALSE»), "
                "order_by(mut self, col, desc: bool), limit(mut self, n), "
                "offset(mut self, n) и build(&self) -> (String, Vec<String>): "
                "'SELECT * FROM t' + ' WHERE a AND b' + ' ORDER BY col ASC|DESC' + "
                "' LIMIT n' + ' OFFSET n'; параметры — в порядке нумерации."
            ),
            "starter": "struct Select {\n    table: String,\n    conds: Vec<String>,\n    params: Vec<String>,\n    order: Option<String>,\n    limit: Option<u32>,\n    offset: Option<u32>,\n}\n\nimpl Select {\n    fn from(table: &str) -> Select {\n        todo!()\n    }\n    fn filter(mut self, col: &str, op: &str, value: &str) -> Select {\n        todo!()\n    }\n    fn filter_in(mut self, col: &str, values: &[&str]) -> Select {\n        todo!()\n    }\n    fn order_by(mut self, col: &str, desc: bool) -> Select {\n        todo!()\n    }\n    fn limit(mut self, n: u32) -> Select {\n        todo!()\n    }\n    fn offset(mut self, n: u32) -> Select {\n        todo!()\n    }\n    fn build(&self) -> (String, Vec<String>) {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let (sql, p) = Select::from(\"users\").build();\n"
                "    println!(\"{} {:?}\", sql, p);\n"
                "    let q = Select::from(\"orders\")\n"
                "        .filter(\"total\", \">\", \"100\")\n"
                "        .filter_in(\"status\", &[\"new\", \"paid\", \"shipped\"])\n"
                "        .filter(\"city\", \"=\", \"Moscow\")\n"
                "        .order_by(\"created_at\", true)\n"
                "        .limit(20)\n"
                "        .offset(40);\n"
                "    let (sql, p) = q.build();\n"
                "    println!(\"{}\", sql);\n"
                "    println!(\"{:?}\", p);\n"
                "    let (sql, p) = Select::from(\"t\").filter_in(\"id\", &[]).limit(1).build();\n"
                "    println!(\"{} {:?}\", sql, p);\n"
                "}\n"
            ),
            "expected": ["SELECT * FROM users []", "SELECT * FROM orders WHERE total > $1 AND status IN ($2, $3, $4) AND city = $5 ORDER BY created_at DESC LIMIT 20 OFFSET 40", "[\"100\", \"new\", \"paid\", \"shipped\", \"Moscow\"]", "SELECT * FROM t WHERE FALSE LIMIT 1 []"],
            "hint": "Номер параметра = длина списка params после добавления; filter_in добавляет сразу несколько.",
        },
        {
            "id": "rs16-pool-timeout",
            "mode": "rust",
            "title": "Пул соединений с таймаутом",
            "statement": (
                "Реализуйте Pool: new(n: u32) -> Arc<Pool> (соединения 1…n), "
                "get(self: &Arc<Self>, timeout: Duration) -> Option<PooledConn> "
                "(ждёт свободного соединения, но не дольше timeout; None по "
                "истечении) и Drop для PooledConn, возвращающий соединение и "
                "будящий ожидающего. Метод idle(&self) -> usize — сколько "
                "соединений свободно."
            ),
            "starter": "use std::sync::{Arc, Condvar, Mutex};\nuse std::time::Duration;\n\nstruct Pool {\n    conns: Mutex<Vec<u32>>,\n    cv: Condvar,\n}\n\nstruct PooledConn {\n    id: u32,\n    pool: Arc<Pool>,\n}\n\nimpl Pool {\n    fn new(n: u32) -> Arc<Pool> {\n        todo!()\n    }\n    fn get(self: &Arc<Self>, timeout: Duration) -> Option<PooledConn> {\n        todo!()\n    }\n    fn idle(&self) -> usize {\n        todo!()\n    }\n}\n\nimpl Drop for PooledConn {\n    fn drop(&mut self) {\n        todo!()\n    }\n}\n",
            "driver": (
                "use std::thread;\n"
                "use std::time::{Duration, Instant};\n"
                "\n"
                "fn main() {\n"
                "    let pool = Pool::new(2);\n"
                "    let a = pool.get(Duration::from_millis(10)).unwrap();\n"
                "    let b = pool.get(Duration::from_millis(10)).unwrap();\n"
                "    println!(\"{} {} {}\", pool.idle(), a.id != b.id, a.id + b.id);\n"
                "    let t = Instant::now();\n"
                "    let none = pool.get(Duration::from_millis(60));\n"
                "    println!(\"{} {}\", none.is_none(), t.elapsed() >= Duration::from_millis(55));\n"
                "    let p2 = Arc::clone(&pool);\n"
                "    let waiter = thread::spawn(move || p2.get(Duration::from_secs(5)).map(|c| c.id));\n"
                "    thread::sleep(Duration::from_millis(30));\n"
                "    let a_id = a.id;\n"
                "    drop(a);\n"
                "    println!(\"{}\", waiter.join().unwrap() == Some(a_id));\n"
                "    drop(b);\n"
                "    println!(\"{}\", pool.idle());\n"
                "    let workers: Vec<_> = (0..8)\n"
                "        .map(|_| {\n"
                "            let p = Arc::clone(&pool);\n"
                "            thread::spawn(move || {\n"
                "                let mut got = 0;\n"
                "                for _ in 0..20 {\n"
                "                    if let Some(c) = p.get(Duration::from_secs(5)) {\n"
                "                        thread::sleep(Duration::from_millis(1));\n"
                "                        got += (c.id > 0) as u32;\n"
                "                    }\n"
                "                }\n"
                "                got\n"
                "            })\n"
                "        })\n"
                "        .collect();\n"
                "    let total: u32 = workers.into_iter().map(|h| h.join().unwrap()).sum();\n"
                "    println!(\"{} {}\", total, pool.idle());\n"
                "}\n"
            ),
            "expected": ["0 true 3", "true true", "true", "2", "160 2"],
            "hint": "Condvar::wait_timeout(guard, остаток) возвращает защитник; пересчитывайте остаток времени в цикле — возможны ложные пробуждения.",
        },
        {
            "id": "rs16-tx-savepoint",
            "mode": "rust",
            "title": "Транзакции и точки сохранения",
            "statement": (
                "Дано Conn (журнал команд). Реализуйте Tx<'a>: begin(conn) → "
                "'BEGIN'; commit(self) → 'COMMIT'; rollback(self) → 'ROLLBACK'; "
                "Drop без commit/rollback → 'ROLLBACK'. Метод savepoint(&mut self, "
                "name: &str) -> Savepoint<'_, 'a> шлёт 'SAVEPOINT name'; у "
                "Savepoint метод release(self) шлёт 'RELEASE SAVEPOINT name', а "
                "Drop без release — 'ROLLBACK TO SAVEPOINT name'."
            ),
            "starter": "use std::cell::RefCell;\n\nstruct Conn {\n    log: RefCell<Vec<String>>,\n}\n\nimpl Conn {\n    fn exec(&self, sql: &str) {\n        self.log.borrow_mut().push(sql.to_string());\n    }\n}\n\nstruct Tx<'a> {\n    conn: &'a Conn,\n    done: bool,\n}\n\nstruct Savepoint<'t, 'a> {\n    tx: &'t Tx<'a>,\n    name: String,\n    done: bool,\n}\n\nimpl<'a> Tx<'a> {\n    fn begin(conn: &'a Conn) -> Tx<'a> {\n        todo!()\n    }\n    fn commit(mut self) {\n        todo!()\n    }\n    fn rollback(mut self) {\n        todo!()\n    }\n    fn savepoint<'t>(&'t mut self, name: &str) -> Savepoint<'t, 'a> {\n        todo!()\n    }\n}\n\nimpl<'a> Drop for Tx<'a> {\n    fn drop(&mut self) {\n        todo!()\n    }\n}\n\nimpl<'t, 'a> Savepoint<'t, 'a> {\n    fn release(mut self) {\n        todo!()\n    }\n}\n\nimpl<'t, 'a> Drop for Savepoint<'t, 'a> {\n    fn drop(&mut self) {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn work(conn: &Conn, fail_inner: bool, fail_outer: bool) -> Result<(), String> {\n"
                "    let mut tx = Tx::begin(conn);\n"
                "    conn.exec(\"INSERT a\");\n"
                "    {\n"
                "        let sp = tx.savepoint(\"s1\");\n"
                "        conn.exec(\"INSERT b\");\n"
                "        if fail_inner {\n"
                "            return_inner(&sp)?;\n"
                "        }\n"
                "        sp.release();\n"
                "    }\n"
                "    if fail_outer {\n"
                "        return Err(\"outer\".to_string());\n"
                "    }\n"
                "    tx.commit();\n"
                "    Ok(())\n"
                "}\n"
                "\n"
                "fn return_inner(_sp: &Savepoint) -> Result<(), String> {\n"
                "    Err(\"inner\".to_string())\n"
                "}\n"
                "\n"
                "fn main() {\n"
                "    let c = Conn { log: RefCell::new(vec![]) };\n"
                "    println!(\"{:?}\", work(&c, false, false));\n"
                "    println!(\"{:?}\", work(&c, true, false));\n"
                "    println!(\"{:?}\", work(&c, false, true));\n"
                "    let tx = Tx::begin(&c);\n"
                "    tx.rollback();\n"
                "    for l in c.log.borrow().iter() {\n"
                "        println!(\"{}\", l);\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["Ok(())", "Err(\"inner\")", "Err(\"outer\")", "BEGIN", "INSERT a", "SAVEPOINT s1", "INSERT b", "RELEASE SAVEPOINT s1", "COMMIT", "BEGIN", "INSERT a", "SAVEPOINT s1", "INSERT b", "ROLLBACK TO SAVEPOINT s1", "ROLLBACK", "BEGIN", "INSERT a", "SAVEPOINT s1", "INSERT b", "RELEASE SAVEPOINT s1", "ROLLBACK", "BEGIN", "ROLLBACK"],
            "hint": "Флаг done у обоих охранных объектов; commit/rollback/release забирают self по значению и помечают done, чтобы Drop ничего не отправил.",
        },
        {
            "id": "rs16-migrations",
            "mode": "rust",
            "title": "Запуск миграций",
            "statement": (
                "Напишите run_migrations(applied: &mut Vec<u32>, migrations: "
                "&[Migration], exec: &mut dyn FnMut(&str) -> Result<(), String>) -> "
                "Result<Vec<u32>, String>: миграции сортируются по версии; если у "
                "двух одинаковая версия — Err(\"duplicate version N\") до выполнения "
                "чего-либо; уже применённые (есть в applied) пропускаются; "
                "остальные выполняются по одной через exec(sql); после успеха "
                "версия добавляется в applied и в результат; при ошибке — остановка "
                "и Err(\"migration N failed: ТЕКСТ\"), уже выполненные остаются в "
                "applied. Результат — список новых версий по порядку."
            ),
            "starter": "struct Migration {\n    version: u32,\n    sql: &'static str,\n}\n\nfn run_migrations(applied: &mut Vec<u32>, migrations: &[Migration], exec: &mut dyn FnMut(&str) -> Result<(), String>) -> Result<Vec<u32>, String> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let ms = [\n"
                "        Migration { version: 3, sql: \"CREATE INDEX i\" },\n"
                "        Migration { version: 1, sql: \"CREATE TABLE t\" },\n"
                "        Migration { version: 2, sql: \"ALTER TABLE t\" },\n"
                "        Migration { version: 4, sql: \"BROKEN\" },\n"
                "        Migration { version: 5, sql: \"DROP TABLE x\" },\n"
                "    ];\n"
                "    let mut executed: Vec<String> = Vec::new();\n"
                "    let mut applied = vec![1];\n"
                "    let mut exec = |sql: &str| -> Result<(), String> {\n"
                "        if sql == \"BROKEN\" {\n"
                "            Err(\"syntax error\".to_string())\n"
                "        } else {\n"
                "            executed.push(sql.to_string());\n"
                "            Ok(())\n"
                "        }\n"
                "    };\n"
                "    println!(\"{:?}\", run_migrations(&mut applied, &ms, &mut exec));\n"
                "    println!(\"{:?}\", applied);\n"
                "    println!(\"{:?}\", run_migrations(&mut applied, &ms[..3], &mut exec));\n"
                "    let dup = [Migration { version: 1, sql: \"A\" }, Migration { version: 1, sql: \"B\" }];\n"
                "    println!(\"{:?}\", run_migrations(&mut applied, &dup, &mut exec));\n"
                "    println!(\"{:?}\", executed);\n"
                "}\n"
            ),
            "expected": ["Err(\"migration 4 failed: syntax error\")", "[1, 2, 3]", "Ok([])", "Err(\"duplicate version 1\")", "[\"ALTER TABLE t\", \"CREATE INDEX i\"]"],
            "hint": "Сначала проверка дубликатов на отсортированном списке (windows(2)); дальше цикл с ранним выходом по ошибке.",
        },
        {
            "id": "rs16-db-url",
            "mode": "rust",
            "title": "Адрес подключения",
            "statement": (
                "Напишите parse_url(url: &str) -> Result<DbUrl, String> для "
                "'postgres://[user[:password]@]host[:port]/db[?k=v&k2=v2]' (также "
                "допустима схема 'postgresql://'): пароль и пользователь "
                "декодируются из процентного кодирования; порт по умолчанию 5432; "
                "IPv6-хост в квадратных скобках ('[::1]') возвращается без скобок; "
                "параметры запроса — в BTreeMap. Ошибки: \"bad scheme\", \"missing "
                "host\", \"missing database\", \"bad port\"."
            ),
            "starter": "use std::collections::BTreeMap;\n\n#[derive(Debug, PartialEq)]\nstruct DbUrl {\n    user: String,\n    password: String,\n    host: String,\n    port: u16,\n    db: String,\n    params: BTreeMap<String, String>,\n}\n\nfn parse_url(url: &str) -> Result<DbUrl, String> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", parse_url(\"postgres://app:p%40ss%3Aw@db.local:6543/shop?sslmode=require&connect_timeout=5\"));\n"
                "    println!(\"{:?}\", parse_url(\"postgresql://localhost/mydb\"));\n"
                "    println!(\"{:?}\", parse_url(\"postgres://u@[::1]:5433/d\"));\n"
                "    println!(\"{:?}\", parse_url(\"postgres://u:pw@[2001:db8::1]/d?x\"));\n"
                "    for bad in [\"mysql://a@b/c\", \"postgres://u@h\", \"postgres://u@h/\", \"postgres://u@:5432/d\", \"postgres://u@h:99999/d\", \"postgres://u@[::1/d\"] {\n"
                "        println!(\"{:?}\", parse_url(bad).err());\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["Ok(DbUrl { user: \"app\", password: \"p@ss:w\", host: \"db.local\", port: 6543, db: \"shop\", params: {\"connect_timeout\": \"5\", \"sslmode\": \"require\"} })", "Ok(DbUrl { user: \"\", password: \"\", host: \"localhost\", port: 5432, db: \"mydb\", params: {} })", "Ok(DbUrl { user: \"u\", password: \"\", host: \"::1\", port: 5433, db: \"d\", params: {} })", "Ok(DbUrl { user: \"u\", password: \"pw\", host: \"2001:db8::1\", port: 5432, db: \"d\", params: {\"x\": \"\"} })", "Some(\"bad scheme\")", "Some(\"missing database\")", "Some(\"missing database\")", "Some(\"missing host\")", "Some(\"bad port\")", "Some(\"missing host\")"],
            "hint": "Разбирайте с конца к началу: сначала query, затем учётные данные (rsplit_once('@') — пароль может содержать '@' в закодированном виде), потом хост и база.",
        },
        {
            "id": "rs16-aggregate",
            "mode": "rust",
            "title": "Агрегирование строк результата",
            "statement": (
                "Напишите aggregate(rows: &[Vec<Option<String>>], key: usize, val: "
                "usize) -> BTreeMap<String, (i64, usize)>: для каждой строки ключ — "
                "колонка key (строки с NULL в ключе пропускаются), значение — "
                "колонка val как i64 (NULL и не число пропускаются, но строка всё "
                "равно учитывается как существующая группа). Результат: ключ → "
                "(сумма значений, число учтённых значений)."
            ),
            "starter": "use std::collections::BTreeMap;\n\nfn aggregate(rows: &[Vec<Option<String>>], key: usize, val: usize) -> BTreeMap<String, (i64, usize)> {\n    todo!()\n}\n",
            "driver": (
                "fn row(cells: &[Option<&str>]) -> Vec<Option<String>> {\n"
                "    cells.iter().map(|c| c.map(|s| s.to_string())).collect()\n"
                "}\n"
                "\n"
                "fn main() {\n"
                "    let rows = vec![\n"
                "        row(&[Some(\"north\"), Some(\"10\")]),\n"
                "        row(&[Some(\"south\"), Some(\"5\")]),\n"
                "        row(&[Some(\"north\"), Some(\"7\")]),\n"
                "        row(&[None, Some(\"100\")]),\n"
                "        row(&[Some(\"west\"), None]),\n"
                "        row(&[Some(\"south\"), Some(\"x\")]),\n"
                "        row(&[Some(\"south\")]),\n"
                "        row(&[Some(\"north\"), Some(\"-2\")]),\n"
                "    ];\n"
                "    println!(\"{:?}\", aggregate(&rows, 0, 1));\n"
                "    println!(\"{:?}\", aggregate(&[], 0, 1));\n"
                "    println!(\"{:?}\", aggregate(&rows, 5, 1));\n"
                "}\n"
            ),
            "expected": ["{\"north\": (15, 3), \"south\": (5, 1), \"west\": (0, 0)}", "{}", "{}"],
            "hint": "entry(ключ).or_insert((0, 0)) создаёт группу даже если значение не удалось разобрать; get(i) защищает от коротких строк.",
        },
    ],
}
