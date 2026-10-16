import { useState } from "react";
import { useMatch, useNavigate } from "react-router-dom";
import { usePlayer } from "../lib/player.tsx";
import { KEYS, readSetting, writeSetting } from "../lib/settings.ts";
import type { Book } from "../types.ts";
import BookIcon from "./BookIcon.tsx";

// Меню разделов (книг курса): список с названиями или, если свёрнуто, колонка квадратных иконок.
export default function AsideMenu({ books }: { books: Book[] }) {
  const navigate = useNavigate();
  const activeBookId = useMatch("/book/:bookId/*")?.params.bookId;
  const { stop } = usePlayer();
  const [collapsed, setCollapsed] = useState(() => readSetting(KEYS.aside) === "1");

  function toggle() {
    setCollapsed((c) => {
      writeSetting(KEYS.aside, c ? "0" : "1");
      return !c;
    });
  }

  function openBook(id: number) {
    stop();
    navigate(`/book/${id}`);
  }

  return (
    <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>
      <div className="aside-head">
        {!collapsed && <div className="s-label">Разделы</div>}
        <button
          className="aside-toggle"
          onClick={toggle}
          title={collapsed ? "Развернуть меню" : "Свернуть меню"}
          aria-label={collapsed ? "Развернуть меню разделов" : "Свернуть меню разделов"}
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
              <BookIcon icon={b.icon} />
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
