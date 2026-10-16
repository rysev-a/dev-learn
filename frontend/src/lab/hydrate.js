/* Движок лаборатории хранит решения схем в localStorage (ключи — по пользователю), а настоящий прогресс
   живёт в кабинете. При входе в лабораторию решённое с сервера переписывается в localStorage:
   блоки собираются из решений других глав, а палитра открывает составные элементы. */
import { api } from "../lib/api.ts";
import { ARCH_BOOK, LAB_CHAPTERS, sectionOf } from "./registry.js";
import { setLabNamespace } from "./exercises/logic-gates/lab/exercise-progress";
import {
  loadProgress,
  saveProgress,
} from "./exercises/logic-gates/lab/exercise-progress";
import { localSolutionStore } from "./exercises/logic-gates/blocks";

let cache = { user: null, promise: null };

export function hydrateLab(userId) {
  setLabNamespace(`u${userId}:`);
  if (cache.user === userId && cache.promise) return cache.promise;
  const circuitChapters = Object.entries(LAB_CHAPTERS).filter(
    ([, v]) => v.kind === "circuit",
  );
  const promise = Promise.all(
    circuitChapters.map(async ([num, lab]) => {
      let state;
      try {
        state = await api(`/api/exercises/${ARCH_BOOK}/${num}/state`);
      } catch {
        return;
      }
      const section = sectionOf(lab.slug);
      const solved = new Set(loadProgress(section).solved);
      section.exercises.forEach((ex, i) => {
        if (state.status?.[ex.id] !== "ok") return;
        solved.add(i);
        const draft = state.drafts?.[ex.id];
        if (!draft) return;
        try {
          localSolutionStore.save(
            section.progressKey,
            ex.id,
            JSON.parse(draft),
          );
        } catch {
          /* не схема — пропускаем */
        }
      });
      saveProgress(section, solved, loadProgress(section).current);
    }),
  ).then(() => undefined);
  cache = { user: userId, promise };
  return promise;
}

/** После «сбросить прогресс»: стереть локальный слепок решений и перечитать сервер при следующем входе */
export function forgetLab(userId) {
  cache = { user: null, promise: null };
  try {
    const prefix = `u${userId}:processor-`;
    for (const key of Object.keys(localStorage))
      if (key.startsWith(prefix)) localStorage.removeItem(key);
  } catch {
    /* localStorage недоступен */
  }
}
