// Реестр слайдов: «книга:глава» → компоненты сцен и их названия.
// Файлы глав лежат в slides/<папка книги>/chNN.jsx и находятся автоматически;
// подгружаются лениво, при открытии главы, поэтому в основной бандл не входят.
// Новая книга — строка в BOOK_DIRS. Файл главы экспортирует SLIDES_* и SLIDE_TITLES_*
// (объекты с ключом «книга:глава»).
import { useEffect, useState } from "react";

const BOOK_DIRS = {
  algo: 7,
  linux: 8,
  db: 9,
  "learn-rust": 10,
  js: 11,
  dm: 12,
  py: 13,
  arch: 14,
  networks: 15,
  "learn-c": 16,
  virtualization: 17,
};

const loaders = {};
for (const [path, load] of Object.entries(import.meta.glob("../slides/*/ch*.jsx"))) {
  const m = path.match(/slides\/([^/]+)\/ch(\d+)\.jsx$/);
  const book = m && BOOK_DIRS[m[1]];
  if (book != null) loaders[`${book}:${Number(m[2])}`] = load;
}

const cache = new Map();

export const hasSlides = (key) => key in loaders;

// Первый экспорт модуля, имя которого начинается с prefix: { "книга:глава": значение }
const pick = (mod, prefix, key) => {
  const name = Object.keys(mod).find((n) => n.startsWith(prefix));
  return name ? mod[name][key] || null : null;
};

export function loadSlides(key) {
  if (!loaders[key]) return Promise.resolve(null);
  if (!cache.has(key))
    cache.set(
      key,
      loaders[key]().then((mod) => ({
        slides: pick(mod, "SLIDES_", key),
        titles: pick(mod, "SLIDE_TITLES_", key),
      })),
    );
  return cache.get(key);
}

// Слайды главы: loading — пока модуль грузится, slides === null — слайдов у главы нет
export function useChapterSlides(key) {
  const [state, setState] = useState({ key: null, data: null });
  useEffect(() => {
    let live = true;
    if (key) loadSlides(key).then((data) => live && setState({ key, data }));
    return () => {
      live = false;
    };
  }, [key]);
  const ready = !key || !hasSlides(key) || state.key === key;
  return {
    loading: !ready,
    slides: ready && state.key === key ? state.data?.slides ?? null : null,
    titles: ready && state.key === key ? state.data?.titles ?? null : null,
  };
}
