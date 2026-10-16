import { useEffect, useState } from "react";
import { NavLink, Route, Routes, useNavigate } from "react-router-dom";
import AsideMenu from "./components/AsideMenu.jsx";
import AudioPlayer from "./components/AudioPlayer.jsx";
import { useAuth } from "./lib/auth.tsx";
import { PlayerProvider, usePlayer } from "./lib/player.tsx";
import { useProgress } from "./lib/progress.tsx";
import { useBooks } from "./lib/queries.ts";
import AuthPage from "./pages/auth/index.jsx";
import BookDetail from "./pages/books/detail.jsx";
import BooksIndex from "./pages/books/index.jsx";
import ChapterDetail from "./pages/chapters/detail.jsx";
import ChapterExercises from "./pages/chapters/exercises.jsx";
import ChapterQuestions from "./pages/chapters/questions.jsx";
import ChapterTheory from "./pages/chapters/theory.jsx";
import ChaptersIndex from "./pages/chapters/index.jsx";
import SettingsPage from "./pages/settings/index.jsx";

export default function App() {
  return (
    <PlayerProvider>
      <Shell />
    </PlayerProvider>
  );
}

function Shell() {
  const books = useBooks();
  const navigate = useNavigate();
  const { stop } = usePlayer();
  const { user, logout } = useAuth();
  const { ready } = useProgress();
  const [theme, setTheme] = useState(
    () => localStorage.getItem("say-theme") || "dark",
  );

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("say-theme", theme);
  }, [theme]);

  function goHome() {
    stop();
    navigate("/");
  }

  const themeButton = (
      <button
        type="button"
        className="btn-icon"
        onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        title={theme === "dark" ? "Светлая тема" : "Тёмная тема"}
        aria-label={theme === "dark" ? "Включить светлую тему" : "Включить тёмную тему"}
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          {theme === "dark" ? (
            <>
              <circle cx="12" cy="12" r="4" />
              <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
            </>
          ) : (
            <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" />
          )}
        </svg>
      </button>
  );

  // пока узнаём, кто вошёл, и пока грузится кабинет — пустой экран; без входа — форма входа
  if (user === undefined || (user && !ready)) return <div className="boot">Загрузка…</div>;
  if (user === null) return <AuthPage themeButton={themeButton} />;

  // Навигация живёт в URL: /, /book/:bookId, /book/:bookId/chapter/:chapterId[/questions|/exercises]
  return (
    <div className="app">
      <header className="topbar">
        <button className="logo" onClick={goHome} title="На главную">
          CS.Core
        </button>
        <div className="topbar-right">
          <NavLink
            to="/settings"
            className={({ isActive }) => `btn-icon ${isActive ? "on" : ""}`}
            title="Настройки"
            aria-label="Настройки"
            onClick={stop}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
          </NavLink>
          {themeButton}
          <span className="user-chip" title={user.email}>
            <span className="user-ava">{user.login[0].toUpperCase()}</span>
            {user.login}
          </span>
          <button
            type="button"
            className="btn-icon"
            onClick={() => {
              stop();
              logout();
            }}
            title="Выйти"
            aria-label="Выйти из аккаунта"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9" />
            </svg>
          </button>
        </div>
      </header>

      <div className="layout">
        <AsideMenu books={books} />
        <Routes>
          <Route path="/" element={<BooksIndex books={books} />} />
          <Route
            path="/settings"
            element={<SettingsPage theme={theme} setTheme={setTheme} />}
          />
          <Route path="/book/:bookId" element={<BookDetail books={books} />}>
            <Route index element={<ChaptersIndex />} />
            <Route path="chapter/:chapterId" element={<ChapterDetail />}>
              <Route index element={<ChapterTheory />} />
              <Route path="questions" element={<ChapterQuestions />} />
              <Route path="exercises" element={<ChapterExercises />} />
            </Route>
          </Route>
        </Routes>
      </div>

      <AudioPlayer />
    </div>
  );
}
