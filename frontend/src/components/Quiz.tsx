import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import type { Quiz as QuizData, QuizAnswerResult, QuizReveal } from "../types.ts";
import { api } from "../lib/api.ts";
import { FsItem } from "./FsTree.tsx";
import { useProgress } from "../lib/progress.tsx";

interface QuizProps {
  bookId: string | undefined;
  chapter: number;
  itemsSlot: HTMLElement | null;
}

/* Квизы на теорию: вопросы с вариантами, ответ проверяется сразу при выборе — на сервере. Верный ответ и пояснение
   сервер отдаёт только после выбора, поэтому в браузере их заранее нет. Выбранные варианты хранятся в кабинете:
   по ним считается прогресс на главной. */
export default function Quiz({ bookId, chapter, itemsSlot }: QuizProps) {
  const progress = useProgress();
  const [quiz, setQuiz] = useState<QuizData | null>(null);
  const [failed, setFailed] = useState<string | null>(null);
  const [reveal, setReveal] = useState<(QuizReveal | null)[]>([]);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (bookId == null) return undefined;
    let live = true;
    setQuiz(null);
    setFailed(null);
    api<QuizData>(`/api/quizzes/${bookId}/${chapter}`)
      .then((d) => {
        if (!live) return;
        setQuiz(d);
        setReveal(d.reveal);
      })
      .catch((e: Error) => live && setFailed(e.message));
    return () => {
      live = false;
    };
  }, [bookId, chapter]);

  if (failed) return <p className="error">{failed}</p>;
  if (!quiz || bookId == null) return <p className="empty">Загрузка…</p>;

  const total = quiz.questions.length;
  const picks = progress.quizPicks(bookId, chapter) ?? [];
  const pickOf = (qi: number) => picks[qi] ?? null;
  const answered = picks.filter((p) => p != null).length;
  const score = progress.quizRight(bookId, chapter);
  const done = answered === total;
  const isRight = (qi: number) => {
    const r = reveal[qi];
    return r != null && pickOf(qi) === r.answer;
  };

  async function pick(qi: number, oi: number) {
    if (busy || reveal[qi] != null) return; // на вопрос уже ответили
    setBusy(true);
    try {
      const r = await api<QuizAnswerResult>(`/api/quizzes/${bookId}/${chapter}/answer`, {
        method: "POST",
        body: { question: qi, pick: oi },
      });
      setReveal((cur) => cur.map((x, i) => (i === qi ? { answer: r.answer, expl: r.expl } : x)));
      progress.recordQuizPick(bookId!, chapter, qi, total, r.pick, r.right);
    } finally {
      setBusy(false);
    }
  }

  function reset() {
    progress.resetQuiz(bookId!, chapter);
    setReveal(Array(total).fill(null));
  }

  // в полноэкранном режиме вопросы — пункты левого дерева с отметками
  const goTo = (qi: number) =>
    document.getElementById(`quiz-q-${qi}`)?.scrollIntoView({ behavior: "smooth", block: "start" });

  return (
    <section className="quiz">
      {itemsSlot &&
        createPortal(
          quiz.questions.map((_, qi) => (
            <FsItem
              key={qi}
              num={qi + 1}
              mark={reveal[qi] == null ? undefined : isRight(qi) ? "✓" : "✗"}
              status={reveal[qi] == null ? "" : isRight(qi) ? "ok" : "bad"}
              onClick={() => goTo(qi)}
            >
              Вопрос {qi + 1}
            </FsItem>
          )),
          itemsSlot,
        )}
      <div className="quiz-head">
        <h3>{quiz.title}</h3>
        <span className="quiz-lang">
          теория{answered > 0 ? ` · ${score}/${answered}` : ""}
        </span>
      </div>

      {quiz.questions.map((q, qi) => {
        const r = reveal[qi] ?? null;
        return (
          <div className="quiz-q" key={qi} id={`quiz-q-${qi}`}>
            <p className="quiz-q-text">
              {qi + 1}. {q.q}
            </p>
            <div className="quiz-opts">
              {q.options.map((opt, oi) => {
                let cls = "";
                if (r) {
                  if (oi === r.answer) cls = "right";
                  else if (pickOf(qi) === oi) cls = "wrong";
                }
                return (
                  <button
                    key={oi}
                    className={`quiz-opt ${cls}`}
                    disabled={r != null || busy}
                    onClick={() => void pick(qi, oi)}
                  >
                    {opt}
                  </button>
                );
              })}
            </div>
            {r && r.expl && <p className="quiz-q-expl">{r.expl}</p>}
          </div>
        );
      })}

      {answered > 0 && (
        <div className="quiz-actions">
          <button className="quiz-btn ghost" onClick={reset}>
            Пройти ещё раз
          </button>
        </div>
      )}

      {done && (
        <div className={`quiz-result ${score === total ? "ok" : "fail"}`}>
          <p className="quiz-ok-line">
            {score === total
              ? `✓ Отлично: ${score}/${total}`
              : `Результат: ${score}/${total}`}
          </p>
        </div>
      )}
    </section>
  );
}
