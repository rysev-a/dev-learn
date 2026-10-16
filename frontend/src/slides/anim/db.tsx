import { Box, Tx, cell, codeIn, type SceneItem } from "./dsl.ts";
export { Box, arrow, slot } from "./rs.tsx";

/* Помощники для сцен книги «Базы данных»: SQL с подсветкой и таблицы из ячеек. */

// Код SQL: lines — строки, hl — подсвеченные, bad — ошибочные (красные)
export const sql = codeIn("sql");

/**
 * Таблица из ячеек: head — заголовки, rows — строки значений, (x, y) — левый верхний угол,
 * widths — ширины колонок, hot — множество номеров выделенных строк (0 — первая строка данных),
 * colors — цвет строки по номеру. Возвращает список элементов сцены с устойчивыми id.
 */
export const tbl = (
  id: string,
  x: number,
  y: number,
  head: readonly (string | number)[],
  rows: readonly (readonly (string | number)[])[],
  widths: readonly number[],
  {
    hot = [],
    c = "b",
    cell: ch = 18,
    size = 8.5,
    dim = [],
  }: { hot?: number[]; c?: string; cell?: number; size?: number; dim?: number[] } = {},
): SceneItem[] => {
  const items: SceneItem[] = [];
  let cx = x;
  head.forEach((h, j) => {
    const w = widths[j]!;
    items.push(
      cell(`${id}-h${j}`, cx + w / 2, y, h, "y", { w: w - 2, h: ch, size }),
    );
    cx += w;
  });
  rows.forEach((r, i) => {
    let px = x;
    r.forEach((v, j) => {
      const w = widths[j]!;
      items.push(
        cell(
          `${id}-r${i}c${j}`,
          px + w / 2,
          y + (i + 1) * (ch + 2),
          String(v),
          hot.includes(i) ? "g" : c,
          {
            w: w - 2,
            h: ch,
            size,
            o: dim.includes(i) ? 0.35 : 1,
          },
        ),
      );
      px += w;
    });
  });
  return items;
};

// Узел схемы и малая метка
export const nd = (id: string, x: number, y: number, text: string, c = "b", w = 66): SceneItem => Box(id, x, y, w, 28, text, c, { size: 9 });
export const sm = (id: string, x: number, y: number, text: string, c = "b", w = 40): SceneItem => Box(id, x, y, w, 20, text, c, { size: 8 });

// Дорожка (временная шкала) с названием слева и событие на ней
export const lane = (id: string, y: number, name: string): SceneItem[] => [
  { t: "line", id: `${id}l`, x1: 46, y1: y, x2: 346, y2: y, c: "m", w: 1.2 },
  Tx(`${id}n`, 20, y, name, { size: 9, mono: true }),
];
export const ev = (id: string, x: number, y: number, text: string, c = "b", w = 56): SceneItem => Box(id, x, y, w, 22, text, c, { size: 8 });
