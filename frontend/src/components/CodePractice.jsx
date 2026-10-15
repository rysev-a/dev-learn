import { useState } from "react";
import { createPortal } from "react-dom";
import { useSearchParams } from "react-router-dom";
import { FsItem } from "./FsTree.jsx";
import CodeEditor from "./CodeEditor.jsx";

/* Вкладка «Практика»: упражнения с проверкой кода в Docker-песочнице
   (бэкенд /api/exercises). Слева — список со статусами и прогресс, справа —
   одно упражнение: условие, редактор, тесты и логи выполнения. Выбранное
   упражнение живёт в адресе (?task=id), черновик кода и статус — в
   localStorage; логи последнего запуска — в памяти на время сессии. */

const key = (kind, bookId, chapter, taskId) =>
  `say-${kind}-${bookId}:${chapter}:${taskId}`;

const read = (k) => {
  try {
    return localStorage.getItem(k);
  } catch {
    return null;
  }
};
const write = (k, v) => {
  try {
    if (v == null) localStorage.removeItem(k);
    else localStorage.setItem(k, v);
  } catch {
    /* хранилище недоступно — работаем без сохранения */
  }
};

// статус задачи: "ok" — решена, "bad" — последняя проверка не прошла, null — не пробовали
function statusOf(bookId, chapter, taskId) {
  if (read(key("cex", bookId, chapter, taskId)) === "1") return "ok";
  if (read(key("cfail", bookId, chapter, taskId)) === "1") return "bad";
  return null;
}

export function solvedCount(bookId, chapter, tasks) {
  return tasks.filter((t) => statusOf(bookId, chapter, t.id) === "ok").length;
}

// логи последнего запуска каждой задачи: переживают переключение вкладок
const resultCache = new Map();

const langOf = (t) => (t.mode === "sql" || t.mode === "rust" ? t.mode : "python");

export default function CodePractice({
  tasks,
  bookId,
  chapter,
  onSolved,
  itemsSlot,
  nextChapter,
}) {
  const [params, setParams] = useSearchParams();
  const [status, setStatus] = useState(() =>
    Object.fromEntries(tasks.map((t) => [t.id, statusOf(bookId, chapter, t.id)])),
  );
  const [code, setCode] = useState(() =>
    Object.fromEntries(
      tasks.map((t) => [
        t.id,
        read(key("code", bookId, chapter, t.id)) ?? (t.starter || ""),
      ]),
    ),
  );
  const [busy, setBusy] = useState(null);
  const [hint, setHint] = useState({});
  const [, redraw] = useState(0);

  const idx = Math.max(
    0,
    tasks.findIndex((t) => String(t.id) === params.get("task")),
  );
  const task = tasks[idx];
  const ck = key("res", bookId, chapter, task.id);
  const res = resultCache.get(ck) || null;
  const done = tasks.filter((t) => status[t.id] === "ok").length;

  // остальные параметры адреса (fs) сохраняются
  const select = (i) =>
    setParams(
      (prev) => {
        const n = new URLSearchParams(prev);
        n.set("task", String(tasks[i].id));
        return n;
      },
      { replace: true },
    );

  function setStatusFor(id, st) {
    setStatus((p) => ({ ...p, [id]: st }));
    write(key("cex", bookId, chapter, id), st === "ok" ? "1" : null);
    write(key("cfail", bookId, chapter, id), st === "bad" ? "1" : null);
    if (onSolved) onSolved();
  }

  function edit(value) {
    setCode((p) => ({ ...p, [task.id]: value }));
    write(key("code", bookId, chapter, task.id), value);
    // правка после успеха снимает «решено»
    if (status[task.id] === "ok") setStatusFor(task.id, null);
  }

  function reset() {
    edit(task.starter || "");
    write(key("code", bookId, chapter, task.id), null);
    resultCache.delete(ck);
    setStatusFor(task.id, null);
  }

  async function run() {
    if (busy != null) return;
    const id = task.id;
    const rk = ck;
    setBusy(id);
    try {
      const r = await fetch("/api/exercises/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          book: Number(bookId),
          chapter: Number(chapter),
          task: id,
          code: code[id],
        }),
      });
      const data = await r.json();
      if (!r.ok) throw new Error(data.detail || "Не удалось запустить проверку");
      const passed = data.results.filter((x) => x.ok).length;
      const okAll = data.status === "ok" && passed === data.results.length;
      resultCache.set(rk, { ...data, passed, okAll, at: new Date() });
      setStatusFor(id, okAll ? "ok" : "bad");
    } catch (e) {
      resultCache.set(rk, { status: "error", stderr: e.message, results: [], at: new Date() });
      setStatusFor(id, "bad");
    } finally {
      setBusy(null);
      redraw((n) => n + 1);
    }
  }

  const running = busy === task.id;
  const solved = status[task.id] === "ok";
  const hasNext = idx < tasks.length - 1 || !!nextChapter;

  // решено → дальше: следующее упражнение или первое упражнение следующей главы
  function goNext() {
    if (idx < tasks.length - 1) select(idx + 1);
    else if (nextChapter) nextChapter.open();
  }
  // Ctrl/Cmd+Enter: проверить; если уже решено — перейти дальше
  const primary = () => (solved && hasNext ? goNext() : run());

  return (
    <section className="pr">
      <div className="pr-top">
        <span className="pr-top-label">
          Решено {done} из {tasks.length}
        </span>
        <div
          className="pr-bar"
          role="progressbar"
          aria-valuemin={0}
          aria-valuemax={tasks.length}
          aria-valuenow={done}
        >
          <i style={{ width: `${(done / tasks.length) * 100}%` }} />
        </div>
        <span className="pr-top-label">
          {tasks.every((t) => t.mode === "sql")
            ? "sql · sqlite"
            : tasks.every((t) => t.mode === "rust")
              ? "rust"
              : "python"}{" "}
          · docker
        </span>
      </div>

      <div className={`pr-body ${itemsSlot ? "single" : ""}`}>
        {itemsSlot ? (
          createPortal(
            tasks.map((t, i) => (
              <FsItem
                key={t.id}
                on={i === idx}
                num={i + 1}
                mark={status[t.id] === "ok" ? "✓" : status[t.id] === "bad" ? "✗" : undefined}
                status={status[t.id] || ""}
                onClick={() => select(i)}
              >
                {t.title}
              </FsItem>
            )),
            itemsSlot,
          )
        ) : (
        <aside className="pr-list" aria-label="Упражнения">
          {tasks.map((t, i) => {
            const st = status[t.id];
            return (
              <button
                key={t.id}
                className={`pr-item ${i === idx ? "on" : ""} ${st || ""}`}
                onClick={() => select(i)}
              >
                <span className="pr-mark">
                  {st === "ok" ? "✓" : st === "bad" ? "✗" : i + 1}
                </span>
                <span className="pr-name">{t.title}</span>
              </button>
            );
          })}
        </aside>
        )}

        <div className="pr-main" key={task.id}>
          <div className="pr-head">
            <h3>
              {idx + 1}. {task.title}
            </h3>
            <span className={`pr-badge ${status[task.id] || ""}`}>
              {status[task.id] === "ok"
                ? "выполнено"
                : status[task.id] === "bad"
                  ? "не пройдено"
                  : "не решено"}
            </span>
          </div>
          <p className="pr-statement">{task.statement}</p>

          <CodeEditor
            className={status[task.id] === "ok" ? "right" : ""}
            lang={langOf(task)}
            value={code[task.id]}
            onChange={edit}
            onRun={primary}
          />

          <div className="ex-row">
            {solved && hasNext ? (
              <button
                className="quiz-btn"
                onClick={goNext}
                title="Дальше (Ctrl+Enter)"
              >
                {idx < tasks.length - 1 ? "Дальше →" : "Следующая глава →"}
              </button>
            ) : (
              <button
                className="quiz-btn"
                onClick={run}
                disabled={busy != null}
                title="Проверить (Ctrl+Enter)"
              >
                {running ? "Запускаю…" : solved ? "✓ Решено — ещё раз" : "Проверить"}
              </button>
            )}
            {task.hint && (
              <button
                className="quiz-btn ghost"
                onClick={() => setHint((p) => ({ ...p, [task.id]: !p[task.id] }))}
              >
                {hint[task.id] ? "Скрыть подсказку" : "Подсказка"}
              </button>
            )}
            {solved && hasNext && (
              <button
                className="quiz-btn ghost"
                onClick={run}
                disabled={busy != null}
                title="Запустить проверку ещё раз"
              >
                {running ? "Запускаю…" : "Проверить ещё раз"}
              </button>
            )}
            <button className="quiz-btn ghost" onClick={reset} title="Вернуть исходный шаблон">
              Сбросить
            </button>
          </div>
          {hint[task.id] && task.hint && <p className="ex-hint">{task.hint}</p>}

          <Results res={res} running={running} />
        </div>
      </div>
    </section>
  );
}

function Results({ res, running }) {
  if (running)
    return (
      <div className="pr-res">
        <p className="pr-empty">Запускаю в песочнице…</p>
      </div>
    );
  if (!res)
    return (
      <div className="pr-res">
        <p className="pr-empty">
          Нажмите «Проверить» (Ctrl/Cmd+Enter): здесь появятся тесты и логи выполнения. Когда упражнение решено, Ctrl/Cmd+Enter ведёт к следующему.
        </p>
      </div>
    );
  const total = res.results.length;
  // в режиме «вывод» программа печатает в перехваченный поток: её вывод лежит в got
  const one = total === 1 ? res.results[0] : null;
  const program =
    res.stdout || (one && !one.args && !one.error && typeof one.got === "string" ? one.got : "");
  return (
    <div className="pr-res">
      <div className="pr-res-block">
        <div className="pr-res-head">
          <span className="s-label">тесты</span>
          {total > 0 && (
            <span className={`pr-res-sum ${res.okAll ? "ok" : "bad"}`}>
              {res.passed} из {total}
            </span>
          )}
          {res.at && <span className="pr-res-time">{res.at.toLocaleTimeString("ru-RU")}</span>}
        </div>
        {res.status === "timeout" && (
          <p className="ex-note">
            Проверка не уложилась в лимит времени — возможно, в коде бесконечный цикл.
          </p>
        )}
        {total === 0 && res.status !== "timeout" && (
          <p className="pr-empty">Тесты не запускались — смотрите логи ниже.</p>
        )}
        <ul className="pr-tests">
          {res.results.map((r, k) => (
            <li key={k} className={`pr-test ${r.ok ? "ok" : "bad"}`}>
              <div className="pr-test-head">
                <span className="cx-mark">{r.ok ? "✓" : "✗"}</span>
                <span>тест {k + 1}</span>
                {r.args && <code className="cx-args">вызов {r.args}</code>}
              </div>
              {!r.ok &&
                (r.error ? (
                  <pre className="cx-error">{r.error}</pre>
                ) : (
                  <div className="pr-diff">
                    <div>
                      <span className="s-label">ожидалось</span>
                      <pre>{String(r.expected)}</pre>
                    </div>
                    <div>
                      <span className="s-label">получено</span>
                      <pre>{r.got === "" || r.got == null ? "(пусто)" : String(r.got)}</pre>
                    </div>
                  </div>
                ))}
            </li>
          ))}
        </ul>
      </div>

      <div className="pr-res-block">
        <div className="pr-res-head">
          <span className="s-label">логи выполнения</span>
        </div>
        {program ? (
          <pre className="pr-log">{program}</pre>
        ) : (
          <p className="pr-empty">программа ничего не вывела</p>
        )}
        {res.stderr && res.status !== "timeout" && <pre className="cx-error">{res.stderr}</pre>}
      </div>
    </div>
  );
}
