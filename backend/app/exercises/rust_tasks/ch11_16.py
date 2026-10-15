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
}
