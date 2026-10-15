/* Помощники для сцен книги «Погружаемся в Unix»: короткие конструкторы
   элементов покадровой схемы (alg.jsx) — текст, рамка, стрелка, указатель. */

export { row, edge, tree, chain } from "./alg.jsx";

export const Tx = (id, x, y, text, extra = {}) => ({
  t: "text",
  id,
  x,
  y,
  text,
  ...extra,
});

// Прямоугольник с подписью (центр x, y).
export const Bx = (id, x, y, w, h, text, c = "m", extra = {}) => ({
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

export const Ar = (id, x1, y1, x2, y2, c = "m", extra = {}) => ({
  t: "line",
  id,
  x1,
  y1,
  x2,
  y2,
  c,
  arrow: true,
  ...extra,
});

export const Ln = (id, x1, y1, x2, y2, c = "m", extra = {}) => ({
  t: "line",
  id,
  x1,
  y1,
  x2,
  y2,
  c,
  ...extra,
});

// Рамка-область с подписью над левым краем.
export const Zn = (id, x, y, w, h, lbl, c = "n", extra = {}) => ({
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

export const Dt = (id, x, y, text, c = "m", extra = {}) => ({
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
export const Pt = (id, x, y, text, c = "g", dir = "down", extra = {}) => ({
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
export const Cd = (id, x, y, lines, hl, extra = {}) => ({
  t: "code",
  id,
  x,
  y,
  lines,
  hl,
  w: 150,
  ...extra,
});

export const Pa = (id, d, c = "g", extra = {}) => ({
  t: "path",
  id,
  d,
  c,
  ...extra,
});

// Ломаная по точкам [[x, y], …].
export const Pl = (id, pts, c = "m", extra = {}) =>
  Pa(id, pts.map(([x, y], i) => `${i ? "L" : "M"}${x} ${y}`).join(" "), c, {
    w: 1.6,
    ...extra,
  });

// Элементы только при выполненном условии: ...If(n >= 2, a, b).
export const If = (cond, ...items) => (cond ? items.flat() : []);

// Цвет «включён с шага k»: on, иначе off.
export const at = (n, k, on = "g", off = "m") => (n >= k ? on : off);

// Горизонтальный ряд одинаковых клеток: id0, id1, …; c — i => цвет или массив.
export const Rw = (id, vals, x0, y, w, h, gap = 2, c = "m", extra = {}) =>
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
export const Sk = (id, vals, x, y0, w, h, gap = 2, c = "m", extra = {}) =>
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
