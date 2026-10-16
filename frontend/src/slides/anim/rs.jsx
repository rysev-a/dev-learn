import { Box, Tx, arrow, codeIn } from "./dsl.js";

/* Помощники для сцен книги «Изучаем Rust»: код с подсветкой, ячейки памяти, стрелки-указатели. */

export { Box, arrow };
// Код Rust: lines — строки, hl — подсвеченные, bad — ошибочные (красные)
export const rs = codeIn("rs");
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
