import { useEffect, useState } from "react";
import { Outlet, useNavigate, useParams } from "react-router-dom";
import { usePlayer } from "../../lib/player.jsx";

export default function BookDetail({ books }) {
  const { bookId, chapterId } = useParams();
  const navigate = useNavigate();
  const { stop } = usePlayer();
  const [course, setCourse] = useState([]);

  useEffect(() => {
    let live = true;
    setCourse([]);
    fetch(`/api/books/${bookId}/course`)
      .then((r) => r.json())
      .then((data) => {
        if (!live) return;
        setCourse(data);
      })
      .catch(() => {});
    return () => {
      live = false;
    };
  }, [bookId]);

  const book = books.find((b) => String(b.id) === String(bookId));

  function openChapter(id) {
    stop();
    navigate(`/book/${bookId}/chapter/${id}`);
  }

  return (
    <>
      {course.length > 0 && (
        <aside className="lessons-menu">
          <div className="s-label">{book ? book.title : ""}</div>
          {course.map((sec) => (
            <div key={sec.id} className="lessons-group">
              <div className="s-label lessons-sec">{sec.title}</div>
              {sec.chapters.map((ch) => (
                <button
                  key={ch.id}
                  className={`slide-fs-toc-item ${
                    String(chapterId) === String(ch.id) ? "on" : ""
                  }`}
                  onClick={() => openChapter(ch.id)}
                >
                  <span className="slide-fs-toc-num">
                    {String(ch.num).padStart(2, "0")}
                  </span>
                  <span className="slide-fs-toc-name">{ch.title}</span>
                </button>
              ))}
            </div>
          ))}
        </aside>
      )}

      <main className="content">
        <Outlet context={{ course }} />
      </main>
    </>
  );
}
