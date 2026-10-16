import { SetStateAction, useState } from "react";
import { GOALS, SIZE, device, free, initial, post, reap } from "./virtq.ts";
import { useGoals } from "./goals.ts";

/* Симулятор виртуальной очереди virtio (глава 6): гость кладёт буферы, устройство их обрабатывает,
   гость забирает результат. Считаются оповещения — выходы в гипервизор. */

export default function VirtqLab({ solved, onSolved }) {
  const goals = useGoals(
    GOALS.map((g) => g.id),
    solved,
    onSolved,
  );
  const [s, setS] = useState(initial);
  const [suppress, setSuppress] = useState(false);
  const [note, setNote] = useState("Очередь пуста: 8 свободных дескрипторов.");

  function apply(next: SetStateAction<{ avail: number; used: number; busy: boolean; notifies: number; posted: number; processed: number; overflow: boolean; }>, text: SetStateAction<string>) {
    setS(next);
    setNote(text);
    for (const g of GOALS) if (g.check(next, { suppress })) goals.mark(g.id);
  }
  const doPost = (n: number) => {
    const t = post(s, n, suppress);
    if (t.overflow)
      return apply(t, `Свободных дескрипторов ${free(s)}, а нужно ${n}: очередь переполнена, гость ждёт.`);
    const rang = t.notifies > s.notifies;
    apply(
      t,
      rang
        ? `Положено ${n}; оповещение отправлено (выход в гипервизор).`
        : `Положено ${n}; устройство занято и само увидит буферы — оповещение не нужно.`,
    );
  };
  const doDevice = () => {
    if (!s.busy || s.avail === 0)
      return setNote("Устройство спит: пока гость не оповестит, оно ничего не обрабатывает.");
    apply(device(s), "Устройство обработало один буфер и положило его в использованное кольцо.");
  };
  const doReap = () => apply(reap(s), "Гость забрал готовые буферы: дескрипторы свободны.");
  const reset = () => {
    setS(initial());
    setNote("Очередь сброшена.");
  };

  const cells = [];
  for (let i = 0; i < SIZE; i++)
    cells.push(i < s.used ? "used" : i < s.used + s.avail ? "avail" : "free");

  return (
    <div className="vl">
      <div className="vl-grid">
        <div className="vl-card">
          <label className="vl-check">
            <input
              type="checkbox"
              checked={suppress}
              onChange={(e) => setSuppress(e.target.checked)}
            />
            <span>подавление оповещений: звонить, только если устройство спит</span>
          </label>
          <div className="vl-actions wrap">
            <button className="quiz-btn" onClick={() => doPost(1)}>Гость: положить 1 буфер</button>
            <button className="quiz-btn" onClick={() => doPost(3)}>Гость: положить пачку из 3</button>
            <button className="quiz-btn ghost" onClick={doDevice}>Устройство: обработать 1</button>
            <button className="quiz-btn ghost" onClick={doReap}>Гость: забрать готовые</button>
            <button className="quiz-btn ghost" onClick={reset}>Сбросить</button>
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
            <span className="s-label">дескрипторы очереди</span>
            <span className="pr-res-time">свободно {free(s)} из {SIZE}</span>
          </div>
          <div className="vl-desc">
            {cells.map((c, i) => (
              <i key={i} className={c}>{c === "free" ? "" : c === "avail" ? "→" : "✓"}</i>
            ))}
          </div>
          <p className="vl-hint">
            серые — свободны, синие — ждут устройство (доступное кольцо), зелёные — обработаны, ждут гостя
            (использованное кольцо).
          </p>
          <table className="vl-stat">
            <tbody>
              <tr><td>устройство</td><td>{s.busy ? "занято" : "спит"}</td></tr>
              <tr><td>положено буферов</td><td>{s.posted}</td></tr>
              <tr><td>обработано</td><td>{s.processed}</td></tr>
              <tr><td><b>оповещений (выходов)</b></td><td><b>{s.notifies}</b></td></tr>
            </tbody>
          </table>
          <p className="vl-final">{note}</p>
        </div>
      </div>
    </div>
  );
}
