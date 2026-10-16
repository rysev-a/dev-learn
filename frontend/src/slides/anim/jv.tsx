import { Box, codeIn, type Extra, type SceneItem } from "./dsl.ts";
export { Tx, Box, arrow } from "./dsl.ts";
export { slot } from "./rs.tsx";

/* Помощники для сцен книги «Современный Frontend»: код JavaScript и CSS с подсветкой. */

export const jc = codeIn("js");
export const cs = codeIn("css");

// Метка года на шкале истории
export const year = (id: string, x: number, y: number, text: string, c = "y"): SceneItem =>
  Box(id, x, y, 52, 22, text, c, { size: 10, mono: true });

// Сетка блоков: cols в ряд, шаг dx × dy; color — один на все или по номеру
export const grid = (
  pre: string,
  names: (string | number)[],
  x0: number,
  y0: number,
  dx: number,
  dy: number,
  cols: number,
  w: number,
  h: number,
  color: string | ((i: number) => string | undefined) | undefined,
  extra: Extra = {},
): SceneItem[] =>
  names.map((n, i) =>
    Box(`${pre}${i}`, x0 + (i % cols) * dx, y0 + Math.floor(i / cols) * dy, w, h, n, typeof color === "function" ? color(i) : color, extra),
  );
