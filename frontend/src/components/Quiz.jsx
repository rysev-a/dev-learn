import { useState } from "react";
import { createPortal } from "react-dom";
import { FsItem } from "./FsTree.jsx";
import { quizPicks, saveQuizPicks } from "../lib/progress.js";

/* Квизы на теорию: вопросы с вариантами, ответ проверяется сразу при выборе. */
export default function Quiz({ quiz, bookId, chapter, itemsSlot }) {
  return <TheoryQuiz quiz={quiz} bookId={bookId} chapter={chapter} itemsSlot={itemsSlot} />;
}

function TheoryQuiz({ quiz, bookId, chapter, itemsSlot }) {
  // ответы сохраняются в браузере: по ним считается прогресс на главной
  const [picked, setPicked] = useState(() => {
    const saved = bookId != null ? quizPicks(bookId, chapter) : null;
    return saved && saved.length === quiz.questions.length
      ? saved
      : Array(quiz.questions.length).fill(null);
  });
  const persist = (next) => {
    if (bookId != null) saveQuizPicks(bookId, chapter, next.some((p) => p != null) ? next : null);
    return next;
  };

  const total = quiz.questions.length;
  const answered = picked.filter((p) => p != null).length;
  const score = quiz.questions.reduce(
    (acc, q, i) => acc + (picked[i] === q.answer ? 1 : 0),
    0,
  );
  const done = answered === total;

  function pick(qi, oi) {
    if (picked[qi] != null) return; // на вопрос уже ответили
    setPicked((prev) => persist(prev.map((p, i) => (i === qi ? oi : p))));
  }

  function reset() {
    setPicked(persist(Array(quiz.questions.length).fill(null)));
  }

  // в полноэкранном режиме вопросы — пункты левого дерева с отметками
  const goTo = (qi) =>
    document.getElementById(`quiz-q-${qi}`)?.scrollIntoView({ behavior: "smooth", block: "start" });

  return (
    <section className="quiz">
      {itemsSlot &&
        createPortal(
          quiz.questions.map((q, qi) => (
            <FsItem
              key={qi}
              num={qi + 1}
              mark={picked[qi] == null ? undefined : picked[qi] === q.answer ? "✓" : "✗"}
              status={picked[qi] == null ? "" : picked[qi] === q.answer ? "ok" : "bad"}
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
        const answeredQ = picked[qi] != null;
        return (
          <div className="quiz-q" key={qi} id={`quiz-q-${qi}`}>
            <p className="quiz-q-text">
              {qi + 1}. {q.q}
            </p>
            <div className="quiz-opts">
              {q.options.map((opt, oi) => {
                let cls = "";
                if (answeredQ) {
                  if (oi === q.answer) cls = "right";
                  else if (picked[qi] === oi) cls = "wrong";
                }
                return (
                  <button
                    key={oi}
                    className={`quiz-opt ${cls}`}
                    disabled={answeredQ}
                    onClick={() => pick(qi, oi)}
                  >
                    {opt}
                  </button>
                );
              })}
            </div>
            {answeredQ && q.expl && <p className="quiz-q-expl">{q.expl}</p>}
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
