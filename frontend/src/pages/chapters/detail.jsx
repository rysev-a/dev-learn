import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { useParams, useSearchParams } from "react-router-dom";
import {
  SLIDES,
  SLIDE_TITLES,
  paraIndexFor,
} from "../../lib/slides.js";
import { usePlayer } from "../../lib/player.jsx";
import { fmtTime } from "../../lib/time.js";
import { QUIZZES } from "../../lib/quizzes.js";
import { EXERCISES } from "../../lib/exercises.js";
import Quiz from "../../components/Quiz.jsx";
import Exercises from "../../components/Exercises.jsx";
import CodeExercises from "../../components/CodeExercises.jsx";

export default function ChapterDetail() {
  const { bookId, chapterId } = useParams();
  const { playingId, paused, progress, togglePause, seek, playSequence } =
    usePlayer();
  const [chapter, setChapter] = useState(null);
  const [error, setError] = useState(null);
  // Код-упражнения (Docker-песочница): приходят с бэкенда, если есть.
  const [codeTasks, setCodeTasks] = useState([]);
  const [searchParams, setSearchParams] = useSearchParams();
  // Ручной выбор слайда живёт в URL (?slide=N) — перезагрузка возвращает на тот же слайд.
  const slideParam = searchParams.get("slide");
  const manualIdx =
    slideParam == null ? null : Math.max(0, parseInt(slideParam, 10) || 0);
  const setManualIdx = (i) =>
    setSearchParams(i == null ? {} : { slide: String(i) }, { replace: true });

  useEffect(() => {
    if (chapterId == null) return;
    setError(null);
    setChapter(null);
    setCodeTasks([]);
    fetch(`/api/chapters/${chapterId}`)
      .then((r) => {
        if (!r.ok) throw new Error("Урок не найден");
        return r.json();
      })
      .then(setChapter)
      .catch((e) => setError(e.message));
  }, [chapterId]);

  // Код-упражнения (Docker-песочница): ключуются номером главы, 404 — просто нет.
  useEffect(() => {
    if (chapter == null || bookId == null) return;
    let alive = true;
    fetch(`/api/exercises/${bookId}/${chapter.num}`)
      .then((r) => (r.ok ? r.json() : { tasks: [] }))
      .then((d) => {
        if (alive) setCodeTasks(d.tasks || []);
      })
      .catch(() => {});
    return () => {
      alive = false;
    };
  }, [chapter, bookId]);

  const activeIdx = chapter
    ? chapter.lessons.findIndex((l) => l.id === playingId)
    : -1;

  // Слайды: следуют за голосом через activeSent, иначе — ручной выбор.
  const slides =
    chapter && bookId != null
      ? SLIDES[`${bookId}:${chapter.num}`] || null
      : null;
  const slideTitles =
    chapter && bookId != null
      ? SLIDE_TITLES[`${bookId}:${chapter.num}`] || null
      : null;
  // Каждая часть главы — один абзац: свой слайд и свой аудио-файл.
  const partMode = !!slides && !!chapter && chapter.lessons.length > 1;

  // Текущее предложение играющей части: кумулятивный вес (длина) против доли времени.
  // В частичном режиме караоке-подсветка выключена.
  let activeSent = -1;
  if (!partMode && chapter && activeIdx >= 0 && progress && progress.d > 0) {
    const weights = splitSentences(chapter.lessons[activeIdx].text)
      .filter((it) => it.type === "s")
      .map((it) => it.text.length);
    const total = weights.reduce((a, b) => a + b, 0) || 1;
    const target = (progress.t / progress.d) * total;
    let acc = 0;
    activeSent = weights.length - 1;
    for (let i = 0; i < weights.length; i++) {
      acc += weights[i];
      if (target < acc) {
        activeSent = i;
        break;
      }
    }
  }

  let slideIdx = 0;
  if (slides) {
    if (partMode) {
      if (activeIdx >= 0) slideIdx = chapter.lessons[activeIdx].ord;
      else if (manualIdx != null) slideIdx = manualIdx;
    } else if (activeSent >= 0) {
      slideIdx = paraIndexFor(
        splitSentences(chapter.lessons[0].text),
        activeSent,
      );
    } else if (manualIdx != null) {
      slideIdx = manualIdx;
    }
    slideIdx = Math.min(slideIdx, slides.length - 1);
  }

  if (error) return <p className="error">{error}</p>;
  if (!chapter) return <p className="empty">Загрузка…</p>;

  const quiz =
    bookId != null ? QUIZZES[`${bookId}:${chapter.num}`] || null : null;
  const practice =
    bookId != null ? EXERCISES[`${bookId}:${chapter.num}`] || null : null;

  function asItems(lessons) {
    return lessons.map((l) => ({
      id: l.id,
      url: l.audio,
      title: `Часть ${l.ord + 1}`,
      subtitle: `Урок ${chapter.num}. ${chapter.title}`,
      badge: String(chapter.num),
    }));
  }

  // Клик по слайду: в частичном режиме — играем с этой части; если глава
  // играет — перематываем аудио к началу абзаца; иначе просто показываем.
  function pickSlide(i) {
    if (partMode) {
      if (chapterPlaying) {
        const cur = activeIdx >= 0 ? chapter.lessons[activeIdx] : null;
        if (cur && cur.ord === i && paused) togglePause();
        else playSequence(asItems(chapter.lessons.slice(i)));
        setManualIdx(null);
      } else {
        setManualIdx(i);
      }
      return;
    }
    const first = chapter.lessons[0];
    if (playingId != null && first && playingId === first.id) {
      seek(paraStartFraction(first.text, i));
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
      const start = partMode && manualIdx != null ? manualIdx : 0;
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
  const slideOrd = partMode ? slideIdx : 0;
  const offsetBefore = chapter.lessons.reduce(
    (a, l) => a + (l.ord < slideOrd ? durOf(l) : 0),
    0,
  );
  const playingThisSlide =
    activeIdx >= 0 && chapter.lessons[activeIdx].ord === slideOrd;
  const chapterPos =
    offsetBefore + (playingThisSlide && progress ? progress.t : 0);

  if (slides) {
    return (
      <div>
        <p className="crumbs">{chapter.section}</p>
        <h2>
          Урок {chapter.num}. {chapter.title}
        </h2>
        <SlidePanel
          slides={slides}
          titles={slideTitles}
          idx={slideIdx}
          onPick={pickSlide}
          t={chapterPos}
          d={chapterDur}
          caption={`Урок ${chapter.num}. ${chapter.title}`}
          playing={chapterPlaying && !paused}
          onPlay={panelPlay}
          onPause={panelPause}
        />
        {quiz && <Quiz quiz={quiz} />}
        {practice && <Exercises quiz={practice} />}
        {codeTasks.length > 0 && (
          <CodeExercises
            key={`${bookId}:${chapter.num}`}
            tasks={codeTasks}
            bookId={bookId}
            chapter={chapter.num}
          />
        )}
      </div>
    );
  }

  return (
    <div>
      <p className="crumbs">{chapter.section}</p>
      <h2>
        Урок {chapter.num}. {chapter.title}
      </h2>
      {/* Текст урока в интерфейсе не показываем — только слайды и аудио;
          эта ветка для глав без слайдов даёт просто список частей. */}
      <ul className="list">
        {chapter.lessons.map((lesson, i) => {
          const isActive = playingId === lesson.id;
          const p = isActive ? progress : null;
          return (
            <li
              key={lesson.id}
              className={
                isActive ? (paused ? "now-playing paused" : "now-playing") : ""
              }
            >
              <button
                className="play"
                onClick={() =>
                  isActive
                    ? togglePause()
                    : playSequence(asItems(chapter.lessons.slice(i)))
                }
                title={isActive && !paused ? "Пауза" : "Плей"}
              >
                {isActive && !paused ? "▮▮" : "▶"}
              </button>
              <div className="body">
                <p className="text">
                  Часть {lesson.ord + 1}
                  {p && p.d > 0 ? ` · ${fmtTime(p.t)} / ${fmtTime(p.d)}` : ""}
                </p>
              </div>
              {p && (
                <div
                  className="track"
                  onClick={(e) => {
                    const r = e.currentTarget.getBoundingClientRect();
                    seek((e.clientX - r.left) / r.width);
                  }}
                >
                  <div
                    className="track-fill"
                    style={{ width: `${p.d > 0 ? (p.t / p.d) * 100 : 0}%` }}
                  />
                </div>
              )}
            </li>
          );
        })}
      </ul>
      {quiz && <Quiz quiz={quiz} />}
      {practice && <Exercises quiz={practice} />}
      {codeTasks.length > 0 && (
        <CodeExercises
          key={`${bookId}:${chapter.num}`}
          tasks={codeTasks}
          bookId={bookId}
          chapter={chapter.num}
        />
      )}
    </div>
  );
}

// Разбивает текст урока на элементы: предложения (type "s") и границы абзацев (type "br").
// Предложение, начинающееся со строчной, — продолжение предыдущего (сокращения «т. д.» и т. п.).
function splitSentences(text) {
  const items = [];
  const paras = text.split("\n\n");
  paras.forEach((para, pi) => {
    const pieces = para.match(/[^.!?…]+[.!?…]+["»)]*\s*|[^.!?…]+$/g) || [];
    const sents = [];
    for (const piece of pieces) {
      const prev = sents[sents.length - 1];
      if (prev && /^\s*[а-яё]/.test(piece)) {
        sents[sents.length - 1] = prev + piece;
      } else {
        sents.push(piece);
      }
    }
    sents.forEach((s) => items.push({ type: "s", text: s }));
    if (pi < paras.length - 1) items.push({ type: "br" });
  });
  return items;
}

// Доля длительности, где начинается абзац paraIdx — та же оценка, что в караоке:
// время пропорционально суммарной длине предложений.
function paraStartFraction(text, paraIdx) {
  const items = splitSentences(text);
  const total =
    items
      .filter((it) => it.type === "s")
      .reduce((a, it) => a + it.text.length, 0) || 1;
  let para = 0;
  let off = 0;
  for (const it of items) {
    if (it.type === "br") {
      para += 1;
      continue;
    }
    if (para === paraIdx) break;
    off += it.text.length;
  }
  return Math.min(1, (off + 0.5) / total);
}

function SlidePanel({
  slides,
  titles,
  idx,
  onPick,
  t,
  d,
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
          <Comp />
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
                <Comp />
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
