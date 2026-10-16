import { useEffect, useState } from "react";
import { api } from "../lib/api.ts";
import { useAuth } from "../lib/auth.tsx";
import { useProgress } from "../lib/progress.tsx";
import PracticeShell, {
  usePracticeDrafts,
  useTaskSelection,
} from "./PracticeShell.tsx";
import { hydrateLab } from "../lab/hydrate.ts";
import { ARCH_BOOK, LAB_CHAPTERS, sectionOf } from "../lab/registry.ts";
import CircuitLab from "../lab/react/CircuitLab.tsx";
import AsmLab from "../lab/react/AsmLab.tsx";
import RvLab from "../lab/react/RvLab.tsx";
import { ASM_BY_ID, REAL_BY_ID, RV_BY_ID } from "../lab/registry.ts";
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
  const [ready, setReady] = useState(false);
  const [version, setVersion] = useState(0);
  const status = progress.codeStatus(bookId, chapter);
  const lab = LAB_CHAPTERS[chapter];
  const isCode =
    lab?.kind === "asm" || lab?.kind === "riscv" || lab?.kind === "real";
  // черновики программ (ассемблер, RISC-V) — в кабинете, сохраняются сами
  const { drafts, edit, flush } = usePracticeDrafts(
    `/api/exercises/${bookId}/${chapter}`,
    {
      enabled: isCode,
      echo: true,
    },
  );

  useEffect(() => {
    let live = true;
    setReady(false);
    hydrateLab(user.id).then(() => live && setReady(true));
    return () => {
      live = false;
    };
  }, [user.id]);

  const { idx, task, select } = useTaskSelection(tasks);

  if (!ready || !task || (isCode && drafts === null))
    return <p className="empty">Загрузка…</p>;

  const solved = status[task.id] === "ok";
  const hasNext = idx < tasks.length - 1 || !!nextChapter;
  const goNext = () =>
    idx < tasks.length - 1 ? select(idx + 1) : nextChapter?.open();
  const nextLabel = idx < tasks.length - 1 ? "Дальше →" : "Следующая глава →";

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
    <PracticeShell
      className="lab-pr"
      tasks={tasks}
      status={status}
      idx={idx}
      select={select}
      itemsSlot={itemsSlot}
      label="лаборатория · в браузере"
    >
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
          nextLabel={nextLabel}
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
          nextLabel={nextLabel}
          progressVersion={version}
          fullscreen={fullscreen}
        />
      )}
    </PracticeShell>
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
