import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { useNavigate, useOutletContext, useSearchParams } from "react-router-dom";
import { SLIDES, SLIDE_TITLES } from "../../lib/slides.js";
import { usePlayer } from "../../lib/player.jsx";
import { SlideAudioContext } from "../../lib/slideAudio.js";
import { fmtTime } from "../../lib/time.js";
import { markSlide } from "../../lib/progress.js";

export default function ChapterTheory() {
  const { chapter, bookId, chapterId, course } = useOutletContext();
  const navigate = useNavigate();
  const { playingId, paused, progress, togglePause, playSequence, stop } = usePlayer();
  const [searchParams, setSearchParams] = useSearchParams();
  // Ручной выбор слайда живёт в URL (?slide=N) — перезагрузка возвращает на тот же слайд.
  const slideParam = searchParams.get("slide");
  const manualIdx =
    slideParam == null ? null : Math.max(0, parseInt(slideParam, 10) || 0);
  // остальные параметры адреса (например, fs) сохраняются
  const patchParams = (fn) =>
    setSearchParams(
      (prev) => {
        const n = new URLSearchParams(prev);
        fn(n);
        return n;
      },
      { replace: true },
    );
  const setManualIdx = (i) =>
    patchParams((n) => (i == null ? n.delete("slide") : n.set("slide", String(i))));
  // полноэкранный режим живёт в адресе (?fs=1) и переживает переход между главами
  const fs = searchParams.get("fs") === "1";
  const setFs = (on) => patchParams((n) => (on ? n.set("fs", "1") : n.delete("fs")));

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
        fs={fs}
        setFs={setFs}
        tree={{
          sections: course,
          chapterId,
          onOpenChapter: (id) => {
            stop();
            navigate(`/book/${bookId}/chapter/${id}?fs=1`);
          },
        }}
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
  fs,
  setFs,
  tree,
  playing,
  onPlay,
  onPause,
}) {
  const fsRef = useRef(null);
  const openedAt = useRef(0);
  const Comp = slides[Math.min(idx, slides.length - 1)];
  const count = String(slides.length).padStart(2, "0");

  useEffect(() => {
    if (!fs) return;
    const el = fsRef.current;
    // Fullscreen API, если доступен; оверлей и так закрывает весь экран.
    if (el && el.requestFullscreen) el.requestFullscreen().catch(() => {});
    openedAt.current = Date.now();
    const onFsChange = () => {
      // при переходе между главами старый оверлей снимается и браузер на миг
      // выходит из полноэкранного режима — это не «закрыть»
      if (Date.now() - openedAt.current < 1200) return;
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
    const el = fsRef.current.querySelector(".fst-slide.on");
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
            <FsTree
              sections={tree.sections}
              chapterId={tree.chapterId}
              onOpenChapter={tree.onOpenChapter}
              titles={titles}
              count={slides.length}
              idx={idx}
              onPick={onPick}
            />
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
          </div>,
          document.body,
        )}
    </>
  );
}

// Левое дерево полноэкранного режима: разделы книги, у открытой главы — слайды.
function FsTree({ sections, chapterId, onOpenChapter, titles, count, idx, onPick }) {
  const curSec = sections.find((sec) =>
    sec.chapters.some((c) => String(c.id) === String(chapterId)),
  )?.id;
  const [open, setOpen] = useState(() => new Set(curSec != null ? [curSec] : []));
  // раздел с текущей главой раскрыт всегда, остальные — по клику
  useEffect(() => {
    if (curSec != null) setOpen((prev) => new Set(prev).add(curSec));
  }, [curSec]);
  const toggle = (id) =>
    setOpen((prev) => {
      const n = new Set(prev);
      if (n.has(id)) n.delete(id);
      else n.add(id);
      return n;
    });

  const slideList = (
    <div className="fst-slides">
      {Array.from({ length: count }, (_, i) => (
        <button
          key={i}
          className={`fst-slide ${i === idx ? "on" : ""}`}
          onClick={() => onPick(i)}
        >
          <span className="fst-slide-num">{String(i + 1).padStart(2, "0")}</span>
          <span className="fst-slide-name">{titles ? titles[i] : `Слайд ${i + 1}`}</span>
        </button>
      ))}
    </div>
  );

  return (
    <aside className="slide-fs-toc" aria-label="Содержание">
      {sections.length === 0
        ? slideList
        : sections.map((sec) => {
            const isOpen = open.has(sec.id);
            return (
              <div key={sec.id} className="fst-sec">
                <button
                  className="fst-sec-head"
                  onClick={() => toggle(sec.id)}
                  aria-expanded={isOpen}
                >
                  <span className={`fst-chev ${isOpen ? "open" : ""}`}>›</span>
                  {sec.title}
                </button>
                {isOpen &&
                  sec.chapters.map((ch) => {
                    const cur = String(ch.id) === String(chapterId);
                    return (
                      <div key={ch.id}>
                        <button
                          className={`slide-fs-toc-item ${cur ? "on" : ""}`}
                          onClick={() => !cur && onOpenChapter(ch.id)}
                        >
                          <span className="slide-fs-toc-num">
                            {String(ch.num).padStart(2, "0")}
                          </span>
                          <span className="slide-fs-toc-name">{ch.title}</span>
                        </button>
                        {cur && slideList}
                      </div>
                    );
                  })}
              </div>
            );
          })}
    </aside>
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
