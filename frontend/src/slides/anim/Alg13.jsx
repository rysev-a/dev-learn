import { edge, row, scene } from "./alg.jsx";

/* Глава 13 книги «Алгоритмы и структуры данных»: кратчайшие пути и остовы. */

const Tx = (id, x, y, text, extra = {}) => ({
  t: "text",
  id,
  x,
  y,
  text,
  ...extra,
});

const NODES = {
  S: [40, 85],
  A: [115, 38],
  B: [115, 132],
  C: [205, 38],
  D: [205, 132],
  T: [295, 85],
};
const EDGES = [
  ["S", "A", 2],
  ["S", "B", 5],
  ["A", "B", 1],
  ["A", "C", 4],
  ["B", "D", 3],
  ["C", "D", 2],
  ["C", "T", 6],
  ["D", "T", 3],
  ["A", "D", 7],
];
const P = (k, nodes = NODES) => ({ x: nodes[k][0], y: nodes[k][1] });
const ek = (a, b) => (a < b ? `${a}-${b}` : `${b}-${a}`);
// граф с весами: colors — вершины, ec — рёбра (ключ «A-B» в алфавитном порядке)
function WG(
  colors = {},
  ec = {},
  {
    nodes = NODES,
    edges = EDGES,
    labels = {},
    directed = false,
    id = "g",
    r = 12,
    o = 1,
  } = {},
) {
  return [
    ...edges.flatMap(([a, b, w]) => {
      const k = ek(a, b);
      const A = P(a, nodes);
      const B = P(b, nodes);
      const mx = (A.x + B.x) / 2;
      const my = (A.y + B.y) / 2;
      const dx = B.x - A.x;
      const dy = B.y - A.y;
      const n = Math.hypot(dx, dy) || 1;
      return [
        edge(`${id}e${k}`, A, B, {
          r,
          c: ec[k] ?? "m",
          arrow: directed,
          o,
          w: ec[k] ? 2.4 : 1.6,
        }),
        {
          t: "text",
          id: `${id}w${k}`,
          x: mx - (dy / n) * 7,
          y: my + (dx / n) * 7 + 3,
          text: w,
          mono: true,
          size: 8.5,
          c: ec[k] ? ec[k] : "y",
          o,
        },
      ];
    }),
    ...Object.keys(nodes).map((k) => ({
      t: "dot",
      id: `${id}${k}`,
      x: nodes[k][0],
      y: nodes[k][1],
      r,
      text: labels[k] ?? k,
      c: colors[k] ?? "m",
      size: 10,
      o,
    })),
  ];
}
const adj = {};
for (const [a, b, w] of EDGES) {
  (adj[a] ||= []).push([b, w]);
  (adj[b] ||= []).push([a, w]);
}
// Дейкстра: шаги
function dijkstraSteps(src = "S") {
  const dist = Object.fromEntries(Object.keys(NODES).map((k) => [k, Infinity]));
  const prev = {};
  dist[src] = 0;
  const done = new Set();
  const steps = [
    { dist: { ...dist }, done: new Set(), cur: null, prev: { ...prev } },
  ];
  while (done.size < Object.keys(NODES).length) {
    const cur = Object.keys(dist)
      .filter((k) => !done.has(k))
      .sort((x, y) => dist[x] - dist[y] || (x < y ? -1 : 1))[0];
    done.add(cur);
    for (const [nb, w] of adj[cur] ?? [])
      if (!done.has(nb) && dist[cur] + w < dist[nb]) {
        dist[nb] = dist[cur] + w;
        prev[nb] = cur;
      }
    steps.push({
      dist: { ...dist },
      done: new Set(done),
      cur,
      prev: { ...prev },
    });
  }
  return steps;
}
const DJ = dijkstraSteps();
const fmt = (v) => (v === Infinity ? "∞" : v);
const distLabels = (dist) =>
  Object.fromEntries(Object.keys(dist).map((k) => [k, fmt(dist[k])]));
const tableOf = (dist, hot) =>
  Object.keys(dist).flatMap((k, i) => [
    Tx(`dk${k}`, 40 + 56 * i, 160, k, {
      mono: true,
      size: 9,
      c: hot === k ? "y" : undefined,
    }),
    {
      t: "cell",
      id: `dv${k}`,
      x: 40 + 56 * i,
      y: 178,
      w: 36,
      h: 20,
      text: fmt(dist[k]),
      c: hot === k ? "y" : dist[k] === Infinity ? "n" : "g",
      size: 10,
    },
  ]);

// 1. От шагов к весам
export const V01 = scene({
  labels: ["Одинаковые рёбра", "Веса", "Минимум суммы"],
  caption: [
    "Раньше все рёбра стоили одно и то же — минимум шагов находит обход в ширину",
    "Теперь у ребра свой вес: километры, минуты, деньги, риск",
    "Нужен путь с минимальной суммой весов: из S в T — это уже задача Дейкстры",
  ],
  frames: [
    [
      ...WG(
        { S: "y", T: "y" },
        {},
        { edges: EDGES.map(([a, b]) => [a, b, 1]) },
      ),
    ],
    [...WG({ S: "y", T: "y" })],
    [
      ...WG(
        { S: "y", A: "g", B: "g", D: "g", T: "y" },
        { "A-S": "g", "A-B": "g", "B-D": "g", "D-T": "g" },
      ),
      Tx("t", 180, 168, "S → A → B → D → T = 2 + 1 + 3 + 3 = 9", {
        mono: true,
        size: 9.5,
        c: "g",
      }),
    ],
  ],
  h: 185,
  cues: [10, 20],
});

// 2. Идея Дейкстры
export const V02 = scene({
  labels: ["Оценки", "Ближайшая", "Релаксация"],
  caption: [
    "Для каждой вершины — оценка расстояния: у старта 0, у остальных ∞",
    "Берём ближайшую ещё не закрытую вершину: её оценка уже точная",
    "Релаксация: не короче ли путь к соседу через неё? Если да — обновляем оценку",
  ],
  frames: [
    [
      ...WG({ S: "y" }, {}, { labels: distLabels(DJ[0].dist) }),
      ...tableOf(DJ[0].dist),
    ],
    [
      ...WG({ S: "g" }, {}, { labels: distLabels(DJ[1].dist) }),
      ...tableOf(DJ[1].dist, "S"),
    ],
    [
      ...WG(
        { S: "g", A: "y", B: "y" },
        { "A-S": "y", "B-S": "y" },
        { labels: distLabels(DJ[1].dist) },
      ),
      ...tableOf(DJ[1].dist, "A"),
    ],
  ],
  h: 205,
  cues: [10, 20],
});

// 3. Прогон по шагам
const names = Object.keys(NODES);
export const V03 = scene({
  labels: ["Старт", "S", "A", "B", "C", "D", "T"],
  caption: [
    "Все расстояния бесконечны, кроме старта",
    ...DJ.slice(1).map(
      (s, i) =>
        `Закрываем ${s.cur} (расстояние ${s.dist[s.cur]}); соседям — релаксация`,
    ),
  ],
  frames: DJ.map((s) => {
    const ec = {};
    for (const [v, u] of Object.entries(s.prev))
      if (s.done.has(v)) ec[ek(u, v)] = "g";
    return [
      ...WG(
        Object.fromEntries(
          [...s.done].map((k) => [k, k === s.cur ? "y" : "g"]),
        ),
        ec,
        { labels: distLabels(s.dist) },
      ),
      ...tableOf(s.dist, s.cur),
    ];
  }),
  h: 205,
  cues: [6, 12, 17, 22, 27, 31],
});

// 4. Куча
const HEAP = [
  ["(0, S)", ["(0,S)"]],
  ["достали S", ["(2,A)", "(5,B)"]],
  ["достали A", ["(3,B)", "(5,B)", "(6,C)", "(9,D)"]],
  ["устаревшая (5,B)", ["(5,B)", "(6,C)", "(6,D)"]],
];
export const V04 = scene({
  labels: ["Куча", "Достали S", "Достали A", "Устаревшие"],
  caption: [
    "Вершины с оценками — в приоритетной очереди (куча)",
    "Достали минимум (0, S), положили оценки соседей",
    "(2, A) дала (3, B) — старая (5, B) осталась в куче",
    "Устаревшую запись при извлечении просто пропускаем: ленивое удаление; всего O((V + E) log V)",
  ],
  frames: HEAP.map(([t, items], k) => [
    Tx("t", 180, 40, t, { mono: true, size: 10.5, c: k === 3 ? "r" : "g" }),
    ...row("h", items, {
      x0: 180 - 26 * (items.length - 1),
      y: 90,
      cw: 52,
      w: 48,
      h: 30,
      size: 9,
      c: (i) => (k === 3 && items[i] === "(5,B)" ? "r" : i === 0 ? "g" : "b"),
    }),
    Tx("n", 180, 140, "минимум — наверху", { size: 9 }),
  ]),
  h: 160,
  cues: [9, 18, 27],
});

// 5. Отрицательные веса ломают Дейкстру
const NN = { S: [50, 85], A: [180, 40], B: [180, 130] };
const NE = [
  ["S", "A", 3],
  ["S", "B", 4],
  ["B", "A", -2],
];
export const V05 = scene({
  labels: ["Отрицательное ребро", "Дейкстра закрыла A", "Правильный ответ"],
  caption: [
    "Ребро B → A с весом −2",
    "A ближе (3 < 4) и закрыта с расстоянием 3. Позже через B выйдет 2 — но закрытую не пересматривают",
    "Верный ответ 2; веса должны быть неотрицательными — иначе Беллман-Форд",
  ],
  frames: [
    [...WG({}, {}, { nodes: NN, edges: NE, directed: true, id: "n" })],
    [
      ...WG(
        { A: "r", S: "g" },
        { "A-S": "r" },
        { nodes: NN, edges: NE, directed: true, id: "n", labels: { A: "3" } },
      ),
      Tx("t", 180, 160, "закрыто 3 ✗", { mono: true, size: 10.5, c: "r" }),
    ],
    [
      ...WG(
        { A: "g", B: "g", S: "g" },
        { "B-S": "g", "A-B": "g" },
        { nodes: NN, edges: NE, directed: true, id: "n", labels: { A: "2" } },
      ),
      Tx("t", 180, 160, "S → B → A = 4 − 2 = 2", {
        mono: true,
        size: 10.5,
        c: "g",
      }),
    ],
  ],
  h: 175,
  cues: [10, 22],
});

// 6. Беллман — Форд
const BF = [
  { d: { S: 0, A: Infinity, B: Infinity }, t: "старт: S = 0" },
  { d: { S: 0, A: 2, B: 4 }, t: "круг 1: S→A 3, S→B 4, B→A 2" },
  { d: { S: 0, A: 2, B: 4 }, t: "круг 2: изменений нет — готово" },
];
export const V06 = scene({
  labels: ["Старт", "Круг 1", "Круг 2", "Отрицательный цикл"],
  caption: [
    "n − 1 раз проходим все рёбра и пытаемся улучшить оценки",
    "За первый круг получили A = 2 и B = 4 — отрицательное ребро учтено",
    "Если за круг ничего не изменилось — можно остановиться: O(V · E)",
    "Если улучшения не прекращаются на n-м круге — достижим отрицательный цикл",
  ],
  frames: [
    ...BF.map((s) => [
      ...WG(
        {
          S: "g",
          A: s.d.A < Infinity ? "g" : "m",
          B: s.d.B < Infinity ? "g" : "m",
        },
        {},
        {
          nodes: NN,
          edges: NE,
          directed: true,
          id: "n",
          labels: Object.fromEntries(
            Object.entries(s.d).map(([k, v]) => [k, fmt(v)]),
          ),
        },
      ),
      Tx("t", 180, 160, s.t, { mono: true, size: 10 }),
    ]),
    [
      ...WG(
        { A: "r", B: "r" },
        { "A-B": "r", "B-A": "r" },
        {
          nodes: { S: [50, 85], A: [180, 40], B: [180, 130] },
          edges: [
            ["S", "A", 1],
            ["A", "B", -3],
            ["B", "A", 1],
          ],
          directed: true,
          id: "c",
          labels: {},
        },
      ),
      Tx("t", 180, 160, "A → B → A: −2 — можно уменьшать бесконечно", {
        mono: true,
        size: 9.5,
        c: "r",
      }),
    ],
  ],
  h: 175,
  cues: [10, 20, 30],
});

// 7. A*: Дейкстра с предвидением
const GW = 11;
const GH = 7;
const START = [1, 3];
const GOAL = [9, 3];
const cellsOf = (pred) =>
  Array.from({ length: GH }, (_, r) =>
    Array.from({ length: GW }, (_, c) => ({ r, c })),
  )
    .flat()
    .filter(pred);
const man = (a, b) => Math.abs(a[0] - b[0]) + Math.abs(a[1] - b[1]);
const GRIDV = (set, col) =>
  Array.from({ length: GH }, (_, r) =>
    Array.from({ length: GW }, (_, c) => ({
      t: "cell",
      id: `g${r}-${c}`,
      x: 70 + 22 * c,
      y: 28 + 20 * r,
      w: 19,
      h: 17,
      text:
        c === START[0] && r === START[1]
          ? "S"
          : c === GOAL[0] && r === GOAL[1]
            ? "T"
            : "",
      size: 8,
      c:
        (c === START[0] && r === START[1]) || (c === GOAL[0] && r === GOAL[1])
          ? "y"
          : set(r, c)
            ? col
            : "m",
    })),
  ).flat();
export const V07 = scene({
  labels: ["Дейкстра", "A* с предвидением", "Эвристика"],
  caption: [
    "Дейкстра расползается во все стороны кругами и добирается до цели, обойдя много лишнего",
    "A* добавляет к расстоянию оценку «сколько осталось» и тянется к цели",
    "Эвристика не должна завышать истинное расстояние — тогда ответ остаётся точным",
  ],
  frames: [
    GRIDV((r, c) => man([c, r], START) <= 7, "b"),
    GRIDV((r, c) => man([c, r], START) + man([c, r], GOAL) <= 9, "g"),
    [
      ...GRIDV((r, c) => man([c, r], START) + man([c, r], GOAL) <= 9, "g").map(
        (x) => ({ ...x, o: 0.4 }),
      ),
      Tx("t", 180, 175, "f = g (пройдено) + h (оценка остатка)", {
        mono: true,
        size: 9.5,
        c: "g",
      }),
    ],
  ],
  h: 188,
  cues: [10, 22],
});

// 8. Флойд — Уоршелл
const FW0 = [
  [0, 3, 8, "∞"],
  ["∞", 0, 2, 5],
  ["∞", "∞", 0, 1],
  [2, "∞", "∞", 0],
];
const FWV = ["A", "B", "C", "D"];
const FWK = [
  [0, 3, 8, "∞"],
  ["∞", 0, 2, 5],
  ["∞", "∞", 0, 1],
  [2, 5, 10, 0],
];
const FWB = [
  [0, 3, 5, 8],
  ["∞", 0, 2, 5],
  ["∞", "∞", 0, 1],
  [2, 5, 7, 0],
];
const MAT = (m, hot = {}) =>
  m.flatMap((rw, i) =>
    rw.map((v, j) => ({
      t: "cell",
      id: `m${i}${j}`,
      x: 130 + 38 * j,
      y: 40 + 28 * i,
      w: 34,
      h: 24,
      text: v,
      size: 10,
      c: hot[`${i}${j}`] ?? (i === j ? "n" : v === "∞" ? "m" : "b"),
    })),
  );
export const V08 = scene({
  labels: ["Матрица", "Через A", "Через B", "Итог"],
  caption: [
    "Расстояния между всеми парами: сначала — только прямые рёбра",
    "Допускаем пересадку через A: D → A → B даёт 2 + 3 = 5 — клетка D, B обновилась",
    "Пересадка через B открывает A → C (3 + 2 = 5) и D → C (7)",
    "n³ времени и n² памяти; для небольших графов — единственная таблица на все вопросы",
  ],
  frames: [
    [
      ...MAT(FW0),
      ...FWV.map((v, i) =>
        Tx(`r${i}`, 98, 44 + 28 * i, v, { mono: true, size: 9 }),
      ),
      ...FWV.map((v, i) =>
        Tx(`c${i}`, 130 + 38 * i, 22, v, { mono: true, size: 9 }),
      ),
    ],
    [
      ...MAT(FWK, { 31: "g" }),
      ...FWV.map((v, i) =>
        Tx(`r${i}`, 98, 44 + 28 * i, v, { mono: true, size: 9 }),
      ),
      ...FWV.map((v, i) =>
        Tx(`c${i}`, 130 + 38 * i, 22, v, { mono: true, size: 9 }),
      ),
    ],
    [
      ...MAT(FWB, { "02": "g", "03": "g", 32: "g" }),
      ...FWV.map((v, i) =>
        Tx(`r${i}`, 98, 44 + 28 * i, v, { mono: true, size: 9 }),
      ),
      ...FWV.map((v, i) =>
        Tx(`c${i}`, 130 + 38 * i, 22, v, { mono: true, size: 9 }),
      ),
    ],
    [
      ...MAT(FWB, {}),
      ...FWV.map((v, i) =>
        Tx(`r${i}`, 98, 44 + 28 * i, v, { mono: true, size: 9 }),
      ),
      ...FWV.map((v, i) =>
        Tx(`c${i}`, 130 + 38 * i, 22, v, { mono: true, size: 9 }),
      ),
      Tx("t", 180, 160, "O(n³)", { mono: true, size: 11, c: "g" }),
    ],
  ],
  h: 170,
  cues: [9, 18, 28],
});

// 9. Разные веса
const WTS = [
  ["время", "минуты в пути"],
  ["деньги", "стоимость билета"],
  ["риск", "−log вероятности успеха"],
  ["комбинация", "взвешенная сумма критериев"],
];
export const V09 = scene({
  labels: ["Время", "Деньги", "Риск", "Комбинация"],
  caption: [
    "Вес — не только километры: время в пути",
    "Деньги, штрафы за пересадки",
    "Риск: перемножение вероятностей превращается в сложение логарифмов",
    "Несколько критериев сворачивают в один вес",
  ],
  frames: [0, 1, 2, 3].map((k) =>
    WTS.flatMap(([a, b], i) => [
      {
        t: "box",
        id: `b${i}`,
        x: 180,
        y: 28 + i * 34,
        w: 334,
        h: 28,
        c: i === k ? "g" : "n",
      },
      Tx(`a${i}`, 24, 32 + i * 34, a, {
        mono: true,
        size: 9.5,
        anchor: "start",
        c: i === k ? "g" : undefined,
      }),
      Tx(`d${i}`, 340, 32 + i * 34, b, {
        size: 8.5,
        anchor: "end",
        o: i === k ? 1 : 0.5,
      }),
    ]),
  ),
  h: 160,
  cues: [8, 16, 25],
});

// 10. Много источников
const MS = [
  [2, 1],
  [8, 5],
];
export const V10 = scene({
  labels: ["Источники", "Волны", "Одно расстояние"],
  caption: [
    "Несколько стартов: пожарные части, склады, антенны",
    "Кладём в очередь все стартовые вершины сразу — волны идут одновременно",
    "Каждая клетка получает расстояние до ближайшего источника за один обход",
  ],
  frames: [0, 1, 2].map((k) =>
    Array.from({ length: 7 }, (_, r) =>
      Array.from({ length: 11 }, (_, c) => {
        const d = Math.min(
          ...MS.map(([sc, sr]) => Math.abs(c - sc) + Math.abs(r - sr)),
        );
        const src = MS.some(([sc, sr]) => sc === c && sr === r);
        return {
          t: "cell",
          id: `m${r}-${c}`,
          x: 70 + 22 * c,
          y: 28 + 20 * r,
          w: 19,
          h: 17,
          text: src ? "S" : k === 2 ? d : "",
          size: 7.5,
          c: src
            ? "y"
            : k === 0
              ? "m"
              : d <= (k === 1 ? 2 : 99)
                ? ["g", "b", "v"][d % 3]
                : "m",
        };
      }),
    ).flat(),
  ),
  h: 175,
  cues: [9, 18],
});

// 11. Остов
export const V11 = scene({
  labels: ["Граф", "Остов", "Минимальный"],
  caption: [
    "Нужно соединить всех самым дешёвым способом",
    "Остов — подграф без циклов, связывающий все вершины: V − 1 ребро",
    "Минимальный остов: наименьший суммарный вес (здесь 11)",
  ],
  frames: [
    [...WG({})],
    [...WG({}, { "A-S": "b", "A-B": "b", "A-C": "b", "B-D": "b", "D-T": "b" })],
    [
      ...WG({}, { "A-S": "g", "A-B": "g", "B-D": "g", "C-D": "g", "D-T": "g" }),
      Tx("t", 180, 168, "2 + 1 + 3 + 2 + 3 = 11", {
        mono: true,
        size: 10.5,
        c: "g",
      }),
    ],
  ],
  h: 185,
  cues: [8, 16],
});

// 12. Краскал
const SORTED = [...EDGES].sort(
  (x, y) => x[2] - y[2] || (x[0] + x[1] < y[0] + y[1] ? -1 : 1),
);
function kruskalSteps() {
  const uf = Object.fromEntries(Object.keys(NODES).map((k) => [k, k]));
  const find = (x) => (uf[x] === x ? x : (uf[x] = find(uf[x])));
  const taken = {};
  const rej = {};
  const steps = [];
  for (const [a, b, w] of SORTED) {
    const ra = find(a);
    const rb = find(b);
    if (ra !== rb) {
      uf[ra] = rb;
      taken[ek(a, b)] = "g";
    } else rej[ek(a, b)] = "r";
    steps.push({
      taken: { ...taken },
      rej: { ...rej },
      edge: `${a}-${b} (${w})`,
      ok: ra !== rb,
    });
  }
  return steps;
}
const KR = kruskalSteps();
const KSEL = [0, 2, 4, 5, 8];
export const V12 = scene({
  labels: ["Сортировка", "Три ребра", "Соединили", "Остов", "Цикл — пропуск"],
  caption: [
    "Сортируем рёбра по весу: A-B 1, S-A 2, C-D 2, B-D 3, D-T 3, A-C 4, …",
    "Берём самые лёгкие, если они не замыкают цикл",
    "B-D соединило две компоненты в одну",
    "Пять рёбер на шесть вершин — остов готов",
    "Ребро A-C замкнуло бы цикл: система непересекающихся множеств отвечает за доли константы",
  ],
  frames: [
    [
      ...WG({}),
      Tx("t", 180, 168, SORTED.map((e) => e[2]).join(" ≤ "), {
        mono: true,
        size: 9,
        c: "y",
      }),
    ],
    [
      ...WG({}, { ...KR[2].taken }),
      Tx("t", 180, 168, "A-B, S-A, C-D", { mono: true, size: 9.5, c: "g" }),
    ],
    [
      ...WG({}, { ...KR[3].taken }),
      Tx("t", 180, 168, "+ B-D: компонент стала одна", {
        mono: true,
        size: 9.5,
        c: "g",
      }),
    ],
    [
      ...WG({}, { ...KR[4].taken }),
      Tx("t", 180, 168, "+ D-T: готово, вес 11", {
        mono: true,
        size: 9.5,
        c: "g",
      }),
    ],
    [
      ...WG({}, { ...KR[4].taken, "A-C": "r" }),
      Tx("t", 180, 168, "A-C — цикл ✗", { mono: true, size: 9.5, c: "r" }),
    ],
  ],
  h: 185,
  cues: [9, 17, 24, 30],
});

// 13. Прим
const PRIM = [
  { v: ["S"], e: {} },
  { v: ["S", "A"], e: { "A-S": "g" } },
  { v: ["S", "A", "B"], e: { "A-S": "g", "A-B": "g" } },
  { v: ["S", "A", "B", "D"], e: { "A-S": "g", "A-B": "g", "B-D": "g" } },
  {
    v: ["S", "A", "B", "D", "C", "T"],
    e: { "A-S": "g", "A-B": "g", "B-D": "g", "C-D": "g", "D-T": "g" },
  },
];
export const V13 = scene({
  labels: ["S", "+ A (2)", "+ B (1)", "+ D (3)", "Готово"],
  caption: [
    "Растим дерево от одной вершины",
    "Самое дешёвое ребро наружу: S-A (2)",
    "Теперь A-B (1)",
    "B-D (3) — самое дешёвое из выходящих",
    "C и T присоединились рёбрами 2 и 3: вес остова 11. Куча даёт O(E log V)",
  ],
  frames: PRIM.map((s) => [
    ...WG(Object.fromEntries(s.v.map((k) => [k, "g"])), s.e),
  ]),
  h: 185,
  cues: [7, 14, 21, 29],
});

// 14. Остов в жизни
const MSTU = [
  ["сети и кабели", "соединить все точки дешевле всего"],
  ["кластеризация", "убрать самые тяжёлые рёбра остова"],
  ["приближения", "обход коммивояжёра по остову"],
  ["изображения", "сегментация по близости пикселей"],
];
export const V14 = scene({
  labels: ["Сети", "Кластеры", "Приближения", "Изображения"],
  caption: [
    "Проложить кабели ко всем офисам с наименьшими затратами",
    "Удалим k − 1 самых длинных рёбер остова — получим k кластеров",
    "Остов даёт быстрые приближения для трудных задач (коммивояжёр)",
    "Сегментация изображений по близости соседних пикселей",
  ],
  frames: [0, 1, 2, 3].map((k) =>
    MSTU.flatMap(([a, b], i) => [
      {
        t: "box",
        id: `b${i}`,
        x: 180,
        y: 28 + i * 34,
        w: 334,
        h: 28,
        c: i === k ? "g" : "n",
      },
      Tx(`a${i}`, 24, 32 + i * 34, a, {
        mono: true,
        size: 9.5,
        anchor: "start",
        c: i === k ? "g" : undefined,
      }),
      Tx(`d${i}`, 340, 32 + i * 34, b, {
        size: 8.5,
        anchor: "end",
        o: i === k ? 1 : 0.5,
      }),
    ]),
  ),
  h: 160,
  cues: [8, 17, 25],
});

// 15. Практика
const PRA = [
  ["Дейкстра с кучей", "на графе из задачи"],
  ["путь по предкам", "восстановить маршрут"],
  ["Беллман — Форд", "отрицательный цикл"],
  ["Краскал и Прим", "один и тот же вес остова"],
];
export const V15 = scene({
  labels: ["Дейкстра", "Маршрут", "Цикл", "Остов"],
  caption: [
    "Реализуйте Дейкстру с кучей",
    "Верните сам маршрут, а не только длину",
    "Найдите отрицательный цикл Беллманом — Фордом",
    "Постройте остов двумя алгоритмами и сравните вес",
  ],
  frames: [0, 1, 2, 3].map((k) =>
    PRA.flatMap(([a, b], i) => [
      {
        t: "box",
        id: `b${i}`,
        x: 180,
        y: 28 + i * 34,
        w: 334,
        h: 28,
        c: i === k ? "g" : "n",
      },
      Tx(`a${i}`, 24, 32 + i * 34, a, {
        mono: true,
        size: 9.5,
        anchor: "start",
        c: i === k ? "g" : undefined,
      }),
      Tx(`d${i}`, 340, 32 + i * 34, b, {
        size: 8.5,
        anchor: "end",
        o: i === k ? 1 : 0.5,
      }),
    ]),
  ),
  h: 160,
  cues: [8, 16, 24],
});

// 16. Итог
const RC = (k) =>
  [
    ["Дейкстра", "w ≥ 0, куча"],
    ["Беллман — Форд", "w < 0"],
    ["A*, Флойд", "цель · все пары"],
    ["Остов", "Краскал · Прим"],
    ["Дальше", "ДП"],
  ].flatMap(([t, c], i) => [
    {
      t: "box",
      id: `b${i}`,
      x: 36 + i * 72,
      y: 80,
      w: 66,
      h: 66,
      c: k === i ? "g" : "n",
    },
    Tx(`t${i}`, 36 + i * 72, 76, t, {
      mono: true,
      size: 7.5,
      c: k === i ? "g" : undefined,
    }),
    Tx(`c${i}`, 36 + i * 72, 96, c, { size: 7.5, o: k === i ? 1 : 0.5 }),
  ]);
export const V16 = scene({
  labels: ["Дейкстра", "Отрицательные", "A* и Флойд", "Остов", "Дальше"],
  caption: [
    "Неотрицательные веса и приоритетная очередь",
    "Беллман — Форд справляется с отрицательными весами и ловит циклы",
    "A* — путь до одной цели; Флойд — все пары",
    "Остов — самое дешёвое соединение всех вершин",
    "Дальше — динамическое программирование",
  ],
  frames: [0, 1, 2, 3, 4].map(RC),
  cues: [8, 17, 26, 36],
});
