import { useState } from "react";

/* Упражнения с проверкой кода в Docker-песочнице (бэкенд /api/exercises).
   Редактор — простая моноширинная textarea (Tab вставляет 4 пробела);
   проверка всегда на сервере. Решения отмечаются в localStorage. */

function solvedKey(bookId, chapter, taskId) {
  return `say-cex-${bookId}:${chapter}:${taskId}`;
}

function loadSolved(bookId, chapter, tasks) {
  return tasks.map(
    (t) => localStorage.getItem(solvedKey(bookId, chapter, t.id)) === "1",
  );
}

export default function CodeExercises({ tasks, bookId, chapter }) {
  const [code, setCode] = useState(() => tasks.map((t) => t.starter || ""));
  const [solved, setSolved] = useState(() =>
    loadSolved(bookId, chapter, tasks),
  );
  const [busy, setBusy] = useState(() => tasks.map(() => false));
  const [results, setResults] = useState(() => tasks.map(() => null));
  const [hints, setHints] = useState(() => tasks.map(() => false));

  const total = tasks.length;
  const done = solved.filter(Boolean).length;

  function setCodeAt(i, value) {
    setCode((prev) => prev.map((p, k) => (k === i ? value : p)));
    // правка после успеха снимает «решено»
    if (solved[i]) {
      setSolved((prev) => prev.map((p, k) => (k === i ? false : p)));
      localStorage.removeItem(solvedKey(bookId, chapter, tasks[i].id));
    }
    if (results[i])
      setResults((prev) => prev.map((p, k) => (k === i ? null : p)));
  }

  function editorKeyDown(e, i) {
    if (e.key === "Tab") {
      e.preventDefault();
      const el = e.currentTarget;
      const { selectionStart: s, selectionEnd: en } = el;
      const next = code[i].slice(0, s) + "    " + code[i].slice(en);
      setCodeAt(i, next);
      requestAnimationFrame(() => {
        el.selectionStart = el.selectionEnd = s + 4;
      });
    }
    // Ctrl/Cmd+Enter — проверить
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      run(i);
    }
  }

  async function run(i) {
    if (busy[i]) return;
    const t = tasks[i];
    setBusy((prev) => prev.map((p, k) => (k === i ? true : p)));
    setResults((prev) => prev.map((p, k) => (k === i ? null : p)));
    try {
      const r = await fetch("/api/exercises/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          book: Number(bookId),
          chapter: Number(chapter),
          task: t.id,
          code: code[i],
        }),
      });
      const data = await r.json();
      if (!r.ok)
        throw new Error(data.detail || "Не удалось запустить проверку");
      const passed = data.results.filter((x) => x.ok).length;
      const okAll = data.status === "ok" && passed === data.results.length;
      if (okAll) {
        setSolved((prev) => prev.map((p, k) => (k === i ? true : p)));
        localStorage.setItem(solvedKey(bookId, chapter, t.id), "1");
      }
      setResults((prev) =>
        prev.map((p, k) => (k === i ? { ...data, passed, okAll } : p)),
      );
    } catch (e) {
      setResults((prev) =>
        prev.map((p, k) =>
          k === i ? { status: "error", stderr: e.message, results: [] } : p,
        ),
      );
    } finally {
      setBusy((prev) => prev.map((p, k) => (k === i ? false : p)));
    }
  }

  return (
    <section className="quiz">
      <div className="quiz-head">
        <h3>Практика в песочнице</h3>
        <span className="quiz-lang">
          python · docker{done > 0 ? ` · решено ${done}/${total}` : ""}
        </span>
      </div>

      {tasks.map((t, i) => {
        const res = results[i];
        const ok = solved[i];
        return (
          <div className="quiz-q" key={t.id}>
            <p className="quiz-q-text">
              {i + 1}. {t.title}. {t.statement}
            </p>
            <textarea
              className={`cx-editor ${ok ? "right" : ""}`}
              value={code[i]}
              rows={Math.max(4, code[i].split("\n").length + 1)}
              spellCheck={false}
              onChange={(e) => setCodeAt(i, e.target.value)}
              onKeyDown={(e) => editorKeyDown(e, i)}
            />
            <div className="ex-row">
              <button
                className="quiz-btn"
                onClick={() => run(i)}
                disabled={busy[i]}
                title="Проверить (Ctrl+Enter)"
              >
                {busy[i] ? "Запускаю…" : ok ? "✓ Решено" : "Проверить"}
              </button>
              {t.hint && (
                <button
                  className="quiz-btn ghost"
                  onClick={() =>
                    setHints((prev) => prev.map((p, k) => (k === i ? !p : p)))
                  }
                >
                  {hints[i] ? "Скрыть подсказку" : "Подсказка"}
                </button>
              )}
              {ok && (
                <button
                  className="quiz-btn ghost"
                  onClick={() => setCodeAt(i, tasks[i].starter || "")}
                  title="Вернуть исходный шаблон"
                >
                  Сбросить
                </button>
              )}
            </div>

            {hints[i] && t.hint && <p className="ex-hint">{t.hint}</p>}

            {res && res.status === "timeout" && (
              <p className="ex-note">
                Проверка не уложилась в лимит времени — возможно, в коде
                бесконечный цикл.
              </p>
            )}
            {res && res.status !== "timeout" && res.stderr && (
              <pre className="cx-error">{res.stderr}</pre>
            )}
            {res && res.results && res.results.length > 1 && (
              <ul className="cx-tests">
                {res.results.map((r, k) => (
                  <li key={k} className={r.ok ? "ok" : "bad"}>
                    <span className="cx-mark">{r.ok ? "✓" : "✗"}</span>
                    <span className="cx-test-body">
                      {r.args && (
                        <span className="cx-args">вызов {r.args}</span>
                      )}
                      {!r.ok && (
                        <span className="cx-diff">
                          {r.error
                            ? r.error
                            : `ожидалось ${r.expected}, получено ${r.got}`}
                        </span>
                      )}
                    </span>
                  </li>
                ))}
              </ul>
            )}
            {res &&
              res.results &&
              res.results.length === 1 &&
              !res.results[0].ok && (
                <p className="ex-note">
                  {res.results[0].error ||
                    `Ожидалось:\n${res.results[0].expected}\n\nПолучено:\n${res.results[0].got}`}
                </p>
              )}
            {res && res.stdout && (
              <div className="cx-stdout">
                <span className="s-label">вывод программы</span>
                <pre>{res.stdout}</pre>
              </div>
            )}
          </div>
        );
      })}
    </section>
  );
}
