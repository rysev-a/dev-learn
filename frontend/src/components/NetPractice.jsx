import { useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { useSearchParams } from "react-router-dom";
import { api } from "../lib/api.js";
import { useProgress } from "../lib/progress.jsx";
import { FsItem } from "./FsTree.jsx";
import { NET_BY_ID } from "../netlab/registry.js";
import NetLab from "../netlab/react/NetLab.jsx";

/* Вкладка «Практика» книги «Компьютерные сети»: упражнения — симулятор сети в браузере
   (устройства, кабели, адреса, маршруты, NAT). Состояние сети сохраняется в кабинете как
   черновик, решённое упражнение отправляется на сервер (режим lab). */

export default function NetPractice({
  tasks,
  bookId,
  chapter,
  itemsSlot,
  nextChapter,
}) {
  const progress = useProgress();
  const [params, setParams] = useSearchParams();
  const status = progress.codeStatus(bookId, chapter);
  const base = `/api/exercises/${bookId}/${chapter}`;
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
    let live = true;
    api(`${base}/state`)
      .then((s) => live && setDrafts(s.drafts || {}))
      .catch(() => live && setDrafts({}));
    return () => {
      live = false;
    };
  }, [base]);
  const edit = (id, value) => {
    pending.current[id] = value;
    clearTimeout(timer.current);
    timer.current = setTimeout(flush, 700);
  };

  const idx = Math.max(
    0,
    tasks.findIndex((t) => String(t.id) === params.get("task")),
  );
  const task = tasks[idx];
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

  if (!task || drafts === null) return <p className="empty">Загрузка…</p>;
  const scenario = NET_BY_ID[task.id];
  if (!scenario) return <p className="empty">Упражнение не найдено</p>;

  const done = tasks.filter((t) => status[t.id] === "ok").length;
  const solved = status[task.id] === "ok";
  const hasNext = idx < tasks.length - 1 || !!nextChapter;
  const goNext = () =>
    idx < tasks.length - 1 ? select(idx + 1) : nextChapter?.open();

  const onSolved = (solution) => {
    flush();
    progress.setCodeStatus(bookId, chapter, task.id, "ok");
    api(`${base}/${task.id}/solved`, {
      method: "PUT",
      body: { solution },
    }).catch(() => {});
  };

  return (
    <section className="pr lab-pr">
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
        <span className="pr-top-label">симулятор сети · в браузере</span>
      </div>

      <div className={`pr-body ${itemsSlot ? "single" : ""}`}>
        {itemsSlot ? (
          createPortal(
            tasks.map((t, i) => (
              <FsItem
                key={t.id}
                on={i === idx}
                num={i + 1}
                mark={status[t.id] === "ok" ? "✓" : undefined}
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
                  title={t.title}
                >
                  <span className="pr-mark">{st === "ok" ? "✓" : i + 1}</span>
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
            <span className={`pr-badge ${solved ? "ok" : ""}`}>
              {solved ? "выполнено" : "не решено"}
            </span>
          </div>
          <p className="pr-statement">{task.statement}</p>
          <NetLab
            key={`${chapter}:${task.id}`}
            scenario={scenario}
            code={drafts[task.id]}
            onCode={(v) => edit(task.id, v)}
            solvedBefore={solved}
            onSolved={onSolved}
            onNext={goNext}
            hasNext={hasNext}
            nextLabel={idx < tasks.length - 1 ? "Дальше →" : "Следующая глава →"}
          />
        </div>
      </div>
    </section>
  );
}
