import { useCallback, useEffect, useRef, useState, type ReactNode } from "react";
import { createPortal } from "react-dom";
import { useSearchParams } from "react-router-dom";
import { api } from "../lib/api.ts";
import type { Task, TaskStatus } from "../types.ts";
import { FsItem } from "./FsTree.tsx";

/* Общая оболочка вкладки «Практика»: полоса «решено N из M», список упражнений (слева или
   порталом в дерево полноэкранного режима), заголовок и условие выбранной задачи.
   Содержимое упражнения (редактор, лаборатория, симулятор) приходит как children. */

const MARKS: Record<TaskStatus, string> = { ok: "✓", bad: "✗" };
const BADGE: Record<TaskStatus, string> = { ok: "выполнено", bad: "не пройдено" };

export interface PracticeTaskInfo {
  id: string;
  title: string;
  statement: string;
}

export type StatusMap = Record<string, TaskStatus>;

/** то, что вкладка «Практика» главы отдаёт конкретной оболочке упражнений */
export interface PracticeProps {
  tasks: Task[];
  bookId: string;
  chapter: number;
  itemsSlot: HTMLElement | null;
  nextChapter?: { open: () => void } | null;
  fullscreen?: boolean;
}

// Выбранная задача хранится в адресе (?task=<id>)
export function useTaskSelection<T extends { id: string }>(tasks: T[]) {
  const [params, setParams] = useSearchParams();
  const idx = Math.max(
    0,
    tasks.findIndex((t) => String(t.id) === params.get("task")),
  );
  const select = useCallback(
    (i: number) =>
      setParams(
        (prev) => {
          const n = new URLSearchParams(prev);
          n.set("task", String(tasks[i]?.id));
          return n;
        },
        { replace: true },
      ),
    [setParams, tasks],
  );
  const task = tasks[idx];
  if (task === undefined) throw new Error("useTaskSelection: пустой список упражнений");
  return { idx, task, select };
}

interface DraftOptions {
  enabled?: boolean;
  echo?: boolean;
  delay?: number;
}

// Черновики задач главы (программа или состояние схемы) в кабинете: правка уходит на сервер
// через паузу и при уходе со страницы. echo — хранить правку и локально (если редактор управляется снаружи).
export function usePracticeDrafts(
  base: string,
  { enabled = true, echo = false, delay = 700 }: DraftOptions = {},
) {
  const [drafts, setDrafts] = useState<Record<string, string> | null>(null);
  const pending = useRef<Record<string, string>>({});
  const timer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
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
    api<{ drafts?: Record<string, string> }>(`${base}/state`)
      .then((s) => live && setDrafts(s.drafts || {}))
      .catch(() => live && setDrafts({}));
    return () => {
      live = false;
    };
  }, [base, enabled]);
  const edit = (id: string, value: string) => {
    if (echo) setDrafts((d) => ({ ...d, [id]: value }));
    pending.current[id] = value;
    clearTimeout(timer.current);
    timer.current = setTimeout(flush, delay);
  };
  return { drafts, edit, flush };
}

interface PracticeShellProps {
  className?: string;
  tasks: PracticeTaskInfo[];
  status: StatusMap;
  idx: number;
  select: (i: number) => void;
  itemsSlot: HTMLElement | null;
  label: string;
  children?: ReactNode;
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
}: PracticeShellProps) {
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
            <span className={`pr-badge ${st || ""}`}>{BADGE[st] || "не решено"}</span>
          </div>
          <p className="pr-statement">{task.statement}</p>
          {children}
        </div>
      </div>
    </section>
  );
}
