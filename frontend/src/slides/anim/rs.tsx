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

// Пара блоков «было → стало»: слева a, справа b
export const pair = (a: string, b: string, ca = "m", cb = "g", y = 60): SceneItem[] => [
  Box("pa", 90, y, 130, 34, a, ca, { size: 10 }),
  Box("pb", 270, y, 130, 34, b, cb, { size: 10 }),
];

// Ряд блоков по горизонтали: имена pre0, pre1, … (подписи — items)
export const rsRow = (pre: string, items: (string | number)[], c = "g", y = 66, size = 10.5): SceneItem[] =>
  items.map((t, i) => Box(`${pre}${i}`, 50 + i * 86, y, 76, 30, t, c, { size }));

