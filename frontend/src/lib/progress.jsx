import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { api } from "./api.js";
import { useAuth } from "./auth.jsx";

/* Прогресс пользователя живёт на сервере (кабинет). Клиент один раз забирает всё
   (`GET /api/progress`), держит копию в состоянии и точечно пишет изменения.
   Ключ главы везде «книга:номер_главы». */

const ProgressContext = createContext(null);

export const useProgress = () => {
  const ctx = useContext(ProgressContext);
  if (!ctx) throw new Error("useProgress must be used within ProgressProvider");
  return ctx;
};

const EMPTY = { slides: {}, quiz: {}, answers: {}, code: {} };
const k = (book, num) => `${book}:${num}`;
const fire = (path, method, body) => api(path, { method, body }).catch(() => {});

export function ProgressProvider({ children }) {
  const { user } = useAuth();
  const [data, setData] = useState(EMPTY);
  const [ready, setReady] = useState(false);

  const load = useCallback(() => {
    return api("/api/progress")
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

  const actions = useMemo(
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
      saveQuizPicks: (book, num, picks) => {
        const key = k(book, num);
        const empty = !picks || picks.every((p) => p == null);
        setData((d) => {
          const quiz = { ...d.quiz };
          if (empty) delete quiz[key];
          else quiz[key] = picks;
          return { ...d, quiz };
        });
        fire("/api/progress/quiz", "PUT", { book, chapter: num, picks: picks || [] });
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

  const value = {
    ready,
    ...actions,
    slidesSeen: (book, num) => data.slides[k(book, num)] || [],
    quizPicks: (book, num) => data.quiz[k(book, num)] || null,
    answerSolved: (book, num) => data.answers[k(book, num)] || {},
    codeStatus: (book, num) => data.code[k(book, num)] || {},
  };

  return (
    <ProgressContext.Provider value={value}>
      {children}
    </ProgressContext.Provider>
  );
}
