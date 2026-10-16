/* Общие помощники сцен глав 8, 9, 14 и 17 книги «Алгоритмы и структуры данных». Всё поверх alg.jsx. */

import { Tx, type SceneItem } from "./dsl.ts";
export { Tx };

// Список «слева моно — справа пояснение»; on — номер или список подсвеченных строк.
export const LIST = (
  items: readonly (readonly string[])[],
  on: number | number[] | null | undefined,
  { w = 334, rowH = 34, y0 = 28 }: { w?: number; rowH?: number; y0?: number } = {},
): SceneItem[] => {
  const hot = new Set(Array.isArray(on) ? on : [on]);
  return items.flatMap(([a, b], i): SceneItem[] => [
    {
      t: "box",
      id: `b${i}`,
      x: 180,
      y: y0 + i * rowH,
      w,
      h: rowH - 6,
      c: hot.has(i) ? "g" : "n",
    },
    Tx(`a${i}`, 24, y0 + 4 + i * rowH, a ?? "", {
      mono: true,
      size: 9.5,
      anchor: "start",
      c: hot.has(i) ? "g" : undefined,
    }),
    Tx(`d${i}`, 340, y0 + 4 + i * rowH, b ?? "", {
      size: 8.5,
      anchor: "end",
      o: hot.has(i) ? 1 : 0.5,
    }),
  ]);
};

// Рамка вокруг клеток ряда: от индекса a до b (включительно), центры x0 + cw·i.
export const span = (id: string, x0: number, cw: number, a: number, b: number, y: number, { c = "g", h = 34, dash }: { c?: string; h?: number; dash?: SceneItem["dash"] } = {}): SceneItem => ({
  t: "box",
  id,
  x: x0 + (cw * (a + b)) / 2,
  y,
  w: cw * (b - a + 1) - 1,
  h,
  c,
  dash,
});
