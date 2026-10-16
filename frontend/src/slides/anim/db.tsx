import { cell, codeIn, type SceneItem } from "./dsl.ts";
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
    const w = widths[j];
    items.push(
      cell(`${id}-h${j}`, cx + w / 2, y, h, "y", { w: w - 2, h: ch, size }),
    );
    cx += w;
  });
  rows.forEach((r, i) => {
    let px = x;
    r.forEach((v, j) => {
      const w = widths[j];
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
