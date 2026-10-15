import { useState } from "react";
import { answerSolved, saveAnswerSolved } from "../lib/progress.js";

/* Нормализация ввода: пробелы, регистр, запятая как десятичный разделитель. */
function normalize(s) {
  return String(s)
    .trim()
    .toLowerCase()
    .replace(/\s+/g, " ")
    .replace(/,(\d)/, ".$1");
}

function isNumeric(s) {
  return /^-?\d+(\.\d+)?$/.test(s);
}

function isCorrect(input, answers) {
  const a = normalize(input);
  if (!a) return false;
  return answers.some((ans) => {
    const b = normalize(ans);
    if (isNumeric(a) && isNumeric(b)) {
      return Math.abs(parseFloat(a) - parseFloat(b)) < 1e-9;
    }
    return a === b;
  });
}

/* Упражнения: задачи с вводом ответа. Ответ показать нельзя (по замыслу
   курса), только подсказку; сложность внутри главы растёт постепенно. */
export default function Exercises({ quiz, bookId, chapter }) {
  // решённые задачи (с ответами) помнит браузер — по ним считается прогресс
  const saved = bookId != null ? answerSolved(bookId, chapter) : {};
  const [vals, setVals] = useState(() =>
    quiz.tasks.map((_, i) => saved[i] ?? ""),
  );
  const [st, setSt] = useState(() =>
    quiz.tasks.map((_, i) => (saved[i] != null ? "right" : "")),
  );
  const persist = (nextVals, nextSt) => {
    if (bookId == null) return;
    const map = {};
    nextSt.forEach((s, i) => {
      if (s === "right") map[i] = nextVals[i];
    });
    saveAnswerSolved(bookId, chapter, map);
  };
  const [hints, setHints] = useState(() =>
    Array(quiz.tasks.length).fill(false),
  );

  const total = quiz.tasks.length;
  const solved = st.filter((s) => s === "right").length;

  function setVal(i, v) {
    if (st[i] === "right") return;
    setVals((prev) => prev.map((p, k) => (k === i ? v : p)));
    // снятие «неверно» при новой правке
    if (st[i] === "wrong")
      setSt((prev) => prev.map((p, k) => (k === i ? "" : p)));
  }

  function check(i) {
    if (st[i] === "right") return;
    const next = st.map((p, k) =>
      k === i ? (isCorrect(vals[i], quiz.tasks[i].answers) ? "right" : "wrong") : p,
    );
    setSt(next);
    persist(vals, next);
  }

  function toggleHint(i) {
    setHints((prev) => prev.map((p, k) => (k === i ? !p : p)));
  }

  function reset() {
    setVals(Array(quiz.tasks.length).fill(""));
    setSt(Array(quiz.tasks.length).fill(""));
    persist([], []);
    setHints(Array(quiz.tasks.length).fill(false));
  }

  return (
    <section className="quiz">
      <div className="quiz-head">
        <h3>{quiz.title}</h3>
        <span className="quiz-lang">
          упражнения{solved > 0 ? ` · решено ${solved}/${total}` : ""}
        </span>
      </div>

      {quiz.tasks.map((t, i) => {
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
                value={vals[i]}
                placeholder="Ответ"
                disabled={right}
                onChange={(e) => setVal(i, e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") check(i);
                }}
              />
              <button
                className="quiz-btn"
                onClick={() => check(i)}
                disabled={right}
                title="Проверить"
              >
                {right ? "✓" : "Проверить"}
              </button>
            </div>
            {wrong && (
              <p className="ex-note">
                Пока неверно — попробуй ещё раз или загляни в подсказку.
              </p>
            )}
            {t.hint && (
              <div className="ex-hint-row">
                <button
                  className="quiz-btn ghost small"
                  onClick={() => toggleHint(i)}
                >
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
