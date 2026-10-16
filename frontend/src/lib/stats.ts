// Прогресс одной главы: слайды, вопросы, упражнения.
import type { ChapterSummary } from "../types.ts";
import type { ProgressValue } from "./progress.tsx";
import type { Counts } from "./queries.ts";

/** [сделано, всего] */
export type Pair = [number, number];

export interface ChapterStats {
  slides: Pair;
  quiz: Pair;
  quizRight: number;
  ex: Pair;
}

export function chapterStats(
  progress: ProgressValue,
  bookId: string | number,
  ch: ChapterSummary,
  counts: Counts,
): ChapterStats {
  const slidesTotal = ch.parts_count || 0; // один абзац = один слайд
  const quizTotal = counts.quiz?.[bookId]?.[ch.num] || 0;
  const picks = quizTotal ? progress.quizPicks(bookId, ch.num) : null;
  const quizDone = picks ? picks.filter((p) => p != null).length : 0;
  const quizRight = quizTotal ? progress.quizRight(bookId, ch.num) : 0;
  const code = counts.code?.[bookId]?.[ch.num] || 0;
  const dm = counts.answers?.[bookId]?.[ch.num] || 0;
  const exTotal = code || dm;
  const exDone = code
    ? Object.values(progress.codeStatus(bookId, ch.num)).filter((v) => v === "ok").length
    : dm
      ? Object.keys(progress.answerSolved(bookId, ch.num)).length
      : 0;
  return {
    slides: [Math.min(progress.slidesSeen(bookId, ch.num).length, slidesTotal), slidesTotal],
    quiz: [quizDone, quizTotal],
    quizRight,
    ex: [exDone, exTotal],
  };
}
