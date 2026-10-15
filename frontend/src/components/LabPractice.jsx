import { useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { useSearchParams } from "react-router-dom";
import { api } from "../lib/api.js";
import { useAuth } from "../lib/auth.jsx";
import { useProgress } from "../lib/progress.jsx";
import { FsItem } from "./FsTree.jsx";
import { hydrateLab } from "../lab/hydrate.js";
import { ARCH_BOOK, LAB_CHAPTERS, sectionOf } from "../lab/registry.js";
import CircuitLab from "../lab/react/CircuitLab.jsx";
import AsmLab from "../lab/react/AsmLab.jsx";
import RvLab from "../lab/react/RvLab.jsx";
import { ASM_BY_ID, REAL_BY_ID, RV_BY_ID } from "../lab/registry.js";
import "../lab/lab.css";

/* Вкладка «Практика» книги «Архитектура компьютера»: упражнения — интерактивные лаборатории
   (схемы из вентилей и блоков), проверка в браузере. Решение запоминается в кабинете:
   статус, схема и запись в истории попыток. */

export default function LabPractice({
  tasks,
  bookId,
  chapter,
  itemsSlot,
  nextChapter,
  fullscreen,
}) {
  const { user } = useAuth();
  const progress = useProgress();
  const [params, setParams] = useSearchParams();
  const [ready, setReady] = useState(false);
  const [version, setVersion] = useState(0);
  const status = progress.codeStatus(bookId, chapter);
  const lab = LAB_CHAPTERS[chapter];
  const isCode =
    lab?.kind === "asm" || lab?.kind === "riscv" || lab?.kind === "real";
  const base = `/api/exercises/${bookId}/${chapter}`;
  // черновики программ (ассемблер, RISC-V) — в кабинете, сохраняются сами
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
    if (!isCode) return;
    let live = true;
    api(`${base}/state`)
      .then((s) => live && setDrafts(s.drafts || {}))
      .catch(() => live && setDrafts({}));
    return () => {
      live = false;
    };
  }, [base, isCode]);
  const edit = (id, value) => {
    setDrafts((d) => ({ ...d, [id]: value }));
    pending.current[id] = value;
    clearTimeout(timer.current);
    timer.current = setTimeout(flush, 700);
  };

  useEffect(() => {
    let live = true;
    setReady(false);
    hydrateLab(user.id).then(() => live && setReady(true));
    return () => {
      live = false;
    };
  }, [user.id]);

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

  if (!ready || !task || (isCode && drafts === null))
    return <p className="empty">Загрузка…</p>;

  const done = tasks.filter((t) => status[t.id] === "ok").length;
  const solved = status[task.id] === "ok";
  const hasNext = idx < tasks.length - 1 || !!nextChapter;
  const goNext = () =>
    idx < tasks.length - 1 ? select(idx + 1) : nextChapter?.open();

  const onSolved = (solution) => {
    progress.setCodeStatus(bookId, chapter, task.id, "ok");
    setVersion((v) => v + 1);
    api(`/api/exercises/${ARCH_BOOK}/${chapter}/${task.id}/solved`, {
      method: "PUT",
      body: { solution },
    }).catch(() => {});
  };

  const section = lab?.kind === "circuit" ? sectionOf(lab.slug) : null;
  const exercise = section?.exercises.find((e) => e.id === task.id);

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
        <span className="pr-top-label">лаборатория · в браузере</span>
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
          {isCode && (
            <CodeTask
              key={`${chapter}:${task.id}`}
              kind={lab.kind}
              task={task}
              code={drafts[task.id]}
              onCode={(v) => edit(task.id, v)}
              solvedBefore={solved}
              onSolved={(code) => {
                flush();
                onSolved(code);
              }}
              onNext={goNext}
              hasNext={hasNext}
              nextLabel={
                idx < tasks.length - 1 ? "Дальше →" : "Следующая глава →"
              }
            />
          )}
          {exercise && (
            <CircuitLab
              key={`${chapter}:${task.id}`}
              section={section}
              exercise={exercise}
              index={section.exercises.indexOf(exercise)}
              solvedBefore={solved}
              onSolved={onSolved}
              onNext={goNext}
              hasNext={hasNext}
              nextLabel={
                idx < tasks.length - 1 ? "Дальше →" : "Следующая глава →"
              }
              progressVersion={version}
              fullscreen={fullscreen}
            />
          )}
        </div>
      </div>
    </section>
  );
}

function CodeTask({ kind, task, ...rest }) {
  if (kind === "asm") return <AsmLab task={ASM_BY_ID[task.id]} {...rest} />;
  return (
    <RvLab
      task={(kind === "real" ? REAL_BY_ID : RV_BY_ID)[task.id]}
      real={kind === "real"}
      {...rest}
    />
  );
}
