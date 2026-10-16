import { useChapterContext } from "./context.ts";
import Quiz from "../../components/Quiz.tsx";

// Вкладка «Вопросы»: квиз на теорию главы.
export default function ChapterQuestions() {
  const { quizCount, bookId, chapter, fs, itemsSlot } = useChapterContext();
  if (!quizCount) return <p className="empty">Для этой главы нет вопросов</p>;
  return <Quiz
      bookId={bookId}
      chapter={chapter.num}
      itemsSlot={fs ? itemsSlot : null}
    />;
}
