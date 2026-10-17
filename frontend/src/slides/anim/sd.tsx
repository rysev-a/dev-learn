/* Помощники для сцен книги «Системный дизайн»: схема из компонентов в ряд, стрелки, шкалы. */

import { Box, arrow } from "./dsl.ts";
import type { SceneItem } from "./dsl.ts";

export { Tx, Box, arrow, line } from "./dsl.ts";
export { scene } from "./alg.tsx";
export { Zn, Cd, If, Pa } from "./lx.tsx";
export type { SceneItem } from "./dsl.ts";

/** узел схемы: центр (x, y), подпись в одну-две строки */
export const X = (id: string, x: number, y: number, text: string, c = "m", w = 56, h = 26): SceneItem => Box(id, x, y, w, h, text, c, { size: 8.5 });

/** ряд узлов с равными промежутками между x0 и x1 и стрелками между ними (id: p0, p1, …, стрелки pa0, …) */
export function flow(p: string, labels: string[], y: number, tones: string | string[] = "m", x0 = 42, x1 = 318, w = 56): SceneItem[] {
  const n = labels.length;
  const step = n > 1 ? (x1 - x0) / (n - 1) : 0;
  const out: SceneItem[] = [];
  labels.forEach((t, i) => {
    const c = Array.isArray(tones) ? (tones[i] ?? "m") : tones;
    out.push(X(`${p}${i}`, x0 + i * step, y, t, c, w));
    if (i + 1 < n) out.push(arrow(`${p}a${i}`, x0 + i * step + w / 2, y, x0 + (i + 1) * step - w / 2, y, c === "r" ? "r" : "m"));
  });
  return out;
}

/** столбик-шкала нагрузки: hh — высота от 0 до max */
export const Bar = (id: string, x: number, y: number, hh: number, c = "g", text = "", w = 28, max = 80): SceneItem => ({
  t: "bar",
  id,
  x,
  y,
  w,
  hh,
  max,
  c,
  text,
});

/** цвет по загрузке: до 60% зелёный, до 90% жёлтый, выше красный */
export const hot = (u: number) => (u <= 0.6 ? "g" : u <= 0.9 ? "y" : "r");
