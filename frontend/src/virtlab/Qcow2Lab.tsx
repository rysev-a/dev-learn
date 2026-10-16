import { useRef, useState } from "react";
import {
  CLUSTERS,
  GOALS,
  commit,
  initialChain,
  read,
  revert,
  snapshot,
  write,
  type Layer,
} from "./qcow2.ts";
import { useGoals, type LabProps } from "./goals.ts";

/* Симулятор слоёв qcow2 (глава 9): снимки, запись с копированием, чтение вниз по цепочке,
   слияние и откат. Решено, когда выполнены все три цели. */

const LETTERS = "EFGHIJKLMNOPQRSTUVWXYZ".split("");

export default function Qcow2Lab({ solved, onSolved }: LabProps) {
  const goals = useGoals(
    GOALS.map((g) => g.id),
    solved,
    onSolved,
  );
  const [chain, setChain] = useState<Layer[]>(initialChain);
  const [cluster, setCluster] = useState(0);
  const [letter, setLetter] = useState("E");
  const [path, setPath] = useState<{ cluster: number; depth: number } | null>(null);
  const [msg, setMsg] = useState("Цепочка из одного слоя: база с кластерами 0–3.");
  const maxLen = useRef(1);
  const snaps = useRef(0);
  const dropped = useRef<Record<number, string> | null>(null); // кластеры отброшенного слоя: {c: данные}

  const setNewChain = (c: Layer[]) => {
    setChain(c);
    maxLen.current = Math.max(maxLen.current, c.length);
  };

  function doSnapshot() {
    snaps.current += 1;
    setNewChain(snapshot(chain, snaps.current));
    setPath(null);
    setMsg("Снимок: сверху добавлен пустой слой, прежний заморожен. Ничего не копировалось.");
  }
  function doWrite() {
    const { chain: c, copyUp } = write(chain, cluster, letter);
    setNewChain(c);
    setPath(null);
    setMsg(
      copyUp
        ? `Запись «${letter}» в кластер ${cluster}: кластер лежит в нижнем слое, новая версия появилась только в верхнем (копирование при записи).`
        : `Запись «${letter}» в кластер ${cluster}: кластер выделен в верхнем слое.`,
    );
  }
  function doRead() {
    const r = read(chain, cluster);
    setPath({ cluster, depth: r.depth ?? chain.length });
    setMsg(
      r.value == null
        ? `Кластера ${cluster} нет ни в одном слое: читаются нули (проверено слоёв: ${r.lookups}).`
        : `Кластер ${cluster} = «${r.value}», найден в слое «${r.layer}», обращений к таблицам: ${r.lookups}.`,
    );
    if (r.value != null && r.lookups >= 4 && chain.length >= 4) goals.mark("deep");
    const d = dropped.current;
    if (d && cluster in d && r.value !== d[cluster]) {
      goals.mark("rollback");
      dropped.current = null;
    }
  }
  function doCommit() {
    const c = commit(chain);
    if (!c) return setMsg("Слияние невозможно: слой всего один.");
    setNewChain(c);
    setPath(null);
    setMsg("Слияние: кластеры верхнего слоя перенесены в нижний, цепочка стала короче.");
    if (maxLen.current >= 4 && c.length <= 2) goals.mark("squash");
  }
  function doRevert() {
    const c = revert(chain);
    if (!c) return setMsg("Откат невозможен: слой всего один.");
    const top = chain[0]!.data;
    dropped.current = Object.keys(top).length ? { ...top } : null;
    setNewChain(c);
    setPath(null);
    setMsg(
      Object.keys(top).length
        ? "Откат: верхний слой с записями отброшен. Прочитайте кластер, который вы в него писали."
        : "Откат: пустой верхний слой отброшен.",
    );
  }

  return (
    <div className="vl">
      <div className="vl-grid">
        <div className="vl-card">
          <div className="vl-field">
            <span>кластер</span>
            <div className="vl-seg">
              {Array.from({ length: CLUSTERS }, (_, i) => (
                <button
                  key={i}
                  className={`vl-segbtn ${cluster === i ? "on" : ""}`}
                  onClick={() => setCluster(i)}
                >
                  {i}
                </button>
              ))}
            </div>
          </div>
          <label className="vl-field">
            <span>данные для записи</span>
            <select value={letter} onChange={(e) => setLetter(e.target.value)}>
              {LETTERS.map((l) => (
                <option key={l} value={l}>
                  {l}
                </option>
              ))}
            </select>
          </label>
          <div className="vl-actions wrap">
            <button className="quiz-btn" onClick={doWrite}>Записать</button>
            <button className="quiz-btn" onClick={doRead}>Прочитать</button>
            <button className="quiz-btn ghost" onClick={doSnapshot}>Снимок</button>
            <button className="quiz-btn ghost" onClick={doCommit}>Слить верхний слой</button>
            <button className="quiz-btn ghost" onClick={doRevert}>Откатить верхний слой</button>
          </div>
          <span className="s-label">цели</span>
          <ul className="vl-goals">
            {GOALS.map((g) => (
              <li key={g.id} className={goals.isDone(g.id) ? "ok" : ""}>
                <span className="vl-gm">{goals.isDone(g.id) ? "✓" : "○"}</span>
                <span>{g.text}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="vl-card">
          <div className="pr-res-head">
            <span className="s-label">цепочка слоёв (сверху вниз)</span>
            <span className="pr-res-time">{chain.length} сл.</span>
          </div>
          <div className="vl-layers">
            {chain.map((l, depth) => (
              <div
                key={l.id}
                className={`vl-layer ${path && depth <= path.depth && depth < chain.length ? "walk" : ""}`}
              >
                <span className="vl-lname">{l.name}</span>
                <div className="vl-cells">
                  {Array.from({ length: CLUSTERS }, (_, c) => {
                    const has = c in l.data;
                    const hit = path && path.cluster === c && path.depth === depth;
                    return (
                      <i key={c} className={`${has ? "has" : ""} ${hit ? "hit" : ""}`}>
                        {has ? l.data[c] : ""}
                      </i>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
          <p className="vl-hint">Клетки — кластеры 0…7; подсвечены слои, которые прошло чтение.</p>
          <p className="vl-final">{msg}</p>
        </div>
      </div>
    </div>
  );
}
