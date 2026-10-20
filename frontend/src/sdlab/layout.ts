import { KINDS } from "./kinds.ts";
import type { SdNode, SdState } from "./types.ts";

/* Раскладка схемы по колонкам слева направо: пользователи → CDN → шлюзы → серверы → кэш/очередь → хранилища.
   Окно просмотра — BOARD_W × BOARD_H единиц (по нему считается масштаб), сама схема шире: колонки стоят через 150,
   а при открытии поле «вписывает» схему в окно (Board.fit). */

export const BOARD_W = 780;
export const BOARD_H = 560;
const LAYOUT_H = 470;
const COL_STEP = 150;
const COL_X = Array.from({ length: 8 }, (_, i) => 70 + i * COL_STEP);

export function place(state: SdState): SdState {
  const byCol = new Map<number, SdNode[]>();
  for (const n of state.nodes) {
    const c = KINDS[n.kind].col;
    byCol.set(c, [...(byCol.get(c) ?? []), n]);
  }
  const nodes = state.nodes.map((n) => {
    if (n.x >= 0 && n.y >= 0) return n;
    const col = KINDS[n.kind].col;
    const list = byCol.get(col) ?? [n];
    const i = list.indexOf(n);
    const step = LAYOUT_H / (list.length + 1);
    return { ...n, x: COL_X[col] ?? 70, y: Math.round(step * (i + 1)) };
  });
  return { ...state, nodes };
}

export function nextY(state: SdState, col: number): number {
  const ys = state.nodes.filter((n) => KINDS[n.kind].col === col).map((n) => n.y);
  return ys.length ? Math.max(...ys) + 80 : LAYOUT_H / 2;
}

export const colX = (col: number) => COL_X[col] ?? 70;
