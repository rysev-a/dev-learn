import { gp, type Pt } from "./alg.tsx";
import { Tx, cell, box, type Extra, type SceneItem } from "./dsl.ts";

/* Помощники для сцен по цифровой схемотехнике (книга «Архитектура компьютера»):
   уровень сигнала → цвет, элементы схем и ломаные провода. Элементы рисует alg.jsx (gate, tr, sw, lamp). */

export { gp, Tx, cell, box };
export const lv = (b: number) => (b ? "g" : "m"); // 1 — зелёный, 0 — приглушённый
export const bit = (id: string, x: number, y: number, v: number | boolean | string | undefined, extra: Extra = {}): SceneItem => ({
  t: "cell",
  id,
  x,
  y,
  w: 24,
  h: 22,
  text: String(v ?? "?"),
  c: v === 1 || v === true ? "g" : "m",
  size: 12,
  ...extra,
});
export const GT = (id: string, g: string, x: number, y: number, extra: Extra = {}): SceneItem => ({
  t: "gate",
  id,
  g,
  x,
  y,
  ...extra,
});
// Ломаная по точкам [[x,y],…]
export const pl = (id: string, pts: [number, number][], c = "m", extra: Extra = {}): SceneItem => ({
  t: "path",
  id,
  d: pts.map(([x, y], i) => `${i ? "L" : "M"}${x} ${y}`).join(" "),
  c,
  w: 1.8,
  ...extra,
});
// Провод между точками a и b с изломом на x = xm
export const wr = (id: string, a: Pt, b: Pt, c = "m", xm?: number, extra: Extra = {}): SceneItem => {
  const m = xm ?? (a.x + b.x) / 2;
  return pl(
    id,
    a.y === b.y
      ? [
          [a.x, a.y],
          [b.x, b.y],
        ]
      : [
          [a.x, a.y],
          [m, a.y],
          [m, b.y],
          [b.x, b.y],
        ],
    c,
    extra,
  );
};

// Трапеция мультиплексора (широкая сторона слева) и демультиплексора (rev — широкая справа). Возвращает [контур, подпись].
export const mux = (id: string, x: number, y: number, w: number, h: number, c = "b", label = "MUX", rev = false): SceneItem[] => [
  {
    t: "path",
    id,
    d: rev
      ? `M${x - w / 2} ${y - h / 4} L${x + w / 2} ${y - h / 2} L${x + w / 2} ${y + h / 2} L${x - w / 2} ${y + h / 4} Z`
      : `M${x - w / 2} ${y - h / 2} L${x + w / 2} ${y - h / 4} L${x + w / 2} ${y + h / 4} L${x - w / 2} ${y + h / 2} Z`,
    c,
    w: 1.8,
    fill: "var(--s-panel2)",
  },
  Tx(`${id}l`, x, y + 3, label, { size: 8.5, mono: true }),
];

// Цифровая диаграмма: vals — уровни по слотам (0/1), x — начало, y — линия нуля, h — высота единицы.
export const wave = (
  id: string,
  vals: (number | boolean)[],
  { x = 30, y = 40, slot = 26, h = 16, c = "b", w = 2, o }: { x?: number; y?: number; slot?: number; h?: number; c?: string; w?: number; o?: number } = {},
): SceneItem => {
  let d = "";
  let prev: number | boolean | null = null;
  vals.forEach((v, i) => {
    const yy = v ? y - h : y;
    const x0 = x + i * slot;
    d += i === 0 ? `M${x0} ${yy}` : v !== prev ? ` V${yy}` : "";
    d += ` H${x0 + slot}`;
    prev = v;
  });
  return { t: "path", id, d, c, w, o };
};
