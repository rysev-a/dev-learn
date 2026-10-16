import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, RsCode } from "../widgets.tsx";
// Слайды для «Изучаем Rust», глава 38 — «Алгоритмы на Rust».
// Тот же дизайн-код, что и в главах 1–5: палитра, IBM Plex Mono / Inter,
// рубрика + номер, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

const Slide = makeSlide("ИЗУЧАЕМ RUST / ПРИМЕНЯЕМ: АЛГОРИТМЫ / ГЛАВА 38", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Алгоритмы курса — на Rust"}
      sub={"Глава 38 · Применяем: алгоритмы"}
      main={"Те же идеи, но со срезами, обобщениями и стандартными коллекциями; числа без знака требуют внимания."}
    >
      <div className="s-grid2">
        {([["&[T] · &mut [T]", "Срезы", "Без копирования"], ["BinaryHeap · HashMap", "Коллекции", "Из коробки"], ["Vec<Vec<usize>>", "Графы", "Индексы вместо указателей"], ["checked · wrapping", "Числа", "Явный выбор операции"]] as const).map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Считаем операции"}
      sub={"Счётчик вместо секундомера"}
      main={"Число сравнений не зависит от машины — его удобно проверять в тестах."}
    >
      <RsCode>{`fn linear(v: &[i32], x: i32, ops: &mut u32) -> Option<usize> {
    for (i, &y) in v.iter().enumerate() {
        *ops += 1;
        if y == x {
            return Some(i);
        }
    }
    None
}

fn main() {
    let v: Vec<i32> = (0..1000).collect();
    let mut ops = 0;
    println!("{:?} {}", linear(&v, 999, &mut ops), ops);
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Some(999) 1000"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Бинарный поиск"}
      sub={"Обобщённый, на срезе"}
      main={"Середина lo + (hi − lo) / 2 не переполняется; сравнение — перечисление Ordering."}
    >
      <RsCode>{`use std::cmp::Ordering;

fn binary_search<T: Ord>(v: &[T], x: &T, steps: &mut u32) -> Option<usize> {
    let (mut lo, mut hi) = (0, v.len());
    while lo < hi {
        *steps += 1;
        let mid = lo + (hi - lo) / 2;
        match v[mid].cmp(x) {
            Ordering::Equal => return Some(mid),
            Ordering::Less => lo = mid + 1,
            Ordering::Greater => hi = mid,
        }
    }
    None
}

fn main() {
    let v: Vec<i32> = (0..1000).collect();
    let mut s = 0;
    println!("{:?} {}", binary_search(&v, &999, &mut s), s);
    println!("{:?} {:?}", v.binary_search(&500), v.binary_search(&-1));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Some(999) 9\nOk(500) Err(0)"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Сортировка вставками"}
      sub={"На изменяемом срезе"}
      main={"swap переставляет соседей без копирования значений — работает и для строк."}
    >
      <RsCode>{`fn insertion_sort<T: PartialOrd>(v: &mut [T]) {
    for i in 1..v.len() {
        let mut j = i;
        while j > 0 && v[j - 1] > v[j] {
            v.swap(j - 1, j);
            j -= 1;
        }
    }
}

fn main() {
    let mut a = [5, 2, 9, 1, 5, 6];
    insertion_sort(&mut a);
    println!("{:?}", a);
    let mut w = vec!["pear", "apple", "fig"];
    insertion_sort(&mut w);
    println!("{:?}", w);
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[1, 2, 5, 5, 6, 9]\n[\"apple\", \"fig\", \"pear\"]"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Сортировка слиянием"}
      sub={"split_at и два указателя"}
      main={"split_at делит срез без копий; слияние устойчиво — равные элементы не меняют порядок."}
    >
      <RsCode>{`fn merge_sort(v: &[i32]) -> Vec<i32> {
    if v.len() <= 1 {
        return v.to_vec();
    }
    let (l, r) = v.split_at(v.len() / 2);
    let (l, r) = (merge_sort(l), merge_sort(r));
    let mut out = Vec::with_capacity(v.len());
    let (mut i, mut j) = (0, 0);
    while i < l.len() && j < r.len() {
        if l[i] <= r[j] {
            out.push(l[i]);
            i += 1;
        } else {
            out.push(r[j]);
            j += 1;
        }
    }
    out.extend_from_slice(&l[i..]);
    out.extend_from_slice(&r[j..]);
    out
}

fn main() {
    println!("{:?}", merge_sort(&[8, 3, 5, 1, 9, 2, 7]));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[1, 2, 3, 5, 7, 8, 9]"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Куча и top-k"}
      sub={"BinaryHeap и Reverse"}
      main={"BinaryHeap — максимальная куча; Reverse превращает её в минимальную."}
    >
      <RsCode>{`use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn top_k(v: &[i32], k: usize) -> Vec<i32> {
    let mut heap = BinaryHeap::new();
    for &x in v {
        heap.push(Reverse(x));
        if heap.len() > k {
            heap.pop();
        }
    }
    let mut out: Vec<i32> = heap.into_iter().map(|Reverse(x)| x).collect();
    out.sort_by(|a, b| b.cmp(a));
    out
}

fn main() {
    println!("{:?}", top_k(&[5, 1, 9, 3, 7, 9, 2], 3));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[9, 9, 7]"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Хеш-таблицы в алгоритмах"}
      sub={"Группировка анаграмм"}
      main={"Отсортированные буквы — ключ группы; entry().or_default() вставляет и меняет за один поиск."}
    >
      <RsCode>{`use std::collections::HashMap;

fn group(words: &[&str]) -> Vec<Vec<String>> {
    let mut m: HashMap<String, Vec<String>> = HashMap::new();
    for w in words {
        let mut k: Vec<char> = w.chars().collect();
        k.sort();
        m.entry(k.into_iter().collect()).or_default().push(w.to_string());
    }
    let mut groups: Vec<Vec<String>> = m.into_values().collect();
    groups.iter_mut().for_each(|g| g.sort());
    groups.sort();
    groups
}

fn main() {
    println!("{:?}", group(&["eat", "tea", "tan", "ate", "nat", "bat"]));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[[\"ate\", \"eat\", \"tea\"], [\"bat\"], [\"nat\", \"tan\"]]"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Граф и обход в ширину"}
      sub={"Список смежности"}
      main={"Вершины — индексы; Option<u32> в массиве расстояний кодирует «недостижима»."}
    >
      <RsCode>{`use std::collections::VecDeque;

fn bfs(adj: &Vec<Vec<usize>>, start: usize) -> Vec<Option<u32>> {
    let mut dist = vec![None; adj.len()];
    dist[start] = Some(0);
    let mut q = VecDeque::from([start]);
    while let Some(v) = q.pop_front() {
        for &u in &adj[v] {
            if dist[u].is_none() {
                dist[u] = Some(dist[v].unwrap() + 1);
                q.push_back(u);
            }
        }
    }
    dist
}

fn main() {
    let adj = vec![vec![1, 2], vec![3], vec![3], vec![], vec![0]];
    println!("{:?}", bfs(&adj, 0));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[Some(0), Some(1), Some(1), Some(2), None]"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Алгоритм Дейкстры"}
      sub={"Куча пар (расстояние, вершина)"}
      main={"Устаревшие записи кучи пропускаем при извлечении; бесконечность — u64::MAX."}
    >
      <RsCode>{`use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn dijkstra(adj: &Vec<Vec<(usize, u64)>>, s: usize) -> Vec<u64> {
    let mut dist = vec![u64::MAX; adj.len()];
    let mut heap = BinaryHeap::new();
    dist[s] = 0;
    heap.push(Reverse((0u64, s)));
    while let Some(Reverse((d, v))) = heap.pop() {
        if d > dist[v] {
            continue;
        }
        for &(u, w) in &adj[v] {
            let nd = d + w;
            if nd < dist[u] {
                dist[u] = nd;
                heap.push(Reverse((nd, u)));
            }
        }
    }
    dist
}

fn main() {
    let adj = vec![vec![(1, 7), (2, 2)], vec![(3, 1)], vec![(1, 3), (3, 8)], vec![]];
    println!("{:?}", dijkstra(&adj, 0));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[0, 5, 2, 6]"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Динамическое программирование"}
      sub={"LCS в двух строках таблицы"}
      main={"Хватает двух строк таблицы — память с произведения длин падает до одной длины."}
    >
      <RsCode>{`fn lcs(a: &str, b: &str) -> usize {
    let (a, b): (Vec<char>, Vec<char>) = (a.chars().collect(), b.chars().collect());
    let mut prev = vec![0; b.len() + 1];
    for i in 1..=a.len() {
        let mut cur = vec![0; b.len() + 1];
        for j in 1..=b.len() {
            cur[j] = if a[i - 1] == b[j - 1] {
                prev[j - 1] + 1
            } else {
                prev[j].max(cur[j - 1])
            };
        }
        prev = cur;
    }
    prev[b.len()]
}

fn main() {
    println!("{} {}", lcs("abcde", "ace"), lcs("abc", "xyz"));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3 0"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Система непересекающихся множеств"}
      sub={"Union-Find"}
      main={"Сжатие путей и объединение по размеру — почти константное время."}
    >
      <RsCode>{`struct Dsu {
    parent: Vec<usize>,
    size: Vec<usize>,
}

impl Dsu {
    fn new(n: usize) -> Dsu {
        Dsu { parent: (0..n).collect(), size: vec![1; n] }
    }
    fn find(&mut self, x: usize) -> usize {
        if self.parent[x] != x {
            let r = self.find(self.parent[x]);
            self.parent[x] = r;
        }
        self.parent[x]
    }
    fn union(&mut self, a: usize, b: usize) -> bool {
        let (mut a, mut b) = (self.find(a), self.find(b));
        if a == b {
            return false;
        }
        if self.size[a] < self.size[b] {
            std::mem::swap(&mut a, &mut b);
        }
        self.parent[b] = a;
        self.size[a] += self.size[b];
        true
    }
}

fn main() {
    let mut d = Dsu::new(5);
    println!("{} {} {}", d.union(0, 1), d.union(1, 2), d.union(0, 2));
    println!("{} {}", d.find(2) == d.find(0), d.find(3) == d.find(0));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"true true false\ntrue false"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Ловушки целых чисел"}
      sub={"checked, saturating, wrapping, overflowing"}
      main={"usize без знака: 3 − 5 — не −2. Выбирайте явную операцию."}
    >
      <RsCode>{`fn main() {
    let a: usize = 3;
    println!("{:?} {}", a.checked_sub(5), a.saturating_sub(5));
    println!("{} {:?}", 250u8.wrapping_add(10), 250u8.checked_add(10));
    println!("{:?}", 200u8.overflowing_add(100));
    let mid = (u32::MAX / 2 + 10).midpoint(u32::MAX / 2 + 20);
    println!("{}", mid);
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"None 0\n4 None\n(44, true)\n2147483662"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Алгоритмы на Rust: срезы, обобщения, стандартные коллекции и аккуратная арифметика."}
    >
      <div className="s-grid2">
        {([["O(n log n)", "Сортировки", "Вставками, слиянием"], ["Reverse(heap)", "Куча", "top-k, Дейкстра"], ["Vec<Vec<>>", "Графы и ДП", "Таблицы и списки"], ["DSU", "Связность", "Union-Find"]] as const).map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_R38 = {
  "10:38": [
    S01,
    S02,
    S03,
    S04,
    S05,
    S06,
    S07,
    S08,
    S09,
    S10,
    S11,
    S12,
    S13,
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R38).
export const SLIDE_TITLES_R38 = {
  "10:38": [
    "Алгоритмы на Rust",
    "Счётчик операций",
    "Бинарный поиск",
    "Вставками",
    "Слиянием",
    "Куча",
    "Хеш-таблицы",
    "BFS",
    "Дейкстра",
    "ДП: LCS",
    "Union-Find",
    "Ловушки целых",
    "Итоги",
  ],
};
