import { cell } from "./hw.jsx";
export { Box, arrow, slot } from "./rs.jsx";

/* Помощники для сцен книги «От assembler к языку C»: код C и ассемблер RISC-V с подсветкой. */

// Код на C: lines — строки, hl — подсвеченные, bad — ошибочные (красные)
export const cc = (id, x, y, lines, hl, extra = {}) => ({
  t: "code",
  id,
  x,
  y,
  lines,
  hl,
  lang: "c",
  size: 9.5,
  lh: 13,
  w: 200,
  ...extra,
});
// Ассемблер RISC-V
export const asm = (id, x, y, lines, hl, extra = {}) => cc(id, x, y, lines, hl, { lang: "asm", ...extra });
// Ячейка памяти с адресом
export const mem = (id, x, y, text, c = "b", extra = {}) => cell(id, x, y, text, c, { w: 40, h: 24, size: 9, ...extra });
