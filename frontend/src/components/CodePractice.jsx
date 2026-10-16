import {
  lazy,
  Suspense,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";
import { useSearchParams } from "react-router-dom";
import { api } from "../lib/api.js";
import { useAuth } from "../lib/auth.jsx";
import { useProgress } from "../lib/progress.jsx";
import CodeEditor from "./CodeEditor.jsx";
import SqlDiff from "./SqlDiff.jsx";
import SqlSchema from "./SqlSchema.jsx";
import PracticeShell from "./PracticeShell.jsx";

// Симуляторы книги «Виртуализация» (задачи режима lab среди код-задач) грузятся лениво
const VirtLab = lazy(() => import("../virtlab/VirtLab.jsx"));

/* Вкладка «Практика»: упражнения с проверкой кода в Docker-песочнице
   (бэкенд /api/exercises). Слева — список со статусами и прогресс, справа —
   одно упражнение: условие, редактор, тесты, логи и история попыток.

   Всё, что набрал пользователь, живёт в кабинете на сервере: статусы задач
   (решённая остаётся решённой), черновик кода (сохраняется сам) и история
   попыток — клик по попытке возвращает её код в редактор. Выбранное упражнение —
   в адресе (?task=id), логи последнего запуска — в памяти на время сессии. */

const langOf = (t) =>
  t.mode === "sql" || t.mode === "rust" || t.mode === "c" || t.mode === "js"
    ? t.mode
    : "python";
const SAVE_DELAY = 700;

// логи последнего запуска каждой задачи переживают переключение вкладок
const resultCache = new Map();

const fmtDate = (iso) =>
  new Date(iso).toLocaleString("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });

export default function CodePractice({
  tasks,
  bookId,
  chapter,
  itemsSlot,
  nextChapter,
}) {
  const { user } = useAuth();
  const progress = useProgress();
  const [params, setParams] = useSearchParams();
  const status = progress.codeStatus(bookId, chapter);

  // черновики приходят с сервера; null — ещё грузятся
  const [code, setCode] = useState(null);
  const [attempts, setAttempts] = useState({}); // id задачи → попытки, новые первыми
  const [busy, setBusy] = useState(null);
  const [hint, setHint] = useState({});
  const [, redraw] = useState(0);

  const base = `/api/exercises/${bookId}/${chapter}`;

  useEffect(() => {
    let live = true;
    api(`${base}/state`)
      .then((s) => {
        if (!live) return;
        setCode(
          Object.fromEntries(
            tasks.map((t) => [t.id, s.drafts[t.id] ?? (t.starter || "")]),
          ),
        );
      })
      .catch(() => {
        if (live)
          setCode(
            Object.fromEntries(tasks.map((t) => [t.id, t.starter || ""])),
          );
      });
    return () => {
      live = false;
    };
  }, [base, tasks]);

  const idx = Math.max(
    0,
    tasks.findIndex((t) => String(t.id) === params.get("task")),
  );
  const task = tasks[idx];

  // история попыток выбранной задачи
  useEffect(() => {
    let live = true;
    api(`${base}/${task.id}/attempts`)
      .then(
        (d) => live && setAttempts((p) => ({ ...p, [task.id]: d.attempts })),
      )
      .catch(() => {});
    return () => {
      live = false;
    };
  }, [base, task.id]);

  // автосохранение черновика: через паузу после правки и при уходе со страницы
  const pending = useRef({});
  const timer = useRef(null);
  const flush = useCallback(() => {
    clearTimeout(timer.current);
    for (const [id, value] of Object.entries(pending.current))
      api(`${base}/${id}/draft`, {
        method: "PUT",
        body: { code: value },
        keepalive: true,
      }).catch(() => {});
    pending.current = {};
  }, [base]);
  useEffect(() => flush, [flush]);

  const select = (i) =>
    setParams(
      (prev) => {
        const n = new URLSearchParams(prev);
        n.set("task", String(tasks[i].id));
        return n;
      },
      { replace: true },
    );

  function edit(value) {
    setCode((p) => ({ ...p, [task.id]: value }));
    pending.current[task.id] = value;
    clearTimeout(timer.current);
    timer.current = setTimeout(flush, SAVE_DELAY);
  }

  const rk = `${user.id}:${bookId}:${chapter}:${task.id}`;
  const res = resultCache.get(rk) || null;

  async function run() {
    if (busy != null || code == null) return;
    const id = task.id;
    const key = rk;
    const source = code[id];
    flush();
    setBusy(id);
    try {
      const data = await api("/api/exercises/run", {
        method: "POST",
        body: {
          book: Number(bookId),
          chapter: Number(chapter),
          task: id,
          code: source,
        },
      });
      resultCache.set(key, { ...data, okAll: data.solved });
      progress.setCodeStatus(bookId, chapter, id, data.solved ? "ok" : "bad");
      setAttempts((p) => ({
        ...p,
        [id]: [
          {
            id: data.attempt.id,
            code: source,
            status: data.attempt.status,
            passed: data.passed,
            total: data.total,
            created_at: data.attempt.created_at,
          },
          ...(p[id] || []),
        ],
      }));
    } catch (e) {
      resultCache.set(key, { status: "error", stderr: e.message, results: [] });
    } finally {
      setBusy(null);
      redraw((n) => n + 1);
    }
  }

  if (code == null) return <p className="empty">Загрузка…</p>;

  const solved = status[task.id] === "ok";
  const running = busy === task.id;
  const history = attempts[task.id] || [];
  // «Дальше» вместо «Проверить», пока код совпадает с принятым решением
  const accepted = history.some(
    (a) => a.status === "ok" && a.code === code[task.id],
  );
  const hasNext = idx < tasks.length - 1 || !!nextChapter;
  const goMode = solved && accepted && hasNext;

  function goNext() {
    if (idx < tasks.length - 1) select(idx + 1);
    else if (nextChapter) nextChapter.open();
  }
  // Ctrl/Cmd+Enter: проверить; если принятое решение не менялось — перейти дальше
  const primary = () => (goMode ? goNext() : run());

  const label = `${
    tasks.every((t) => t.mode === "sql")
      ? "sql · sqlite"
      : tasks.every((t) => t.mode === "rust")
        ? "rust"
        : tasks.every((t) => t.mode === "c")
          ? "c · gcc"
          : tasks.every((t) => t.mode === "js")
            ? "javascript · node"
            : tasks.some((t) => t.mode === "c")
              ? "python + c"
              : "python"
  } · docker`;

  return (
    <PracticeShell
      tasks={tasks}
      status={status}
      idx={idx}
      select={select}
      itemsSlot={itemsSlot}
      label={label}
    >
      {task.mode === "sql" && task.schema && (
        <SqlSchema key={task.dataset} schema={task.schema} />
      )}

      {task.mode === "lab" ? (
        <Suspense fallback={<p className="empty">Загрузка…</p>}>
          <VirtLab
            key={task.id}
            task={task}
            solved={solved}
            onSolved={(solution) => {
              progress.setCodeStatus(bookId, chapter, task.id, "ok");
              api(`${base}/${task.id}/solved`, {
                method: "PUT",
                body: { solution },
              }).catch(() => {});
            }}
          />
          {hasNext && solved && (
            <div className="ex-row">
              <button className="quiz-btn" onClick={goNext}>
                {idx < tasks.length - 1 ? "Дальше →" : "Следующая глава →"}
              </button>
            </div>
          )}
        </Suspense>
      ) : (
        <>
          <CodeEditor
            className={solved && accepted ? "right" : ""}
            lang={langOf(task)}
            value={code[task.id]}
            onChange={edit}
            onRun={primary}
          />

          <div className="ex-row">
            {goMode ? (
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
                {running ? "Запускаю…" : "Проверить"}
              </button>
            )}
            {goMode && (
              <button
                className="quiz-btn ghost"
                onClick={run}
                disabled={busy != null}
                title="Запустить проверку ещё раз"
              >
                {running ? "Запускаю…" : "Проверить ещё раз"}
              </button>
            )}
            {task.hint && (
              <button
                className="quiz-btn ghost"
                onClick={() =>
                  setHint((p) => ({ ...p, [task.id]: !p[task.id] }))
                }
              >
                {hint[task.id] ? "Скрыть подсказку" : "Подсказка"}
              </button>
            )}
            <button
              className="quiz-btn ghost"
              onClick={() => edit(task.starter || "")}
              title="Вернуть исходный шаблон"
            >
              Сбросить
            </button>
          </div>
          {hint[task.id] && task.hint && <p className="ex-hint">{task.hint}</p>}

          <Results res={res} running={running} />

          <History
            items={history}
            current={code[task.id]}
            onPick={(a) => edit(a.code)}
          />
        </>
      )}
    </PracticeShell>
  );
}

function History({ items, current, onPick }) {
  if (items.length === 0) return null;
  return (
    <div className="pr-hist">
      <div className="pr-res-head">
        <span className="s-label">история попыток</span>
        <span className="pr-res-time">{items.length}</span>
      </div>
      <ul className="pr-hist-list">
        {items.map((a, i) => (
          <li key={a.id}>
            <button
              className={`pr-hist-item ${a.status} ${a.code === current ? "on" : ""}`}
              onClick={() => onPick(a)}
              title="Вернуть этот код в редактор"
            >
              <span className="pr-hist-n">#{items.length - i}</span>
              <span className="pr-hist-mark">
                {a.status === "ok" ? "✓" : "✗"}
              </span>
              <span className="pr-hist-score">
                {a.passed}/{a.total}
              </span>
              <span className="pr-hist-code">
                {a.code.split("\n").find((l) => l.trim()) || ""}
              </span>
              <span className="pr-hist-time">{fmtDate(a.created_at)}</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
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
          Нажмите «Проверить» (Ctrl/Cmd+Enter): здесь появятся тесты и логи
          выполнения. Когда решение принято, Ctrl/Cmd+Enter ведёт к следующему
          упражнению.
        </p>
      </div>
    );
  const total = res.results.length;
  const passed = res.passed ?? res.results.filter((r) => r.ok).length;
  // в режиме «вывод» программа печатает в перехваченный поток: её вывод лежит в got
  const one = total === 1 ? res.results[0] : null;
  const program =
    res.stdout ||
    (one && !one.args && !one.error && typeof one.got === "string"
      ? one.got
      : "");
  return (
    <div className="pr-res">
      <div className="pr-res-block">
        <div className="pr-res-head">
          <span className="s-label">тесты</span>
          {total > 0 && (
            <span className={`pr-res-sum ${res.okAll ? "ok" : "bad"}`}>
              {passed} из {total}
            </span>
          )}
        </div>
        {res.status === "timeout" && (
          <p className="ex-note">
            Проверка не уложилась в лимит времени — возможно, в коде бесконечный
            цикл.
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
                ) : r.kind === "rows" ? (
                  <SqlDiff r={r} />
                ) : (
                  <div className="pr-diff">
                    <div>
                      <span className="s-label">ожидалось</span>
                      <pre>{String(r.expected)}</pre>
                    </div>
                    <div>
                      <span className="s-label">получено</span>
                      <pre>
                        {r.got === "" || r.got == null
                          ? "(пусто)"
                          : String(r.got)}
                      </pre>
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
        {res.stderr && res.status !== "timeout" && (
          <pre className="cx-error">{res.stderr}</pre>
        )}
      </div>
    </div>
  );
}
