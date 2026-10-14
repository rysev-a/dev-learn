// Реестр упражнений: ключ «bookId:номер_главы» → задачи с вводом ответа.
// Проверка — в браузере сравнением с эталонами (числа/короткие строки).
import { DM_EXERCISES } from "../exercises/dm.js";

export const EXERCISES = {
  ...DM_EXERCISES,
};
