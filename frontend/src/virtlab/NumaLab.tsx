import { useState } from "react";
import { NODES, PLACES, SCENARIOS, defaultPlan, evaluate } from "./numa.ts";
import { useGoals } from "./goals.ts";

/* Симулятор размещения по узлам NUMA (глава 11): для каждой машины выбирают узлы процессоров и
   памяти. Показаны загрузка узлов и доля удалённых обращений. Цель сценария проверяется по
   кнопке «Принять размещение»; решено, когда приняты оба сценария. */

const pct = (x: number) => `${Math.round(x * 100)}%`;

export default function NumaLab({ solved, onSolved }) {
  const goals = useGoals(
    SCENARIOS.map((s) => s.id),
    solved,
    onSolved,
  );
  const [sid, setSid] = useState(SCENARIOS[0].id);
  const sc = SCENARIOS.find((s) => s.id === sid);
  const [plans, setPlans] = useState(() =>
    Object.fromEntries(SCENARIOS.map((s) => [s.id, defaultPlan(s.vms)])),
  );
  const [msg, setMsg] = useState(null);
  const plan = plans[sid];
  const ev = evaluate(sc.vms, plan);

  const set = (name: string, key: string, value: string) => {
    setPlans((p) => ({ ...p, [sid]: { ...p[sid], [name]: { ...p[sid][name], [key]: value } } }));
    setMsg(null);
  };
  function accept() {
    if (ev.over) return setMsg({ bad: true, text: "Размещение не помещается: на каком-то узле не хватает ядер или памяти." });
    if (ev.avg > sc.max + 1e-9)
      return setMsg({ bad: true, text: `Удалённых обращений ${pct(ev.avg)} — больше допустимых ${pct(sc.max)}.` });
    setMsg({ bad: false, text: `✓ Принято: удалённых обращений ${pct(ev.avg)}.` });
    goals.mark(sc.id, plan);
  }

  return (
    <div className="vl">
      <div className="vl-tabs" role="tablist">
        {SCENARIOS.map((s) => (
          <button
            key={s.id}
            role="tab"
            aria-selected={s.id === sid}
            className={`vl-tab ${s.id === sid ? "on" : ""} ${goals.isDone(s.id) ? "ok" : ""}`}
            onClick={() => {
              setSid(s.id);
              setMsg(null);
            }}
          >
            <span className="vl-tab-mark">{goals.isDone(s.id) ? "✓" : ""}</span>
            {s.title}
          </button>
        ))}
      </div>
      <div className="vl-grid">
        <div className="vl-card">
          <p className="vl-goal">
            <span className="s-label">цель</span> {sc.goal}
          </p>
          <table className="vl-vms">
            <thead>
              <tr>
                <th>машина</th>
                <th>процессоры</th>
                <th>память</th>
                <th>удалённых</th>
              </tr>
            </thead>
            <tbody>
              {sc.vms.map((vm) => (
                <tr key={vm.name}>
                  <td>
                    <b>{vm.name}</b>
                    <br />
                    <span className="vl-hint">
                      {vm.vcpus} vCPU · {vm.mem} ГиБ
                    </span>
                  </td>
                  {["cpu", "mem"].map((k) => (
                    <td key={k}>
                      <select value={plan[vm.name][k]} onChange={(e) => set(vm.name, k, e.target.value)}>
                        {PLACES.map(([v, t]) => (
                          <option key={v} value={v}>
                            {t}
                          </option>
                        ))}
                      </select>
                    </td>
                  ))}
                  <td>{pct(ev.per[vm.name])}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <label className="vl-check">
            <input
              type="checkbox"
              checked={sc.vms.some((v) => plan[v.name].vnuma)}
              onChange={(e) => {
                const on = e.target.checked;
                setPlans((p) => ({
                  ...p,
                  [sid]: Object.fromEntries(
                    Object.entries(p[sid]).map(([n, v]) => [n, { ...v, vnuma: on }]),
                  ),
                }));
                setMsg(null);
              }}
            />
            <span>виртуальная топология NUMA для растянутых машин</span>
          </label>
          <div className="vl-actions">
            <button className="quiz-btn" onClick={accept}>Принять размещение</button>
          </div>
          {msg && <p className={msg.bad ? "vl-no" : "vl-yes"}>{msg.text}</p>}
        </div>

        <div className="vl-card">
          <span className="s-label">узлы хоста</span>
          {NODES.map((n, i) => {
            const l = ev.load[i];
            return (
              <div key={i} className="vl-node">
                <b>узел {i}</b>
                <Meter label="ядра" used={l.cores} max={n.cores} />
                <Meter label="память, ГиБ" used={l.mem} max={n.mem} />
              </div>
            );
          })}
          <table className="vl-stat">
            <tbody>
              <tr>
                <td>
                  <b>средняя доля удалённых обращений</b>
                </td>
                <td>
                  <b>{pct(ev.avg)}</b>
                </td>
              </tr>
            </tbody>
          </table>
          <p className="vl-hint">
            Своя память — 0%, чужой узел — 100%, растянутое — 50% (с виртуальной NUMA у полностью растянутой
            машины — 25%).
          </p>
        </div>
      </div>
    </div>
  );
}

function Meter({ label, used, max }) {
  const over = used > max;
  return (
    <div className="vl-meter">
      <span>
        {label}: {used} / {max}
      </span>
      <div className="vl-bar">
        <i style={{ width: `${Math.min(100, (used / max) * 100)}%` }} className={over ? "full" : ""} />
      </div>
    </div>
  );
}
