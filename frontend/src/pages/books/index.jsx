import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import BookIcon from "../../components/BookIcon.tsx";
import { QUIZZES } from "../../lib/quizzes.ts";
import { EXERCISES } from "../../lib/exercises.ts";
import { pct } from "../../lib/format.ts";
import { usePlayer } from "../../lib/player.tsx";
import { useProgress } from "../../lib/progress.tsx";
import { useCodeCounts, useCourses } from "../../lib/queries.ts";

/* Главная — дашборд: прогресс по слайдам, вопросам и упражнениям во всех
   разделах. Данные о составе курса приходят с бэкенда (главы разделов и число
   код-упражнений), прогресс берётся из кабинета пользователя (сервер). */

// прогресс одной главы: слайды, вопросы, упражнения (сделано / всего)
export function chapterStats(progress, bookId, ch, codeCounts) {
  const key = `${bookId}:${ch.num}`;
  const slidesTotal = ch.parts_count || 0; // один абзац = один слайд
  const quiz = QUIZZES[key];
  const quizTotal = quiz ? quiz.questions.length : 0;
  const picks = quizTotal ? progress.quizPicks(bookId, ch.num) : null;
  const quizDone = picks ? picks.filter((p) => p != null).length : 0;
  const quizRight = picks
    ? picks.filter((p, i) => p != null && p === quiz.questions[i].answer).length
    : 0;
  const code = codeCounts?.[bookId]?.[ch.num] || 0;
  const dm = EXERCISES[key] ? EXERCISES[key].tasks.length : 0;
  const exTotal = code || dm;
  const exDone = code
    ? Object.values(progress.codeStatus(bookId, ch.num)).filter((v) => v === "ok").length
    : dm
      ? Object.keys(progress.answerSolved(bookId, ch.num)).length
      : 0;
  return {
    slides: [Math.min(progress.slidesSeen(bookId, ch.num).length, slidesTotal), slidesTotal],
    quiz: [quizDone, quizTotal],
    quizRight,
    ex: [exDone, exTotal],
  };
}

const sum = (list, f) => list.reduce((a, x) => a + f(x), 0);

export default function BooksIndex({ books }) {
  const navigate = useNavigate();
  const { stop } = usePlayer();
  const progress = useProgress();
  const courses = useCourses(books); // bookId → разделы с главами
  const codeCounts = useCodeCounts();

  const rows = useMemo(
    () =>
      books.map((b) => {
        const chapters = (courses[b.id] || []).flatMap((s) => s.chapters);
        const stats = chapters.map((ch) => ({
          ch,
          ...chapterStats(progress, b.id, ch, codeCounts),
        }));
        return {
          book: b,
          loaded: courses[b.id] != null,
          stats,
          slides: [sum(stats, (s) => s.slides[0]), sum(stats, (s) => s.slides[1])],
          quiz: [sum(stats, (s) => s.quiz[0]), sum(stats, (s) => s.quiz[1])],
          ex: [sum(stats, (s) => s.ex[0]), sum(stats, (s) => s.ex[1])],
        };
      }),
    [books, courses, codeCounts, progress],
  );

  const total = {
    slides: [sum(rows, (r) => r.slides[0]), sum(rows, (r) => r.slides[1])],
    quiz: [sum(rows, (r) => r.quiz[0]), sum(rows, (r) => r.quiz[1])],
    ex: [sum(rows, (r) => r.ex[0]), sum(rows, (r) => r.ex[1])],
  };
  const doneAll = total.slides[0] + total.quiz[0] + total.ex[0];
  const allAll = total.slides[1] + total.quiz[1] + total.ex[1];

  function open(path) {
    stop();
    navigate(path);
  }

  if (books.length === 0)
    return (
      <main className="content home">
        <p className="empty">Разделы не загружены. Запусти seed_textbook.py</p>
      </main>
    );

  return (
    <main className="content home">
      <div className="dash-head">
        <h2>Прогресс</h2>
        <span className="dash-all">
          {pct(doneAll, allAll)}% · {doneAll} из {allAll}
        </span>
      </div>

      <div className="dash-totals">
        <Stat title="Слайды" hint="просмотрено" v={total.slides} />
        <Stat title="Вопросы" hint="отвечено" v={total.quiz} />
        <Stat title="Упражнения" hint="решено" v={total.ex} />
      </div>

      <h2 className="dash-sub">Разделы</h2>
      <div className="dash-grid">
        {rows.map(({ book, loaded, stats, slides, quiz, ex }) => (
          <section className="dash-card" key={book.id}>
            <button
              className="dash-card-head"
              onClick={() => open(`/book/${book.id}`)}
            >
              <span className="dash-ico">
                <BookIcon id={book.id} size={18} />
              </span>
              <span className="dash-title">{book.title}</span>
              <span className="dash-meta">{book.lessons_count} уроков</span>
            </button>

            <Bar label="Слайды" v={slides} />
            <Bar label="Вопросы" v={quiz} />
            <Bar label="Упражнения" v={ex} none="нет" />

            <div className="dash-chapters" aria-label="Главы">
              {loaded
                ? stats.map((s) => {
                    const done = s.slides[0] + s.quiz[0] + s.ex[0];
                    const all = s.slides[1] + s.quiz[1] + s.ex[1];
                    const level = !done ? 0 : done >= all ? 3 : done * 2 >= all ? 2 : 1;
                    return (
                      <button
                        key={s.ch.id}
                        className={`dash-ch l${level}`}
                        title={`${s.ch.num}. ${s.ch.title} — слайды ${s.slides[0]}/${s.slides[1]}, вопросы ${s.quiz[0]}/${s.quiz[1]}, упражнения ${s.ex[0]}/${s.ex[1]}`}
                        onClick={() => open(`/book/${book.id}/chapter/${s.ch.id}`)}
                      >
                        {s.ch.num}
                      </button>
                    );
                  })
                : null}
            </div>
          </section>
        ))}
      </div>
    </main>
  );
}

function Stat({ title, hint, v }) {
  return (
    <div className="dash-stat">
      <span className="dash-stat-title">{title}</span>
      <span className="dash-stat-num">
        {v[0]}
        <small> / {v[1]}</small>
      </span>
      <div className="pr-bar">
        <i style={{ width: `${pct(v[0], v[1])}%` }} />
      </div>
      <span className="dash-stat-hint">
        {hint} · {pct(v[0], v[1])}%
      </span>
    </div>
  );
}

function Bar({ label, v, none }) {
  return (
    <div className="dash-bar">
      <span className="dash-bar-label">{label}</span>
      <div className="pr-bar">
        <i style={{ width: `${pct(v[0], v[1])}%` }} />
      </div>
      <span className="dash-bar-num">
        {v[1] ? `${v[0]}/${v[1]}` : none || "—"}
      </span>
    </div>
  );
}
