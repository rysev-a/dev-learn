import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import ResultAlert from "../../lab/react/ResultAlert.tsx";
import { checkGoals, resolveTarget, runProbe } from "../check.ts";
import { transfer } from "../transfer.ts";
import { clone, connect, disconnect, strip } from "../model.ts";
import { fmtMs } from "../sim.ts";
import { exec, toIp } from "../term.ts";
import Board from "./Board.tsx";
import Chart from "./Chart.tsx";
import DevicePanel from "./DevicePanel.tsx";
import "../../lab/lab.css";
import "../netlab.css";

/* Лаборатория «Компьютерные сети»: поле с устройствами, карточка выбранного устройства
   (формы и терминал), цели упражнения и журнал последнего пакета. Проверка — в браузере. */

const SLOT = 320; // мс на один «момент» анимации

function restore(scenario: { build: () => any; }, code: string) {
  const fresh = scenario.build();
  if (!code) return fresh;
  try {
    const s = JSON.parse(code);
    const a = Object.keys(s.devices ?? {}).sort().join();
    const b = Object.keys(fresh.devices).sort().join();
    return a === b && Array.isArray(s.links) ? s : fresh;
  } catch {
    return fresh;
  }
}

function timelineOf(run: { hops: any; events: any; }) {
  const ts = new Set();
  for (const h of run.hops) (ts.add(h.t0), ts.add(h.t1));
  for (const e of run.events) ts.add(e.t);
  return [...ts].sort((a, b) => a - b);
}

export default function NetLab({
  scenario,
  code,
  onCode,
  solvedBefore,
  onSolved,
  onNext,
  hasNext,
  nextLabel,
}) {
  const tools = scenario.tools ?? {};
  const [net, setNet] = useState(() => restore(scenario, code));
  const [sel, setSel] = useState(() => Object.keys(restore(scenario, code).devices)[0]);
  const [cable, setCable] = useState(false);
  const [cableFrom, setCableFrom] = useState(null);
  const [selLink, setSelLink] = useState(null);
  const [notice, setNotice] = useState("");
  const [results, setResults] = useState(null);
  const [terms, setTerms] = useState({});
  const [hintOpen, setHintOpen] = useState(false);
  const [run, setRun] = useState(null); // {hops, events, tl, title}
  const [chart, setChart] = useState(null);
  const [slot, setSlot] = useState(0);
  const raf = useRef(0);

  const save = useCallback(
    (n) => {
      onCode?.(JSON.stringify(strip(n)));
    },
    [onCode],
  );

  const apply = (fn: (arg0: any) => any) => {
    const n = clone(net);
    const r = fn(n);
    setNet(n);
    save(n);
    setResults(null);
    return r;
  };

  /* --- анимация пробы --- */
  const play = useCallback((r: SetStateAction<null>, title: any) => {
    cancelAnimationFrame(raf.current);
    if (!r || (!r.hops.length && !r.events.length)) return setRun(null);
    const tl = timelineOf(r);
    setRun({ ...r, tl, title });
    const t0 = performance.now();
    const total = tl.length + 3;
    const tick = (now: number) => {
      const s = (now - t0) / SLOT;
      setSlot(Math.min(s, total));
      if (s < total) raf.current = requestAnimationFrame(tick);
    };
    raf.current = requestAnimationFrame(tick);
  }, []);
  useEffect(() => () => cancelAnimationFrame(raf.current), []);

  const dots = useMemo(() => {
    if (!run) return [];
    return run.hops
      .map((h) => {
        const a = run.tl.indexOf(h.t0);
        const b = Math.max(a + 0.6, run.tl.indexOf(h.t1));
        return { ...h, a, b, p: (slot - a) / (b - a) };
      })
      .filter((h) => h.p >= 0 && h.p <= 1);
  }, [run, slot]);

  const shown = useMemo(
    () => (run ? run.events.filter((e) => run.tl.indexOf(e.t) <= slot) : []),
    [run, slot],
  );
  const marks = useMemo(() => {
    const out = [];
    for (const e of shown) {
      if (!["drop", "fw", "nat"].includes(e.kind)) continue;
      if (slot - run.tl.indexOf(e.t) > 5) continue;
      const row = out.filter((m) => m.dev === e.dev).length;
      out.push({
        dev: e.dev,
        kind: e.kind,
        row,
        text: e.text.length > 38 ? e.text.slice(0, 36) + "…" : e.text,
      });
    }
    return out;
  }, [shown, run, slot]);

  /* --- команды терминала и форм --- */
  const terminalRun = (devId: string, line: any) => {
    const n = clone(net);
    const res = exec(n, devId, line);
    setNet(n);
    if (res.changed) {
      save(n);
      setResults(null);
    }
    setTerms((t) => {
      const cur = t[devId] ?? [];
      const out = [...cur, { cmd: true, text: line }];
      if (res.clear) return { ...t, [devId]: [] };
      if (res.out) for (const l of res.out.split("\n")) out.push({ text: l });
      return { ...t, [devId]: out };
    });
    if (res.probe) play(res.probe, line);
    if (res.chart) setChart(res.chart);
    return res;
  };

  // формы NAT/файрвола зовут терминал и показывают его ответ рядом
  const formExec = (line: any) => {
    const n = clone(net);
    const res = exec(n, sel, line);
    setNet(n);
    if (res.changed) {
      save(n);
      setResults(null);
    }
    return res.out;
  };

  /* --- кабели --- */
  const onDevice = (id: number|SetStateAction<string>|SetStateAction<null>) => {
    if (cable) {
      if (!cableFrom) {
        setCableFrom(id);
        setNotice("");
      } else {
        const n = clone(net);
        const r = connect(n, cableFrom, id);
        if (r.ok) {
          setNet(n);
          save(n);
          setResults(null);
          setNotice("");
        } else setNotice(r.error);
        setCableFrom(null);
      }
      return;
    }
    setSel(id);
    setSelLink(null);
  };
  const removeLink = () => {
    if (selLink === null) return;
    const n = clone(net);
    disconnect(n, selLink);
    setNet(n);
    save(n);
    setSelLink(null);
    setResults(null);
  };

  /* --- проверка --- */
  const check = () => {
    const r = checkGoals(net, scenario.goals);
    setResults(r);
    if (r.every((x) => x.ok)) {
      const code = JSON.stringify(strip(net));
      onSolved?.(code);
    }
  };
  const allOk = results?.every((x) => x.ok);
  const playGoal = (g: { xfer?: any; dns?: any; text?: any; ping?: any; tcp?: any; udp?: any; }) => {
    if (g.xfer) {
      const s = clone(net);
      const r = transfer(s, g.xfer.from, resolveTarget(s, g.xfer.to), { bytes: (g.xfer.mb ?? 50) * 1e6 });
      setChart(r.chart);
      return;
    }
    const s = clone(net);
    let r;
    if (g.dns) {
      r = toIp(s, s.devices[g.dns.from], g.dns.name).run;
      if (!r) return;
    } else r = runProbe(s, g);
    play(r, g.text);
    setNet((c: any) => ({ ...c, rt: s.rt }));
  };
  const reset = () => {
    const n = scenario.build();
    setNet(n);
    save(n);
    setResults(null);
    setRun(null);
    setChart(null);
    setTerms({});
    setSelLink(null);
    setCable(false);
    setCableFrom(null);
  };

  const lastLines = shown.length ? shown : run?.events ?? [];
  const nameOf = (id: string|number) => net.devices[id]?.name ?? id;

  return (
    <div className="nl">
      <div className="nl-main">
        <div className="nl-boardcard">
          <div className="nl-toolbar">
            {tools.cable && (
              <>
                <button
                  type="button"
                  className={`quiz-btn ghost ${cable ? "running" : ""}`}
                  onClick={() => {
                    setCable((v) => !v);
                    setCableFrom(null);
                    setNotice("");
                  }}
                >
                  {cable ? "Кабель: выберите два устройства" : "Кабель"}
                </button>
                {selLink !== null && (
                  <button type="button" className="quiz-btn ghost" onClick={removeLink}>
                    Удалить кабель
                  </button>
                )}
              </>
            )}
            <span className="nl-spacer" />
            <button type="button" className="quiz-btn ghost" onClick={() => setHintOpen((v) => !v)}>
              Подсказка
            </button>
            <button type="button" className="quiz-btn ghost" onClick={reset}>
              Сбросить
            </button>
          </div>
          {hintOpen && <p className="nl-hint">{scenario.hint}</p>}
          {notice && <p className="nl-notice">{notice}</p>}
          <Board
            state={net}
            selected={sel}
            cableFrom={cableFrom}
            selectedLink={selLink}
            dots={dots}
            marks={marks}
            onDevice={onDevice}
            onLink={(i: SetStateAction<null>) => {
              if (tools.cable) setSelLink(i);
            }}
          />
          {chart && <Chart chart={chart} />}
          {run && (
            <p className="nl-caption">
              {dots[0]?.label ?? (slot >= run.tl.length ? "готово" : "…")}
            </p>
          )}
        </div>

        <DevicePanel
          key={sel}
          state={net}
          devId={sel}
          tools={tools}
          apply={apply}
          exec={formExec}
          lines={terms[sel] ?? []}
          onRun={(line: any) => terminalRun(sel, line)}
        />
      </div>

      <div className="nl-bottom">
        <div className="nl-goals">
          <h4>Цели</h4>
          <ul>
            {scenario.goals.map((g, i: number) => {
              const r = results?.[i];
              return (
                <li key={g.id} className={r ? (r.ok ? "ok" : "bad") : ""}>
                  <span className="nl-gmark">{r ? (r.ok ? "✓" : "✗") : i + 1}</span>
                  <span className="nl-gtext">
                    {g.text}
                    {r && <small>{r.detail}</small>}
                  </span>
                  <button type="button" className="nl-play" title="Показать путь пакета" onClick={() => playGoal(g)}>
                    ▶
                  </button>
                </li>
              );
            })}
          </ul>
          <div className="nl-actions">
            <button type="button" className="quiz-btn" onClick={check}>
              Проверить
            </button>
          </div>
          {results && (
            <ResultAlert
              ok={allOk}
              title={allOk ? "Все цели выполнены" : "Пока не всё работает"}
              onNext={allOk && hasNext ? onNext : undefined}
              nextLabel={nextLabel}
            >
              {allOk
                ? solvedBefore
                  ? "Упражнение уже было решено."
                  : "Упражнение засчитано."
                : "Нажмите ▶ у цели — увидите, где пакет теряется, и поправьте настройки."}
            </ResultAlert>
          )}
        </div>

        <div className="nl-log">
          <h4>
            Журнал {run?.title ? <small>· {run.title}</small> : null}
          </h4>
          {lastLines.length === 0 ? (
            <p className="nl-none">Запустите ping в терминале или нажмите ▶ у цели — здесь появится путь пакета: ARP, пересылка, NAT, потери.</p>
          ) : (
            <ol>
              {lastLines.map((e, i: Key|null|undefined) => (
                <li key={i} className={e.kind}>
                  <time>{fmtMs(e.t)}</time>
                  <b>{nameOf(e.dev)}</b>
                  <span>{e.text}</span>
                </li>
              ))}
            </ol>
          )}
        </div>
      </div>
    </div>
  );
}
