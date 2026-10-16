import { useMemo, useRef, useState, type PointerEvent } from "react";
import { readSetting, writeSetting } from "../lib/settings.ts";
import type { SqlDataset, SqlTable, SqlValue } from "../types.ts";

/* Виджет «База данных» в SQL-упражнении: ERD-диаграмма (таблицы можно перетаскивать,
   связи подсвечиваются при наведении) и просмотр данных таблиц. Схема приходит с сервера
   вместе с задачей (backend/app/exercises/schema_view.py). */

const BOX_W = 176;
const HEAD_H = 24;
const ROW_H = 19;
const GAP_X = 96;
const GAP_Y = 22;
const PAD = 16;

const LS_OPEN = "say-sx-open";
const LS_VIEW = "say-sx-view";

type Pos = Record<string, { x: number; y: number }>;
type View = "erd" | "data";

const boxH = (t: SqlTable) => HEAD_H + t.columns.length * ROW_H + 6;

// Начальная раскладка: родители (на кого ссылаются) слева, дети справа
function autoLayout(schema: SqlDataset): Pos {
  const level: Record<string, number> = {};
  const names = schema.tables.map((t) => t.name);
  names.forEach((n) => (level[n] = 0));
  for (let pass = 0; pass < names.length; pass++) {
    for (const r of schema.relations) {
      if (r.from === r.to) continue;
      level[r.from] = Math.max(level[r.from], level[r.to] + 1);
    }
  }
  const byLevel: Record<number, SqlTable[]> = {};
  for (const t of schema.tables) (byLevel[level[t.name]] ||= []).push(t);
  const pos: Pos = {};
  for (const lv of Object.keys(byLevel).map(Number).sort((a, b) => a - b)) {
    let y = PAD;
    for (const t of byLevel[lv]) {
      pos[t.name] = { x: PAD + lv * (BOX_W + GAP_X), y };
      y += boxH(t) + GAP_Y;
    }
  }
  return pos;
}

function Erd({ schema, onOpenTable }: { schema: SqlDataset; onOpenTable: (name: string) => void }) {
  const initial = useMemo(() => autoLayout(schema), [schema]);
  const [pos, setPos] = useState<Pos>(initial);
  const [hover, setHover] = useState<string | null>(null);
  const drag = useRef<{ name: string; dx: number; dy: number; moved: boolean } | null>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  const byName = useMemo(
    () => Object.fromEntries(schema.tables.map((t) => [t.name, t])),
    [schema],
  );

  const maxX = Math.max(...Object.values(pos).map((p) => p.x)) + BOX_W + PAD;
  const maxY =
    Math.max(...schema.tables.map((t) => (pos[t.name]?.y ?? 0) + boxH(t))) +
    PAD;

  // координаты указателя в системе viewBox
  function toSvg(e: PointerEvent): { x: number; y: number } {
    const svg = svgRef.current;
    if (!svg) return { x: 0, y: 0 };
    const pt = svg.createSVGPoint();
    pt.x = e.clientX;
    pt.y = e.clientY;
    const m = svg.getScreenCTM();
    return m ? pt.matrixTransform(m.inverse()) : { x: 0, y: 0 };
  }

  function down(e: PointerEvent<SVGGElement>, name: string) {
    const p = toSvg(e);
    drag.current = {
      name,
      dx: p.x - pos[name].x,
      dy: p.y - pos[name].y,
      moved: false,
    };
    e.currentTarget.setPointerCapture(e.pointerId);
  }
  function move(e: PointerEvent) {
    const d = drag.current;
    if (!d) return;
    const p = toSvg(e);
    const x = Math.max(4, p.x - d.dx);
    const y = Math.max(4, p.y - d.dy);
    if (Math.abs(x - pos[d.name].x) + Math.abs(y - pos[d.name].y) > 3)
      d.moved = true;
    setPos((prev) => ({ ...prev, [d.name]: { x, y } }));
  }
  function up() {
    const d = drag.current;
    drag.current = null;
    if (d && !d.moved) onOpenTable(d.name);
  }

  const colY = (t: SqlTable, col: string) =>
    pos[t.name].y +
    HEAD_H +
    t.columns.findIndex((c) => c.name === col) * ROW_H +
    ROW_H / 2;

  const lines = schema.relations
    .filter((r) => byName[r.from] && byName[r.to] && pos[r.from] && pos[r.to])
    .map((r, i) => {
      const a = byName[r.from];
      const b = byName[r.to];
      const pa = pos[a.name];
      const pb = pos[b.name];
      const ya = colY(a, r.from_col);
      const yb = colY(b, r.to_col);
      let d: string;
      let fx: number; // где рисовать «N» (ребёнок)
      let tx: number; // где рисовать «1» (родитель)
      if (a.name === b.name) {
        const x = pa.x + BOX_W;
        d = `M${x},${ya} C${x + 46},${ya} ${x + 46},${yb} ${x},${yb}`;
        fx = x + 8;
        tx = x + 8;
      } else if (pa.x >= pb.x + BOX_W) {
        const x1 = pa.x;
        const x2 = pb.x + BOX_W;
        const k = Math.max(30, (x1 - x2) / 2);
        d = `M${x1},${ya} C${x1 - k},${ya} ${x2 + k},${yb} ${x2},${yb}`;
        fx = x1 - 10;
        tx = x2 + 10;
      } else if (pb.x >= pa.x + BOX_W) {
        const x1 = pa.x + BOX_W;
        const x2 = pb.x;
        const k = Math.max(30, (x2 - x1) / 2);
        d = `M${x1},${ya} C${x1 + k},${ya} ${x2 - k},${yb} ${x2},${yb}`;
        fx = x1 + 10;
        tx = x2 - 10;
      } else {
        // таблицы друг над другом: обводим справа
        const x1 = Math.max(pa.x, pb.x) + BOX_W;
        d = `M${pa.x + BOX_W},${ya} C${x1 + 50},${ya} ${x1 + 50},${yb} ${pb.x + BOX_W},${yb}`;
        fx = pa.x + BOX_W + 10;
        tx = pb.x + BOX_W + 10;
      }
      const on = hover && (hover === r.from || hover === r.to);
      return { i, d, fx, ya, tx, yb, on, r };
    });

  return (
    <div className="sx-erd">
      <svg
        ref={svgRef}
        viewBox={`0 0 ${maxX + 40} ${maxY}`}
        style={{
          width: "100%",
          minWidth: Math.round((maxX + 40) * 0.75),
          maxWidth: maxX + 40,
          height: "auto",
        }}
        role="img"
        aria-label="ERD-диаграмма учебной базы"
        onPointerMove={move}
        onPointerUp={up}
        onPointerCancel={up}
      >
        {lines.map((l) => (
          <g key={l.i} className={`sx-rel ${l.on ? "on" : ""}`}>
            <path d={l.d} fill="none" />
            <text x={l.fx} y={l.ya - 4} className="sx-card">
              N
            </text>
            <text x={l.tx} y={l.yb - 4} className="sx-card">
              1
            </text>
          </g>
        ))}
        {schema.tables.map((t) => {
          const p = pos[t.name];
          if (!p) return null;
          const linked =
            hover &&
            schema.relations.some(
              (r) =>
                (r.from === hover && r.to === t.name) ||
                (r.to === hover && r.from === t.name),
            );
          return (
            <g
              key={t.name}
              transform={`translate(${p.x},${p.y})`}
              className={`sx-tbl ${t.kind === "view" ? "view" : ""} ${hover === t.name ? "on" : ""} ${linked ? "linked" : ""}`}
              onPointerDown={(e) => down(e, t.name)}
              onPointerEnter={() => setHover(t.name)}
              onPointerLeave={() => setHover(null)}
            >
              <rect
                width={BOX_W}
                height={boxH(t)}
                rx="7"
                className="sx-frame"
              />
              <path
                d={`M0,${HEAD_H} V7 a7,7 0 0 1 7,-7 H${BOX_W - 7} a7,7 0 0 1 7,7 V${HEAD_H} Z`}
                className="sx-head"
              />
              <text x="10" y="16" className="sx-name">
                {t.kind === "view" ? "◇ " : ""}
                {t.name}
              </text>
              <text x={BOX_W - 10} y="16" className="sx-count" textAnchor="end">
                {t.total}
              </text>
              {t.columns.map((c, i) => (
                <g
                  key={c.name}
                  transform={`translate(0,${HEAD_H + i * ROW_H})`}
                  className={c.pk ? "pk" : c.fk ? "fk" : ""}
                >
                  <text x="10" y={ROW_H - 6} className="sx-key">
                    {c.pk ? "PK" : c.fk ? "FK" : ""}
                  </text>
                  <text x="32" y={ROW_H - 6} className="sx-col">
                    {c.name}
                  </text>
                  <text
                    x={BOX_W - 10}
                    y={ROW_H - 6}
                    className="sx-type"
                    textAnchor="end"
                  >
                    {(c.type || "").toLowerCase()}
                  </text>
                </g>
              ))}
            </g>
          );
        })}
      </svg>
      <div className="sx-erd-foot">
        <span>PK — первичный ключ · FK — внешний ключ · N : 1 — связь</span>
        <button
          className="sx-link"
          onClick={() => setPos(initial)}
          title="Вернуть таблицы на места"
        >
          расставить заново
        </button>
      </div>
    </div>
  );
}

function Cell({ v }: { v: SqlValue | undefined }) {
  if (v === null || v === undefined) return <i className="sx-null">NULL</i>;
  const num = typeof v === "number";
  return <span className={num ? "sx-num" : ""}>{String(v)}</span>;
}

function Data({ schema, table, setTable }: { schema: SqlDataset; table: string | undefined; setTable: (name: string) => void }) {
  const t = schema.tables.find((x) => x.name === table) || schema.tables[0];
  return (
    <div className="sx-data">
      <div className="sx-tabs" role="tablist">
        {schema.tables.map((x) => (
          <button
            key={x.name}
            role="tab"
            aria-selected={x.name === t.name}
            className={`sx-tab ${x.name === t.name ? "on" : ""}`}
            onClick={() => setTable(x.name)}
          >
            {x.kind === "view" ? "◇ " : ""}
            {x.name}
            <em>{x.total}</em>
          </button>
        ))}
      </div>
      <div className="sx-scroll">
        <table className="sx-grid">
          <thead>
            <tr>
              {t.columns.map((c) => (
                <th key={c.name} className={c.pk ? "pk" : c.fk ? "fk" : ""}>
                  {c.pk && <b>PK</b>}
                  {!c.pk && c.fk && <b>FK</b>}
                  {c.name}
                  <small>{(c.type || "").toLowerCase()}</small>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {t.rows.length === 0 && (
              <tr>
                <td colSpan={t.columns.length} className="sx-empty">
                  таблица пуста
                </td>
              </tr>
            )}
            {t.rows.map((r, i) => (
              <tr key={i}>
                {r.map((v, j) => (
                  <td key={j}>
                    <Cell v={v} />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {t.total > t.rows.length && (
        <p className="sx-more">
          Показаны первые {t.rows.length} из {t.total} строк.
        </p>
      )}
    </div>
  );
}

export default function SqlSchema({ schema }: { schema: SqlDataset | null | undefined }) {
  const [open, setOpen] = useState(() => readSetting(LS_OPEN, "1") === "1");
  const [view, setView] = useState<View>(() =>
    readSetting(LS_VIEW, "erd") === "data" ? "data" : "erd",
  );
  const [table, setTable] = useState(schema?.tables?.[0]?.name);

  if (!schema || !schema.tables?.length) return null;

  const toggle = (v: View) => {
    setView(v);
    writeSetting(LS_VIEW, v);
    if (!open) {
      setOpen(true);
      writeSetting(LS_OPEN, "1");
    }
  };
  const fold = () => {
    setOpen(!open);
    writeSetting(LS_OPEN, open ? "0" : "1");
  };
  const tables = schema.tables.filter((t) => t.kind !== "view");
  const views = schema.tables.length - tables.length;

  return (
    <section className="sx" aria-label="Учебная база">
      <div className="sx-bar">
        <button className="sx-fold" onClick={fold} aria-expanded={open}>
          <span className={`sx-chev ${open ? "on" : ""}`}>▸</span>
          База данных
          <em>
            {tables.length}{" "}
            {tables.length === 1
              ? "таблица"
              : tables.length < 5
                ? "таблицы"
                : "таблиц"}
            {views ? ` · ${views} представл.` : ""}
          </em>
        </button>
        <div className="sx-seg" role="group" aria-label="Вид">
          <button
            className={open && view === "erd" ? "on" : ""}
            onClick={() => toggle("erd")}
          >
            ERD
          </button>
          <button
            className={open && view === "data" ? "on" : ""}
            onClick={() => toggle("data")}
          >
            Данные
          </button>
        </div>
      </div>
      {open &&
        (view === "erd" ? (
          <Erd
            schema={schema}
            onOpenTable={(name) => {
              setTable(name);
              toggle("data");
            }}
          />
        ) : (
          <Data schema={schema} table={table} setTable={setTable} />
        ))}
    </section>
  );
}
