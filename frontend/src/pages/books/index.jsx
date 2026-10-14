import { useNavigate } from "react-router-dom";
import { usePlayer } from "../../lib/player.jsx";

export default function BooksIndex({ books }) {
  const navigate = useNavigate();
  const { stop } = usePlayer();

  function openBook(id) {
    stop();
    navigate(`/book/${id}`);
  }

  return (
    <main className="content home">
      <h2>Книги</h2>
      {books.length === 0 ? (
        <p className="empty">Книги не загружены. Запусти seed_textbook.py</p>
      ) : (
        <div className="book-grid">
          {books.map((b, i) => (
            <button
              key={b.id}
              className="book-card"
              onClick={() => openBook(b.id)}
            >
              <span className="book-num">{String(i + 1).padStart(2, "0")}</span>
              <span className="book-name">{b.title}</span>
              <span className="book-meta">
                {b.sections_count} разделов · {b.lessons_count} уроков
              </span>
            </button>
          ))}
        </div>
      )}
    </main>
  );
}
