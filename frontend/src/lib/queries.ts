// Чтение курса с сервера: запросы кешируются на время сессии (содержимое курса не меняется,
// пока открыта страница), поэтому меню, дашборд и главы не запрашивают одно и то же по нескольку раз.
import { useEffect, useMemo, useState } from "react";
import type { Book, Section } from "../types.ts";
import { api } from "./api.ts";

const cache = new Map<string, Promise<unknown>>();

function getJson<T>(path: string): Promise<T> {
  let hit = cache.get(path);
  if (!hit) {
    hit = api<T>(path).catch((e: unknown) => {
      cache.delete(path);
      throw e;
    });
    cache.set(path, hit);
  }
  return hit as Promise<T>;
}

interface QueryState<T> {
  path: string | null;
  data: T | null;
  error: Error | null;
}

export interface Query<T, F> {
  data: T | F;
  error: Error | null;
  loading: boolean;
}

// { data, error, loading }; пока запрос не завершён или path === null, data = fallback
export function useApi<T, F = null>(path: string | null, fallback: F = null as F): Query<T, F> {
  const [state, setState] = useState<QueryState<T>>({ path: null, data: null, error: null });
  useEffect(() => {
    if (!path) return undefined;
    let live = true;
    getJson<T>(path)
      .then((data) => live && setState({ path, data, error: null }))
      .catch((error: Error) => live && setState({ path, data: null, error }));
    return () => {
      live = false;
    };
  }, [path]);
  const ready = path != null && state.path === path;
  return {
    data: ready && state.data != null ? state.data : fallback,
    error: ready ? state.error : null,
    loading: path != null && !ready,
  };
}

const NO_BOOKS: Book[] = [];
const NO_SECTIONS: Section[] = [];

export const useBooks = (): Book[] => useApi<Book[], Book[]>("/api/books", NO_BOOKS).data;

// разделы с главами книги
export const useCourse = (bookId: string | number | undefined): Section[] =>
  useApi<Section[], Section[]>(
    bookId == null ? null : `/api/books/${bookId}/course`,
    NO_SECTIONS,
  ).data;

// число код-упражнений: {книга: {глава: число}}
export type CodeCounts = Record<string, Record<string, number>>;

// null, пока не загружено ({} при ошибке)
export function useCodeCounts(): CodeCounts | null {
  const { data, error, loading } = useApi<CodeCounts>("/api/exercises");
  return loading ? null : error ? {} : data;
}

// число вопросов квиза: {книга: {глава: число}}; null, пока не загружено ({} при ошибке)
export type QuizCounts = Record<string, Record<string, number>>;

export function useQuizCounts(): QuizCounts | null {
  const { data, error, loading } = useApi<QuizCounts>("/api/quizzes");
  return loading ? null : error ? {} : data;
}

// число задач с вводом ответа: {книга: {глава: число}}; null, пока не загружено ({} при ошибке)
export type AnswerCounts = Record<string, Record<string, number>>;

export function useAnswerCounts(): AnswerCounts | null {
  const { data, error, loading } = useApi<AnswerCounts>("/api/answers");
  return loading ? null : error ? {} : data;
}

/** Составы глав: сколько в каждой код-упражнений, вопросов квиза и задач с вводом ответа (null — ещё грузится) */
export interface Counts {
  code: CodeCounts | null;
  quiz: QuizCounts | null;
  answers: AnswerCounts | null;
}

export function useCounts(): Counts {
  const code = useCodeCounts();
  const quiz = useQuizCounts();
  const answers = useAnswerCounts();
  return useMemo(() => ({ code, quiz, answers }), [code, quiz, answers]);
}

// курсы всех книг сразу: {bookId: разделы}; книга без ответа пока отсутствует
export function useCourses(books: Book[]): Record<number, Section[]> {
  const [courses, setCourses] = useState<Record<number, Section[]>>({});
  useEffect(() => {
    let live = true;
    books.forEach((b) =>
      getJson<Section[]>(`/api/books/${b.id}/course`)
        .then((d) => live && setCourses((p) => ({ ...p, [b.id]: d })))
        .catch(() => {}),
    );
    return () => {
      live = false;
    };
  }, [books]);
  return courses;
}
