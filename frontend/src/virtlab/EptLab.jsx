import { useState } from "react";
import { GOALS, LEVELS, TLB_ENTRIES, WORKLOADS, simulate } from "./ept.js";
import { useGoals } from "./goals.js";

/* Симулятор трансляции адресов (глава 4): режим (теневые таблицы или EPT), размеры страниц гостя и
   хозяина, нагрузка. Показывает цену обхода (двумерная сетка обращений), промахи TLB и общую
   стоимость в обращениях к памяти. Решено, когда достигнуты все цели. */

const fmt = (n) => Math.round(n).toLocaleString("ru-RU");
const SIZES = [
  ["4K", "4 КиБ"],
  ["2M", "2 МиБ"],
  ["1G", "1 ГиБ"],
];

function Grid({ mode, guest, host }) {
  if (mode === "shadow") {
    const n = Math.min(LEVELS[guest], LEVELS[host]);
    return (
      <div className="vl-grid2" style={{ gridTemplateColumns: `repeat(${n}, 22px)` }}>
        {Array.from({ length: n }, (_, i) => (
          <i key={i} className="on" />
        ))}
      </div>
    );
  }
  const g = LEVELS[guest] + 1;
  const h = LEVELS[host] + 1;
  return (
    <div className="vl-grid2" style={{ gridTemplateColumns: `repeat(${h}, 22px)` }}>
      {Array.from({ length: g * h }, (_, i) => (
        <i key={i} className={i === g * h - 1 ? "data" : "on"} />
      ))}
    </div>
  );
}

export default function EptLab({ solved, onSolved }) {
  const goals = useGoals(
    GOALS.map((g) => g.id),
    solved,
    onSolved,
  );
  const [mode, setMode] = useState("ept");
  const [guest, setGuest] = useState("4K");
  const [host, setHost] = useState("4K");
  const [workload, setWorkload] = useState("one");
  const [res, setRes] = useState(null);

  function run() {
    const cfg = { mode, guest, host, workload };
    const r = simulate(cfg);
    setRes({ ...r, cfg });
    for (const g of GOALS)
      if (g.workload === workload && g.check(r, cfg)) goals.mark(g.id, cfg);
  }
  const wl = WORKLOADS.find((w) => w.id === workload);

  return (
    <div className="vl">
      <div className="vl-grid">
        <div className="vl-card">
          <div className="vl-field">
            <span className="s-label">режим</span>
            <div className="vl-seg">
              {[
                ["shadow", "теневые таблицы"],
                ["ept", "EPT / NPT"],
              ].map(([v, t]) => (
                <button
                  key={v}
                  className={`vl-segbtn ${mode === v ? "on" : ""}`}
                  onClick={() => setMode(v)}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>
          <div className="vl-row">
            <label className="vl-field">
              <span>страница гостя</span>
              <select value={guest} onChange={(e) => setGuest(e.target.value)}>
                {SIZES.map(([v, t]) => (
                  <option key={v} value={v}>
                    {t}
                  </option>
                ))}
              </select>
            </label>
            <label className="vl-field">
              <span>страница хозяина</span>
              <select value={host} onChange={(e) => setHost(e.target.value)}>
                {SIZES.map(([v, t]) => (
                  <option key={v} value={v}>
                    {t}
                  </option>
                ))}
              </select>
            </label>
          </div>
          <label className="vl-field">
            <span>нагрузка</span>
            <select value={workload} onChange={(e) => setWorkload(e.target.value)}>
              {WORKLOADS.map((w) => (
                <option key={w.id} value={w.id}>
                  {w.title}
                </option>
              ))}
            </select>
          </label>
          <p className="vl-hint">
            {wl.note}. TLB — {TLB_ENTRIES} записей; запись описывает страницу
            меньшего из двух размеров.
          </p>
          <div className="vl-actions">
            <button className="quiz-btn" onClick={run}>
              Запустить нагрузку
            </button>
          </div>
          <span className="s-label">цели</span>
          <ul className="vl-goals">
            {GOALS.map((g) => (
              <li key={g.id} className={goals.isDone(g.id) ? "ok" : ""}>
                <span className="vl-gm">{goals.isDone(g.id) ? "✓" : "○"}</span>
                <span>
                  {g.text}
                  <em> — нагрузка «{WORKLOADS.find((w) => w.id === g.workload).title}»</em>
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div className="vl-card">
          <div className="pr-res-head">
            <span className="s-label">промах TLB</span>
            <span className="pr-res-time">
              {mode === "ept"
                ? `(${LEVELS[guest]}+1)×(${LEVELS[host]}+1)−1`
                : `${Math.min(LEVELS[guest], LEVELS[host])} уровня`}
            </span>
          </div>
          <Grid mode={mode} guest={guest} host={host} />
          <p className="vl-hint">
            Каждая клетка — одно обращение к памяти при промахе; зелёная — сами
            данные.
          </p>
          {res && (
            <div className="vl-final">
              <table className="vl-stat">
                <tbody>
                  <tr>
                    <td>обращений гостя</td>
                    <td>{fmt(res.accesses)}</td>
                  </tr>
                  <tr>
                    <td>промахов TLB</td>
                    <td>
                      {fmt(res.misses)} (страница в TLB: {res.effPage})
                    </td>
                  </tr>
                  <tr>
                    <td>цена одного промаха</td>
                    <td>{res.walk} обращ.</td>
                  </tr>
                  <tr>
                    <td>выходов из-за правок таблиц</td>
                    <td>{fmt(res.exits)}</td>
                  </tr>
                  <tr>
                    <td>
                      <b>всего обращений к памяти</b>
                    </td>
                    <td>
                      <b>{fmt(res.cost)}</b>
                    </td>
                  </tr>
                </tbody>
              </table>
              <p className="vl-hint">
                Выход стоит {fmt(1000)} обращений; попадание в TLB — одно
                обращение к данным.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
