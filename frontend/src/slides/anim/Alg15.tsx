import { edge, scene } from "./alg.tsx";
import { Tx, type SceneItem } from "./dsl.ts";

/* Глава 15 книги «Алгоритмы и структуры данных»: графы — обходы и связность. */

// общий граф: вершины A…G и рёбра
type Pos = number[];
const NODES: Record<string, Pos> = {
  A: [46, 85],
  B: [112, 42],
  C: [112, 128],
  D: [184, 22],
  E: [184, 85],
  F: [184, 148],
  G: [262, 85],
};
const EDGES: [string, string][] = [
  ["A", "B"],
  ["A", "C"],
  ["B", "D"],
  ["B", "E"],
  ["C", "E"],
  ["C", "F"],
  ["E", "G"],
  ["F", "G"],
];
const P = (k: string, nodes: Record<string, Pos> = NODES) => ({ x: nodes[k]![0], y: nodes[k]![1] });
// граф: colors — {вершина: цвет}, ec — {"A-B": цвет}
function GR(
  colors: Record<string, string> = {},
  ec: Record<string, string> = {},
  {
    nodes = NODES,
    edges = EDGES,
    labels = {},
    directed = false,
    id = "g",
    r = 12,
    o = 1,
  }: {
    nodes?: Record<string, Pos>;
    edges?: [string, string][];
    labels?: Record<string, string | number>;
    directed?: boolean;
    id?: string;
    r?: number;
    o?: number;
  } = {},
): SceneItem[] {
  return [
    ...edges.map(([a, b]) =>
      edge(`${id}e${a}${b}`, P(a, nodes)!, P(b, nodes), {
        r,
        c: ec[`${a}-${b}`] ?? ec[`${b}-${a}`] ?? "m",
        arrow: directed,
        o: o,
      }),
    ),
    ...Object.keys(nodes).map((k): SceneItem => ({
      t: "dot",
      id: `${id}${k}`,
      x: nodes[k]![0],
      y: nodes[k]![1],
      r,
      text: labels[k] ?? k,
      c: colors[k] ?? "m",
      size: 10.5,
      o,
    })),
  ];
}

// 1. Дерево — частный случай графа
const TREE_E: [string, string][] = [
  ["A", "B"],
  ["A", "C"],
  ["B", "D"],
  ["B", "E"],
];
export const V01 = scene({
  labels: ["Дерево", "Лишнее ребро", "Граф"],
  caption: [
    "Дерево — граф без циклов с одним корнем",
    "Добавим ребро между «двоюродными» — появился цикл",
    "Граф: набор вершин и рёбер; рёбра бывают направленными и со стрелками, с весами и без",
  ],
  frames: [
    [...GR({ A: "y" }, {}, { edges: TREE_E })],
    [
      ...GR(
        { A: "y", E: "r", C: "r" },
        { "C-E": "r" },
        { edges: [...TREE_E, ["C", "E"]] },
      ),
    ],
    [...GR({}, {}, { edges: EDGES })],
  ],
  h: 165,
  cues: [9, 19],
});

// 2. Матрица и списки
const M4 = ["A", "B", "C", "D"];
const ME: [number, number][] = [
  [0, 1],
  [0, 2],
  [1, 2],
  [2, 3],
];
const MN = { A: [50, 50], B: [50, 120], C: [120, 85], D: [190, 85] };
export const V02 = scene({
  labels: ["Граф", "Матрица смежности", "Списки смежности"],
  caption: [
    "Четыре вершины, четыре ребра",
    "Матрица n × n: ребро проверяется за O(1), но память всегда n² — даже для разреженного графа",
    "Списки: у каждой вершины — её соседи; память O(V + E), перебор соседей мгновенный",
  ],
  frames: [
    [
      ...GR(
        {},
        {},
        {
          nodes: MN,
          edges: [
            ["A", "B"],
            ["A", "C"],
            ["B", "C"],
            ["C", "D"],
          ],
        },
      ),
    ],
    [
      ...GR(
        {},
        {},
        {
          nodes: Object.fromEntries(
            Object.entries(MN).map(([k, v]) => [
              k,
              [v[0]! * 0.6, v[1]! * 0.9 + 6],
            ]),
          ),
          edges: [
            ["A", "B"],
            ["A", "C"],
            ["B", "C"],
            ["C", "D"],
          ],
          r: 10,
          o: 0.5,
        },
      ),
      ...M4.flatMap((_, i): SceneItem[] =>
        M4.map((__, j): SceneItem => ({
          t: "cell",
          id: `m${i}${j}`,
          x: 210 + 30 * j,
          y: 40 + 28 * i,
          w: 26,
          h: 24,
          text: ME.some(
            ([a, b]) => (a === i && b === j) || (a === j && b === i),
          )
            ? 1
            : 0,
          c: ME.some(([a, b]) => (a === i && b === j) || (a === j && b === i))
            ? "g"
            : "m",
          size: 10,
        })),
      ),
    ],
    [
      ...GR(
        {},
        {},
        {
          nodes: Object.fromEntries(
            Object.entries(MN).map(([k, v]) => [
              k,
              [v[0]! * 0.6, v[1]! * 0.9 + 6],
            ]),
          ),
          edges: [
            ["A", "B"],
            ["A", "C"],
            ["B", "C"],
            ["C", "D"],
          ],
          r: 10,
          o: 0.5,
        },
      ),
      ...[
        ["A", "B C"],
        ["B", "A C"],
        ["C", "A B D"],
        ["D", "C"],
      ].flatMap(([k, ns], i): SceneItem[] => [
        {
          t: "cell",
          id: `ls${i}`,
          x: 205,
          y: 38 + 30 * i,
          w: 26,
          h: 24,
          text: k,
          c: "b",
          size: 10,
        },
        {
          t: "cell",
          id: `ln${i}`,
          x: 275,
          y: 38 + 30 * i,
          w: 80,
          h: 24,
          text: ns,
          c: "g",
          size: 10,
        },
      ]),
    ],
  ],
  h: 165,
  cues: [8, 20],
});

// 3. Обход в глубину
const DFS: { vis: string[]; ec: Record<string, string>; cur: string; t: string }[] = [
  { vis: ["A"], ec: {}, cur: "A", t: "A" },
  {
    vis: ["A", "B", "D"],
    ec: { "A-B": "g", "B-D": "g" },
    cur: "D",
    t: "A B D — тупик",
  },
  {
    vis: ["A", "B", "D", "E"],
    ec: { "A-B": "g", "B-D": "g", "B-E": "g" },
    cur: "E",
    t: "откатились в B, ныряем в E",
  },
  {
    vis: ["A", "B", "D", "E", "C", "F"],
    ec: { "A-B": "g", "B-D": "g", "B-E": "g", "C-E": "g", "C-F": "g" },
    cur: "F",
    t: "E → C → F",
  },
  {
    vis: ["A", "B", "D", "E", "C", "F", "G"],
    ec: {
      "A-B": "g",
      "B-D": "g",
      "B-E": "g",
      "C-E": "g",
      "C-F": "g",
      "F-G": "g",
    },
    cur: "G",
    t: "порядок: A B D E C F G",
  },
];
export const V03 = scene({
  labels: ["Старт", "Тупик", "Откат", "Дальше", "Все"],
  caption: [
    "Ныряем в первого непосещённого соседа",
    "Упёрлись в тупик D — откатываемся на шаг назад",
    "Из B идём в следующую ветку — в E",
    "Нужно множество посещённых, иначе на циклах — бесконечный обход",
    "Все вершины обойдены; время O(V + E)",
  ],
  frames: DFS.map((s): SceneItem[] => [
    ...GR(
      Object.fromEntries(s.vis.map((v) => [v, v === s.cur ? "y" : "g"])),
      s.ec,
    ),
    Tx("t", 180, 160, s.t, { mono: true, size: 10 }),
  ]),
  h: 172,
  cues: [10, 18, 28, 36],
});

// 4. Связность и циклы: компоненты
const N2 = {
  A: [60, 50],
  B: [120, 50],
  C: [90, 110],
  X: [240, 50],
  Y: [300, 50],
  Z: [270, 110],
  W: [270, 150],
};
const E2: [string, string][] = [
  ["A", "B"],
  ["B", "C"],
  ["A", "C"],
  ["X", "Y"],
  ["Y", "Z"],
  ["X", "Z"],
  ["Z", "W"],
];
export const V04 = scene({
  labels: ["Две компоненты", "Запуск 1", "Запуск 2", "Число компонент"],
  caption: [
    "Граф распался на два острова",
    "Первый запуск обхода посетил один остров",
    "Непосещённая вершина — второй запуск; запусков столько, сколько компонент",
    "Связность, число компонент, поиск циклов — всё за O(V + E)",
  ],
  frames: [
    [...GR({}, {}, { nodes: N2, edges: E2 })],
    [
      ...GR(
        { A: "g", B: "g", C: "g" },
        { "A-B": "g", "B-C": "g", "A-C": "g" },
        { nodes: N2, edges: E2 },
      ),
    ],
    [
      ...GR(
        { A: "g", B: "g", C: "g", X: "b", Y: "b", Z: "b", W: "b" },
        {
          "A-B": "g",
          "B-C": "g",
          "A-C": "g",
          "X-Y": "b",
          "Y-Z": "b",
          "X-Z": "b",
          "Z-W": "b",
        },
        { nodes: N2, edges: E2 },
      ),
    ],
    [
      ...GR(
        { A: "g", B: "g", C: "g", X: "b", Y: "b", Z: "b", W: "b" },
        {},
        { nodes: N2, edges: E2, o: 0.5 },
      ),
      Tx("t", 180, 150, "компонент: 2", { mono: true, size: 12, c: "g" }),
    ],
  ],
  h: 172,
  cues: [9, 18, 28],
});

// 5. Три цвета на ориентированном графе
const DN = { P: [60, 60], Q: [140, 60], R: [220, 60], S: [180, 125] };
const DE: [string, string][] = [
  ["P", "Q"],
  ["Q", "R"],
  ["R", "S"],
  ["S", "Q"],
];
export const V05 = scene({
  labels: ["Белые", "Серая цепочка", "Ребро в серую", "Чёрные"],
  caption: [
    "Белая — не тронута, серая — погружение идёт сейчас, чёрная — вершина и всё её поддерево исследованы",
    "Идём P → Q → R → S: вся цепочка — серая",
    "S указывает на серую Q: вернулись в собственный текущий путь — цикл",
    "Ребро в чёрную вершину не страшно: та ветка закончена, кольца через неё нет",
  ],
  frames: [
    [...GR({}, {}, { nodes: DN, edges: DE, directed: true })],
    [
      ...GR(
        { P: "y", Q: "y", R: "y", S: "y" },
        {},
        { nodes: DN, edges: DE, directed: true },
      ),
    ],
    [
      ...GR(
        { P: "y", Q: "r", R: "y", S: "y" },
        { "S-Q": "r" },
        { nodes: DN, edges: DE, directed: true },
      ),
      Tx("t", 180, 160, "цикл: Q → R → S → Q", {
        mono: true,
        size: 10.5,
        c: "r",
      }),
    ],
    [
      ...GR(
        { P: "m", Q: "m", R: "m", S: "m" },
        {},
        { nodes: DN, edges: DE, directed: true, o: 0.4 },
      ),
      Tx("t", 180, 90, "серая = в пути, чёрная = закончена", {
        mono: true,
        size: 10,
        c: "g",
      }),
    ],
  ],
  h: 172,
  cues: [9, 16, 24],
});

// 6. Топологическая сортировка через выход из вершины
const TN: Record<string, Pos> = {
  A: [50, 85],
  B: [120, 42],
  C: [120, 128],
  D: [200, 85],
  E: [280, 85],
};
const TE: [string, string][] = [
  ["A", "B"],
  ["A", "C"],
  ["B", "D"],
  ["C", "D"],
  ["D", "E"],
];
export const V06 = scene({
  labels: ["Зависимости", "Выход из вершин", "Порядок"],
  caption: [
    "Граф зависимостей: стрелка — «должно быть сделано раньше»; циклов нет",
    "Задачу кладём в ответ, когда обход вернулся из всех зависимостей: E, D, B, C, A",
    "Выгрузка стека в обратном порядке: A C B D E — зависимости всегда впереди",
  ],
  frames: [
    [...GR({}, {}, { nodes: TN, edges: TE, directed: true })],
    [
      ...GR(
        { E: "g", D: "g", B: "g", C: "g", A: "g" },
        {},
        {
          nodes: TN,
          edges: TE,
          directed: true,
          labels: { E: "1", D: "2", B: "3", C: "4", A: "5" },
        },
      ),
      Tx("t", 180, 160, "порядок выхода: E D B C A", {
        mono: true,
        size: 10,
        c: "g",
      }),
    ],
    [
      ...GR(
        { A: "g", C: "g", B: "g", D: "g", E: "g" },
        {},
        {
          nodes: TN,
          edges: TE,
          directed: true,
          labels: { A: "1", C: "2", B: "3", D: "4", E: "5" },
        },
      ),
      Tx("t", 180, 160, "обратный порядок: A C B D E", {
        mono: true,
        size: 10,
        c: "g",
      }),
    ],
  ],
  h: 172,
  cues: [10, 20],
});

// 7. Алгоритм Кана
const KS: { deg: Record<string, number>; q: string[]; out: string[]; c: Record<string, string> }[] = [
  { deg: { A: 0, B: 1, C: 1, D: 2, E: 1 }, q: ["A"], out: [], c: { A: "y" } },
  {
    deg: { A: 0, B: 0, C: 0, D: 2, E: 1 },
    q: ["B", "C"],
    out: ["A"],
    c: { A: "g", B: "y", C: "y" },
  },
  {
    deg: { A: 0, B: 0, C: 0, D: 0, E: 1 },
    q: ["D"],
    out: ["A", "B", "C"],
    c: { A: "g", B: "g", C: "g", D: "y" },
  },
  {
    deg: { A: 0, B: 0, C: 0, D: 0, E: 0 },
    q: [],
    out: ["A", "B", "C", "D", "E"],
    c: { A: "g", B: "g", C: "g", D: "g", E: "g" },
  },
];
export const V07 = scene({
  labels: ["Степени захода", "Достали A", "Достали B, C", "Достали D, E"],
  caption: [
    "Степень захода — число зависимостей; с нулевой — делаем сразу",
    "Убрали A: у B и C степень стала нулём — они встают в очередь",
    "B и C сняли зависимости D — степень D стала нулём",
    "Очередь опустела; если вершин в ответе меньше, чем в графе, — есть цикл. Время O(V + E)",
  ],
  frames: KS.map((s): SceneItem[] => [
    ...GR(s.c, {}, { nodes: TN, edges: TE, directed: true, labels: {} }),
    ...Object.entries(TN).map(([k, [x, y]]) =>
      Tx(`d${k}`, x!, y! + 26, `вх ${s.deg[k]}`, {
        mono: true,
        size: 8,
        c: s.deg[k] === 0 ? "g" : "m",
      }),
    ),
    Tx(
      "q",
      24,
      160,
      "очередь: " +
        (s.q.join(" ") || "—") +
        "   ответ: " +
        (s.out.join(" ") || "—"),
      { mono: true, size: 9, anchor: "start" },
    ),
  ]),
  h: 172,
  cues: [9, 19, 28],
});

// 8. Обход в ширину: волны
const DIST = { A: 0, B: 1, C: 1, D: 2, E: 2, F: 2, G: 3 };
const WCOL = ["y", "g", "b", "v"];
export const V08 = scene({
  labels: ["Старт", "Волна 1", "Волна 2", "Волна 3"],
  caption: [
    "Очередь с одной вершиной; волны будут расходиться кругами",
    "Первая волна — непосредственные соседи B и C",
    "Вторая — соседи соседей: D, E, F",
    "Третья — G. Расстояние = номер волны: кратчайшие пути в невзвешенном графе",
  ],
  frames: [0, 1, 2, 3].map((k): SceneItem[] => [
    ...GR(
      Object.fromEntries(
        Object.entries(DIST)
          .filter(([, d]) => d <= k)
          .map(([v, d]) => [v, WCOL[d]]),
      )!,
      {},
      {
        labels: Object.fromEntries(
          Object.entries(DIST)
            .filter(([, d]) => d <= k)
            .map(([v, d]) => [v, `${v}${d}`]),
        ),
      },
    ),
    Tx(
      "t",
      180,
      160,
      ["", "дистанция 1: B, C", "дистанция 2: D, E, F", "дистанция 3: G"][k]!,
      { mono: true, size: 10 },
    ),
  ]),
  h: 172,
  cues: [8, 17, 26],
});

// 9. Кратчайший путь по рёбрам
export const V09 = scene({
  labels: ["Расстояния", "Путь назад", "Состояния"],
  caption: [
    "Каждая вершина запомнила, из какой пришла (родитель) и расстояние",
    "Путь восстанавливается по родителям от цели к старту: G ← E ← B ← A",
    "Вершиной может быть любое состояние: позиция коня, слово, конфигурация игры",
  ],
  frames: [
    [
      ...GR(
        { A: "y", B: "g", C: "g", D: "b", E: "b", F: "b", G: "v" },
        {},
        { labels: { A: "0", B: "1", C: "1", D: "2", E: "2", F: "2", G: "3" } },
      ),
    ],
    [
      ...GR(
        { A: "y", B: "g", E: "b", G: "v" },
        { "A-B": "g", "B-E": "g", "E-G": "g" },
        { labels: { A: "A", B: "B", E: "E", G: "G" } },
      ),
      Tx("t", 180, 160, "A → B → E → G: 3 ребра", {
        mono: true,
        size: 10,
        c: "g",
      }),
    ],
    [
      Tx("a", 180, 50, "ходы коня на шахматной доске", {
        mono: true,
        size: 10.5,
        c: "g",
      }),
      Tx("b", 180, 85, "слово → слово (одна буква)", {
        mono: true,
        size: 10.5,
        c: "g",
      }),
      Tx("c", 180, 120, "расклад игры → расклад игры", {
        mono: true,
        size: 10.5,
        c: "g",
      }),
    ],
  ],
  h: 172,
  cues: [10, 20],
});

// 10. Лабиринт: глубина против ширины (пути считаются здесь же)
const MAZE = ["S...#....", ".##.#.##.", ".#.....#.", ".#.####.#", "........G"];
const ROWS = MAZE.length;
const COLS = MAZE[0]!.length;
const free = (r: number, c: number) =>
  r >= 0 && r < ROWS && c >= 0 && c < COLS && MAZE[r]![c] !== "#";
const DIRS: [number, number][] = [
  [0, 1],
  [1, 0],
  [0, -1],
  [-1, 0],
];
const key = (r: number, c: number) => r * COLS + c;
function bfsPath() {
  const prev = new Map<number, number>([[0, -1]]);
  const q: [number, number][] = [[0, 0]];
  while (q.length) {
    const [r, c] = q.shift()!;
    for (const [dr, dc] of DIRS) {
      const nr = r + dr;
      const nc = c + dc;
      if (free(nr, nc) && !prev.has(key(nr, nc))) {
        prev.set(key(nr, nc), key(r, c));
        q.push([nr, nc]);
      }
    }
  }
  const path: number[] = [];
  for (let k = key(ROWS - 1, COLS - 1); k !== -1; k = prev.get(k) ?? -1) path.push(k);
  return path;
}
function dfsPath(): number[] | null {
  const seen = new Set<number>();
  let found: number[] | null = null;
  const go = (r: number, c: number, path: number[]) => {
    if (found) return;
    seen.add(key(r, c));
    path.push(key(r, c));
    if (r === ROWS - 1 && c === COLS - 1) {
      found = [...path];
      return;
    }
    for (const [dr, dc] of DIRS) {
      const nr = r + dr;
      const nc = c + dc;
      if (free(nr, nc) && !seen.has(key(nr, nc))) go(nr, nc, path);
    }
    path.pop();
  };
  go(0, 0, []);
  return found;
}
const BP = new Set(bfsPath());
const DP = new Set(dfsPath());
const MZ = (set: Set<number>, c?: string): SceneItem[] =>
  MAZE.flatMap((line, r): SceneItem[] =>
    [...line].map((ch, cc): SceneItem => ({
      t: "cell",
      id: `z${r}${cc}`,
      x: 92 + 22 * cc,
      y: 34 + 22 * r,
      w: 20,
      h: 20,
      text: ch === "S" || ch === "G" ? ch : "",
      size: 9,
      c:
        ch === "#"
          ? "W"
          : set.has(key(r, cc))
            ? c
            : ch === "S" || ch === "G"
              ? "y"
              : "m",
    })),
  );
export const V10 = scene({
  labels: ["Лабиринт", "В глубину", "В ширину"],
  caption: [
    "Клетки — вершины, проходы — рёбра; нужно добраться от S до G",
    `Глубина доберётся быстро, но путь вычурный: ${DP.size} клеток`,
    `Ширина разливается волной — первый дошедший путь кратчайший: ${BP.size} клеток`,
  ],
  frames: [MZ(new Set<number>(), "g"), MZ(DP, "r"), MZ(BP, "g")],
  h: 160,
  cues: [10, 20],
});

// 11. Шесть рукопожатий
const RINGS = [
  [5, 30, "g"],
  [14, 56, "b"],
  [28, 82, "y"],
] as const;
const RD = (k: number) =>
  RINGS.flatMap(([n, rad, c], ri) =>
    Array.from({ length: n }, (_, i): SceneItem => {
      const a = (i / n) * Math.PI * 2 + ri * 0.4;
      return {
        t: "dot",
        id: `p${ri}-${i}`,
        x: 180 + rad * 1.6 * Math.cos(a),
        y: 82 + rad * Math.sin(a),
        r: ri === 2 ? 3.5 : 4.5,
        c: ri < k ? c : "n",
        o: ri < k ? 1 : 0.2,
      };
    }),
  );
export const V11 = scene({
  labels: ["Я", "Друзья", "Друзья друзей", "Шесть волн"],
  caption: [
    "Вы — центр волны",
    "Первая волна — друзья",
    "Вторая — друзья друзей: число людей растёт по экспоненте",
    "Шесть волн охватывают почти всё население: рукопожатия — это обход в ширину",
  ],
  frames: [
    [
      { t: "dot", id: "me", x: 180, y: 82, r: 8, c: "y", text: "я", size: 8 },
      ...RD(0),
    ],
    [
      { t: "dot", id: "me", x: 180, y: 82, r: 8, c: "y", text: "я", size: 8 },
      ...RD(1),
    ],
    [
      { t: "dot", id: "me", x: 180, y: 82, r: 8, c: "y", text: "я", size: 8 },
      ...RD(3),
    ],
    [
      { t: "dot", id: "me", x: 180, y: 82, r: 8, c: "y", text: "я", size: 8 },
      ...RD(3),
      Tx("t", 180, 160, "≈ 6 волн", { mono: true, size: 11, c: "y" }),
    ],
  ],
  h: 172,
  cues: [9, 17, 26],
});

// 12. Двудольная раскраска
const SQN = { a: [120, 50], b: [240, 50], c: [240, 120], d: [120, 120] };
const SQE: [string, string][] = [
  ["a", "b"],
  ["b", "c"],
  ["c", "d"],
  ["d", "a"],
];
const TRN = { a: [180, 40], b: [110, 120], c: [250, 120] };
const TRE: [string, string][] = [
  ["a", "b"],
  ["b", "c"],
  ["c", "a"],
];
export const V12 = scene({
  labels: ["Чётный цикл", "Нечётный цикл", "Вывод"],
  caption: [
    "Красим волнами: соседям — противоположный цвет; четырёхугольник раскрашивается",
    "В треугольнике соседи оказываются одного цвета — раскраска невозможна",
    "Нечётный цикл — препятствие для двудольности; удалось — две команды без конфликтов",
  ],
  frames: [
    [
      ...GR(
        { a: "g", b: "b", c: "g", d: "b" },
        {},
        { nodes: SQN, edges: SQE, id: "q" },
      ),
    ],
    [
      ...GR(
        { a: "g", b: "b", c: "g" },
        { "c-a": "r" },
        { nodes: TRN, edges: TRE, id: "t" },
      ),
    ],
    [
      Tx("a", 180, 50, "двудольный ⇔ нет нечётных циклов", {
        mono: true,
        size: 11,
        c: "g",
      }),
      Tx("b", 180, 90, "две команды: «враги» — только между командами", {
        size: 9,
      }),
    ],
  ],
  h: 165,
  cues: [10, 20],
});

// 13. Практические тонкости
const PT: [string, string][] = [
  ["рекурсия на миллионе", "явный стек — безопаснее"],
  ["посещённые", "помечать при постановке в очередь"],
  ["родители", "хранить для восстановления пути"],
  ["несвязные графы", "запускать обход из каждой вершины"],
];
export const V13 = scene({
  labels: ["Стек", "Очередь", "Родители", "Несвязные"],
  caption: [
    "Рекурсия на графе в миллион вершин уронит стек — пишите итеративно",
    "Помечайте посещённые при помещении в очередь, а не при извлечении — иначе дубликаты",
    "Запоминайте родителя: по нему восстанавливается путь",
    "Один запуск покрывает одну компоненту — для всего графа запускайте из каждой непосещённой",
  ],
  frames: [0, 1, 2, 3].map((k) =>
    PT.flatMap(([a, b], i) => [
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
  cues: [10, 21, 30],
});

// 14. Сетка как граф: острова
const LAND = ["11000", "11010", "00011", "00001", "10000"];
const LR = LAND.length;
const LC = LAND[0]!.length;
function islands() {
  const id = Array.from({ length: LR }, () => Array(LC).fill(-1));
  let n = 0;
  for (let r = 0; r < LR; r++)
    for (let c = 0; c < LC; c++)
      if (LAND[r]![c] === "1" && id[r]![c] < 0) {
        const st: [number, number][] = [[r, c]];
        id[r]![c] = n;
        while (st.length) {
          const [a, b] = st.pop()!;
          for (const [dr, dc] of DIRS) {
            const x = a + dr;
            const y = b + dc;
            if (
              x >= 0 &&
              x < LR &&
              y >= 0 &&
              y < LC &&
              LAND[x]![y] === "1" &&
              id[x]![y] < 0
            ) {
              id[x]![y] = n;
              st.push([x, y]);
            }
          }
        }
        n++;
      }
  return { id, n };
}
const ISL = islands();
const ICOL = ["g", "b", "y", "v"];
const GRID = (colorOf: (r: number, c: number) => string): SceneItem[] =>
  LAND.flatMap((line, r): SceneItem[] =>
    [...line].map((ch, c): SceneItem => ({
      t: "cell",
      id: `l${r}${c}`,
      x: 110 + 28 * c,
      y: 28 + 28 * r,
      w: 24,
      h: 24,
      text: "",
      c: ch === "1" ? colorOf(r, c) : "n",
      size: 9,
    })),
  );
export const V14 = scene({
  labels: ["Сетка", "Четыре соседа", "Острова"],
  caption: [
    "Суша и вода: клетка — вершина",
    "Рёбра — касания по вертикали и горизонтали",
    "Каждая непосещённая суша запускает обход, помечающий остров целиком: " +
      ISL.n +
      " острова — " +
      ISL.n +
      " запуска",
  ],
  frames: [
    GRID(() => "m"),
    [
      ...GRID(() => "m"),
      { t: "dot", id: "ctr", x: 110 + 28 * 1, y: 28 + 28 * 1, r: 4, c: "y" },
      ...[
        [0, 1],
        [1, 2],
        [2, 1],
        [1, 0],
      ].map(([dr, dc], i): SceneItem => ({
        t: "line",
        id: `ar${i}`,
        x1: 110 + 28 * 1,
        y1: 28 + 28 * 1,
        x2: 110 + 28 * (1 + dc! * 0.9),
        y2: 28 + 28 * (1 + dr! * 0.9),
        c: "y",
        arrow: true,
      })),
    ],
    GRID((r, c) => ICOL[ISL.id[r]![c] % 4]!),
  ],
  h: 175,
  cues: [8, 18],
});

// 15. Мосты и точки сочленения
const BN = {
  a1: [60, 50],
  a2: [60, 120],
  a3: [130, 85],
  b1: [230, 85],
  b2: [300, 50],
  b3: [300, 120],
};
const BE: [string, string][] = [
  ["a1", "a2"],
  ["a2", "a3"],
  ["a1", "a3"],
  ["a3", "b1"],
  ["b1", "b2"],
  ["b2", "b3"],
  ["b1", "b3"],
];
export const V15 = scene({
  labels: ["Сеть", "Мост", "Если упадёт"],
  caption: [
    "Две плотные группы, связанные одной связью",
    "Мост — ребро, без которого граф распадается; точка сочленения — такая же вершина",
    "Один модифицированный обход в глубину находит все за O(V + E): какой сервер критичен, что дублировать",
  ],
  frames: [
    [...GR({}, {}, { nodes: BN, edges: BE, id: "n" })],
    [
      ...GR({}, { "a3-b1": "r" }, { nodes: BN, edges: BE, id: "n" }),
      Tx("t", 180, 150, "мост", { mono: true, size: 11, c: "r" }),
    ],
    [
      ...GR(
        { a1: "g", a2: "g", a3: "g", b1: "b", b2: "b", b3: "b" },
        {},
        { nodes: BN, edges: BE.filter((e) => e[0] + e[1] !== "a3b1"), id: "n" },
      ),
      Tx("t", 180, 150, "две несвязные части", {
        mono: true,
        size: 11,
        c: "r",
      }),
    ],
  ],
  h: 165,
  cues: [8, 18],
});

// 16. Практика
const PRA: [string, string][] = [
  ["компоненты связности", "обход в глубину по знакомствам"],
  ["кратчайшая цепочка", "обход в ширину между двумя людьми"],
  ["двудольность", "раскраска волнами"],
  ["словесная лестница", "слова — вершины, замена буквы — ребро"],
];
export const V16 = scene({
  labels: ["Компоненты", "Цепочка", "Двудольность", "Лестница"],
  caption: [
    "Посчитайте компоненты связности в списке знакомств",
    "Найдите минимальное число знакомств между двумя людьми",
    "Проверьте двудольность маленького графа раскраской",
    "Словесная лестница: превратить слово в другое заменами по одной букве",
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

// 17. Итог
const RC = (k: number): SceneItem[] =>
  [
    ["Хранение", "матрица · списки"],
    ["Глубина", "стек"],
    ["Ширина", "очередь"],
    ["Применения", "компоненты · порядок"],
    ["Дальше", "веса"],
  ].flatMap(([t, c], i): SceneItem[] => [
    {
      t: "box",
      id: `b${i}`,
      x: 36 + i * 72,
      y: 80,
      w: 66,
      h: 66,
      c: k === i ? "g" : "n",
    },
    Tx(`t${i}`, 36 + i * 72, 76, t!, {
      mono: true,
      size: 8,
      c: k === i ? "g" : undefined,
    }),
    Tx(`c${i}`, 36 + i * 72, 96, c!, { size: 7.5, o: k === i ? 1 : 0.5 }),
  ]);
export const V17 = scene({
  labels: ["Хранение", "Глубина", "Ширина", "Применения", "Дальше"],
  caption: [
    "Матрица для плотных графов, списки — для разреженных",
    "Нырок по стеку: компоненты, циклы, топологический порядок",
    "Волны по очереди: минимум шагов, уровни, двудольность",
    "Оба обхода линейны и различаются контейнером",
    "Дальше — рёбра с весами: кратчайшие пути и остовы",
  ],
  frames: [0, 1, 2, 3, 4].map(RC),
  cues: [8, 17, 26, 36],
});
