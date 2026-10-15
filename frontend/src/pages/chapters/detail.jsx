import { useEffect, useState } from "react";
import { NavLink, Outlet, useParams } from "react-router-dom";
import { SLIDES } from "../../lib/slides.js";
import { QUIZZES } from "../../lib/quizzes.js";
import { EXERCISES } from "../../lib/exercises.js";
import { solvedCount } from "../../components/CodePractice.jsx";

/* Страница главы: заголовок и три вкладки, каждая со своим адресом —
     /book/:bookId/chapter/:chapterId             Теория  (слайды)
     /book/:bookId/chapter/:chapterId/questions   Вопросы (квизы)
     /book/:bookId/chapter/:chapterId/exercises   Практика (код в Docker)
   Данные главы грузятся один раз и отдаются вкладкам через контекст. */
export default function ChapterDetail() {
  const { bookId, chapterId } = useParams();
  const [chapter, setChapter] = useState(null);
  const [error, setError] = useState(null);
  // Код-упражнения (Docker-песочница): приходят с бэкенда, если есть.
  const [codeTasks, setCodeTasks] = useState([]);
  const [tasksReady, setTasksReady] = useState(false);
  const [tick, setTick] = useState(0); // перерисовать бейдж после решённой задачи

  useEffect(() => {
    if (chapterId == null) return;
    setError(null);
    setChapter(null);
    setCodeTasks([]);
    setTasksReady(false);
    fetch(`/api/chapters/${chapterId}`)
      .then((r) => {
        if (!r.ok) throw new Error("Урок не найден");
        return r.json();
      })
      .then(setChapter)
      .catch((e) => setError(e.message));
  }, [chapterId]);

  // Код-упражнения ключуются номером главы, 404 — просто нет.
  useEffect(() => {
    if (chapter == null || bookId == null) return;
    let alive = true;
    fetch(`/api/exercises/${bookId}/${chapter.num}`)
      .then((r) => (r.ok ? r.json() : { tasks: [] }))
      .then((d) => {
        if (alive) setCodeTasks(d.tasks || []);
      })
      .catch(() => {})
      .finally(() => {
        if (alive) setTasksReady(true);
      });
    return () => {
      alive = false;
    };
  }, [chapter, bookId]);

  if (error) return <p className="error">{error}</p>;
  if (!chapter) return <p className="empty">Загрузка…</p>;

  const key = `${bookId}:${chapter.num}`;
  const quiz = QUIZZES[key] || null;
  const practice = EXERCISES[key] || null;
  const hasSlides = !!SLIDES[key];
  const hasPractice = codeTasks.length > 0 || !!practice;
  const solved = codeTasks.length ? solvedCount(bookId, chapter.num, codeTasks) : 0;

  const tabs = [
    hasSlides && { to: "", end: true, label: "Теория" },
    quiz && {
      to: "questions",
      label: "Вопросы",
      badge: String(quiz.questions.length),
    },
    hasPractice && {
      to: "exercises",
      label: "Практика",
      badge: codeTasks.length ? `${solved}/${codeTasks.length}` : null,
    },
  ].filter(Boolean);

  return (
    <div>
      <p className="crumbs">{chapter.section}</p>
      <h2>
        Урок {chapter.num}. {chapter.title}
      </h2>
      <nav className="ch-tabs" aria-label="Разделы урока">
        {tabs.map((t) => (
          <NavLink
            key={t.label}
            to={t.to}
            end={t.end}
            className={({ isActive }) => `ch-tab ${isActive ? "on" : ""}`}
          >
            {t.label}
            {t.badge && <span className="ch-tab-badge">{t.badge}</span>}
          </NavLink>
        ))}
      </nav>
      <Outlet
        context={{
          bookId,
          chapter,
          quiz,
          practice,
          codeTasks,
          tasksReady,
          onSolved: () => setTick((n) => n + 1),
          tick,
        }}
      />
    </div>
  );
}
