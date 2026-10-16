import { Box, Tx, arrow, codeIn, type Extra, type SceneItem } from "./dsl.ts";

/* Помощники для сцен книги «Изучаем Rust»: код с подсветкой, ячейки памяти, стрелки-указатели. */

export { Box, arrow };
// Код Rust: lines — строки, hl — подсвеченные, bad — ошибочные (красные)
export const rs = codeIn("rs");
// Ячейка переменной: имя сверху, значение внизу
export const slot = (id: string, x: number, y: number, name: string, val: string | number, c = "b", extra: Extra = {}) =>
  Box(id, x, y, extra.w ?? 54, extra.h ?? 32, `${name}\n${val}`, c, {
    size: 9,
    ...extra,
  });
export const note = (id: string, x: number, y: number, text: string | number, c?: string, extra: Extra = {}) =>
  Tx(id, x, y, text, { size: 9, c, ...extra });
export const ring = (id: string, x: number, y: number, r: number, c = "g"): SceneItem => ({
  t: "dot",
  id,
  x,
  y,
  r,
  text: "",
  c,
});
