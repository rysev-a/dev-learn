import { useNavigate, useOutletContext } from "react-router-dom";
import CodePractice from "../../components/CodePractice.jsx";
import Exercises from "../../components/Exercises.jsx";

// Вкладка «Практика»: код-задачи в Docker (по одной, со списком слева);
// у книги без кода — задачи с вводом ответа.
export default function ChapterExercises() {
  const { bookId, chapter, codeTasks, tasksReady, practice, fs, itemsSlot, nextPractice } =
    useOutletContext();
  const navigate = useNavigate();
  if (codeTasks.length > 0)
    return (
      <CodePractice
        key={`${bookId}:${chapter.num}`}
        tasks={codeTasks}
        bookId={bookId}
        chapter={chapter.num}
        itemsSlot={fs ? itemsSlot : null}
        nextChapter={
          nextPractice
            ? {
                title: nextPractice.title,
                open: () =>
                  navigate(
                    `/book/${bookId}/chapter/${nextPractice.id}/exercises${fs ? "?fs=1" : ""}`,
                  ),
              }
            : null
        }
      />
    );
  if (practice) return <Exercises quiz={practice} bookId={bookId} chapter={chapter.num} />;
  if (!tasksReady) return <p className="empty">Загрузка…</p>;
  return <p className="empty">Для этой главы нет упражнений</p>;
}
