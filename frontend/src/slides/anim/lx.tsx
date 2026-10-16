/* Помощники для сцен книги «Погружаемся в Unix»: короткие конструкторы
   элементов покадровой схемы (alg.jsx) — текст, рамка, стрелка, указатель. */

import type { Extra, SceneItem } from "./dsl.ts";

export { row, edge, tree, chain } from "./alg.tsx";

export { Tx } from "./dsl.ts";

/** цвет клеток ряда: один на всех, по номеру или функцией */
type CellColor = string | string[] | ((i: number) => string);

// Прямоугольник с подписью (центр x, y).
export const Bx = (id: string, x: number, y: number, w: number, h: number, text: string | number, c = "m", extra: Extra = {}): SceneItem => ({
  t: "cell",
  id,
  x,
  y,
  w,
  h,
  text,
  c,
  size: 9,
  ...extra,
});

export { arrow as Ar, line as Ln } from "./dsl.ts";


// Рамка-область с подписью над левым краем.
export const Zn = (id: string, x: number, y: number, w: number, h: number, lbl: string, c = "n", extra = {}) => ({
  t: "box",
  id,
  x,
  y,
  w,
  h,
  c,
  lbl,
  ...extra,
});

export const Dt = (id: string, x: number, y: number, text: string, c = "m", extra = {}) => ({
  t: "dot",
  id,
  x,
  y,
  r: 11,
  text,
  c,
  ...extra,
});

// Указатель-стрелка с именем: острие в (x, y).
export const Pt = (id: string, x: number, y: number, text: string, c = "g", dir = "down", extra = {}) => ({
  t: "ptr",
  id,
  x,
  y,
  text,
  c,
  dir,
  ...extra,
});

// Врезка кода; hl — подсвеченные строки.
export const Cd = (id: string, x: number, y: number, lines: string[], hl: number|number[]|undefined, extra = {}) => ({
  t: "code",
  id,
  x,
  y,
  lines,
  hl,
  w: 150,
  ...extra,
});

export const Pa = (id: any, d: any, c = "g", extra = {}) => ({
  t: "path",
  id,
  d,
  c,
  ...extra,
});

// Ломаная по точкам [[x, y], …].
export const Pl = (id: string, pts: number[][]|[any,any][], c = "m", extra = {}) =>
  Pa(id, pts.map(([x, y], i) => `${i ? "L" : "M"}${x} ${y}`).join(" "), c, {
    w: 1.6,
    ...extra,
  });

// Элементы только при выполненном условии: ...If(n >= 2, a, b).
export const If = (cond: boolean, ...items: ({ t: string; id: string; x: number; y: number; w: number; h: number; text: string; c: string; size: number; }|{ t: string; id: string; x1: number; y1: number; x2: number; y2: number; c: string; })[]) => (cond ? items.flat() : []);

// Цвет «включён с шага k»: on, иначе off.
export const at = (n: number, k: number, on = "g", off = "m") => (n >= k ? on : off);

// Горизонтальный ряд одинаковых клеток: id0, id1, …; c — i => цвет или массив.
export const Rw = (id: string, vals: (string | number)[], x0: number, y: number, w: number, h: number, gap = 2, c: CellColor = "m", extra: Extra = {}): SceneItem[] =>
  vals.map((v, i) => ({
    t: "cell",
    id: `${id}${i}`,
    x: x0 + i * (w + gap),
    y,
    w,
    h,
    text: v,
    c: typeof c === "function" ? c(i) : Array.isArray(c) ? c[i] : c,
    size: 9,
    ...extra,
  }));

// Вертикальный стек клеток сверху вниз.
export const Sk = (id: string, vals: (string | number)[], x: number, y0: number, w: number, h: number, gap = 2, c: CellColor = "m", extra: Extra = {}): SceneItem[] =>
  vals.map((v, i) => ({
    t: "cell",
    id: `${id}${i}`,
    x,
    y: y0 + i * (h + gap),
    w,
    h,
    text: v,
    c: typeof c === "function" ? c(i) : Array.isArray(c) ? c[i] : c,
    size: 9,
    ...extra,
  }));
