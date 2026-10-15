import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { useOutletContext, useSearchParams } from "react-router-dom";
import { SLIDES, SLIDE_TITLES } from "../../lib/slides.js";
import { usePlayer } from "../../lib/player.jsx";
import { SlideAudioContext } from "../../lib/slideAudio.js";
import { fmtTime } from "../../lib/time.js";
import { markSlide } from "../../lib/progress.js";

export default function ChapterTheory() {
  const { chapter, bookId } = useOutletContext();
  const { playingId, paused, progress, togglePause, playSequence } = usePlayer();
  const [searchParams, setSearchParams] = useSearchParams();
  // Ручной выбор слайда живёт в URL (?slide=N) — перезагрузка возвращает на тот же слайд.
  const slideParam = searchParams.get("slide");
  const manualIdx =
    slideParam == null ? null : Math.max(0, parseInt(slideParam, 10) || 0);
  const setManualIdx = (i) =>
    setSearchParams(i == null ? {} : { slide: String(i) }, { replace: true });

  const activeIdx = chapter
    ? chapter.lessons.findIndex((l) => l.id === playingId)
    : -1;

  // У каждой главы есть слайды; каждая часть — один абзац со своим слайдом и
  // своим аудио-файлом. Слайд следует за играющей частью, иначе — ручной выбор.
  const slides =
    chapter && bookId != null
      ? SLIDES[`${bookId}:${chapter.num}`] || null
      : null;
  const slideTitles =
    chapter && bookId != null
      ? SLIDE_TITLES[`${bookId}:${chapter.num}`] || null
      : null;

  let slideIdx = 0;
  if (slides) {
    if (activeIdx >= 0) slideIdx = chapter.lessons[activeIdx].ord;
    else if (manualIdx != null) slideIdx = manualIdx;
    slideIdx = Math.min(slideIdx, slides.length - 1);
  }

  // просмотренный слайд идёт в прогресс (дашборд на главной)
  useEffect(() => {
    if (slides) markSlide(bookId, chapter.num, slideIdx);
  }, [slides, bookId, chapter.num, slideIdx]);

  if (!slides) return <p className="error">У этой главы нет слайдов</p>;

  function asItems(lessons) {
    return lessons.map((l) => ({
      id: l.id,
      url: l.audio,
      title: `Часть ${l.ord + 1}`,
      subtitle: `Урок ${chapter.num}. ${chapter.title}`,
      badge: String(chapter.num),
    }));
  }

  // Клик по слайду: если глава играет — начинаем с этой части, иначе просто
  // показываем слайд.
  function pickSlide(i) {
    if (chapterPlaying) {
      const cur = activeIdx >= 0 ? chapter.lessons[activeIdx] : null;
      if (cur && cur.ord === i && paused) togglePause();
      else playSequence(asItems(chapter.lessons.slice(i)));
      setManualIdx(null);
    } else {
      setManualIdx(i);
    }
  }

  const chapterPlaying =
    playingId != null && chapter.lessons.some((l) => l.id === playingId);

  function panelPlay() {
    if (chapterPlaying && paused) togglePause();
    else if (!chapterPlaying) {
      const start = manualIdx != null ? manualIdx : 0;
      playSequence(asItems(chapter.lessons.slice(start)));
      setManualIdx(null);
    }
  }

  function panelPause() {
    if (chapterPlaying && !paused) togglePause();
  }

  // Время на уровне главы: позиция = сумма частей до показанного слайда
  // + прогресс внутри него; всего — сумма всех частей.
  const durOf = (l) => (l.dur ? Number(l.dur) : 0);
  const chapterDur = chapter.lessons.reduce((a, l) => a + durOf(l), 0);
  const offsetBefore = chapter.lessons.reduce(
    (a, l) => a + (l.ord < slideIdx ? durOf(l) : 0),
    0,
  );
  const playingThisSlide =
    activeIdx >= 0 && chapter.lessons[activeIdx].ord === slideIdx;
  const chapterPos =
    offsetBefore + (playingThisSlide && progress ? progress.t : 0);

  return (
    <div>
      <SlidePanel
        slides={slides}
        titles={slideTitles}
        idx={slideIdx}
        onPick={pickSlide}
        t={chapterPos}
        d={chapterDur}
        audioT={
          playingThisSlide
            ? progress?.id === playingId
              ? progress.t
              : 0
            : null
        }
        caption={`Урок ${chapter.num}. ${chapter.title}`}
        playing={chapterPlaying && !paused}
        onPlay={panelPlay}
        onPause={panelPause}
      />
    </div>
  );
}

function SlidePanel({
  slides,
  titles,
  idx,
  onPick,
  t,
  d,
  audioT,
  caption,
  playing,
  onPlay,
  onPause,
}) {
  const [fs, setFs] = useState(false);
  const fsRef = useRef(null);
  const Comp = slides[Math.min(idx, slides.length - 1)];
  const count = String(slides.length).padStart(2, "0");

  useEffect(() => {
    if (!fs) return;
    const el = fsRef.current;
    // Fullscreen API, если доступен; оверлей и так закрывает весь экран.
    if (el && el.requestFullscreen) el.requestFullscreen().catch(() => {});
    const onFsChange = () => {
      if (!document.fullscreenElement) setFs(false);
    };
    const onKey = (e) => {
      if (e.key === "Escape") setFs(false);
      else if (e.key === "ArrowRight" || e.key === "ArrowDown")
        onPick(Math.min(idx + 1, slides.length - 1));
      else if (e.key === "ArrowLeft" || e.key === "ArrowUp")
        onPick(Math.max(idx - 1, 0));
    };
    document.addEventListener("fullscreenchange", onFsChange);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("fullscreenchange", onFsChange);
      document.removeEventListener("keydown", onKey);
    };
  }, [fs, idx, slides.length, onPick]);

  // При закрытии оверлея выходим и из нативного фулскрина.
  useEffect(() => {
    if (!fs && document.fullscreenElement) {
      document.exitFullscreen().catch(() => {});
    }
  }, [fs]);

  // Список названий следует за активным слайдом.
  useEffect(() => {
    if (!fs || !fsRef.current) return;
    const el = fsRef.current.querySelector(".slide-fs-toc-item.on");
    if (el) el.scrollIntoView({ block: "nearest" });
  }, [idx, fs]);

  const dots = (cls) => (
    <div className={cls}>
      {slides.map((_, i) => (
        <button
          key={i}
          className={`slide-dot ${i === idx ? "on" : ""}`}
          onClick={() => onPick(i)}
          title={`Слайд ${i + 1}`}
        />
      ))}
    </div>
  );

  return (
    <>
      <aside className="slide-panel">
        <div className="slide-panel-head">
          <span className="slide-panel-num">
            {String(idx + 1).padStart(2, "0")} / {count}
          </span>
          <span className="s-time-mono">
            {t != null ? `${fmtTime(t)} / ${fmtTime(d)}` : "—"}
          </span>
          <button
            className="slide-btn"
            onClick={playing ? onPause : onPlay}
            title={playing ? "Пауза" : "Играть"}
          >
            {playing ? <PauseIcon /> : <PlayIcon />}
            <span>{playing ? "Пауза" : "Играть"}</span>
          </button>
          <button
            className="slide-btn"
            onClick={() => setFs(true)}
            title="Слайды на весь экран"
          >
            <ExpandIcon />
          </button>
        </div>
        <div className="slide-stage" key={idx}>
          <SlideAudioContext.Provider value={audioT}>
            <Comp />
          </SlideAudioContext.Provider>
        </div>
        {dots("slide-dots")}
      </aside>

      {fs &&
        createPortal(
          <div className="slide-fs" ref={fsRef}>
            <div className="slide-fs-main">
              <div className="slide-fs-head">
                <span className="slide-fs-caption">{caption}</span>
                <span className="slide-panel-num">
                  {String(idx + 1).padStart(2, "0")} / {count}
                </span>
                <span className="s-time-mono">
                  {t != null ? `${fmtTime(t)} / ${fmtTime(d)}` : "—"}
                </span>
                <button
                  className="slide-btn"
                  onClick={playing ? onPause : onPlay}
                  title={playing ? "Пауза" : "Играть"}
                >
                  {playing ? <PauseIcon /> : <PlayIcon />}
                  <span>{playing ? "Пауза" : "Играть"}</span>
                </button>
                <button
                  className="slide-btn"
                  onClick={() => setFs(false)}
                  title="Свернуть (Esc)"
                >
                  <CollapseIcon />
                  <span>Свернуть</span>
                </button>
              </div>
              <div className="slide-fs-stage" key={idx}>
                <SlideAudioContext.Provider value={audioT}>
                  <Comp />
                </SlideAudioContext.Provider>
              </div>
            </div>
            <aside className="slide-fs-toc">
              {slides.map((_, i) => (
                <button
                  key={i}
                  className={`slide-fs-toc-item ${i === idx ? "on" : ""}`}
                  onClick={() => onPick(i)}
                >
                  <span className="slide-fs-toc-num">
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <span className="slide-fs-toc-name">
                    {titles ? titles[i] : `Слайд ${i + 1}`}
                  </span>
                </button>
              ))}
            </aside>
          </div>,
          document.body,
        )}
    </>
  );
}

const ExpandIcon = () => (
  <svg
    width="13"
    height="13"
    viewBox="0 0 14 14"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.7"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M5 1H1v4M9 1h4v4M5 13H1V9M9 13h4V9" />
  </svg>
);

const CollapseIcon = () => (
  <svg
    width="11"
    height="11"
    viewBox="0 0 14 14"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.7"
    strokeLinecap="round"
  >
    <path d="M2 2l10 10M12 2L2 12" />
  </svg>
);

const PlayIcon = () => (
  <svg width="11" height="11" viewBox="0 0 12 12" fill="currentColor">
    <path d="M2.5 1.2v9.6L10.5 6z" />
  </svg>
);

const PauseIcon = () => (
  <svg width="11" height="11" viewBox="0 0 12 12" fill="currentColor">
    <rect x="2" y="1.5" width="3" height="9" rx="0.8" />
    <rect x="7" y="1.5" width="3" height="9" rx="0.8" />
  </svg>
);
