import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { usePlayer } from "../lib/player.jsx";
import BookIcon from "./BookIcon.jsx";

const STORE = "say-aside-collapsed";

// Меню книг: список с названиями или, если свёрнуто, колонка квадратных иконок.
export default function AsideMenu({ books, activeBookId }) {
  const navigate = useNavigate();
  const { stop } = usePlayer();
  const [collapsed, setCollapsed] = useState(() => {
    try {
      return localStorage.getItem(STORE) === "1";
    } catch {
      return false;
    }
  });

  function toggle() {
    setCollapsed((c) => {
      try {
        localStorage.setItem(STORE, c ? "0" : "1");
      } catch {
        /* без сохранения */
      }
      return !c;
    });
  }

  function openBook(id) {
    stop();
    navigate(`/book/${id}`);
  }

  return (
    <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>
      <div className="aside-head">
        {!collapsed && <div className="s-label">Книги</div>}
        <button
          className="aside-toggle"
          onClick={toggle}
          title={collapsed ? "Развернуть меню" : "Свернуть меню"}
          aria-label={collapsed ? "Развернуть меню книг" : "Свернуть меню книг"}
          aria-expanded={!collapsed}
        >
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <rect x="3" y="3" width="18" height="18" rx="2" />
            <path d="M9 3v18" />
            {collapsed ? <path d="m14 9 3 3-3 3" /> : <path d="m16 15-3-3 3-3" />}
          </svg>
        </button>
      </div>
      <nav className="menu">
        {books.map((b, i) => {
          const on = String(activeBookId) === String(b.id);
          return collapsed ? (
            <button
              key={b.id}
              className={`aside-icon ${on ? "on" : ""}`}
              onClick={() => openBook(b.id)}
              title={b.title}
              aria-label={b.title}
            >
              <BookIcon id={b.id} />
            </button>
          ) : (
            <button
              key={b.id}
              className={`slide-fs-toc-item ${on ? "on" : ""}`}
              onClick={() => openBook(b.id)}
            >
              <span className="slide-fs-toc-num">
                {String(i + 1).padStart(2, "0")}
              </span>
              <span className="slide-fs-toc-name">{b.title}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}
