import { useEffect, useState } from "react";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import { usePlayer } from "../../lib/player.jsx";
import { useProgress } from "../../lib/progress.jsx";
import { chapterStats } from "../books/index.jsx";

/* Корень раздела: карточки всех тем (глав), сгруппированные по подразделам. */

const pct = (a, b) => (b ? Math.round((a / b) * 100) : 0);

export default function ChaptersIndex() {
  const { course } = useOutletContext();
  const { bookId } = useParams();
  const navigate = useNavigate();
  const { stop } = usePlayer();
  const progress = useProgress();
  const [codeCounts, setCodeCounts] = useState(null);

  useEffect(() => {
    let live = true;
    fetch("/api/exercises")
      .then((r) => (r.ok ? r.json() : {}))
      .then((d) => live && setCodeCounts(d))
      .catch(() => live && setCodeCounts({}));
    return () => {
      live = false;
    };
  }, []);

  function open(id) {
    stop();
    navigate(`/book/${bookId}/chapter/${id}`);
  }

  return (
    <>
      {course.map((sec) => (
        <section key={sec.id} className="topics-sec">
          <h2 className="topics-title">{sec.title}</h2>
          <div className="topics-grid">
            {sec.chapters.map((ch) => {
              const s = chapterStats(progress, bookId, ch, codeCounts);
              const done = s.slides[0] + s.quiz[0] + s.ex[0];
              const all = s.slides[1] + s.quiz[1] + s.ex[1];
              const parts = [
                s.slides[1] ? `${s.slides[1]} слайдов` : null,
                s.quiz[1] ? `${s.quiz[1]} вопросов` : null,
                s.ex[1] ? `${s.ex[1]} упражнений` : null,
              ].filter(Boolean);
              return (
                <button key={ch.id} className="topic-card" onClick={() => open(ch.id)}>
                  <span className="topic-num">{String(ch.num).padStart(2, "0")}</span>
                  <span className="topic-name">{ch.title}</span>
                  <span className="topic-meta">
                    {parts.length ? parts.join(" · ") : "скоро"}
                  </span>
                  {all > 0 && (
                    <span className="topic-prog">
                      <span className="pr-bar">
                        <i style={{ width: `${pct(done, all)}%` }} />
                      </span>
                      <span className="topic-pct">{pct(done, all)}%</span>
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </section>
      ))}
    </>
  );
}
