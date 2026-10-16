// Реестр слайдов: глава → компоненты сцен и их названия.
// Файлы глав лежат в slides/<каталог книги>/chNN.tsx и находятся автоматически; каталог книги задаёт сервер
// (поле slides_dir в backend/app/data/sql/books.sql, приходит в /api/books). Главы подгружаются лениво, при
// открытии, поэтому в основной бандл не входят. Файл главы экспортирует SLIDES_* и SLIDE_TITLES_*
// (объекты с ключом «книга:глава»).
import { useEffect, useState, type ComponentType } from "react";

export type SlideComponent = ComponentType;

/** Где искать главу: каталог слайдов книги, id книги и номер главы */
export interface SlideRef {
  dir: string;
  book: number | string;
  num: number;
}

export interface ChapterSlides {
  slides: SlideComponent[] | null;
  titles: string[] | null;
}

type ChapterModule = Record<string, unknown>;

// «каталог:номер главы» → загрузчик модуля
const loaders: Record<string, () => Promise<ChapterModule>> = {};
for (const [path, load] of Object.entries(import.meta.glob<ChapterModule>("../slides/*/ch*.tsx"))) {
  const m = path.match(/slides\/([^/]+)\/ch(\d+)\.tsx$/);
  if (m) loaders[`${m[1]}:${Number(m[2])}`] = load;
}

const cache = new Map<string, Promise<ChapterSlides>>();

const loaderKey = (ref: SlideRef) => `${ref.dir}:${ref.num}`;

export const hasSlides = (ref: SlideRef | null): boolean => ref != null && loaderKey(ref) in loaders;

// Первый экспорт модуля, имя которого начинается с prefix: { "книга:глава": значение }
function pick<T>(mod: ChapterModule, prefix: string, key: string): T | null {
  const name = Object.keys(mod).find((n) => n.startsWith(prefix));
  const table = name ? (mod[name] as Record<string, T>) : null;
  return table?.[key] ?? null;
}

export function loadSlides(ref: SlideRef): Promise<ChapterSlides | null> {
  const load = loaders[loaderKey(ref)];
  if (!load) return Promise.resolve(null);
  const key = `${ref.book}:${ref.num}`;
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
export function useChapterSlides(ref: SlideRef | null): ChapterSlides & { loading: boolean } {
  const key = ref ? loaderKey(ref) : null;
  const [state, setState] = useState<{ key: string | null; data: ChapterSlides | null }>({
    key: null,
    data: null,
  });
  useEffect(() => {
    let live = true;
    if (ref && key) loadSlides(ref).then((data) => live && setState({ key, data }));
    return () => {
      live = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key]);
  const ready = !ref || !hasSlides(ref) || state.key === key;
  const data = ready && state.key === key ? state.data : null;
  return { loading: !ready, slides: data?.slides ?? null, titles: data?.titles ?? null };
}
