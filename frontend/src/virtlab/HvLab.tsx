import { useMemo, useState } from "react";
import { PROGRAMS, apply, expected, initial, inspect, type GuestState, type TrapOption } from "./hv.ts";
import { useGoals, type LabProps } from "./goals.ts";

/* Симулятор мини-гипервизора (глава 2): гость исполняет программу, а ученик — монитор:
   на каждой ловушке выбирает верную имитацию над виртуальным состоянием. Команда POPF
   не вызывает ловушку, пока не включена двоичная трансляция. Решено, когда пройдены все программы. */

const shuffle = <T,>(arr: T[], seed: number): T[] => {
  const a = [...arr];
  let x = seed;
  for (let i = a.length - 1; i > 0; i--) {
    x = (x * 1103515245 + 12345) & 0x7fffffff;
    const j = x % (i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};

export default function HvLab({ solved, onSolved }: LabProps) {
  const goals = useGoals(
    PROGRAMS.map((p) => p.id),
    solved,
    onSolved,
  );
  const [pid, setPid] = useState(PROGRAMS[0].id);
  const prog = PROGRAMS.find((p) => p.id === pid) ?? PROGRAMS[0];
  const [translate, setTranslate] = useState(false);
  const [s, setS] = useState<GuestState>(initial());
  const [msg, setMsg] = useState<{ bad: boolean; text: string } | null>(null);
  const [finished, setFinished] = useState<{ ok: boolean; state: GuestState; want: GuestState } | null>(null); // итог последнего прогона

  const started = s.pc > 0 || s.log.length > 0;
  const ins = prog.code[s.pc];
  const info = useMemo(
    () => (ins && !s.halted ? inspect(ins, s, translate) : null),
    [ins, s, translate],
  );
  const options = useMemo(
    () => (info?.kind === "trap" ? shuffle(info.options, s.pc * 7 + pid.length) : []),
    [info, s.pc, pid],
  );

  function reset(nextPid = pid) {
    setS(initial());
    setMsg(null);
    setFinished(null);
    if (nextPid !== pid) setTranslate(false);
    setPid(nextPid);
  }

  function finish(state: GuestState) {
    const want = expected(prog.code);
    const ok =
      !state.silent &&
      state.acc === want.acc &&
      state.vif === want.vif &&
      state.vcr3 === want.vcr3 &&
      state.delivered.join() === want.delivered.join();
    setFinished({ ok, state, want });
    if (ok) goals.mark(prog.id, { translate, mistakes: state.mistakes });
  }

  function step() {
    if (!ins || s.halted || !info || info.kind === "trap") return;
    if (info.kind === "direct") {
      const t = apply(ins, s);
      t.log = [...s.log, `${ins} — напрямую на процессоре`];
      setS(t);
      setMsg(null);
      return;
    }
    // silent: команда «молча» не сработала, ловушки не было
    const t = { ...s, pc: s.pc + 1, silent: true, log: [...s.log, `${ins} — без ловушки, ничего не изменилось`] };
    setS(t);
    setMsg({ bad: true, text: info.why });
  }

  function choose(o: TrapOption) {
    if (!ins) return;
    if (!o.ok) {
      setS({ ...s, mistakes: s.mistakes + 1 });
      setMsg({ bad: true, text: `Нет: ${o.why}.` });
      return;
    }
    const t = apply(ins, s);
    t.log = [...s.log, `${ins} — ловушка: ${o.label}`];
    setS(t);
    setMsg(null);
    if (t.halted) finish(t);
  }

  return (
    <div className="vl">
      <div className="vl-tabs" role="tablist">
        {PROGRAMS.map((p) => (
          <button
            key={p.id}
            role="tab"
            aria-selected={p.id === pid}
            className={`vl-tab ${p.id === pid ? "on" : ""} ${goals.isDone(p.id) ? "ok" : ""}`}
            onClick={() => reset(p.id)}
          >
            <span className="vl-tab-mark">{goals.isDone(p.id) ? "✓" : ""}</span>
            {p.title}
          </button>
        ))}
      </div>

      <div className="vl-grid">
        <div className="vl-card">
          <p className="vl-goal">
            <span className="s-label">цель</span> {prog.goal}
          </p>
          <ol className="vl-code">
            {prog.code.map((c, i) => (
              <li key={i} className={i === s.pc && !s.halted ? "cur" : i < s.pc ? "past" : ""}>
                <span className="vl-ln">{i + 1}</span>
                <code>{c}</code>
              </li>
            ))}
          </ol>
          <label className="vl-check">
            <input
              type="checkbox"
              checked={translate}
              disabled={started}
              onChange={(e) => setTranslate(e.target.checked)}
            />
            <span>двоичная трансляция гостевого ядра (до запуска)</span>
          </label>
          <div className="vl-actions">
            <button
              className="quiz-btn"
              onClick={step}
              disabled={s.halted || !ins || info?.kind === "trap"}
            >
              Шаг
            </button>
            <button className="quiz-btn ghost" onClick={() => reset()}>
              Сначала
            </button>
          </div>
        </div>

        <div className="vl-card">
          <div className="vl-state">
            <div>
              <span className="s-label">гость видит</span>
              <table className="vl-stat">
                <tbody>
                  <tr><td>acc</td><td>{s.acc}</td></tr>
                  <tr><td>vif (виртуальный IF)</td><td>{s.vif}</td></tr>
                  <tr><td>vcr3</td><td>{s.vcr3}</td></tr>
                  <tr><td>очередь IRQ</td><td>{s.queue.join(", ") || "—"}</td></tr>
                  <tr><td>доставлено</td><td>{s.delivered.join(", ") || "—"}</td></tr>
                </tbody>
              </table>
            </div>
            <div>
              <span className="s-label">настоящий процессор</span>
              <table className="vl-stat">
                <tbody>
                  <tr><td>IF</td><td>1 всегда</td></tr>
                  <tr><td>CR3</td><td>монитор</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          {info?.kind === "trap" && (
            <div className="vl-trap">
              <div className="vl-trap-t">⚡ Ловушка: {info.title}</div>
              <div className="vl-opts">
                {options.map((o) => (
                  <button key={o.label} className="vl-opt" onClick={() => choose(o)}>
                    {o.label}
                  </button>
                ))}
              </div>
            </div>
          )}
          {msg && <p className={msg.bad ? "vl-no" : "vl-yes"}>{msg.text}</p>}
          {finished && (
            <p className={finished.ok ? "vl-yes" : "vl-no"}>
              {finished.ok
                ? `✓ Программа выполнена верно (ошибок выбора: ${finished.state.mistakes}).`
                : "Программа дала неверный результат: монитор не заметил команду POPF, и vif остался 0. Включите двоичную трансляцию и начните сначала."}
            </p>
          )}
          {s.log.length > 0 && (
            <ul className="vl-log">
              {s.log.map((l, i) => (
                <li key={i}>{l}</li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
