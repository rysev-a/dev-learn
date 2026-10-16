// Данные главы, которые страница главы отдаёт вкладкам («Теория», «Вопросы», «Практика») через контекст маршрута.
import { useOutletContext } from "react-router-dom";
import type { Chapter, ChapterSummary, PracticeSet, Section, Task } from "../../types.ts";

export interface ChapterContext {
  bookId: string;
  chapterId: string;
  course: Section[];
  chapter: Chapter;
  /** число вопросов квиза главы (сами вопросы Quiz загружает с сервера) */
  quizCount: number;
  practice: PracticeSet | null;
  codeTasks: Task[];
  tasksReady: boolean;
  nextPractice: ChapterSummary | null;
  fs: boolean;
  itemsSlot: HTMLElement | null;
  headSlot: HTMLElement | null;
}

export const useChapterContext = (): ChapterContext => useOutletContext<ChapterContext>();
