import { useEffect, useRef, useState } from "react";
import type { LabProps } from "./goals.ts";
import { MEM_MIB, SCENARIOS, simulate, type MigrationInput, type Simulation } from "./migration.ts";

/* Симулятор живой миграции (глава 10): сценарий задаёт скорость записи гостя и сети, ученик
   подбирает допустимый простой, замедление, сжатие и момент перехода на post-copy. Цель каждого
   сценария проверяется по результату запуска; упражнение решено, когда достигнуты все три. */

const fmt = (n: number) => Math.round(n).toLocaleString("ru-RU");

export default function MigrationLab({ solved, onSolved }: LabProps) {
  const [sid, setSid] = useState(SCENARIOS[0]!.id);
  const sc = SCENARIOS.find((s) => s.id === sid) ?? SCENARIOS[0]!;
  const [downtimeMs, setDowntimeMs] = useState(300);
  const [autoConverge, setAutoConverge] = useState(false);
  const [compress, setCompress] = useState(false);
  const [hybrid, setHybrid] = useState(false);
  const [after, setAfter] = useState(3);
  const [run, setRun] = useState<{ result: Simulation; shown: number; scenario: string } | null>(null);
  const [done, setDone] = useState<Record<string, MigrationInput>>({}); // id сценария → настройки, при которых цель достигнута
  const timer = useRef<ReturnType<typeof setInterval> | undefined>(undefined);
  const reported = useRef(false);

  useEffect(() => () => clearInterval(timer.current), []);
  useEffect(() => {
    setRun(null);
    clearInterval(timer.current);
  }, [sid]);

  const params = (): MigrationInput => ({
    dirty: sc.dirty,
    bw: sc.bw,
    downtimeMs,
    autoConverge,
    compress,
    postcopyAfter: hybrid ? after : null,
  });

  function start() {
    clearInterval(timer.current);
    const p = params();
    const result = simulate(p);
    setRun({ result, shown: 0, scenario: sc.id });
    let shown = 0;
    timer.current = setInterval(() => {
      shown += 1;
      setRun((r) => (r ? { ...r, shown } : r));
      if (shown > result.rounds.length) {
        clearInterval(timer.current);
        if (sc.check(result)) {
          setDone((d) => {
            const next = { ...d, [sc.id]: p };
            if (
              SCENARIOS.every((s) => next[s.id]) &&
              !solved &&
              !reported.current
            ) {
              reported.current = true;
              onSolved(JSON.stringify(next));
            }
            return next;
          });
        }
      }
    }, 380);
  }

  const result = run?.result;
  const finished = run && result ? run.shown > result.rounds.length : false;
  const reachedNow = !!result && finished && sc.check(result);
  const maxBar = MEM_MIB;

  return (
    <div className="vl">
      <div className="vl-tabs" role="tablist">
        {SCENARIOS.map((s) => (
          <button
            key={s.id}
            role="tab"
            aria-selected={s.id === sid}
            className={`vl-tab ${s.id === sid ? "on" : ""} ${done[s.id] || solved ? "ok" : ""}`}
            onClick={() => setSid(s.id)}
          >
            <span className="vl-tab-mark">{done[s.id] || solved ? "✓" : ""}</span>
            {s.title}
          </button>
        ))}
      </div>

      <div className="vl-grid">
        <div className="vl-card">
          <div className="vl-facts">
            <span>
              <b>16 ГиБ</b> памяти гостя
            </span>
            <span>
              гость пишет <b>{fmt(sc.dirty)} МиБ/с</b>
            </span>
            <span>
              сеть <b>{fmt(sc.bw)} МиБ/с</b> (≈10 Гбит/с)
            </span>
          </div>
          <p className="vl-goal">
            <span className="s-label">цель</span> {sc.goal}
          </p>

          <label className="vl-field">
            <span>
              допустимый простой: <b>{downtimeMs} мс</b>
            </span>
            <input
              type="range"
              min="20"
              max="1000"
              step="10"
              value={downtimeMs}
              onChange={(e) => setDowntimeMs(+e.target.value)}
            />
          </label>
          <label className="vl-check">
            <input
              type="checkbox"
              checked={autoConverge}
              onChange={(e) => setAutoConverge(e.target.checked)}
            />
            <span>
              auto-converge: притормаживать vCPU (20%, затем +10% за круг)
            </span>
          </label>
          <label className="vl-check">
            <input
              type="checkbox"
              checked={compress}
              onChange={(e) => setCompress(e.target.checked)}
            />
            <span>сжатие страниц (канал ×1,5)</span>
          </label>
          <label className="vl-check row">
            <input
              type="checkbox"
              checked={hybrid}
              onChange={(e) => setHybrid(e.target.checked)}
            />
            <span>гибрид: перейти на post-copy после</span>
            <select
              value={after}
              disabled={!hybrid}
              onChange={(e) => setAfter(+e.target.value)}
            >
              {[1, 2, 3, 4, 5, 6].map((n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              ))}
            </select>
            <span>кругов</span>
          </label>
          <div className="vl-actions">
            <button className="quiz-btn" onClick={start}>
              Запустить миграцию
            </button>
          </div>
          <p className="vl-hint">{sc.hint}</p>
        </div>

        <div className="vl-card">
          <div className="pr-res-head">
            <span className="s-label">круги pre-copy</span>
            {result && (
              <span className="pr-res-time">
                порог остановки ≈ {fmt(result.limit)} МиБ
              </span>
            )}
          </div>
          {!result && (
            <p className="pr-empty">
              Нажмите «Запустить миграцию»: здесь по кругам будет уменьшаться
              остаток памяти.
            </p>
          )}
          {result && (
            <ul className="vl-rounds">
              {result.rounds.slice(0, run.shown).map((r) => (
                <li key={r.k}>
                  <span className="vl-rk">круг {r.k}</span>
                  <div className="vl-bar">
                    <i
                      style={{ width: `${(r.sent / maxBar) * 100}%` }}
                      className={r.sent >= maxBar * 0.98 ? "full" : ""}
                    />
                  </div>
                  <span className="vl-rv">
                    {fmt(r.sent)} МиБ · {r.secs.toFixed(1)} с
                    {r.throttle ? ` · тормоз ${r.throttle}%` : ""}
                  </span>
                </li>
              ))}
            </ul>
          )}
          {finished && result && (
            <div className={`vl-final ${result.outcome}`}>
              {result.outcome === "precopy" && (
                <p>
                  Остаток {fmt(result.remaining)} МиБ помещается в порог:
                  машина остановлена на <b>{result.downtime} мс</b>, миграция
                  заняла <b>{result.total} с</b>.
                </p>
              )}
              {result.outcome === "postcopy" && (
                <p>
                  Гость переключён на цель с простоем <b>{result.downtime} мс</b>
                  , остаток {fmt(result.remaining)} МиБ подтягивается по
                  требованию (≈{result.faults} ошибок страниц). Всего{" "}
                  <b>{result.total} с</b>. Пока память разбросана между
                  серверами, сбой сети потерял бы машину.
                </p>
              )}
              {result.outcome === "failed" && (
                <p>
                  Миграция не сошлась за 12 кругов: остаток{" "}
                  {fmt(result.remaining)} МиБ, остановка длилась бы{" "}
                  <b>{fmt(result.downtime)} мс</b>. Гость пишет быстрее, чем
                  уходит по сети.
                </p>
              )}
              <p className={reachedNow ? "vl-yes" : "vl-no"}>
                {reachedNow
                  ? "✓ Цель сценария достигнута"
                  : "Цель сценария не достигнута — измените параметры"}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
