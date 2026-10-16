import { useOutletContext } from "react-router-dom";
import Quiz from "../../components/Quiz.tsx";

// Вкладка «Вопросы»: квиз на теорию главы.
export default function ChapterQuestions() {
  const { quiz, bookId, chapter, fs, itemsSlot } = useOutletContext();
  if (!quiz) return <p className="empty">Для этой главы нет вопросов</p>;
  return <Quiz
      quiz={quiz}
      bookId={bookId}
      chapter={chapter.num}
      itemsSlot={fs ? itemsSlot : null}
    />;
}
