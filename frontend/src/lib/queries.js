// Чтение курса с сервера: запросы кешируются на время сессии (содержимое курса не меняется,
// пока открыта страница), поэтому меню, дашборд и главы не запрашивают одно и то же по нескольку раз.
import { useEffect, useState } from "react";
import { api } from "./api.js";

const cache = new Map();

function getJson(path) {
  if (!cache.has(path))
    cache.set(
      path,
      api(path).catch((e) => {
        cache.delete(path);
        throw e;
      }),
    );
  return cache.get(path);
}

// { data, error, loading }; пока запрос не завершён или path === null, data = fallback
export function useApi(path, fallback = null) {
  const [state, setState] = useState({ path: null, data: null, error: null });
  useEffect(() => {
    if (!path) return undefined;
    let live = true;
    getJson(path)
      .then((data) => live && setState({ path, data, error: null }))
      .catch((error) => live && setState({ path, data: null, error }));
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

const NO_BOOKS = [];
const NO_SECTIONS = [];

// книги: [{id, title, ...}]
export const useBooks = () => useApi("/api/books", NO_BOOKS).data;

// разделы с главами книги: [{id, title, chapters: [{id, num, title, parts_count}]}]
export const useCourse = (bookId) =>
  useApi(bookId == null ? null : `/api/books/${bookId}/course`, NO_SECTIONS).data;

// число код-упражнений: {книга: {глава: число}}; null, пока не загружено ({} при ошибке)
export function useCodeCounts() {
  const { data, error, loading } = useApi("/api/exercises");
  return loading ? null : error ? {} : data;
}

// курсы всех книг сразу: {bookId: разделы}; книга без ответа пока отсутствует
export function useCourses(books) {
  const [courses, setCourses] = useState({});
  useEffect(() => {
    let live = true;
    books.forEach((b) =>
      getJson(`/api/books/${b.id}/course`)
        .then((d) => live && setCourses((p) => ({ ...p, [b.id]: d })))
        .catch(() => {}),
    );
    return () => {
      live = false;
    };
  }, [books]);
  return courses;
}
