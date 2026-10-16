// Исходники упражнений с вводом ответа: ключ «bookId:номер_главы» → набор задач. В приложение они не попадают:
// `npm run answers:export` превращает их в SQL-файлы backend/app/data/sql/answers, а проверяет ответ сервер.
import { DM_EXERCISES } from "./dm.ts";
import type { PracticeSet } from "./types.ts";

export const EXERCISES: Record<string, PracticeSet> = {
  ...DM_EXERCISES,
};
