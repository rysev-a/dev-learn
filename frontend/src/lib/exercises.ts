// Реестр упражнений: ключ «bookId:номер_главы» → задачи с вводом ответа.
// Проверка — в браузере сравнением с эталонами (числа/короткие строки).
import { DM_EXERCISES } from "../exercises/dm.ts";
import type { PracticeSet } from "../types.ts";

export const EXERCISES: Record<string, PracticeSet> = {
  ...DM_EXERCISES,
};
