/* Общие помощники сцен глав 8, 9, 14 и 17 книги «Алгоритмы и структуры данных». Всё поверх alg.jsx. */

export const Tx = (id, x, y, text, extra = {}) => ({
  t: "text",
  id,
  x,
  y,
  text,
  ...extra,
});

// Список «слева моно — справа пояснение»; on — номер или список подсвеченных строк.
export const LIST = (items, on, { w = 334, rowH = 34, y0 = 28 } = {}) => {
  const hot = new Set(Array.isArray(on) ? on : [on]);
  return items.flatMap(([a, b], i) => [
    {
      t: "box",
      id: `b${i}`,
      x: 180,
      y: y0 + i * rowH,
      w,
      h: rowH - 6,
      c: hot.has(i) ? "g" : "n",
    },
    Tx(`a${i}`, 24, y0 + 4 + i * rowH, a, {
      mono: true,
      size: 9.5,
      anchor: "start",
      c: hot.has(i) ? "g" : undefined,
    }),
    Tx(`d${i}`, 340, y0 + 4 + i * rowH, b, {
      size: 8.5,
      anchor: "end",
      o: hot.has(i) ? 1 : 0.5,
    }),
  ]);
};

// Рамка вокруг клеток ряда: от индекса a до b (включительно), центры x0 + cw·i.
export const span = (id, x0, cw, a, b, y, { c = "g", h = 34, dash } = {}) => ({
  t: "box",
  id,
  x: x0 + (cw * (a + b)) / 2,
  y,
  w: cw * (b - a + 1) - 1,
  h,
  c,
  dash,
});
