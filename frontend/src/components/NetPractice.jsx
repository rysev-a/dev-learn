import { api } from "../lib/api.ts";
import { useProgress } from "../lib/progress.tsx";
import PracticeShell, {
  usePracticeDrafts,
  useTaskSelection,
} from "./PracticeShell.tsx";
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
  const status = progress.codeStatus(bookId, chapter);
  const base = `/api/exercises/${bookId}/${chapter}`;
  const { drafts, edit, flush } = usePracticeDrafts(base);
  const { idx, task, select } = useTaskSelection(tasks);

  if (!task || drafts === null) return <p className="empty">Загрузка…</p>;
  const scenario = NET_BY_ID[task.id];
  if (!scenario) return <p className="empty">Упражнение не найдено</p>;

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
    <PracticeShell
      className="lab-pr"
      tasks={tasks}
      status={status}
      idx={idx}
      select={select}
      itemsSlot={itemsSlot}
      label="симулятор сети · в браузере"
    >
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
    </PracticeShell>
  );
}
