import { G, Steps, useSteps } from "./kit.jsx";

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

const COL = {
  m: "var(--s-muted)",
  g: "var(--s-accent)",
  y: "var(--s-amber)",
  r: "var(--s-red)",
  b: "var(--s-blue)",
  v: "var(--s-violet)",
};

function tone(c = "m") {
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
    return { fill: "var(--s-border)", fo: 1, stroke: "var(--s-border)", text: "var(--s-text)" };
  if (c === "n")
    return {
      fill: "none",
      fo: 0,
      stroke: "var(--s-border)",
      text: "var(--s-text)",
    };
  return { fill: COL[c], fo: 0.28, stroke: COL[c], text: "var(--s-text)" };
}

const ARROW_OK = new Set(["m", "g", "y", "r", "b"]);
const arrowId = (c) => `url(#a-hd-${ARROW_OK.has(c) ? c : "m"})`;

function Lines({ text, size, anchor = "middle", lh = 1.25 }) {
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

function Item({ it }) {
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
          <Lines text={it.text ?? ""} size={size} />
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
          <Lines text={it.text} size={size} anchor={it.anchor ?? "middle"} />
        </text>
      </G>
    );
  }
  if (t === "ptr") {
    const down = (it.dir ?? "down") === "down";
    const col = COL[it.c ?? "g"] ?? COL.g;
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
    const { x1, y1, x2, y2 } = it;
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
          strokeDasharray: it.dash,
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
          strokeDasharray: drawn ? "1 1" : it.dash,
          strokeDashoffset: drawn ? 1 - it.draw : 0,
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
    const hl = new Set(
      Array.isArray(it.hl) ? it.hl : it.hl == null ? [] : [it.hl],
    );
    return (
      <G x={it.x} y={it.y} o={o}>
        {it.lines.map((l, i) => (
          <g key={i}>
            <rect
              className="a-t"
              x="-4"
              y={i * lh - lh * 0.78}
              width={w}
              height={lh}
              rx="3"
              style={{
                fill: "var(--s-accent)",
                fillOpacity: hl.has(i) ? 0.2 : 0,
              }}
            />
            <text
              y={i * lh}
              className="a-mono"
              style={{
                fontSize: size,
                whiteSpace: "pre",
                fill: hl.has(i) ? "var(--s-text)" : "var(--s-muted)",
              }}
              xmlSpace="preserve"
            >
              {l}
            </text>
          </g>
        ))}
      </G>
    );
  }
  return null;
}

// Фабрика сцены. base — элементы, которые есть в каждом кадре (если кадр не
// переопределил их по id). cues — секунды начала шагов 1, 2, …
export function scene({
  labels,
  caption,
  frames,
  base = [],
  cues,
  ms = 2800,
  h = 170,
}) {
  const full = frames.map((f) => {
    const m = new Map();
    for (const it of [...base, ...f]) m.set(it.id, it);
    return m;
  });
  const order = [];
  const seen = new Set();
  full.forEach((m) =>
    m.forEach((_, id) => !seen.has(id) && (seen.add(id), order.push(id))),
  );
  // что рисовать, если в кадре элемента нет: его последнее показанное состояние, но невидимое
  const lastSeen = {};
  const ghost = full.map((m) => {
    const g = {};
    for (const id of order) {
      if (m.has(id)) lastSeen[id] = m.get(id);
      else if (lastSeen[id]) g[id] = { ...lastSeen[id], o: 0 };
    }
    return g;
  });
  // элементы, впервые появляющиеся позже: до появления тоже невидимы на своём месте
  const firstOf = {};
  full.forEach((m) =>
    m.forEach((it, id) => !(id in firstOf) && (firstOf[id] = it)),
  );
  if (labels.length !== frames.length)
    throw new Error("scene: labels и frames разной длины");
  return function Scene({ cues: given }) {
    const ctl = useSteps(given || cues || defaultCues(frames.length), ms);
    const k = Math.min(ctl.step, frames.length - 1);
    return (
      <Steps ctl={ctl} labels={labels} caption={caption} h={h}>
        {order.map((id) => {
          const it = full[k].get(id) ??
            ghost[k][id] ?? { ...firstOf[id], o: 0 };
          return <Item key={id} it={it} />;
        })}
      </Steps>
    );
  };
}

function defaultCues(n) {
  return Array.from({ length: n - 1 }, (_, i) => 5 + i * 8);
}

/* ---------- помощники для авторов сцен ---------- */

// Ряд клеток: id0, id1, …; c — {i: цвет} или i => цвет; sub — i => подпись под клеткой.
export function row(
  id,
  vals,
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
    o = 1,
    dash,
  } = {},
) {
  return vals.map((v, i) => ({
    t: "cell",
    id: `${id}${i}`,
    x: x0 + cw * i,
    y,
    w: w ?? cw - 3,
    h,
    text: v,
    c: typeof c === "function" ? (c(i) ?? "m") : (c[i] ?? "m"),
    tc,
    size,
    sub: typeof sub === "function" ? sub(i) : sub?.[i],
    o: typeof o === "function" ? o(i) : o,
    dash,
  }));
}

export const X = (x0, cw, i) => x0 + cw * i;

// Линия между центрами двух узлов, укороченная на радиус r с обоих концов.
export function edge(
  id,
  a,
  b,
  { r = 12, r2, c = "m", arrow = false, o = 1, dash, w, bend } = {},
) {
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

/* Бинарное дерево: node = {k, l, r, c}. Позиция x — по порядку обхода слева
   направо (стабильна при вставках), y — по глубине; id узла — `${id}:${k}`.
   Возвращает массив элементов (рёбра и узлы). colors — {k: цвет} поверх node.c. */
export function tree(
  id,
  root,
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
  } = {},
) {
  const nodes = [];
  let i = 0;
  (function walk(n, d, parent) {
    if (!n) return;
    walk(n.l, d + 1, n);
    n._x = i++;
    n._d = d;
    walk(n.r, d + 1, n);
  })(root, 0);
  const cnt = i;
  const pos = (n) => ({
    x: x0 + (n._x - (center ? (cnt - 1) / 2 : 0)) * dx,
    y: y0 + n._d * dy,
  });
  const items = [];
  (function emit(n, parent) {
    if (!n) return;
    const p = pos(n);
    if (parent) {
      const q = pos(parent);
      items.push(
        edge(`${id}~${parent.k}-${n.k}`, q, p, {
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
export function curveD(fn, { x, y, w, h, xmax = 1, ymax = 1, n = 48 }) {
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
  id,
  vals,
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
  } = {},
) {
  const at = (i) => (pos ? pos(i) : { x: x0 + dx * i, y });
  const out = [];
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
      c: typeof c === "function" ? (c(i) ?? "m") : (c[i] ?? "m"),
      nil: nilLast && i === vals.length - 1,
      sub: typeof sub === "function" ? sub(i) : sub?.[i],
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
