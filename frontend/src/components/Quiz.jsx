import { useState } from "react";

/* Квизы на теорию: вопросы с вариантами, ответ проверяется сразу при выборе. */
export default function Quiz({ quiz }) {
  return <TheoryQuiz quiz={quiz} />;
}

function TheoryQuiz({ quiz }) {
  const [picked, setPicked] = useState(() =>
    Array(quiz.questions.length).fill(null),
  );

  const total = quiz.questions.length;
  const answered = picked.filter((p) => p != null).length;
  const score = quiz.questions.reduce(
    (acc, q, i) => acc + (picked[i] === q.answer ? 1 : 0),
    0,
  );
  const done = answered === total;

  function pick(qi, oi) {
    if (picked[qi] != null) return; // на вопрос уже ответили
    setPicked((prev) => prev.map((p, i) => (i === qi ? oi : p)));
  }

  function reset() {
    setPicked(Array(quiz.questions.length).fill(null));
  }

  return (
    <section className="quiz">
      <div className="quiz-head">
        <h3>{quiz.title}</h3>
        <span className="quiz-lang">
          теория{answered > 0 ? ` · ${score}/${answered}` : ""}
        </span>
      </div>

      {quiz.questions.map((q, qi) => {
        const answeredQ = picked[qi] != null;
        return (
          <div className="quiz-q" key={qi}>
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
