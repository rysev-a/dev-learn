import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import type { ProgressData, TaskStatus } from "../types.ts";
import { api } from "./api.ts";
import { useAuth } from "./auth.tsx";

/* Прогресс пользователя живёт на сервере (кабинет). Клиент один раз забирает всё
   (`GET /api/progress`), держит копию в состоянии и точечно пишет изменения.
   Ключ главы везде «книга:номер_главы». */

type BookId = number | string;
export type ResetScope = "practice" | "all";

interface ProgressActions {
  markSlide: (book: BookId, num: number, slide: number) => void;
  /** ответ на вопрос квиза принят сервером: обновить копию выбранных вариантов и число верных */
  recordQuizPick: (book: BookId, num: number, question: number, total: number, pick: number, right: number) => void;
  resetQuiz: (book: BookId, num: number) => void;
  saveAnswers: (book: BookId, num: number, solved: Record<string, string>) => void;
  setCodeStatus: (book: BookId, num: number, task: string, status: TaskStatus) => void;
  reset: (scope: ResetScope) => Promise<void>;
}

export interface ProgressValue extends ProgressActions {
  ready: boolean;
  slidesSeen: (book: BookId, num: number) => number[];
  quizPicks: (book: BookId, num: number) => (number | null)[] | null;
  quizRight: (book: BookId, num: number) => number;
  answerSolved: (book: BookId, num: number) => Record<string, string>;
  codeStatus: (book: BookId, num: number) => Record<string, TaskStatus>;
}

const ProgressContext = createContext<ProgressValue | null>(null);

export const useProgress = (): ProgressValue => {
  const ctx = useContext(ProgressContext);
  if (!ctx) throw new Error("useProgress must be used within ProgressProvider");
  return ctx;
};

const EMPTY: ProgressData = { slides: {}, quiz: {}, quizRight: {}, answers: {}, code: {} };
const k = (book: BookId, num: number) => `${book}:${num}`;
const fire = (path: string, method: "POST" | "PUT", body: unknown) =>
  api(path, { method, body }).catch(() => {});

export function ProgressProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const [data, setData] = useState<ProgressData>(EMPTY);
  const [ready, setReady] = useState(false);

  const load = useCallback(() => {
    return api<Partial<ProgressData>>("/api/progress")
      .then((d) => setData({ ...EMPTY, ...d }))
      .catch(() => {})
      .finally(() => setReady(true));
  }, []);

  // при входе — загрузить прогресс, при выходе или смене пользователя — очистить
  useEffect(() => {
    setData(EMPTY);
    setReady(false);
    if (user) load();
  }, [user?.id, load]); // eslint-disable-line react-hooks/exhaustive-deps

  // мутаторы стабильны (их можно класть в зависимости эффектов): текущие данные
  // читают из ref, а запись на сервер идёт вне обновления состояния
  const ref = useRef(data);
  ref.current = data;

  const actions = useMemo<ProgressActions>(
    () => ({
      markSlide: (book, num, slide) => {
        const key = k(book, num);
        if ((ref.current.slides[key] || []).includes(slide)) return;
        fire("/api/progress/slides", "POST", { book, chapter: num, slide });
        setData((d) => ({
          ...d,
          slides: { ...d.slides, [key]: [...(d.slides[key] || []), slide] },
        }));
      },
      recordQuizPick: (book, num, question, total, pick, right) => {
        const key = k(book, num);
        setData((d) => {
          const picks: (number | null)[] = Array.from({ length: total }, (_, i) => d.quiz[key]?.[i] ?? null);
          picks[question] = pick;
          return { ...d, quiz: { ...d.quiz, [key]: picks }, quizRight: { ...d.quizRight, [key]: right } };
        });
      },
      resetQuiz: (book, num) => {
        const key = k(book, num);
        setData((d) => {
          const { [key]: _picks, ...quiz } = d.quiz;
          const { [key]: _right, ...quizRight } = d.quizRight;
          return { ...d, quiz, quizRight };
        });
        api(`/api/progress/quiz?book=${book}&chapter=${num}`, { method: "DELETE" }).catch(() => {});
      },
      saveAnswers: (book, num, solved) => {
        const key = k(book, num);
        setData((d) => {
          const answers = { ...d.answers };
          if (Object.keys(solved).length) answers[key] = solved;
          else delete answers[key];
          return { ...d, answers };
        });
        fire("/api/progress/answers", "PUT", { book, chapter: num, solved });
      },
      // статус код-задачи после проверки на сервере (решённое остаётся решённым)
      setCodeStatus: (book, num, task, status) => {
        const key = k(book, num);
        setData((d) => {
          const cur = d.code[key] || {};
          if (cur[task] === "ok") return d;
          return { ...d, code: { ...d.code, [key]: { ...cur, [task]: status } } };
        });
      },
      reset: async (scope) => {
        await api(`/api/progress?scope=${scope}`, { method: "DELETE" });
        await load();
      },
    }),
    [load],
  );

  const value: ProgressValue = {
    ready,
    ...actions,
    slidesSeen: (book, num) => data.slides[k(book, num)] || [],
    quizPicks: (book, num) => data.quiz[k(book, num)] || null,
    quizRight: (book, num) => data.quizRight[k(book, num)] ?? 0,
    answerSolved: (book, num) => data.answers[k(book, num)] || {},
    codeStatus: (book, num) => data.code[k(book, num)] || {},
  };

  return (
    <ProgressContext.Provider value={value}>
      {children}
    </ProgressContext.Provider>
  );
}
