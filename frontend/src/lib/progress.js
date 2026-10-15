// Прогресс обучения в этом браузере (localStorage): просмотренные слайды,
// ответы на вопросы, решённые упражнения. Читает дашборд на главной.
import { readSetting, writeSetting } from "./settings.js";

const json = (k, fallback) => {
  try {
    const v = readSetting(k);
    return v == null ? fallback : JSON.parse(v);
  } catch {
    return fallback;
  }
};

// слайды: список просмотренных индексов главы
export const slidesSeen = (book, num) => json(`say-sv-${book}:${num}`, []);

export function markSlide(book, num, idx) {
  const seen = slidesSeen(book, num);
  if (seen.includes(idx)) return;
  writeSetting(`say-sv-${book}:${num}`, JSON.stringify([...seen, idx]));
}

// вопросы: выбранные варианты по порядку (null — без ответа)
export const quizPicks = (book, num) => json(`say-qz-${book}:${num}`, null);

export function saveQuizPicks(book, num, picks) {
  writeSetting(`say-qz-${book}:${num}`, picks ? JSON.stringify(picks) : null);
}

// упражнения с кодом: решённые задачи главы
export function codeSolved(book, num) {
  const prefix = `say-cex-${book}:${num}:`;
  let n = 0;
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k.startsWith(prefix) && localStorage.getItem(k) === "1") n++;
    }
  } catch {
    /* хранилище недоступно */
  }
  return n;
}

// упражнения с вводом ответа: {индекс: ответ} для решённых
export const answerSolved = (book, num) => json(`say-dex-${book}:${num}`, {});

export function saveAnswerSolved(book, num, map) {
  writeSetting(`say-dex-${book}:${num}`, Object.keys(map).length ? JSON.stringify(map) : null);
}
