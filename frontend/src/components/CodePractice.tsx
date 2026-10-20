import { lazy, Suspense, useEffect, useState } from "react";
import { api } from "../lib/api.ts";
import { useAuth } from "../lib/auth.tsx";
import { useProgress } from "../lib/progress.tsx";
import CodeEditor from "./CodeEditor.tsx";
import SqlDiff from "./SqlDiff.tsx";
import SqlSchema from "./SqlSchema.tsx";
import type { Attempt, RunResult, Task } from "../types.ts";
import PracticeShell, { usePracticeDrafts, useTaskSelection } from "./PracticeShell.tsx";
import type { EditorLang } from "./CodeEditor.tsx";

// Симуляторы книги «Виртуализация» (задачи режима lab среди код-задач) грузятся лениво
const VirtLab = lazy(() => import("../virtlab/VirtLab.tsx"));

/* Вкладка «Практика»: упражнения с проверкой кода в Docker-песочнице
   (бэкенд /api/exercises). Слева — список со статусами и прогресс, справа —
   одно упражнение: условие, редактор, тесты, логи и история попыток.

   Всё, что набрал пользователь, живёт в кабинете на сервере: статусы задач
   (решённая остаётся решённой), черновик кода (сохраняется сам) и история
   попыток — клик по попытке возвращает её код в редактор. Выбранное упражнение —
   в адресе (?task=id), логи последнего запуска — в памяти на время сессии. */

const langOf = (t: Task): EditorLang =>
  t.mode === "sql" || t.mode === "rust" || t.mode === "c" || t.mode === "js"
    ? t.mode
    : "python";

interface RunRequest {
  book: number;
  chapter: number;
  task: string;
  code: string;
}
type JobState = { state: "queued"; position?: number } | { state: "running" } | ({ state: "done" } & RunResult);

/** Ставит решение в очередь проверки и ждёт результат (опрос раз в ~0,7 с); onPhase — «в очереди» / «выполняется» */
async function checkCode(req: RunRequest, onPhase: (state: "queued" | "running", position?: number) => void): Promise<RunResult> {
  let job = await api<JobState & { id: string }>("/api/exercises/run", { method: "POST", body: req });
  const id = job.id;
  const t0 = Date.now();
  while (job.state !== "done") {
    onPhase(job.state, job.state === "queued" ? job.position : undefined);
    if (Date.now() - t0 > 6 * 60_000) throw new Error("Проверка слишком долго ждёт в очереди — попробуйте позже.");
    await new Promise((r) => setTimeout(r, 700));
    job = { ...(await api<JobState>(`/api/exercises/run/${id}`)), id };
  }
  return job;
}

// логи последнего запуска каждой задачи переживают переключение вкладок
const resultCache = new Map<string, RunResult>();

const fmtDate = (iso: string) =>
  new Date(iso).toLocaleString("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });

interface CodePracticeProps {
  tasks: Task[];
  bookId: string;
  chapter: number;
  itemsSlot: HTMLElement | null;
  nextChapter?: { open: () => void } | null;
}

export default function CodePractice({
  tasks,
  bookId,
  chapter,
  itemsSlot,
  nextChapter,
}: CodePracticeProps) {
  const { user } = useAuth();
  const progress = useProgress();
  const status = progress.codeStatus(bookId, chapter);

  const base = `/api/exercises/${bookId}/${chapter}`;
  // черновики приходят с сервера и сохраняются сами; null — ещё грузятся
  const { drafts, edit: editDraft, flush } = usePracticeDrafts(base, { echo: true });
  const { idx, task, select } = useTaskSelection(tasks);
  const codeOf = (t: Task) => drafts?.[t.id] ?? (t.starter || "");
  const [attempts, setAttempts] = useState<Record<string, Attempt[]>>({}); // id задачи → попытки, новые первыми
  const [busy, setBusy] = useState<string | null>(null);
  // где проверка: «в очереди (N)» или «выполняется»
  const [phase, setPhase] = useState("");
  const [hint, setHint] = useState<Record<string, boolean>>({});
  const [, redraw] = useState(0);

  // история попыток выбранной задачи
  useEffect(() => {
    let live = true;
    api<{ attempts: Attempt[] }>(`${base}/${task.id}/attempts`)
      .then(
        (d) => live && setAttempts((p) => ({ ...p, [task.id]: d.attempts })),
      )
      .catch(() => {});
    return () => {
      live = false;
    };
  }, [base, task.id]);

  const edit = (value: string) => editDraft(task.id, value);

  const rk = `${user?.id}:${bookId}:${chapter}:${task.id}`;
  const res = resultCache.get(rk) || null;

  async function run() {
    if (busy != null || drafts == null) return;
    const id = task.id;
    const key = rk;
    const source = codeOf(task);
    flush();
    setBusy(id);
    try {
      const data = await checkCode(
        { book: Number(bookId), chapter: Number(chapter), task: id, code: source },
        (state, position) =>
          setPhase(state === "queued" ? `В очереди${position && position > 1 ? ` (перед вами ${position - 1})` : ""}…` : "Выполняется в песочнице…"),
      );
      resultCache.set(key, { ...data, okAll: data.solved });
      progress.setCodeStatus(bookId, chapter, id, data.solved ? "ok" : "bad");
      setAttempts((p) => ({
        ...p,
        [id]: [
          {
            id: data.attempt!.id,
            code: source,
            status: data.attempt!.status,
            passed: data.passed ?? 0,
            total: data.total ?? 0,
            created_at: data.attempt!.created_at,
          },
          ...(p[id] || []),
        ],
      }));
    } catch (e) {
      resultCache.set(key, {
        status: "error",
        stderr: e instanceof Error ? e.message : String(e),
        results: [],
      });
    } finally {
      setBusy(null);
      setPhase("");
      redraw((n) => n + 1);
    }
  }

  if (drafts == null) return <p className="empty">Загрузка…</p>;

  const solved = status[task.id] === "ok";
  const running = busy === task.id;
  const history = attempts[task.id] || [];
  // «Дальше» вместо «Проверить», пока код совпадает с принятым решением
  const accepted = history.some(
    (a) => a.status === "ok" && a.code === codeOf(task),
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
            onSolved={(solution: string) => {
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
            value={codeOf(task)}
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
                {running ? (phase.startsWith("В очереди") ? "В очереди…" : "Проверяю…") : "Проверить"}
              </button>
            )}
            {goMode && (
              <button
                className="quiz-btn ghost"
                onClick={run}
                disabled={busy != null}
                title="Запустить проверку ещё раз"
              >
                {running ? (phase.startsWith("В очереди") ? "В очереди…" : "Проверяю…") : "Проверить ещё раз"}
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

          <Results res={res} running={running} phase={phase} />

          <History
            items={history}
            current={codeOf(task)}
            onPick={(a) => edit(a.code)}
          />
        </>
      )}
    </PracticeShell>
  );
}

function History({
  items,
  current,
  onPick,
}: {
  items: Attempt[];
  current: string;
  onPick: (a: Attempt) => void;
}) {
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

function Results({ res, running, phase }: { res: RunResult | null; running: boolean; phase: string }) {
  if (running)
    return (
      <div className="pr-res">
        <p className="pr-empty">{phase || "Ставлю в очередь…"}</p>
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
