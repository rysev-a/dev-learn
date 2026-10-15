import { useOutletContext } from "react-router-dom";
import Quiz from "../../components/Quiz.jsx";

// Вкладка «Вопросы»: квиз на теорию главы.
export default function ChapterQuestions() {
  const { quiz } = useOutletContext();
  if (!quiz) return <p className="empty">Для этой главы нет вопросов</p>;
  return <Quiz quiz={quiz} />;
}
