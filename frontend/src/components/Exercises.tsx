import { useEffect, useState } from "react";
import { api } from "../lib/api.ts";
import { useProgress } from "../lib/progress.tsx";
import type { PracticeSet } from "../types.ts";

/* Упражнения: задачи с вводом ответа. Верные ответы знает только сервер, он же проверяет введённое; ответ показать
   нельзя (по замыслу курса), только подсказку; сложность внутри главы растёт постепенно. */
type Verdict = "" | "right" | "wrong";

interface ExercisesProps {
  bookId: string | undefined;
  chapter: number;
}

export default function Exercises({ bookId, chapter }: ExercisesProps) {
  const progress = useProgress();
  const [set, setSet] = useState<PracticeSet | null>(null);
  const [failed, setFailed] = useState<string | null>(null);
  const [vals, setVals] = useState<string[]>([]);
  const [st, setSt] = useState<Verdict[]>([]);
  const [hints, setHints] = useState<boolean[]>([]);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (bookId == null) return undefined;
    let live = true;
    setSet(null);
    setFailed(null);
    api<PracticeSet>(`/api/answers/${bookId}/${chapter}`)
      .then((d) => {
        if (!live) return;
        setSet(d);
        setVals(d.tasks.map((_, i) => d.solved[i] ?? ""));
        setSt(d.tasks.map((_, i): Verdict => (d.solved[i] != null ? "right" : "")));
        setHints(Array(d.tasks.length).fill(false));
      })
      .catch((e: Error) => live && setFailed(e.message));
    return () => {
      live = false;
    };
  }, [bookId, chapter]);

  if (failed) return <p className="error">{failed}</p>;
  if (!set || bookId == null) return <p className="empty">Загрузка…</p>;

  const total = set.tasks.length;
  const solved = st.filter((s) => s === "right").length;

  function setVal(i: number, v: string) {
    if (st[i] === "right") return;
    setVals((prev) => prev.map((p, k) => (k === i ? v : p)));
    // снятие «неверно» при новой правке
    if (st[i] === "wrong") setSt((prev) => prev.map((p, k) => (k === i ? "" : p)));
  }

  async function check(i: number) {
    if (busy || st[i] === "right") return;
    const value = vals[i] ?? "";
    if (!value.trim()) return;
    setBusy(true);
    try {
      const r = await api<{ ok: boolean }>(`/api/answers/${bookId}/${chapter}/check`, {
        method: "POST",
        body: { task: i, value },
      });
      setSt((prev) => prev.map((p, k): Verdict => (k === i ? (r.ok ? "right" : "wrong") : p)));
      if (r.ok) progress.recordAnswer(bookId!, chapter, i, value.trim());
    } finally {
      setBusy(false);
    }
  }

  function toggleHint(i: number) {
    setHints((prev) => prev.map((p, k) => (k === i ? !p : p)));
  }

  function reset() {
    progress.resetAnswers(bookId!, chapter);
    setVals(Array(total).fill(""));
    setSt(Array(total).fill(""));
    setHints(Array(total).fill(false));
  }

  return (
    <section className="quiz">
      <div className="quiz-head">
        <h3>{set.title}</h3>
        <span className="quiz-lang">
          упражнения{solved > 0 ? ` · решено ${solved}/${total}` : ""}
        </span>
      </div>

      {set.tasks.map((t, i) => {
        const right = st[i] === "right";
        const wrong = st[i] === "wrong";
        return (
          <div className="quiz-q" key={i}>
            <p className="quiz-q-text">
              {i + 1}. {t.q}
            </p>
            <div className="ex-row">
              <input
                className={`ex-input ${right ? "right" : wrong ? "wrong" : ""}`}
                value={vals[i] ?? ""}
                placeholder="Ответ"
                disabled={right}
                onChange={(e) => setVal(i, e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") void check(i);
                }}
              />
              <button className="quiz-btn" onClick={() => void check(i)} disabled={right || busy} title="Проверить">
                {right ? "✓" : "Проверить"}
              </button>
            </div>
            {wrong && <p className="ex-note">Пока неверно — попробуй ещё раз или загляни в подсказку.</p>}
            {t.hint && (
              <div className="ex-hint-row">
                <button className="quiz-btn ghost small" onClick={() => toggleHint(i)}>
                  {hints[i] ? "Скрыть подсказку" : "Подсказка"}
                </button>
                {hints[i] && <p className="ex-hint">{t.hint}</p>}
              </div>
            )}
          </div>
        );
      })}

      {solved > 0 && (
        <div className="quiz-actions">
          <button className="quiz-btn ghost" onClick={reset}>
            Начать заново
          </button>
        </div>
      )}

      {solved === total && (
        <div className="quiz-result ok">
          <p className="quiz-ok-line">
            ✓ Все задачи решены: {solved}/{total}
          </p>
        </div>
      )}
    </section>
  );
}
