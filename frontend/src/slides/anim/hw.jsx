import { gp } from "./alg.jsx";

/* Помощники для сцен по цифровой схемотехнике (книга «Архитектура компьютера»):
   уровень сигнала → цвет, элементы схем и ломаные провода. Элементы рисует alg.jsx (gate, tr, sw, lamp). */

export { gp };
export const Tx = (id, x, y, text, extra = {}) => ({
  t: "text",
  id,
  x,
  y,
  text,
  ...extra,
});
export const lv = (b) => (b ? "g" : "m"); // 1 — зелёный, 0 — приглушённый
export const bit = (id, x, y, v, extra = {}) => ({
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
export const GT = (id, g, x, y, extra = {}) => ({
  t: "gate",
  id,
  g,
  x,
  y,
  ...extra,
});
// Ломаная по точкам [[x,y],…]
export const pl = (id, pts, c = "m", extra = {}) => ({
  t: "path",
  id,
  d: pts.map(([x, y], i) => `${i ? "L" : "M"}${x} ${y}`).join(" "),
  c,
  w: 1.8,
  ...extra,
});
// Провод между точками a и b с изломом на x = xm
export const wr = (id, a, b, c = "m", xm, extra = {}) => {
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

// Трапеция мультиплексора (широкая сторона слева) и демультиплексора (rev — широкая справа). Возвращает [контур, подпись].
export const mux = (id, x, y, w, h, c = "b", label = "MUX", rev = false) => [
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
  id,
  vals,
  { x = 30, y = 40, slot = 26, h = 16, c = "b", w = 2, o } = {},
) => {
  let d = "";
  let prev = null;
  vals.forEach((v, i) => {
    const yy = v ? y - h : y;
    const x0 = x + i * slot;
    d += i === 0 ? `M${x0} ${yy}` : v !== prev ? ` V${yy}` : "";
    d += ` H${x0 + slot}`;
    prev = v;
  });
  return { t: "path", id, d, c, w, o };
};
