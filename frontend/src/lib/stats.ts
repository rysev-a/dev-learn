// Прогресс одной главы: слайды, вопросы, упражнения.
import type { ChapterSummary } from "../types.ts";
import { EXERCISES } from "./exercises.ts";
import type { ProgressValue } from "./progress.tsx";
import type { CodeCounts } from "./queries.ts";
import { QUIZZES } from "./quizzes.ts";

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
  codeCounts: CodeCounts | null,
): ChapterStats {
  const key = `${bookId}:${ch.num}`;
  const slidesTotal = ch.parts_count || 0; // один абзац = один слайд
  const quiz = QUIZZES[key];
  const quizTotal = quiz ? quiz.questions.length : 0;
  const picks = quizTotal ? progress.quizPicks(bookId, ch.num) : null;
  const quizDone = picks ? picks.filter((p) => p != null).length : 0;
  const quizRight = picks
    ? picks.filter((p, i) => p != null && p === quiz.questions[i].answer).length
    : 0;
  const code = codeCounts?.[bookId]?.[ch.num] || 0;
  const dm = EXERCISES[key] ? EXERCISES[key].tasks.length : 0;
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
