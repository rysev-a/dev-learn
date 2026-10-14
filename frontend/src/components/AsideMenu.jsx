import { useNavigate } from "react-router-dom";
import { usePlayer } from "../lib/player.jsx";

export default function AsideMenu({ books, activeBookId }) {
  const navigate = useNavigate();
  const { stop } = usePlayer();

  function openBook(id) {
    stop();
    navigate(`/book/${id}`);
  }

  return (
    <aside className="sidebar">
      <div className="s-label">Книги</div>
      <nav className="menu">
        {books.map((b, i) => (
          <button
            key={b.id}
            className={`slide-fs-toc-item ${
              String(activeBookId) === String(b.id) ? "on" : ""
            }`}
            onClick={() => openBook(b.id)}
          >
            <span className="slide-fs-toc-num">
              {String(i + 1).padStart(2, "0")}
            </span>
            <span className="slide-fs-toc-name">{b.title}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}
