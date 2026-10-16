import type { ReactNode } from "react";
import type { SceneItem, ItemKind } from "./dsl.ts";
import { G, Steps, useSteps, type StepsCtl } from "./kit.tsx";

/* Покадровые схемы для книги «Алгоритмы и структуры данных».

   Сцена задаётся данными: frames[k] — список элементов, видимых на шаге k.
   У элемента есть id; один и тот же id в соседних кадрах — это один и тот же
   объект на экране: он плавно переезжает, меняет цвет, исчезает (если в кадре
   его нет) — всё делают CSS-переходы (.a-t). Время шагов берётся из голоса
   (useSteps), как и в остальных анимациях.

   Элементы (x, y — центр; цвета m g y r b v — приглушённый, зелёный, жёлтый,
   красный, синий, фиолетовый; K и R — «чёрный» и «красный» узлы дерева):
     cell  {x,y,w,h,text,c,sub,dash}     клетка массива / значение
     dot   {x,y,r,text,c}                круглый узел
     lnode {x,y,w,h,text,c,nil}          узел списка: значение | ссылка
     text  {x,y,text,c,size,mono,anchor} подпись (\n — перенос строки)
     ptr   {x,y,text,c,dir}              указатель: стрелка к точке (x,y) + имя
     line  {x1,y1,x2,y2,c,arrow,dash,bend,w}  линия/стрелка (двигается плавно)
     box   {x,y,w,h,c,dash,lbl}          рамка-область
     path  {d,c,w,draw,dash,fill}        кривая; draw 0…1 — «прорисовка»
     bar   {x,y,w,hh,c,max}              столбик высотой hh (y — основание)
     code  {x,y,lines,hl,size,lh,w}      строки кода, hl — подсвеченные номера
   Любой элемент: o — прозрачность, s — масштаб. */

const COL: Record<string, string> = {
  m: "var(--s-muted)",
  g: "var(--s-accent)",
  y: "var(--s-amber)",
  r: "var(--s-red)",
  b: "var(--s-blue)",
  v: "var(--s-violet)",
};

interface ToneStyle {
  fill: string;
  fo: number;
  stroke: string;
  text: string;
}

function tone(c: string = "m"): ToneStyle {
  if (c === "K")
    return {
      fill: "var(--s-ink)",
      fo: 1,
      stroke: "var(--s-text)",
      text: "var(--s-onink)",
    };
  if (c === "R")
    return {
      fill: "var(--s-red)",
      fo: 0.92,
      stroke: "var(--s-red)",
      text: "var(--s-bg)",
    };
  if (c === "m")
    return {
      fill: "var(--s-panel2)",
      fo: 1,
      stroke: "var(--s-border)",
      text: "var(--s-text)",
    };
  if (c === "W")
    return {
      fill: "var(--s-border)",
      fo: 1,
      stroke: "var(--s-border)",
      text: "var(--s-text)",
    };
  if (c === "n")
    return {
      fill: "none",
      fo: 0,
      stroke: "var(--s-border)",
      text: "var(--s-text)",
    };
  const col = COL[c] ?? "var(--s-muted)";
  return { fill: col, fo: 0.28, stroke: col, text: "var(--s-text)" };
}

const GATE_BODY: Record<string, string> = {
  and: "M-14 -11 H2 A12 11 0 0 1 2 11 H-14 Z",
  nand: "M-14 -11 H2 A12 11 0 0 1 2 11 H-14 Z",
  or: "M-14 -11 Q4 -11 14 0 Q4 11 -14 11 Q-8 0 -14 -11 Z",
  nor: "M-14 -11 Q4 -11 14 0 Q4 11 -14 11 Q-8 0 -14 -11 Z",
  xor: "M-14 -11 Q4 -11 14 0 Q4 11 -14 11 Q-8 0 -14 -11 Z",
  xnor: "M-14 -11 Q4 -11 14 0 Q4 11 -14 11 Q-8 0 -14 -11 Z",
  not: "M-12 -10 L8 0 L-12 10 Z",
  buf: "M-12 -10 L12 0 L-12 10 Z",
};

/* Контакты элемента для проводов: a, b — входы (у НЕ один — a), y — выход.
   g — {x, y, s} элемента `gate`. */
export interface Pt {
  x: number;
  y: number;
}

export function gp(g: { x: number; y: number; s?: number; g?: string }, pin: string): Pt {
  const s = g.s ?? 1;
  const one = g.g === "not" || g.g === "buf";
  if (pin === "y") return { x: g.x + 22 * s, y: g.y };
  if (one) return { x: g.x - 22 * s, y: g.y };
  return { x: g.x - 22 * s, y: g.y + (pin === "a" ? -6 : 6) * s };
}

// Провод с изломом: ломаная (x1,y1) → (xm,y1) → (xm,y2) → (x2,y2); c — цвет, o — прозрачность.
export function wire(
  id: string,
  a: Pt,
  b: Pt,
  { c = "m", xm, w = 1.8, o = 1, dash }: { c?: string; xm?: number; w?: number; o?: number; dash?: SceneItem["dash"] } = {},
): SceneItem {
  const mid = xm ?? (a.x + b.x) / 2;
  const d =
    a.y === b.y
      ? `M${a.x} ${a.y} H${b.x}`
      : `M${a.x} ${a.y} H${mid} V${b.y} H${b.x}`;
  return { t: "path", id, d, c, w, o, dash };
}

/* Подсветка Rust в элементе code (lang: "rs"): цвета только из --s-*. */
const RS_KW = new Set([
  "fn",
  "let",
  "mut",
  "pub",
  "struct",
  "enum",
  "impl",
  "match",
  "if",
  "else",
  "for",
  "while",
  "loop",
  "return",
  "use",
  "mod",
  "self",
  "Self",
  "move",
  "const",
  "static",
  "type",
  "where",
  "async",
  "await",
  "unsafe",
  "trait",
  "dyn",
  "in",
  "as",
  "break",
  "continue",
  "ref",
]);
const RS_TY = new Set([
  "i8",
  "i16",
  "i32",
  "i64",
  "i128",
  "isize",
  "u8",
  "u16",
  "u32",
  "u64",
  "u128",
  "usize",
  "f32",
  "f64",
  "bool",
  "char",
  "str",
  "String",
  "Vec",
  "Option",
  "Result",
  "Box",
  "Rc",
  "Arc",
  "RefCell",
  "HashMap",
  "Some",
  "None",
  "Ok",
  "Err",
]);
function rsTokens(src: string): ReactNode[] {
  const out: ReactNode[] = [];
  const re =
    /(\/\/[^\n]*)|("(?:[^"\\]|\\.)*")|('\w+\b)|(\b\d[\d_]*(?:\.\d+)?\b)|([A-Za-z_]\w*!)|([A-Za-z_]\w*)|(\s+|.)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, life, num, mac, word] = m;
    let fill: string | undefined;
    if (com) fill = "var(--s-muted)";
    else if (str) fill = "var(--s-amber)";
    else if (life) fill = "var(--s-violet)";
    else if (num) fill = "var(--s-red)";
    else if (mac) fill = "var(--s-accent)";
    else if (word)
      fill = RS_KW.has(word)
        ? "var(--s-blue)"
        : RS_TY.has(word) || /^[A-Z]/.test(word)
          ? "var(--s-violet)"
          : undefined;
    out.push(
      fill ? (
        <tspan key={out.length} style={{ fill }}>
          {tok}
        </tspan>
      ) : (
        tok
      ),
    );
  }
  return out;
}

/* Подсветка C (lang: "c") и ассемблера RISC-V (lang: "asm"). */
const C_KW = new Set(
  "if else for while do switch case default break continue return goto sizeof typedef struct union enum static const volatile extern register inline restrict".split(
    " ",
  ),
);
const C_TY = new Set(
  "int char short long float double void unsigned signed size_t ssize_t ptrdiff_t bool FILE NULL true false uint8_t uint16_t uint32_t uint64_t int8_t int16_t int32_t int64_t uintptr_t".split(
    " ",
  ),
);
function cTokens(src: string): ReactNode[] {
  const out: ReactNode[] = [];
  const re =
    /(\/\/[^\n]*|\/\*.*?\*\/)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)')|(^\s*#\s*\w+)|(\b(?:0x[0-9a-fA-F]+|\d+)[uUlL]*\b)|([A-Za-z_]\w*)|(\s+|.)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, pre, num, word] = m;
    let fill: string | undefined;
    if (com) fill = "var(--s-muted)";
    else if (str) fill = "var(--s-amber)";
    else if (pre) fill = "var(--s-accent)";
    else if (num) fill = "var(--s-red)";
    else if (word)
      fill = C_KW.has(word)
        ? "var(--s-blue)"
        : C_TY.has(word) || /_t$/.test(word)
          ? "var(--s-violet)"
          : undefined;
    out.push(
      fill ? (
        <tspan key={out.length} style={{ fill }}>
          {tok}
        </tspan>
      ) : (
        tok
      ),
    );
  }
  return out;
}
const ASM_REG = /^(zero|ra|sp|gp|tp|fp|[xfa]\d+|t[0-6]|s(?:\d|1[01])|pc)$/;
function asmTokens(src: string): ReactNode[] {
  const out: ReactNode[] = [];
  const re =
    /(#[^\n]*)|(^\s*[.\w$]+:)|(-?\b(?:0x[0-9a-fA-F]+|\d+)\b)|([A-Za-z_.][\w.]*)|(\s+|.)/g;
  let m: RegExpExecArray | null;
  let first = true;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, label, num, word] = m;
    let fill: string | undefined;
    if (com) fill = "var(--s-muted)";
    else if (label) fill = "var(--s-accent)";
    else if (num) fill = "var(--s-red)";
    else if (word) {
      if (ASM_REG.test(word)) fill = "var(--s-violet)";
      else if (first && !label) fill = "var(--s-blue)";
      else if (word.startsWith(".")) fill = "var(--s-accent)";
    }
    if (word || label) first = false;
    out.push(
      fill ? (
        <tspan key={out.length} style={{ fill }}>
          {tok}
        </tspan>
      ) : (
        tok
      ),
    );
  }
  return out;
}

/* Подсветка Python (lang: "py"). */
const PY_KW = new Set(
  "def class if elif else for while in not and or return import from as with try except finally raise lambda yield pass break continue None True False is del global async await".split(
    " ",
  ),
);
const PY_BI = new Set(
  "print len range int str float bool list dict set tuple type input sum max min sorted enumerate zip open abs round self isinstance".split(
    " ",
  ),
);
function pyTokens(src: string): ReactNode[] {
  const out: ReactNode[] = [];
  const re =
    /(#[^\n]*)|([fFrRbB]?"(?:[^"\\]|\\.)*"|[fFrRbB]?'(?:[^'\\]|\\.)*')|(\b\d[\d_]*(?:\.\d+)?\b)|([A-Za-z_]\w*)|(\s+|.)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, num, word] = m;
    let fill: string | undefined;
    if (com) fill = "var(--s-muted)";
    else if (str) fill = "var(--s-amber)";
    else if (num) fill = "var(--s-red)";
    else if (word)
      fill = PY_KW.has(word)
        ? "var(--s-blue)"
        : PY_BI.has(word)
          ? "var(--s-violet)"
          : src[re.lastIndex] === "("
            ? "var(--s-accent)"
            : undefined;
    out.push(
      fill ? (
        <tspan key={out.length} style={{ fill }}>
          {tok}
        </tspan>
      ) : (
        tok
      ),
    );
  }
  return out;
}

/* Подсветка SQL (lang: "sql"). */
const SQL_KW = new Set(
  "select from where group by having order limit offset join inner left right full outer cross on using as and or not in is null like between exists case when then else end union all distinct insert into values update set delete create table index primary key foreign references unique check default begin commit rollback with recursive over partition returning asc desc explain analyze view alter add drop column constraint if true false cascade".split(
    " ",
  ),
);
const SQL_FN = new Set(
  "count sum avg min max coalesce nullif round length lower upper substr row_number rank dense_rank lag lead now date strftime cast".split(
    " ",
  ),
);
function sqlTokens(src: string): ReactNode[] {
  const out: ReactNode[] = [];
  const re =
    /(--[^\n]*)|('(?:[^']|'')*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)|(\s+|.)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, num, word] = m;
    let fill: string | undefined;
    if (com) fill = "var(--s-muted)";
    else if (str) fill = "var(--s-amber)";
    else if (num) fill = "var(--s-red)";
    else if (word) {
      const w = word.toLowerCase();
      fill = SQL_KW.has(w)
        ? "var(--s-blue)"
        : SQL_FN.has(w)
          ? "var(--s-violet)"
          : undefined;
    }
    out.push(
      fill ? (
        <tspan key={out.length} style={{ fill }}>
          {tok}
        </tspan>
      ) : (
        tok
      ),
    );
  }
  return out;
}

/* Подсветка JavaScript (lang: "js"): цвета только из --s-*. */
const JS_KW = new Set(
  "const let var function return if else for while do switch case default break continue new class extends super this typeof instanceof in of import export from async await try catch finally throw yield static get set delete void".split(
    " ",
  ),
);
const JS_LIT = new Set([
  "true",
  "false",
  "null",
  "undefined",
  "NaN",
  "Infinity",
]);
function jsTokens(src: string): ReactNode[] {
  const out: ReactNode[] = [];
  const re =
    /(\/\/[^\n]*)|(`(?:[^`\\]|\\.)*`|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b\d[\d_]*(?:\.\d+)?n?\b)|([A-Za-z_$][\w$]*)|(=>)|(\s+|.)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, num, word, arrow] = m;
    let fill: string | undefined;
    if (com) fill = "var(--s-muted)";
    else if (str) fill = "var(--s-amber)";
    else if (num) fill = "var(--s-red)";
    else if (arrow) fill = "var(--s-accent)";
    else if (word)
      fill = JS_KW.has(word)
        ? "var(--s-blue)"
        : JS_LIT.has(word)
          ? "var(--s-red)"
          : /^[A-Z]/.test(word)
            ? "var(--s-violet)"
            : undefined;
    out.push(
      fill ? (
        <tspan key={out.length} style={{ fill }}>
          {tok}
        </tspan>
      ) : (
        tok
      ),
    );
  }
  return out;
}

// Подсветка CSS: комментарии, строки, числа с единицами, #цвета, --переменные, @правила, имена свойств
function cssTokens(src: string): ReactNode[] {
  const out: ReactNode[] = [];
  const re =
    /(\/\*.*?\*\/|\/\/[^\n]*)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(#[0-9a-fA-F]{3,8}\b|-?\d*\.?\d+(?:px|rem|em|%|vh|vw|dvh|fr|s|ms|deg|ch)?)|(--[\w-]+)|(@[\w-]+)|([A-Za-z_-][\w-]*)(?=\s*:(?!:))|(\s+|.)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, num, cv, at, prop] = m;
    let fill: string | undefined;
    if (com) fill = "var(--s-muted)";
    else if (str) fill = "var(--s-amber)";
    else if (num) fill = "var(--s-red)";
    else if (cv) fill = "var(--s-violet)";
    else if (at) fill = "var(--s-accent)";
    else if (prop) fill = "var(--s-blue)";
    out.push(
      fill ? (
        <tspan key={out.length} style={{ fill }}>
          {tok}
        </tspan>
      ) : (
        tok
      ),
    );
  }
  return out;
}

// dash: true — пунктир по умолчанию, строка или число — свой штрих
const dashOf = (d: SceneItem["dash"]) => (typeof d === "boolean" ? (d ? "3 3" : undefined) : d);

const ARROW_OK = new Set(["m", "g", "y", "r", "b"]);
const arrowId = (c: string) => `url(#a-hd-${ARROW_OK.has(c) ? c : "m"})`;

function Lines({ text, anchor = "middle", lh = 1.25 }: { text: string | number; anchor?: "start" | "middle" | "end"; lh?: number }) {
  const parts = String(text).split("\n");
  if (parts.length === 1) return <>{text}</>;
  return parts.map((p, i) => (
    <tspan
      key={i}
      x="0"
      dy={i === 0 ? `${-((parts.length - 1) * lh * 0.5)}em` : `${lh}em`}
      textAnchor={anchor}
    >
      {p}
    </tspan>
  ));
}

function Item({ it }: { it: SceneItem }) {
  const { t, o = 1, s = 1 } = it;
  if (t === "cell") {
    const w = it.w ?? 30;
    const h = it.h ?? 26;
    const k = tone(it.c);
    const size = it.size ?? 11;
    return (
      <G x={it.x} y={it.y} o={o} s={s}>
        <rect
          x={-w / 2}
          y={-h / 2}
          width={w}
          height={h}
          rx="5"
          style={{
            fill: k.fill,
            fillOpacity: k.fo,
            stroke: k.stroke,
            strokeWidth: 1.5,
            strokeDasharray: it.dash ? "3 3" : undefined,
          }}
        />
        <text
          y={size * 0.36}
          textAnchor="middle"
          className="a-mono"
          style={{ fill: it.tc ?? k.text, fontSize: size }}
        >
          <Lines text={it.text ?? ""} />
        </text>
        {it.sub != null && (
          <text
            y={h / 2 + 10}
            textAnchor="middle"
            className="a-cap"
            style={{ fontSize: it.subSize ?? 8.5 }}
          >
            {it.sub}
          </text>
        )}
      </G>
    );
  }
  if (t === "dot") {
    const r = it.r ?? 12;
    const k = tone(it.c);
    const size = it.size ?? 10.5;
    return (
      <G x={it.x} y={it.y} o={o} s={s}>
        <circle
          r={r}
          style={{
            fill: k.fill,
            fillOpacity: k.fo,
            stroke: k.stroke,
            strokeWidth: 1.7,
            strokeDasharray: it.dash ? "3 3" : undefined,
          }}
        />
        <text
          y={size * 0.36}
          textAnchor="middle"
          className="a-mono"
          style={{ fill: it.tc ?? k.text, fontSize: size }}
        >
          {it.text}
        </text>
        {it.sub != null && (
          <text
            y={r + 10}
            textAnchor="middle"
            className="a-cap"
            style={{ fontSize: 8.5 }}
          >
            {it.sub}
          </text>
        )}
      </G>
    );
  }
  if (t === "lnode") {
    const w = it.w ?? 46;
    const h = it.h ?? 24;
    const k = tone(it.c);
    return (
      <G x={it.x} y={it.y} o={o} s={s}>
        <rect
          x={-w / 2}
          y={-h / 2}
          width={w}
          height={h}
          rx="5"
          style={{
            fill: k.fill,
            fillOpacity: k.fo,
            stroke: k.stroke,
            strokeWidth: 1.5,
          }}
        />
        <line
          x1={w / 2 - 14}
          y1={-h / 2}
          x2={w / 2 - 14}
          y2={h / 2}
          style={{ stroke: k.stroke, strokeWidth: 1.2 }}
        />
        <text
          x={-7}
          y="3.8"
          textAnchor="middle"
          className="a-mono"
          style={{ fill: k.text, fontSize: it.size ?? 11 }}
        >
          {it.text}
        </text>
        {it.nil ? (
          <path
            d={`M${w / 2 - 11} ${h / 2 - 5} L${w / 2 - 3} ${-h / 2 + 5}`}
            style={{ stroke: "var(--s-muted)", strokeWidth: 1.3 }}
          />
        ) : (
          <circle
            cx={w / 2 - 7}
            cy="0"
            r="2.4"
            style={{ fill: "var(--s-accent)" }}
          />
        )}
        {it.sub != null && (
          <text
            y={h / 2 + 10}
            textAnchor="middle"
            className="a-cap"
            style={{ fontSize: 8.5 }}
          >
            {it.sub}
          </text>
        )}
      </G>
    );
  }
  if (t === "text") {
    const size = it.size ?? 10;
    return (
      <G x={it.x} y={it.y} o={o} s={s}>
        <text
          textAnchor={it.anchor ?? "middle"}
          className={it.mono ? "a-mono" : "a-cap"}
          style={{
            fill: it.c
              ? (COL[it.c] ?? it.c)
              : it.mono
                ? undefined
                : "var(--s-muted)",
            fontSize: size,
            fontWeight: it.bold ? 600 : undefined,
          }}
        >
          <Lines text={it.text ?? ""} anchor={it.anchor ?? "middle"} />
        </text>
      </G>
    );
  }
  if (t === "ptr") {
    const down = (it.dir ?? "down") === "down";
    const col = COL[it.c ?? "g"] ?? COL["g"];
    const c = it.c ?? "g";
    return (
      <G x={it.x} y={it.y} o={o} s={s}>
        <line
          x1="0"
          y1={down ? -17 : 17}
          x2="0"
          y2={down ? -2 : 2}
          markerEnd={arrowId(c)}
          style={{ stroke: col, strokeWidth: 1.6 }}
        />
        <text
          y={down ? -21 : 27}
          textAnchor="middle"
          className="a-mono"
          style={{ fill: col, fontSize: it.size ?? 9.5, fontWeight: 600 }}
        >
          {it.text}
        </text>
      </G>
    );
  }
  if (t === "line") {
    const { x1 = 0, y1 = 0, x2 = 0, y2 = 0 } = it;
    const bend = it.bend ?? 0;
    let d = `M${x1} ${y1} L${x2} ${y2}`;
    if (bend) {
      const mx = (x1 + x2) / 2;
      const my = (y1 + y2) / 2;
      const dx = x2 - x1;
      const dy = y2 - y1;
      const n = Math.hypot(dx, dy) || 1;
      d = `M${x1} ${y1} Q${mx - (dy / n) * bend} ${my + (dx / n) * bend} ${x2} ${y2}`;
    }
    const c = it.c ?? "m";
    return (
      <path
        className="a-t"
        d={d}
        markerEnd={it.arrow ? arrowId(c) : undefined}
        style={{
          d: `path("${d}")`,
          fill: "none",
          stroke: COL[c] ?? "var(--s-border)",
          strokeWidth: it.w ?? 1.6,
          strokeDasharray: dashOf(it.dash),
          opacity: o,
        }}
      />
    );
  }
  if (t === "box") {
    const w = it.w ?? 100;
    const h = it.h ?? 40;
    const k = tone(it.c ?? "n");
    return (
      <G x={it.x} y={it.y} o={o} s={s}>
        <rect
          x={-w / 2}
          y={-h / 2}
          width={w}
          height={h}
          rx="8"
          style={{
            fill: k.fill,
            fillOpacity: k.fo,
            stroke: it.c && it.c !== "n" ? k.stroke : "var(--s-border)",
            strokeWidth: 1.3,
            strokeDasharray: it.dash ? "4 3" : undefined,
          }}
        />
        {it.lbl != null && (
          <text
            x={-w / 2 + 6}
            y={-h / 2 - 4}
            className="a-cap"
            style={{ fontSize: 8.5 }}
          >
            {it.lbl}
          </text>
        )}
      </G>
    );
  }
  if (t === "path") {
    const c = it.c ?? "g";
    const drawn = it.draw != null;
    return (
      <path
        className="a-t"
        d={it.d}
        pathLength={drawn ? 1 : undefined}
        style={{
          fill: it.fill ?? "none",
          fillOpacity: it.fillOpacity,
          stroke: COL[c] ?? c,
          strokeWidth: it.w ?? 2,
          strokeDasharray: drawn ? "1 1" : dashOf(it.dash),
          strokeDashoffset: drawn ? 1 - (it.draw ?? 0) : 0,
          opacity: o,
        }}
      />
    );
  }
  if (t === "bar") {
    const w = it.w ?? 16;
    const k = tone(it.c);
    const max = it.max ?? 100;
    const hh = Math.max(0.5, Math.min(it.hh ?? 0, max));
    return (
      <G x={it.x} y={it.y} o={o}>
        <g
          className="a-t"
          style={{
            transform: `scaleY(${hh / max})`,
            transformOrigin: "50% 100%",
            transformBox: "fill-box",
          }}
        >
          <rect
            x={-w / 2}
            y={-max}
            width={w}
            height={max}
            rx="3"
            style={{
              fill: k.fill,
              fillOpacity: k.fo === 1 ? 1 : 0.35,
              stroke: k.stroke,
              strokeWidth: 1.3,
            }}
          />
        </g>
        {it.text != null && (
          <text
            y="11"
            textAnchor="middle"
            className="a-mono"
            style={{ fontSize: 9.5 }}
          >
            {it.text}
          </text>
        )}
      </G>
    );
  }
  if (t === "code") {
    const lh = it.lh ?? 13;
    const size = it.size ?? 9.5;
    const w = it.w ?? 150;
    const set = (v: number | number[] | undefined) => new Set(Array.isArray(v) ? v : v == null ? [] : [v]);
    const hl = set(it.hl);
    const bad = set(it.bad);
    return (
      <G x={it.x} y={it.y} o={o}>
        {(it.lines ?? []).map((l, i) => (
          <g key={i}>
            <rect
              className="a-t"
              x="-4"
              y={i * lh - lh * 0.78}
              width={w}
              height={lh}
              rx="3"
              style={{
                fill: bad.has(i) ? "var(--s-red)" : "var(--s-accent)",
                fillOpacity: bad.has(i) ? 0.22 : hl.has(i) ? 0.2 : 0,
              }}
            />
            <text
              y={i * lh}
              className="a-mono"
              style={{
                fontSize: size,
                whiteSpace: "pre",
                fill:
                  hl.has(i) || bad.has(i) ? "var(--s-text)" : "var(--s-muted)",
              }}
              xmlSpace="preserve"
            >
              {it.lang === "rs"
                ? rsTokens(l)
                : it.lang === "c"
                  ? cTokens(l)
                  : it.lang === "asm"
                    ? asmTokens(l)
                    : it.lang === "py"
                      ? pyTokens(l)
                      : it.lang === "sql"
                        ? sqlTokens(l)
                        : it.lang === "js"
                          ? jsTokens(l)
                          : it.lang === "css"
                            ? cssTokens(l)
                            : l}
            </text>
          </g>
        ))}
      </G>
    );
  }
  if (t === "gate") {
    const k = tone(it.c);
    const type = it.g ?? "and";
    const one = type === "not" || type === "buf";
    const bubble = type === "nand" || type === "nor" || type === "xnor";
    const bodyX = type === "not" ? 11 : 17;
    const stroke = { stroke: k.stroke, strokeWidth: 1.7, fill: "none" };
    return (
      <G x={it.x} y={it.y} o={o} s={s}>
        <path
          d={GATE_BODY[type]}
          style={{ ...stroke, fill: k.fill, fillOpacity: k.fo }}
        />
        {(type === "xor" || type === "xnor") && (
          <path d="M-19 -11 Q-13 0 -19 11" style={stroke} />
        )}
        {(bubble || type === "not") && (
          <circle
            cx={bodyX}
            cy="0"
            r="3"
            style={{ ...stroke, fill: "var(--s-bg)" }}
          />
        )}
        {one ? (
          <path d="M-22 0 H-12" style={stroke} />
        ) : (
          <path d="M-22 -6 H-15 M-22 6 H-15" style={stroke} />
        )}
        <path
          d={`M${bubble || type === "not" ? bodyX + 3 : 14} 0 H22`}
          style={stroke}
        />
        {it.text != null && (
          <text
            y="3.5"
            x={
              type === "or" ||
              type === "nor" ||
              type === "xor" ||
              type === "xnor"
                ? -2
                : -4
            }
            textAnchor="middle"
            className="a-mono"
            style={{ fill: k.text, fontSize: it.size ?? 8.5 }}
          >
            {it.text}
          </text>
        )}
        {it.sub != null && (
          <text
            y="23"
            textAnchor="middle"
            className="a-cap"
            style={{ fontSize: 8.5 }}
          >
            {it.sub}
          </text>
        )}
      </G>
    );
  }
  if (t === "tr") {
    const k = tone(it.c);
    const stroke = { stroke: k.stroke, strokeWidth: 1.7, fill: "none" };
    const p = it.kind === "p";
    return (
      <G x={it.x} y={it.y} o={o} s={s}>
        <path d="M-5 -8 V8" style={stroke} />
        <path
          d="M0 -9 V9"
          style={{
            ...stroke,
            strokeWidth: it.on ? 2.8 : 1.7,
            strokeDasharray: it.on ? undefined : "3 2.5",
          }}
        />
        <path d="M0 -8 H10 V-16 M0 8 H10 V16" style={stroke} />
        {p ? (
          <circle
            cx="-8"
            cy="0"
            r="2.5"
            style={{ ...stroke, fill: "var(--s-bg)" }}
          />
        ) : null}
        <path d={p ? "M-16 0 H-10.5" : "M-16 0 H-5"} style={stroke} />
        {it.sub != null && (
          <text
            y="27"
            textAnchor="middle"
            className="a-cap"
            style={{ fontSize: 8.5 }}
          >
            {it.sub}
          </text>
        )}
      </G>
    );
  }
  if (t === "sw") {
    const k = tone(it.c);
    const stroke = { stroke: k.stroke, strokeWidth: 1.7, fill: "none" };
    return (
      <G x={it.x} y={it.y} o={o} s={s}>
        <circle
          cx="-14"
          cy="0"
          r="2.4"
          style={{ ...stroke, fill: "var(--s-bg)" }}
        />
        <circle
          cx="14"
          cy="0"
          r="2.4"
          style={{ ...stroke, fill: "var(--s-bg)" }}
        />
        <path
          className="a-t"
          d={it.on ? "M-14 0 L14 0" : "M-14 0 L11 -11"}
          style={{ ...stroke, strokeWidth: 2.2 }}
        />
        {it.sub != null && (
          <text
            y="16"
            textAnchor="middle"
            className="a-cap"
            style={{ fontSize: 8.5 }}
          >
            {it.sub}
          </text>
        )}
      </G>
    );
  }
  if (t === "lamp") {
    const k = tone(it.c);
    const r = it.r ?? 9;
    return (
      <G x={it.x} y={it.y} o={o} s={s}>
        <circle
          r={r}
          className="a-t"
          style={{
            fill: it.on ? "var(--s-accent)" : "var(--s-panel2)",
            fillOpacity: it.on ? 0.55 : 1,
            stroke: it.on ? "var(--s-accent)" : k.stroke,
            strokeWidth: 1.7,
          }}
        />
        <path
          d={`M${-r * 0.65} ${-r * 0.65} L${r * 0.65} ${r * 0.65} M${r * 0.65} ${-r * 0.65} L${-r * 0.65} ${r * 0.65}`}
          style={{
            stroke: it.on ? "var(--s-text)" : k.stroke,
            strokeWidth: 1.3,
          }}
        />
        {it.sub != null && (
          <text
            y={r + 10}
            textAnchor="middle"
            className="a-cap"
            style={{ fontSize: 8.5 }}
          >
            {it.sub}
          </text>
        )}
      </G>
    );
  }
  return null;
}

const KNOWN = new Set<ItemKind>([
  "cell",
  "dot",
  "lnode",
  "text",
  "ptr",
  "line",
  "box",
  "path",
  "bar",
  "code",
  "gate",
  "tr",
  "sw",
  "lamp",
]);
const NUMERIC = [
  "x",
  "y",
  "x1",
  "y1",
  "x2",
  "y2",
  "w",
  "h",
  "r",
  "o",
  "s",
  "hh",
] as const;

// Проверка при создании сцены: неизвестный тип или нечисловая координата — ошибка автора, а не «тихая» пустота.
function validate(frames: Frame[], base: Frame, labels: string[]) {
  frames.forEach((f, k) => {
    for (const it of [...base, ...f]) {
      const where = `сцена «${labels[0]}…», кадр ${k}, элемент ${it?.id}`;
      if (!it || !KNOWN.has(it.t) || it.id == null)
        throw new Error(`${where}: неизвестный элемент`);
      for (const key of NUMERIC) {
        const v = it[key];
        if (v !== undefined && !Number.isFinite(v)) throw new Error(`${where}: ${key} = ${v}`);
      }
      if (it.t === "path" && typeof it.d !== "string")
        throw new Error(`${where}: нет d`);
    }
  });
}

/** Кадр — список элементов, видимых на шаге. */
export type Frame = SceneItem[];

export interface SceneSpec {
  labels: string[];
  caption: string[];
  frames: Frame[];
  base?: Frame;
  cues?: number[];
  ms?: number;
  h?: number;
}

// Фабрика сцены. base — элементы, которые есть в каждом кадре (если кадр не
// переопределил их по id). cues — секунды начала шагов 1, 2, …
export function scene({ labels, caption, frames, base = [], cues, ms = 2800, h = 170 }: SceneSpec) {
  const full = frames.map((f) => {
    const m = new Map<string, SceneItem>();
    for (const it of [...base, ...f]) m.set(it.id, it);
    return m;
  });
  const order: string[] = [];
  const seen = new Set<string>();
  full.forEach((m) =>
    m.forEach((_, id) => !seen.has(id) && (seen.add(id), order.push(id))),
  );
  // что рисовать, если в кадре элемента нет: его последнее показанное состояние, но невидимое
  const lastSeen: Record<string, SceneItem> = {};
  const ghost = full.map((m) => {
    const g: Record<string, SceneItem> = {};
    for (const id of order) {
      const cur = m.get(id);
      if (cur) lastSeen[id] = cur;
      else if (lastSeen[id]) g[id] = { ...lastSeen[id], o: 0 };
    }
    return g;
  });
  // элементы, впервые появляющиеся позже: до появления тоже невидимы на своём месте
  const firstOf: Record<string, SceneItem> = {};
  full.forEach((m) =>
    m.forEach((it, id) => !(id in firstOf) && (firstOf[id] = it)),
  );
  if (labels.length !== frames.length)
    throw new Error(
      `scene «${labels[0]}…»: labels ${labels.length}, кадров ${frames.length}`,
    );
  if (caption.length !== frames.length)
    throw new Error(
      `scene «${labels[0]}…»: подписей ${caption.length}, кадров ${frames.length}`,
    );
  validate(frames, base, labels);
  return function Scene({ cues: given }: { cues?: number[] }) {
    const ctl: StepsCtl = useSteps(given || cues || defaultCues(frames.length), ms);
    const k = Math.min(ctl.step, frames.length - 1);
    return (
      <Steps ctl={ctl} labels={labels} caption={caption} h={h}>
        {order.map((id) => {
          const it = full[k]?.get(id) ?? ghost[k]?.[id] ?? { ...firstOf[id]!, o: 0 };
          return <Item key={id} it={it} />;
        })}
      </Steps>
    );
  };
}

function defaultCues(n: number) {
  return Array.from({ length: n - 1 }, (_, i) => 5 + i * 8);
}

/* ---------- помощники для авторов сцен ---------- */

/** Параметр «по индексу»: таблица {i: значение}, массив или функция i => значение. */
type ByIndex<T> = Partial<Record<number, T>> | T[] | ((i: number) => T | undefined);
const pick = <T,>(v: ByIndex<T> | undefined, i: number): T | undefined =>
  typeof v === "function" ? v(i) : (v as Partial<Record<number, T>> | undefined)?.[i];

// Ряд клеток: id0, id1, …; c — {i: цвет} или i => цвет; sub — i => подпись под клеткой.
/** Параметры ряда клеток row(). */
export interface RowOpts {
  x0?: number;
  y?: number;
  cw?: number;
  h?: number;
  w?: number;
  c?: ByIndex<string>;
  tc?: string | undefined;
  size?: number;
  sub?: ByIndex<string | number>;
  subSize?: number;
  o?: number | ((i: number) => number);
  dash?: SceneItem["dash"];
}

export function row(
  id: string,
  vals: (string | number)[],
  {
    x0 = 40,
    y = 60,
    cw = 30,
    h = 26,
    w,
    c = {},
    tc,
    size,
    sub,
    subSize,
    o = 1,
    dash,
  }: RowOpts = {},
): SceneItem[] {
  return vals.map((v, i) => ({
    t: "cell",
    id: `${id}${i}`,
    x: x0 + cw * i,
    y,
    w: w ?? cw - 3,
    h,
    text: v,
    c: pick(c, i) ?? "m",
    tc,
    size,
    sub: pick(sub, i),
    subSize,
    o: typeof o === "function" ? o(i) : o,
    dash,
  }));
}

export const X = (x0: number, cw: number, i: number) => x0 + cw * i;

// Линия между центрами двух узлов, укороченная на радиус r с обоих концов.
export function edge(
  id: string,
  a: Pt,
  b: Pt,
  {
    r = 12,
    r2,
    c = "m",
    arrow = false,
    o = 1,
    dash,
    w,
    bend,
  }: { r?: number; r2?: number; c?: string; arrow?: boolean; o?: number; dash?: SceneItem["dash"]; w?: number; bend?: number } = {},
): SceneItem {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const n = Math.hypot(dx, dy) || 1;
  const rb = r2 ?? r;
  return {
    t: "line",
    id,
    x1: a.x + (dx / n) * r,
    y1: a.y + (dy / n) * r,
    x2: b.x - (dx / n) * (rb + (arrow ? 2 : 0)),
    y2: b.y - (dy / n) * (rb + (arrow ? 2 : 0)),
    c,
    arrow,
    o,
    dash,
    w,
    bend,
  };
}

/** Узел бинарного дерева для tree(): k — ключ, l и r — потомки, c — цвет. */
export interface TreeNode {
  k: string | number;
  l?: TreeNode | null;
  r?: TreeNode | null;
  c?: string;
}

/* Бинарное дерево: node = {k, l, r, c}. Позиция x — по порядку обхода слева
   направо (стабильна при вставках), y — по глубине; id узла — `${id}:${k}`.
   Возвращает массив элементов (рёбра и узлы). colors — {k: цвет} поверх node.c. */
export function tree(
  id: string,
  root: TreeNode | null,
  {
    x0 = 180,
    y0 = 24,
    dx = 26,
    dy = 36,
    r = 11,
    colors = {},
    texts = {},
    size,
    o = 1,
    center = true,
  }: {
    x0?: number;
    y0?: number;
    dx?: number;
    dy?: number;
    r?: number | undefined;
    colors?: Record<string, string>;
    texts?: Record<string, string | number>;
    size?: number | undefined;
    o?: number | undefined;
    center?: boolean;
  } = {},
): SceneItem[] {
  // позиция узла: порядковый номер при обходе слева направо и глубина
  const where = new Map<TreeNode, { x: number; d: number }>();
  let i = 0;
  (function walk(n: TreeNode | null | undefined, d: number) {
    if (!n) return;
    walk(n.l, d + 1);
    where.set(n, { x: i++, d });
    walk(n.r, d + 1);
  })(root, 0);
  const cnt = i;
  const pos = (n: TreeNode): Pt => {
    const w = where.get(n) ?? { x: 0, d: 0 };
    return { x: x0 + (w.x - (center ? (cnt - 1) / 2 : 0)) * dx, y: y0 + w.d * dy };
  };
  const items: SceneItem[] = [];
  const nodes: SceneItem[] = [];
  (function emit(n: TreeNode | null | undefined, parent: TreeNode | null) {
    if (!n) return;
    const p = pos(n);
    if (parent) {
      items.push(
        edge(`${id}~${parent.k}-${n.k}`, pos(parent), p, {
          r,
          o,
          c: colors[`~${n.k}`] ?? "m",
        }),
      );
    }
    nodes.push({
      t: "dot",
      id: `${id}:${n.k}`,
      x: p.x,
      y: p.y,
      r,
      text: texts[n.k] ?? n.k,
      c: colors[n.k] ?? n.c ?? "m",
      size,
      o,
    });
    emit(n.l, n);
    emit(n.r, n);
  })(root, null);
  return [...items, ...nodes];
}

// Путь-график функции fn на прямоугольнике {x, y, w, h} (y — нижний левый угол), x ∈ [0, xmax], значения обрезаются на ymax.
export function curveD(
  fn: (u: number) => number,
  { x, y, w, h, xmax = 1, ymax = 1, n = 48 }: { x: number; y: number; w: number; h: number; xmax?: number; ymax?: number; n?: number },
) {
  let d = "";
  for (let i = 0; i <= n; i++) {
    const u = (i / n) * xmax;
    const v = Math.min(fn(u), ymax);
    d += `${i === 0 ? "M" : "L"}${(x + (u / xmax) * w).toFixed(1)} ${(y - (v / ymax) * h).toFixed(1)} `;
    if (fn(u) > ymax) break;
  }
  return d.trim();
}

// Цепочка узлов списка: узлы `${id}${i}` и стрелки `${id}~${i}` от ссылки узла i к левому краю узла i+1.
// pos — i => {x, y} (по умолчанию в ряд); last — рисовать ли у последнего узла «пустую» ссылку.
export function chain(
  id: string,
  vals: (string | number)[],
  {
    x0 = 48,
    y = 60,
    dx = 62,
    w = 44,
    h = 24,
    c = {},
    o = 1,
    pos,
    sub,
    arrows = true,
    edgeC = "g",
    nilLast = true,
  }: {
    x0?: number;
    y?: number;
    dx?: number;
    w?: number;
    h?: number;
    c?: ByIndex<string>;
    o?: number | ((i: number) => number);
    pos?: (i: number) => Pt;
    sub?: ByIndex<string | number>;
    arrows?: boolean;
    edgeC?: string;
    nilLast?: boolean;
  } = {},
): SceneItem[] {
  const at = (i: number): Pt => (pos ? pos(i) : { x: x0 + dx * i, y });
  const out: SceneItem[] = [];
  vals.forEach((v, i) => {
    const p = at(i);
    out.push({
      t: "lnode",
      id: `${id}${i}`,
      x: p.x,
      y: p.y,
      w,
      h,
      text: v,
      c: pick(c, i) ?? "m",
      nil: nilLast && i === vals.length - 1,
      sub: pick(sub, i),
      o: typeof o === "function" ? o(i) : o,
    });
    if (arrows && i < vals.length - 1) {
      const q = at(i + 1);
      out.push({
        t: "line",
        id: `${id}~${i}`,
        x1: p.x + w / 2 - 7,
        y1: p.y,
        x2: q.x - w / 2 - 1,
        y2: q.y,
        c: edgeC,
        arrow: true,
        o: typeof o === "function" ? o(i) : o,
      });
    }
  });
  return out;
}
