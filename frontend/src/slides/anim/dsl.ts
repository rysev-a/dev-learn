/* Базовые конструкторы элементов покадровой схемы (alg.tsx). Все пакеты помощников —
   hw, lx, rs, cl, jv, db, ad — строятся на них; сцены не определяют их заново. */

/** Цвет элемента: m g y r b v — приглушённый, зелёный, жёлтый, красный, синий, фиолетовый;
    K, R — «чёрный» и «красный» узлы дерева; W — светлая заливка; n — только рамка. */
export type Tone = "m" | "g" | "y" | "r" | "b" | "v" | "K" | "R" | "W" | "n";

export type ItemKind =
  | "cell"
  | "dot"
  | "lnode"
  | "text"
  | "ptr"
  | "line"
  | "box"
  | "path"
  | "bar"
  | "code"
  | "gate"
  | "tr"
  | "sw"
  | "lamp";

export type CodeLang = "rs" | "c" | "asm" | "py" | "sql" | "js" | "css";

/** Один элемент кадра. Набор полей зависит от `t` (см. описание в alg.tsx); один и тот же `id`
    в соседних кадрах — один и тот же объект на экране. */
export interface SceneItem {
  t: ItemKind;
  id: string;
  x?: number;
  y?: number;
  x1?: number;
  y1?: number;
  x2?: number;
  y2?: number;
  w?: number;
  h?: number;
  r?: number;
  /** высота столбика (bar) */
  hh?: number;
  max?: number;
  c?: Tone | string;
  text?: string | number;
  sub?: string | number;
  lbl?: string;
  d?: string;
  /** true — пунктир по умолчанию, строка — свой dasharray */
  dash?: boolean | string | number;
  size?: number;
  subSize?: number;
  mono?: boolean;
  bold?: boolean;
  anchor?: "start" | "middle" | "end";
  dir?: string;
  nil?: boolean;
  bend?: number;
  arrow?: boolean;
  draw?: number;
  fill?: string;
  fillOpacity?: number;
  /** code: строки, подсвеченные и ошибочные номера */
  lines?: string[];
  hl?: number | number[];
  bad?: number | number[];
  lh?: number;
  lang?: CodeLang;
  /** прозрачность и масштаб любого элемента */
  o?: number;
  s?: number;
  /** gate: тип вентиля; sw/tr/lamp: состояние */
  g?: string;
  kind?: string;
  on?: boolean | number;
  tc?: string;
}

/** Необязательные поля поверх обязательных аргументов конструктора. */
export type Extra = Partial<SceneItem>;

export const Tx = (id: string, x: number, y: number, text: string | number, extra: Extra = {}): SceneItem => ({
  t: "text",
  id,
  x,
  y,
  text,
  ...extra,
});

export const cell = (id: string, x: number, y: number, text: string | number, c: Tone | string = "m", extra: Extra = {}): SceneItem => ({
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

export const box = (id: string, x: number, y: number, w: number, h: number, c: Tone | string = "n", lbl?: string): SceneItem => ({
  t: "box",
  id,
  x,
  y,
  w,
  h,
  c,
  lbl,
});

// Ячейка заданного размера с подписью по центру
export const Box = (id: string, x: number, y: number, w: number, h: number, text: string | number, c: Tone | string = "m", extra: Extra = {}) =>
  cell(id, x, y, text, c, { w, h, size: 9.5, ...extra });

export const line = (id: string, x1: number, y1: number, x2: number, y2: number, c: Tone | string = "m", extra: Extra = {}): SceneItem => ({
  t: "line",
  id,
  x1,
  y1,
  x2,
  y2,
  c,
  ...extra,
});

export const arrow = (id: string, x1: number, y1: number, x2: number, y2: number, c: Tone | string = "m", extra: Extra = {}) =>
  line(id, x1, y1, x2, y2, c, { arrow: true, ...extra });

// Конструктор врезки кода на языке lang: lines — строки, hl — подсвеченные, bad — ошибочные (красные)
export const codeIn =
  (lang: CodeLang) =>
  (id: string, x: number, y: number, lines: string[], hl?: number | number[], extra: Extra = {}): SceneItem => ({
    t: "code",
    id,
    x,
    y,
    lines,
    hl,
    lang,
    size: 9.5,
    lh: 13,
    w: 200,
    ...extra,
  });
