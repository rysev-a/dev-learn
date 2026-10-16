/* Движок лаборатории хранит решения схем в localStorage (ключи — по пользователю), а настоящий прогресс
   живёт в кабинете. При входе в лабораторию решённое с сервера переписывается в localStorage:
   блоки собираются из решений других глав, а палитра открывает составные элементы. */
import { api } from "../lib/api.ts";
import { ARCH_BOOK, LAB_CHAPTERS, sectionOf } from "./registry.ts";
import { setLabNamespace } from "./exercises/logic-gates/lab/exercise-progress.ts";
import {
  loadProgress,
  saveProgress,
} from "./exercises/logic-gates/lab/exercise-progress.ts";
import { localSolutionStore } from "./exercises/logic-gates/blocks.ts";

let cache: { user: number | null; promise: Promise<void> | null } = { user: null, promise: null };

interface ServerState {
  status?: Record<string, string>;
  drafts?: Record<string, string>;
}

export function hydrateLab(userId: number | null): Promise<void> {
  setLabNamespace(`u${userId}:`);
  if (cache.user === userId && cache.promise) return cache.promise;
  const circuitChapters = Object.entries(LAB_CHAPTERS).flatMap(([n, v]) => (v.kind === "circuit" ? [[n, v] as const] : []));
  const promise = Promise.all(
    circuitChapters.map(async ([num, lab]) => {
      let state: ServerState;
      try {
        state = await api<ServerState>(`/api/exercises/${ARCH_BOOK}/${num}/state`);
      } catch {
        return;
      }
      const section = sectionOf(lab.slug);
      if (!section) return;
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
export function forgetLab(userId: number) {
  cache = { user: null, promise: null };
  try {
    const prefix = `u${userId}:processor-`;
    for (const key of Object.keys(localStorage))
      if (key.startsWith(prefix)) localStorage.removeItem(key);
  } catch {
    /* localStorage недоступен */
  }
}
