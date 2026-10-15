import { cell, Tx } from "./hw.jsx";

/* Помощники для сцен книги «Изучаем Rust»: код с подсветкой, ячейки памяти, стрелки-указатели. */

export const Box = (id, x, y, w, h, text, c = "m", extra = {}) =>
  cell(id, x, y, text, c, { w, h, size: 9.5, ...extra });
export const arrow = (id, x1, y1, x2, y2, c = "m", extra = {}) => ({
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
// Код Rust: lines — строки, hl — подсвеченные, bad — ошибочные (красные)
export const rs = (id, x, y, lines, hl, extra = {}) => ({
  t: "code",
  id,
  x,
  y,
  lines,
  hl,
  lang: "rs",
  size: 9.5,
  lh: 13,
  w: 200,
  ...extra,
});
// Ячейка переменной: имя сверху, значение внизу
export const slot = (id, x, y, name, val, c = "b", extra = {}) =>
  Box(id, x, y, extra.w ?? 54, extra.h ?? 32, `${name}\n${val}`, c, {
    size: 9,
    ...extra,
  });
export const note = (id, x, y, text, c, extra = {}) =>
  Tx(id, x, y, text, { size: 9, c, ...extra });
export const ring = (id, x, y, r, c = "g") => ({
  t: "dot",
  id,
  x,
  y,
  r,
  text: "",
  c,
});
