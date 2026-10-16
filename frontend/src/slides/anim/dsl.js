/* Базовые конструкторы элементов покадровой схемы (alg.jsx). Все пакеты помощников —
   hw, lx, rs, cl, jv, db, ad — строятся на них; сцены не определяют их заново. */

export const Tx = (id, x, y, text, extra = {}) => ({
  t: "text",
  id,
  x,
  y,
  text,
  ...extra,
});

export const cell = (id, x, y, text, c = "m", extra = {}) => ({
  t: "cell",
  id,
  x,
  y,
  w: 30,
  h: 22,
  text,
  c,
  size: 11,
  ...extra,
});

export const box = (id, x, y, w, h, c = "n", lbl) => ({
  t: "box",
  id,
  x,
  y,
  w,
  h,
  c,
  lbl,
});

// Ячейка заданного размера с подписью по центру
export const Box = (id, x, y, w, h, text, c = "m", extra = {}) =>
  cell(id, x, y, text, c, { w, h, size: 9.5, ...extra });

export const line = (id, x1, y1, x2, y2, c = "m", extra = {}) => ({
  t: "line",
  id,
  x1,
  y1,
  x2,
  y2,
  c,
  ...extra,
});

export const arrow = (id, x1, y1, x2, y2, c = "m", extra = {}) =>
  line(id, x1, y1, x2, y2, c, { arrow: true, ...extra });

// Конструктор врезки кода на языке lang: lines — строки, hl — подсвеченные, bad — ошибочные (красные)
export const codeIn =
  (lang) =>
  (id, x, y, lines, hl, extra = {}) => ({
    t: "code",
    id,
    x,
    y,
    lines,
    hl,
    lang,
    size: 9.5,
    lh: 13,
    w: 200,
    ...extra,
  });
