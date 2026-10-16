import { useEffect, useMemo, useState } from "react";
import { createPortal } from "react-dom";
import {
  NavLink,
  Outlet,
  useLocation,
  useNavigate,
  useOutletContext,
  useParams,
  useSearchParams,
} from "react-router-dom";
import FsTree from "../../components/FsTree.jsx";
import { usePlayer } from "../../lib/player.jsx";
import { hasSlides as chapterHasSlides } from "../../lib/slides.js";
import { QUIZZES } from "../../lib/quizzes.js";
import { EXERCISES } from "../../lib/exercises.js";
import { useProgress } from "../../lib/progress.jsx";
import { useApi, useCodeCounts } from "../../lib/queries.js";

/* Страница главы: заголовок и три вкладки, каждая со своим адресом —
     /book/:bookId/chapter/:chapterId             Теория  (слайды)
     /book/:bookId/chapter/:chapterId/questions   Вопросы (квизы)
     /book/:bookId/chapter/:chapterId/exercises   Практика (код в Docker)
   Данные главы грузятся один раз и отдаются вкладкам через контекст. */
export default function ChapterDetail() {
  const { bookId, chapterId } = useParams();
  const parent = useOutletContext();
  const navigate = useNavigate();
  const location = useLocation();
  const { stop } = usePlayer();
  const [searchParams, setSearchParams] = useSearchParams();
  // полноэкранный режим — в адресе (?fs=1): переживает смену вкладки и главы
  const fs = searchParams.get("fs") === "1";
  const setFs = (on) =>
    setSearchParams(
      (prev) => {
        const n = new URLSearchParams(prev);
        if (on) n.set("fs", "1");
        else n.delete("fs");
        return n;
      },
      { replace: true },
    );
  // слоты левого дерева и шапки: активная вкладка публикует в них пункты и кнопки
  const [itemsSlot, setItemsSlot] = useState(null);
  const [headSlot, setHeadSlot] = useState(null);
  const { data: chapter, error: chapterError } = useApi(
    chapterId == null ? null : `/api/chapters/${chapterId}`,
  );
  const error = chapterError ? "Урок не найден" : null;
  const codeCounts = useCodeCounts(); // {книга: {глава: число}} — куда идти по Ctrl+Enter

  // Код-упражнения (Docker-песочница) ключуются номером главы; ответ 404 — упражнений нет.
  const tasksQuery = useApi(
    chapter == null || bookId == null ? null : `/api/exercises/${bookId}/${chapter.num}`,
  );
  const tasksReady = chapter != null && !tasksQuery.loading;
  const codeTasks = useMemo(() => {
    const d = tasksQuery.data;
    return (d?.tasks || []).map((t) =>
      t.dataset && d.datasets?.[t.dataset] ? { ...t, schema: d.datasets[t.dataset] } : t,
    );
  }, [tasksQuery.data]);

  useEffect(() => {
    if (!fs) {
      if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
      return;
    }
    // Полный экран берём у корня документа, а не у оверлея: оверлей можно пересоздать,
    // и браузер вышел бы из полноэкранного режима, когда его элемент исчезает из DOM.
    const root = document.documentElement;
    if (!document.fullscreenElement && root.requestFullscreen)
      root.requestFullscreen().catch(() => {});
    const onFsChange = () => {
      if (!document.fullscreenElement) setFs(false);
    };
    const onKey = (e) => {
      if (e.key === "Escape") setFs(false);
    };
    document.addEventListener("fullscreenchange", onFsChange);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("fullscreenchange", onFsChange);
      document.removeEventListener("keydown", onKey);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fs]);

  const search = fs ? "?fs=1" : "";
  const inner = error ? (
    <p className="error">{error}</p>
  ) : !chapter ? (
    <p className="empty">Загрузка…</p>
  ) : null;

  const key = chapter ? `${bookId}:${chapter.num}` : null;
  const quiz = (key && QUIZZES[key]) || null;
  const practice = (key && EXERCISES[key]) || null;
  const hasSlides = !!key && chapterHasSlides(key);
  const hasPractice = codeTasks.length > 0 || !!practice;
  const progress = useProgress();
  const doneCodes = chapter ? progress.codeStatus(bookId, chapter.num) : {};
  const solved = codeTasks.filter((t) => doneCodes[t.id] === "ok").length;

  const tabs = chapter
    ? [
        hasSlides && { to: ".", end: true, label: "Теория" },
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
      ].filter(Boolean)
    : [];

  const tabsNav = (
    <nav className="ch-tabs" aria-label="Разделы урока">
      {tabs.map((t) => (
        <NavLink
          key={t.label}
          to={{ pathname: t.to, search }}
          end={t.end}
          className={({ isActive }) => `ch-tab ${isActive ? "on" : ""}`}
        >
          {t.label}
          {t.badge && <span className="ch-tab-badge">{t.badge}</span>}
        </NavLink>
      ))}
      {!fs && (
        <button
          className="ch-expand"
          onClick={() => setFs(true)}
          title="Весь экран"
          aria-label="Развернуть на весь экран"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
            <path d="M5 1H1v4M9 1h4v4M5 13H1V9M9 13h4V9" />
          </svg>
        </button>
      )}
    </nav>
  );

  // следующая глава этой книги, где есть код-упражнения (если число упражнений
  // неизвестно — просто следующая)
  const flat = (parent?.course || []).flatMap((sec) => sec.chapters);
  const at = flat.findIndex((c) => String(c.id) === String(chapterId));
  const nextPractice =
    at < 0
      ? null
      : flat
          .slice(at + 1)
          .find((c) => (codeCounts ? codeCounts[bookId]?.[c.num] > 0 : true)) || null;

  const content =
    inner ||
    (
      <Outlet
        context={{
          bookId,
          chapterId,
          course: parent?.course || [],
          chapter,
          quiz,
          practice,
          codeTasks,
          tasksReady,
          nextPractice,
          fs,
          itemsSlot,
          headSlot,
        }}
      />
    );

  if (fs)
    return createPortal(
      <div className="slide-fs">
        <FsTree
          sections={parent?.course || []}
          chapterId={chapterId}
          setItemsSlot={setItemsSlot}
          onOpenChapter={(id) => {
            stop();
            // другая глава открывается с теории
            navigate(`/book/${bookId}/chapter/${id}?fs=1`);
          }}
        />
        <div className="slide-fs-main">
          <div className="slide-fs-head">
            <span className="slide-fs-caption">
              {chapter ? `Урок ${chapter.num}. ${chapter.title}` : "…"}
            </span>
            {tabsNav}
            <span className="slide-fs-slot" ref={setHeadSlot} />
            <button
              className="slide-btn"
              onClick={() => setFs(false)}
              title="Свернуть (Esc)"
            >
              <svg width="11" height="11" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round">
                <path d="M2 2l10 10M12 2L2 12" />
              </svg>
              <span>Свернуть</span>
            </button>
          </div>
          <div className="slide-fs-body">{content}</div>
        </div>
      </div>,
      document.body,
    );

  if (inner) return inner;
  return (
    <div>
      <p className="crumbs">{chapter.section}</p>
      <h2>
        Урок {chapter.num}. {chapter.title}
      </h2>
      {tabsNav}
      {content}
    </div>
  );
}
