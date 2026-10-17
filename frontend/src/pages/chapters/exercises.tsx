import { lazy, Suspense } from "react";
import { useNavigate } from "react-router-dom";
import { useChapterContext } from "./context.ts";
import CodePractice from "../../components/CodePractice.tsx";
import Exercises from "../../components/Exercises.tsx";

// Лаборатория (схемы, ассемблер) тяжёлая: грузится только на вкладке «Практика» нужных глав
const LabPractice = lazy(() => import("../../components/LabPractice.tsx"));
// Симулятор сети («Компьютерные сети») — тоже лаборатория, но со своим движком
const NetPractice = lazy(() => import("../../components/NetPractice.tsx"));
// Схема высоконагруженного сервиса («Системный дизайн») — тоже лаборатория со своим движком
const SdPractice = lazy(() => import("../../components/SdPractice.tsx"));

// Вкладка «Практика»: код-задачи в Docker (по одной, со списком слева);
// у книги без кода — задачи с вводом ответа.
export default function ChapterExercises() {
  const {
    bookId,
    chapter,
    codeTasks,
    tasksReady,
    answerCount,
    fs,
    itemsSlot,
    nextPractice,
  } = useChapterContext();
  const navigate = useNavigate();
  const Practice =
    codeTasks.length > 0 && codeTasks.every((t) => t.mode === "lab")
      ? String(bookId) === "15"
        ? NetPractice
        : String(bookId) === "18"
          ? SdPractice
          : LabPractice
      : CodePractice;
  if (codeTasks.length > 0)
    return (
      <Suspense fallback={<p className="empty">Загрузка…</p>}>
        <Practice
          fullscreen={fs}
          key={`${bookId}:${chapter.num}`}
          tasks={codeTasks}
          bookId={bookId}
          chapter={chapter.num}
          itemsSlot={fs ? itemsSlot : null}
          nextChapter={
            nextPractice
              ? {
                  open: () =>
                    navigate(
                      `/book/${bookId}/chapter/${nextPractice.id}/exercises${fs ? "?fs=1" : ""}`,
                    ),
                }
              : null
          }
        />
      </Suspense>
    );
  if (answerCount) return <Exercises bookId={bookId} chapter={chapter.num} />;
  if (!tasksReady) return <p className="empty">Загрузка…</p>;
  return <p className="empty">Для этой главы нет упражнений</p>;
}
