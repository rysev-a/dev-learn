import { useEffect, useMemo, useRef, useState } from "react";
import { createPortal } from "react-dom";
import ResultAlert from "../../lab/react/ResultAlert.tsx";
import { allOk, checkGoals } from "../checks.ts";
import { evaluate, REF, param } from "../engine.ts";
import { KINDS, defaultParams, type ParamSpec } from "../kinds.ts";
import { colX, nextY, place } from "../layout.ts";
import { NODE_H, NODE_W, connectError } from "../ports.ts";
import type { FailKind, Kind, ParamValue, SdEdge, SdScenario, SdState, Workload } from "../types.ts";
import Board from "./Board.tsx";
import "../../lab/lab.css";
import "../sdlab.css";

/* Лаборатория «Системный дизайн»: поле схемы, панель компонента, цели и метрики. Расчёт идёт сразу
   при каждой правке; решение засчитывается, когда выполнены все цели. */

interface SdLabProps {
  scenario: SdScenario;
  code?: string | undefined;
  onCode?: (code: string) => void;
  solvedBefore: boolean;
  onSolved?: (code: string) => void;
  onNext?: () => void;
  hasNext: boolean;
  nextLabel: string;
}

const clone = (s: SdState): SdState => JSON.parse(JSON.stringify(s)) as SdState;

/** схема старой раскладки (узлы налезают друг на друга) — расставляем по колонкам заново */
function tidy(s: SdState): SdState {
  const crowded = s.nodes.some((a, i) => s.nodes.some((b, j) => j > i && Math.abs(a.x - b.x) < NODE_W && Math.abs(a.y - b.y) < NODE_H));
  return crowded ? place({ ...s, nodes: s.nodes.map((n) => ({ ...n, x: -1, y: -1 })) }) : s;
}

function restore(scenario: SdScenario, code?: string): SdState {
  if (!code) return clone(scenario.start);
  try {
    const s = JSON.parse(code) as SdState;
    if (Array.isArray(s.nodes) && Array.isArray(s.edges) && s.nodes.some((n) => n.kind === "clients")) return tidy(s);
  } catch {
    /* повреждённый черновик */
  }
  return clone(scenario.start);
}

const fmtPct = (x: number) => `${(x * 100).toFixed(x >= 0.9999 ? 4 : x >= 0.999 ? 3 : 1)}%`;

function workloadChips(w: Workload): string[] {
  const out: string[] = [];
  if (w.static) out.push(`статика ${w.static}/с`);
  if (w.read) out.push(`чтения ${w.read}/с`);
  if (w.write) out.push(`записи ${w.write}/с`);
  out.push(`данные ${w.dataGB} ГБ`);
  out.push(`рабочий набор ${Math.round(w.hotSet * 100)}%`);
  if (w.searchShare) out.push(`поиск ${Math.round(w.searchShare * 100)}% чтений`);
  if (w.hotKey) out.push(`горячий ключ ${Math.round(w.hotKey * 100)}%`);
  if (w.connections) out.push(`соединений ${w.connections}`);
  if (w.msgPerConn) out.push(`${w.msgPerConn} сообщ/с на соединение`);
  if (w.spikeSec) out.push(`пик ${w.spikeSec} с`);
  return out;
}

const FAIL_LABEL: Partial<Record<FailKind, string>> = {
  zone: "отказ зоны доступности",
  region: "отказ региона",
  deploy: "выкладка новой версии",
  app: "падает сервер приложения",
  lb: "падает балансировщик",
  db: "падает лидер базы",
  cache: "падает кэш",
  cdn: "падает CDN",
  queue: "падает очередь",
  worker: "падает обработчик",
  gateway: "падает шлюз",
  search: "падает реплика поиска",
  ws: "падает WebSocket-шлюз",
  auth: "падает сервис входа",
  geo: "падает геосервис",
  ml: "падает сервис ранжирования",
  pay: "падает платёжный канал",
  stream: "падает поток событий",
  notify: "падает сервис уведомлений",
  analytics: "падает узел аналитики",
};

export default function SdLab({ scenario, code, onCode, solvedBefore, onSolved, onNext, hasNext, nextLabel }: SdLabProps) {
  const [state, setState] = useState(() => restore(scenario, code));
  const [sel, setSel] = useState<string | null>(null);
  const [selEdge, setSelEdge] = useState<number | null>(null);
  const [notice, setNotice] = useState("");
  const [hintOpen, setHintOpen] = useState(false);
  const [fs, setFs] = useState(false);
  const [helpOpen, setHelpOpen] = useState(false);
  const [down, setDown] = useState<string[]>([]);
  const [fail, setFail] = useState<FailKind | "">("");
  const solvedRef = useRef(solvedBefore);

  const wl = scenario.workload;
  const result = useMemo(() => evaluate(state, wl, { down, fail: fail || undefined }), [state, wl, down, fail]);
  const base = useMemo(() => evaluate(state, wl), [state, wl]);
  const goals = useMemo(() => checkGoals(state, wl, scenario.goals, base), [state, wl, scenario.goals, base]);
  const solved = allOk(goals) && state.nodes.length > 0;

  const persist = (s: SdState) => onCode?.(JSON.stringify(s));
  const update = (fn: (s: SdState) => void, save = true) => {
    const s = clone(state);
    fn(s);
    setState(s);
    if (save) persist(s);
  };

  useEffect(() => {
    if (solved && !solvedRef.current) {
      solvedRef.current = true;
      onSolved?.(JSON.stringify(state));
    }
  }, [solved, state, onSolved]);

  useEffect(() => {
    if (!fs) return;
    const key = (e: KeyboardEvent) => e.key === "Escape" && setFs(false);
    document.addEventListener("keydown", key);
    const old = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", key);
      document.body.style.overflow = old;
    };
  }, [fs]);

  const kindsOnBoard = [...new Set(state.nodes.map((n) => n.kind))].filter((k) => k !== "clients" && k !== "monitor" && FAIL_LABEL[k]);
  const selected = state.nodes.find((n) => n.id === sel) ?? null;

  /** поставить компонент; (x, y) не заданы — на свободное место своей колонки */
  const place = (kind: Kind, at?: { x: number; y: number }, edges: SdEdge[] = []) => {
    if (state.nodes.length >= (scenario.maxNodes ?? 14)) return setNotice(`На схеме не больше ${scenario.maxNodes ?? 14} компонентов.`);
    setNotice("");
    let i = 1;
    while (state.nodes.some((n) => n.id === `${kind}${i}`)) i++;
    const same = state.nodes.filter((n) => n.kind === kind).length;
    const id = `${kind}${i}`;
    update((s) => {
      s.nodes.push({
        id,
        kind,
        name: same ? `${KINDS[kind].label} ${same + 1}` : KINDS[kind].label,
        x: at ? at.x : colX(KINDS[kind].col),
        y: at ? at.y : nextY(state, KINDS[kind].col),
        params: defaultParams(kind),
      });
      for (const e of edges) {
        const from = e.from === "__new__" ? id : e.from;
        const to = e.to === "__new__" ? id : e.to;
        if (!s.edges.some((x) => x.from === from && x.to === to)) s.edges.push({ from, to });
      }
    });
    setSel(id);
    setSelEdge(null);
  };

  const connect = (from: string, to: string): string | null => {
    const a = state.nodes.find((n) => n.id === from);
    const b = state.nodes.find((n) => n.id === to);
    if (!a || !b) return "Компонент не найден.";
    const err = connectError(state, a, b);
    if (err) return err;
    setNotice("");
    update((s) => {
      s.edges.push({ from, to });
    });
    return null;
  };

  const autoEdges = (edges: SdEdge[]) =>
    update((s) => {
      for (const e of edges) if (!s.edges.some((x) => x.from === e.from && x.to === e.to)) s.edges.push({ from: e.from, to: e.to });
    });

  const remove = () => {
    if (selEdge !== null) {
      update((s) => {
        s.edges.splice(selEdge, 1);
      });
      setSelEdge(null);
    } else if (selected && selected.kind !== "clients") {
      update((s) => {
        s.nodes = s.nodes.filter((n) => n.id !== selected.id);
        s.edges = s.edges.filter((e) => e.from !== selected.id && e.to !== selected.id);
      });
      setSel(null);
      setDown((d) => d.filter((x) => x !== selected.id));
    }
  };

  const setParam = (key: string, v: ParamValue) =>
    selected &&
    update((s) => {
      const n = s.nodes.find((x) => x.id === selected.id);
      if (n) n.params[key] = v;
    });

  const reset = () => {
    const s = clone(scenario.start);
    setState(s);
    persist(s);
    setSel(null);
    setSelEdge(null);
    setDown([]);
    setFail("");
    setNotice("");
  };

  const fieldOf = (p: ParamSpec) => {
    if (!selected) return null;
    const v = param(selected, p.key);
    if (p.type === "int")
      return (
        <input
          type="number"
          min={p.min}
          max={p.max}
          value={Number(v)}
          onChange={(e) => {
            const x = Math.round(Number(e.target.value));
            if (Number.isFinite(x)) setParam(p.key, Math.max(p.min ?? 0, Math.min(p.max ?? 1e9, x)));
          }}
        />
      );
    if (p.type === "bool")
      return (
        <input type="checkbox" checked={v === true} onChange={(e) => setParam(p.key, e.target.checked)} />
      );
    return (
      <select value={String(v)} onChange={(e) => setParam(p.key, typeof p.options?.[0]?.value === "number" ? Number(e.target.value) : e.target.value)}>
        {p.options?.map((o) => (
          <option key={String(o.value)} value={String(o.value)}>
            {o.label}
          </option>
        ))}
      </select>
    );
  };

  const load = selected ? result.loads[selected.id] : undefined;
  const nameOf = (id: string) => state.nodes.find((n) => n.id === id)?.name ?? id;

  const paramsEl = selected ? (
    <div className="sd-float" onPointerDown={(e) => e.stopPropagation()}>
      <button type="button" className="sd-float-x" title="Закрыть" aria-label="Закрыть" onClick={() => setSel(null)}>
        ×
      </button>
              <h4>{selected.name}</h4>
              <p className="sd-about">{KINDS[selected.kind].about}</p>
              {KINDS[selected.kind].params
                .filter((p) => p.basic !== false || scenario.show?.includes(`${selected.kind}.${p.key}`))
                .map((p) => (
                <label key={p.key} className="sd-field">
                  <span>{p.label}</span>
                  {fieldOf(p)}
                  {p.help && <small>{p.help}</small>}
                </label>
              ))}
              {selected.kind !== "clients" && selected.kind !== "monitor" && (
                <>
                  <label className="sd-field row">
                    <span>Отключить (проверить отказ)</span>
                    <input
                      type="checkbox"
                      checked={down.includes(selected.id)}
                      onChange={(e) => setDown((d) => (e.target.checked ? [...d, selected.id] : d.filter((x) => x !== selected.id)))}
                    />
                  </label>
                  {load && (
                    <p className={`sd-load ${load.status}`}>
                      Нагрузка: {Math.round(load.load)} · ёмкость: {Math.round(load.cap)} · загрузка {Math.round(load.util * 100)}%
                      {load.note ? ` · ${load.note}` : ""}
                    </p>
                  )}
                </>
              )}
    </div>
  ) : null;
  const helpEl = helpOpen ? (
    <div className="sd-help" role="dialog" aria-label="Справка по схеме">
      <p className="sd-about">Выберите компонент на схеме, чтобы изменить его параметры. Новые компоненты перетащите на поле из палитры над ним (или кликните по кнопке), связи тяните от выходного порта к входному — подходящие соседи подключаются сами.</p>
          <h5>Справочник чисел</h5>
            <ul>
              <li>Сервер приложения: S/M/L = {REF.app.cap.S}/{REF.app.cap.M}/{REF.app.cap.L} запр/с, ${REF.app.cost.S}/{REF.app.cost.M}/{REF.app.cost.L}; статика — {REF.staticWeight} запроса.</li>
              <li>База: чтения {REF.db.read.S}/{REF.db.read.M}/{REF.db.read.L} в с, записи {REF.db.write.S}/{REF.db.write.M}/{REF.db.write.L} в с на узел; ${REF.db.cost.S}/{REF.db.cost.M}/{REF.db.cost.L} за узел; NoSQL ×{REF.db.nosql}.</li>
              <li>Кэш: {REF.cache.cap} запр/с, ${REF.cache.costPerGB} за ГБ; CDN ${REF.cdn.cost}; балансировщик {REF.lb.cap} запр/с, ${REF.lb.cost}.</li>
              <li>Очередь: {REF.queue.capPerPartition} сообщ/с на партицию; обработчик S/M: {REF.worker.cap.S}/{REF.worker.cap.M} записей/с.</li>
              <li>Поиск: {REF.search.cap} запр/с на реплику, не больше {REF.search.maxGBPerShard} ГБ на шард, ${REF.search.cost} за узел.</li>
              <li>WebSocket-шлюз: {REF.ws.cap} соединений на экземпляр, ${REF.ws.cost}.</li>
              <li>Доступность одного экземпляра: сервер 99,5%, база 99,9%, балансировщик 99,95%; n экземпляров: 1 − (1 − a)ⁿ.</li>
            </ul>
    </div>
  ) : null;
  const cornerEl = (
    <div className="sd-corner">
      <div className="sd-corner-btns">
        <button type="button" className={`sd-iconbtn ${helpOpen ? "on" : ""}`} title="Справка" aria-label="Справка" aria-pressed={helpOpen} onClick={() => setHelpOpen((v) => !v)}>
          ?
        </button>
        <button type="button" className="sd-iconbtn" title={fs ? "Свернуть (Esc)" : "Схема на весь экран"} aria-label={fs ? "Свернуть" : "На весь экран"} onClick={() => setFs((v) => !v)}>
          {fs ? (
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" />
            </svg>
          ) : (
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" />
            </svg>
          )}
        </button>
      </div>
      {helpEl}
    </div>
  );
  const boardCard = (
        <div className="sd-boardcard">
          <div className="sd-chips">
            {workloadChips(wl).map((c) => (
              <span key={c}>{c}</span>
            ))}
          </div>
          <div className="sd-toolbar">
            <button type="button" className="quiz-btn ghost" onClick={remove} disabled={selEdge === null && (!selected || selected.kind === "clients")}>
              Удалить
            </button>
            <span className="sd-spacer" />
            <label className="sd-fail">
              <span>Отказ:</span>
              <select value={fail} onChange={(e) => setFail(e.target.value as FailKind | "")}>
                <option value="">нет</option>
                <option value="zone">{FAIL_LABEL.zone}</option>
                <option value="region">{FAIL_LABEL.region}</option>
                <option value="deploy">{FAIL_LABEL.deploy}</option>
                {kindsOnBoard.map((k) => (
                  <option key={k} value={k}>
                    {FAIL_LABEL[k]}
                  </option>
                ))}
              </select>
            </label>
            <button type="button" className="quiz-btn ghost" onClick={() => setHintOpen((v) => !v)}>
              Подсказка
            </button>
            <button type="button" className="quiz-btn ghost" onClick={reset}>
              Сбросить
            </button>
          </div>
          {hintOpen && <p className="sd-hint">{scenario.hint}</p>}
          <Board
            state={state}
            loads={result.loads}
            selected={sel}
            selectedEdge={selEdge}
            down={down}
            palette={scenario.palette}
            fullscreen={fs}
            corner={cornerEl}
            overlay={paramsEl}
            onSelectNode={(id) => {
              setSel(id);
              setSelEdge(null);
            }}
            onSelectEdge={(i) => {
              setSelEdge(i);
              if (i !== null) setSel(null);
            }}
            onMove={(id, x, y, done) =>
              update((s) => {
                const n = s.nodes.find((m) => m.id === id);
                if (n) {
                  n.x = x;
                  n.y = y;
                }
              }, done)
            }
            onConnect={connect}
            onPlace={(kind, x, y, edges) => place(kind, { x, y }, edges)}
            onAddDefault={(kind) => place(kind)}
            onAutoEdges={autoEdges}
            onDelete={remove}
            onMessage={setNotice}
          />
          {notice && <p className="sd-notice">{notice}</p>}
          {selEdge !== null && state.edges[selEdge] && (
            <p className="sd-hint">
              Связь «{nameOf(state.edges[selEdge].from)} → {nameOf(state.edges[selEdge].to)}» выбрана — «Удалить» уберёт её.
            </p>
          )}
        </div>
  );
  const goalsEl = (
        <div className="sd-goals">
          <h4>Цели</h4>
          <ul>
            {scenario.goals.map((g, i) => {
              const r = goals[i];
              return (
                <li key={i} className={r?.ok ? "ok" : "bad"}>
                  <span className="sd-gmark">{r?.ok ? "✓" : "✗"}</span>
                  <span className="sd-gtext">
                    {r?.text}
                    {r && <small>{r.detail}</small>}
                  </span>
                </li>
              );
            })}
          </ul>
          {solved && (
            <ResultAlert ok title="Все цели выполнены" onNext={hasNext ? onNext : undefined} nextLabel={nextLabel}>
              {solvedBefore ? "Упражнение уже было решено." : "Упражнение засчитано."}
            </ResultAlert>
          )}
        </div>
  );
  const metricsEl = (
        <div className="sd-metrics">
          <h4>
            Метрики {fail ? <small>· {FAIL_LABEL[fail]}</small> : null}
          </h4>
          <dl>
            <div>
              <dt>p50 / p99</dt>
              <dd>{result.entry ? `${result.p50} / ${result.p99} мс` : "—"}</dd>
            </div>
            <div>
              <dt>Успешных ответов</dt>
              <dd className={result.success < 0.99 ? "bad" : ""}>{fmtPct(result.success)}</dd>
            </div>
            <div>
              <dt>Доступность</dt>
              <dd>{fmtPct(result.availability)}</dd>
            </div>
            <div>
              <dt>Стоимость</dt>
              <dd>${result.cost} в мес.</dd>
            </div>
            {result.hit !== null && (
              <div>
                <dt>Попаданий в кэш</dt>
                <dd>{Math.round(result.hit * 100)}%</dd>
              </div>
            )}
            {result.cdnHit !== null && (
              <div>
                <dt>Попаданий в CDN</dt>
                <dd>{Math.round(result.cdnHit * 100)}%</dd>
              </div>
            )}
            {result.lagSec !== null && (
              <div>
                <dt>Отставание очереди</dt>
                <dd className={result.lagSec >= 999 ? "bad" : ""}>{result.lagSec >= 999 ? "не разбирается" : `${result.lagSec} с`}</dd>
              </div>
            )}
            {result.replicaLagMs !== null && (
              <div>
                <dt>Отставание реплик</dt>
                <dd>{result.replicaLagMs} мс</dd>
              </div>
            )}
          </dl>
          {result.warnings.map((w) => (
            <p key={w} className="sd-warn">
              {w}
            </p>
          ))}
        </div>
  );

  const content = fs ? (
    <div className="sd fs">
      <div className="sd-fs-main">{boardCard}</div>
      <div className="sd-side">
        {goalsEl}
        {metricsEl}
      </div>
    </div>
  ) : (
    <div className="sd">
      <div className="sd-work">{boardCard}</div>
      <div className="sd-bottom">
        {goalsEl}
        {metricsEl}
      </div>
    </div>
  );
  // на весь экран — поверх страницы, вне её вёрстки
  return fs ? createPortal(content, document.body) : content;
}
