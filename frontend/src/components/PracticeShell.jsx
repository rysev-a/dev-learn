import { useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { useSearchParams } from "react-router-dom";
import { api } from "../lib/api.ts";
import { FsItem } from "./FsTree.jsx";

/* Общая оболочка вкладки «Практика»: полоса «решено N из M», список упражнений (слева или
   порталом в дерево полноэкранного режима), заголовок и условие выбранной задачи.
   Содержимое упражнения (редактор, лаборатория, симулятор) приходит как children. */

const MARKS = { ok: "✓", bad: "✗" };
const BADGE = { ok: "выполнено", bad: "не пройдено" };

// Выбранная задача хранится в адресе (?task=<id>)
export function useTaskSelection(tasks) {
  const [params, setParams] = useSearchParams();
  const idx = Math.max(
    0,
    tasks.findIndex((t) => String(t.id) === params.get("task")),
  );
  const select = useCallback(
    (i) =>
      setParams(
        (prev) => {
          const n = new URLSearchParams(prev);
          n.set("task", String(tasks[i].id));
          return n;
        },
        { replace: true },
      ),
    [setParams, tasks],
  );
  return { idx, task: tasks[idx], select };
}

// Черновики задач главы (программа или состояние схемы) в кабинете: правка уходит на сервер
// через паузу и при уходе со страницы. echo — хранить правку и локально (если редактор управляется снаружи).
export function usePracticeDrafts(
  base,
  { enabled = true, echo = false, delay = 700 } = {},
) {
  const [drafts, setDrafts] = useState(null);
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
  useEffect(() => {
    if (!enabled) return undefined;
    let live = true;
    api(`${base}/state`)
      .then((s) => live && setDrafts(s.drafts || {}))
      .catch(() => live && setDrafts({}));
    return () => {
      live = false;
    };
  }, [base, enabled]);
  const edit = (id, value) => {
    if (echo) setDrafts((d) => ({ ...d, [id]: value }));
    pending.current[id] = value;
    clearTimeout(timer.current);
    timer.current = setTimeout(flush, delay);
  };
  return { drafts, edit, flush };
}

export default function PracticeShell({
  className = "",
  tasks,
  status,
  idx,
  select,
  itemsSlot,
  label,
  children,
}) {
  const task = tasks[idx];
  const done = tasks.filter((t) => status[t.id] === "ok").length;
  const st = status[task.id];
  return (
    <section className={`pr ${className}`.trim()}>
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
        <span className="pr-top-label">{label}</span>
      </div>

      <div className={`pr-body ${itemsSlot ? "single" : ""}`}>
        {itemsSlot ? (
          createPortal(
            tasks.map((t, i) => (
              <FsItem
                key={t.id}
                on={i === idx}
                num={i + 1}
                mark={MARKS[status[t.id]]}
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
            {tasks.map((t, i) => (
              <button
                key={t.id}
                className={`pr-item ${i === idx ? "on" : ""} ${status[t.id] || ""}`}
                onClick={() => select(i)}
                title={t.title}
              >
                <span className="pr-mark">{MARKS[status[t.id]] || i + 1}</span>
                <span className="pr-name">{t.title}</span>
              </button>
            ))}
          </aside>
        )}

        <div className="pr-main" key={task.id}>
          <div className="pr-head">
            <h3>
              {idx + 1}. {task.title}
            </h3>
            <span className={`pr-badge ${st || ""}`}>
              {BADGE[st] || "не решено"}
            </span>
          </div>
          <p className="pr-statement">{task.statement}</p>
          {children}
        </div>
      </div>
    </section>
  );
}
