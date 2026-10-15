import { useEffect, useState } from "react";
import { Route, Routes, useNavigate } from "react-router-dom";
import AudioPlayer from "./components/AudioPlayer.jsx";
import { PlayerProvider, usePlayer } from "./lib/player.jsx";
import BookDetail from "./pages/books/detail.jsx";
import BooksIndex from "./pages/books/index.jsx";
import ChapterDetail from "./pages/chapters/detail.jsx";
import ChapterExercises from "./pages/chapters/exercises.jsx";
import ChapterQuestions from "./pages/chapters/questions.jsx";
import ChapterTheory from "./pages/chapters/theory.jsx";
import ChaptersIndex from "./pages/chapters/index.jsx";

export default function App() {
  return (
    <PlayerProvider>
      <Shell />
    </PlayerProvider>
  );
}

function Shell() {
  const [books, setBooks] = useState([]);
  const navigate = useNavigate();
  const { stop } = usePlayer();
  const [theme, setTheme] = useState(
    () => localStorage.getItem("say-theme") || "dark",
  );

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("say-theme", theme);
  }, [theme]);

  useEffect(() => {
    fetch("/api/books")
      .then((r) => r.json())
      .then(setBooks)
      .catch(() => {});
  }, []);

  function goHome() {
    stop();
    navigate("/");
  }

  // Навигация живёт в URL: /, /book/:bookId, /book/:bookId/chapter/:chapterId[/questions|/exercises]
  return (
    <div className="app">
      <header className="topbar">
        <button className="logo" onClick={goHome} title="На главную">
          Аудитория
        </button>
        <div className="topbar-right">
          <button
            className="theme-toggle"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            title={theme === "dark" ? "Светлая тема" : "Тёмная тема"}
          >
            {theme === "dark" ? "Светлая" : "Тёмная"}
          </button>
        </div>
      </header>

      <Routes>
        <Route path="/" element={<BooksIndex books={books} />} />
        <Route path="/book/:bookId" element={<BookDetail books={books} />}>
          <Route index element={<ChaptersIndex />} />
          <Route path="chapter/:chapterId" element={<ChapterDetail />}>
            <Route index element={<ChapterTheory />} />
            <Route path="questions" element={<ChapterQuestions />} />
            <Route path="exercises" element={<ChapterExercises />} />
          </Route>
        </Route>
      </Routes>

      <AudioPlayer />
    </div>
  );
}
