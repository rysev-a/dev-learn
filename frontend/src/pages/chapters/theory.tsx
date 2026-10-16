import { useEffect, useMemo, useRef } from "react";
import { createPortal } from "react-dom";
import { useSearchParams } from "react-router-dom";
import { useChapterContext } from "./context.ts";
import type { PlayerItem } from "../../lib/player.tsx";
import type { Lesson } from "../../types.ts";
import type { SlideComponent } from "../../lib/slides.ts";
import { FsItem } from "../../components/FsTree.tsx";
import { useChapterSlides } from "../../lib/slides.ts";
import { usePlayer } from "../../lib/player.tsx";
import { SlideAudioContext } from "../../lib/slideAudio.ts";
import { fmtTime } from "../../lib/format.ts";
import { estimateSeconds } from "../../lib/voice.ts";
import { useProgress } from "../../lib/progress.tsx";

export default function ChapterTheory() {
  const { chapter, bookId, fs, itemsSlot, headSlot } = useChapterContext();
  const { markSlide } = useProgress();
  const { playingId, paused, progress, togglePause, playSequence } = usePlayer();
  const [searchParams, setSearchParams] = useSearchParams();
  // Ручной выбор слайда живёт в URL (?slide=N) — перезагрузка возвращает на тот же слайд.
  const slideParam = searchParams.get("slide");
  const manualIdx =
    slideParam == null ? null : Math.max(0, parseInt(slideParam, 10) || 0);
  // остальные параметры адреса (например, fs) сохраняются
  const patchParams = (fn: (p: URLSearchParams) => void) =>
    setSearchParams(
      (prev) => {
        const n = new URLSearchParams(prev);
        fn(n);
        return n;
      },
      { replace: true },
    );
  const setManualIdx = (i: number | null) =>
    patchParams((n) => (i == null ? n.delete("slide") : n.set("slide", String(i))));

  const activeIdx = chapter
    ? chapter.lessons.findIndex((l) => l.id === playingId)
    : -1;

  // У каждой главы есть слайды; каждая часть — один абзац со своим слайдом и
  // своим аудио-файлом. Слайд следует за играющей частью, иначе — ручной выбор.
  const { slides, titles: slideTitles, loading } = useChapterSlides(
    chapter && bookId != null ? `${bookId}:${chapter.num}` : null,
  );

  let slideIdx = 0;
  if (slides) {
    if (activeIdx >= 0) slideIdx = chapter.lessons[activeIdx].ord;
    else if (manualIdx != null) slideIdx = manualIdx;
    slideIdx = Math.min(slideIdx, slides.length - 1);
  }

  // просмотренный слайд идёт в прогресс (дашборд на главной)
  useEffect(() => {
    if (slides) markSlide(bookId, chapter.num, slideIdx);
  }, [slides, bookId, chapter.num, slideIdx, markSlide]);

  if (loading) return <p className="empty">Загрузка…</p>;
  if (!slides) return <p className="error">У этой главы нет слайдов</p>;

  function asItems(lessons: Lesson[]): PlayerItem[] {
    return lessons.map((l) => ({
      id: l.id,
      // файл озвучки есть только когда бэкенд знает его длительность
      url: l.dur > 0 ? l.audio : null,
      text: l.text,
      est: estimateSeconds(l.text),
      title: `Часть ${l.ord + 1}`,
      subtitle: `Урок ${chapter.num}. ${chapter.title}`,
      badge: String(chapter.num),
    }));
  }

  // Клик по слайду: если глава играет — начинаем с этой части, иначе просто
  // показываем слайд.
  function pickSlide(i: number) {
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
  const durOf = (l: Lesson) => (l.dur > 0 ? Number(l.dur) : estimateSeconds(l.text));
  const chapterDur = chapter.lessons.reduce((a, l) => a + durOf(l), 0);
  const offsetBefore = chapter.lessons.reduce(
    (a, l) => a + (l.ord < slideIdx ? durOf(l) : 0),
    0,
  );
  const playingThisSlide =
    activeIdx >= 0 && chapter.lessons[activeIdx].ord === slideIdx;
  const chapterPos =
    offsetBefore + (playingThisSlide && progress ? progress.t : 0);

  const slideLesson = chapter.lessons.find((l) => l.ord === slideIdx);
  const spokenT = playingThisSlide
    ? progress?.id === playingId
      ? progress.t
      : 0
    : null;
  const spokenD = slideLesson
    ? slideLesson.dur > 0
      ? Number(slideLesson.dur)
      : estimateSeconds(slideLesson.text)
    : 0;

  return (
    <div>
      {slideLesson && (
        <VoiceText text={slideLesson.text} t={spokenT} d={spokenD} key={slideLesson.id} />
      )}
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
        itemsSlot={itemsSlot}
        headSlot={headSlot}
        playing={chapterPlaying && !paused}
        onPlay={panelPlay}
        onPause={panelPause}
      />
    </div>
  );
}

// Всплывающее окно снизу: текст абзаца, который звучит за кадром. Слова,
// которые уже «прочитаны», светлее, текущее подсвечено; без воспроизведения —
// просто текст.
function VoiceText({ text, t, d }: { text: string; t: number | null; d: number }) {
  const words = useMemo(() => text.split(/\s+/).filter(Boolean), [text]);
  const boxRef = useRef<HTMLParagraphElement>(null);
  const curRef = useRef<HTMLSpanElement>(null);
  const cur =
    t == null || !d ? -1 : Math.min(words.length - 1, Math.floor((t / d) * words.length));

  useEffect(() => {
    const box = boxRef.current;
    const el = curRef.current;
    if (!box || !el) return;
    const top = el.offsetTop - box.offsetTop;
    if (top < box.scrollTop || top + el.offsetHeight > box.scrollTop + box.clientHeight)
      box.scrollTop = Math.max(0, top - box.clientHeight / 3);
  }, [cur]);

  return (
    <div className="voice-pop" role="region" aria-label="Текст озвучки">
      <div className="voice-pop-tag">За кадром</div>
      <p className="voice-pop-text" ref={boxRef}>
        {words.map((w, i) => (
          <span
            key={i}
            ref={i === cur ? curRef : null}
            className={cur < 0 ? "" : i < cur ? "past" : i === cur ? "now" : "next"}
          >
            {w}{" "}
          </span>
        ))}
      </p>
    </div>
  );
}

interface SlidePanelProps {
  slides: SlideComponent[];
  titles: string[] | null;
  idx: number;
  onPick: (i: number) => void;
  t: number;
  d: number;
  audioT: number | null;
  caption: string;
  fs: boolean;
  itemsSlot: HTMLElement | null;
  headSlot: HTMLElement | null;
  playing: boolean;
  onPlay: () => void;
  onPause: () => void;
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
  itemsSlot,
  headSlot,
  playing,
  onPlay,
  onPause,
}: SlidePanelProps) {
  const Comp = slides[Math.min(idx, slides.length - 1)];
  const count = String(slides.length).padStart(2, "0");

  // стрелки листают слайды в полноэкранном режиме
  useEffect(() => {
    if (!fs) return;
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      const tag = target?.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || target?.isContentEditable) return;
      if (e.key === "ArrowRight" || e.key === "ArrowDown")
        onPick(Math.min(idx + 1, slides.length - 1));
      else if (e.key === "ArrowLeft" || e.key === "ArrowUp")
        onPick(Math.max(idx - 1, 0));
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [fs, idx, slides.length, onPick]);

  const dots = (cls: string) => (
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

  const controls = (
    <>
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
    </>
  );

  const stage = (cls: string) => (
    <div className={cls} key={idx}>
      <SlideAudioContext.Provider value={audioT}>
        <Comp />
      </SlideAudioContext.Provider>
    </div>
  );

  // Полноэкранный режим: оболочка (дерево, вкладки, «Свернуть») живёт в макете
  // главы; вкладка кладёт свои кнопки в шапку и слайды в дерево через порталы.
  if (fs)
    return (
      <>
        {headSlot && createPortal(controls, headSlot)}
        {itemsSlot &&
          createPortal(
            slides.map((_, i) => (
              <FsItem key={i} on={i === idx} num={i + 1} onClick={() => onPick(i)}>
                {titles ? titles[i] : `Слайд ${i + 1}`}
              </FsItem>
            )),
            itemsSlot,
          )}
        {stage("slide-fs-stage")}
      </>
    );

  return (
    <aside className="slide-panel">
      <div className="slide-panel-head">{controls}</div>
      {stage("slide-stage")}
      {dots("slide-dots")}
    </aside>
  );
}

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
