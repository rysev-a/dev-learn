import { Tx } from "./hw.jsx";
export { Box, arrow, slot } from "./rs.jsx";
export { Tx };

/* Помощники для сцен книги «Современный Frontend»: код JavaScript с подсветкой. */

// Код JavaScript: lines — строки, hl — подсвеченные, bad — ошибочные (красные)
export const jc = (id, x, y, lines, hl, extra = {}) => ({
  t: "code",
  id,
  x,
  y,
  lines,
  hl,
  lang: "js",
  size: 9.5,
  lh: 13,
  w: 200,
  ...extra,
});

// Код CSS
export const cs = (id, x, y, lines, hl, extra = {}) =>
  jc(id, x, y, lines, hl, { lang: "css", ...extra });
