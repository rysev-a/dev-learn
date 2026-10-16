// Реестр слайдов: «книга:глава» → компоненты сцен и их названия.
// Файлы глав лежат в slides/<папка книги>/chNN.jsx и находятся автоматически;
// подгружаются лениво, при открытии главы, поэтому в основной бандл не входят.
// Новая книга — строка в BOOK_DIRS. Файл главы экспортирует SLIDES_* и SLIDE_TITLES_*
// (объекты с ключом «книга:глава»).
import { useEffect, useState, type ComponentType } from "react";

const BOOK_DIRS: Record<string, number> = {
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

export type SlideComponent = ComponentType;

export interface ChapterSlides {
  slides: SlideComponent[] | null;
  titles: string[] | null;
}

type ChapterModule = Record<string, unknown>;

const loaders: Record<string, () => Promise<ChapterModule>> = {};
for (const [path, load] of Object.entries(
  import.meta.glob<ChapterModule>("../slides/*/ch*.{jsx,tsx}"),
)) {
  const m = path.match(/slides\/([^/]+)\/ch(\d+)\.[jt]sx$/);
  const book = m ? BOOK_DIRS[m[1]!] : undefined;
  if (m && book != null) loaders[`${book}:${Number(m[2])}`] = load;
}

const cache = new Map<string, Promise<ChapterSlides>>();

export const hasSlides = (key: string): boolean => key in loaders;

// Первый экспорт модуля, имя которого начинается с prefix: { "книга:глава": значение }
function pick<T>(mod: ChapterModule, prefix: string, key: string): T | null {
  const name = Object.keys(mod).find((n) => n.startsWith(prefix));
  const table = name ? (mod[name] as Record<string, T>) : null;
  return table?.[key] ?? null;
}

export function loadSlides(key: string): Promise<ChapterSlides | null> {
  const load = loaders[key];
  if (!load) return Promise.resolve(null);
  let hit = cache.get(key);
  if (!hit) {
    hit = load().then((mod) => ({
      slides: pick<SlideComponent[]>(mod, "SLIDES_", key),
      titles: pick<string[]>(mod, "SLIDE_TITLES_", key),
    }));
    cache.set(key, hit);
  }
  return hit;
}

// Слайды главы: loading — пока модуль грузится, slides === null — слайдов у главы нет
export function useChapterSlides(key: string | null): ChapterSlides & { loading: boolean } {
  const [state, setState] = useState<{ key: string | null; data: ChapterSlides | null }>({
    key: null,
    data: null,
  });
  useEffect(() => {
    let live = true;
    if (key) loadSlides(key).then((data) => live && setState({ key, data }));
    return () => {
      live = false;
    };
  }, [key]);
  const ready = !key || !hasSlides(key) || state.key === key;
  const data = ready && state.key === key ? state.data : null;
  return { loading: !ready, slides: data?.slides ?? null, titles: data?.titles ?? null };
}
