import { useEffect, useState, type ReactNode } from "react";
import type { Section } from "../types.ts";

/* Левое дерево полноэкранного режима: разделы книги → главы. Под текущей
   главой — слот (`setItemsSlot`): активная вкладка (слайды, вопросы или
   упражнения) кладёт в него свои пункты через портал. */
interface FsTreeProps {
  sections: Section[];
  chapterId: string | undefined;
  onOpenChapter: (id: number) => void;
  setItemsSlot: (el: HTMLDivElement | null) => void;
}

export default function FsTree({ sections, chapterId, onOpenChapter, setItemsSlot }: FsTreeProps) {
  const curSec = sections.find((sec) =>
    sec.chapters.some((c) => String(c.id) === String(chapterId)),
  )?.id;
  const [open, setOpen] = useState<Set<number>>(() => new Set(curSec != null ? [curSec] : []));
  // раздел с текущей главой раскрыт всегда, остальные — по клику
  useEffect(() => {
    if (curSec != null) setOpen((prev) => new Set(prev).add(curSec));
  }, [curSec]);
  const toggle = (id: number) =>
    setOpen((prev) => {
      const n = new Set(prev);
      if (n.has(id)) n.delete(id);
      else n.add(id);
      return n;
    });

  const slot = <div className="fst-slides" ref={setItemsSlot} />;

  return (
    <aside className="slide-fs-toc" aria-label="Содержание">
      {sections.length === 0
        ? slot
        : sections.map((sec) => {
            const isOpen = open.has(sec.id);
            return (
              <div key={sec.id} className="fst-sec">
                <button
                  className="fst-sec-head"
                  onClick={() => toggle(sec.id)}
                  aria-expanded={isOpen}
                >
                  <span className={`fst-chev ${isOpen ? "open" : ""}`}>›</span>
                  {sec.title}
                </button>
                {isOpen &&
                  sec.chapters.map((ch) => {
                    const cur = String(ch.id) === String(chapterId);
                    return (
                      <div key={ch.id}>
                        <button
                          className={`slide-fs-toc-item ${cur ? "on" : ""}`}
                          onClick={() => !cur && onOpenChapter(ch.id)}
                        >
                          <span className="slide-fs-toc-num">
                            {String(ch.num).padStart(2, "0")}
                          </span>
                          <span className="slide-fs-toc-name">{ch.title}</span>
                        </button>
                        {cur && slot}
                      </div>
                    );
                  })}
              </div>
            );
          })}
    </aside>
  );
}

// Пункт под текущей главой (слайд, вопрос, упражнение).
interface FsItemProps {
  on?: boolean;
  mark?: string | undefined;
  num: number;
  children: ReactNode;
  onClick: () => void;
  status?: string;
}

export function FsItem({ on, mark, num, children, onClick, status }: FsItemProps) {
  return (
    <button className={`fst-slide ${on ? "on" : ""} ${status || ""}`} onClick={onClick}>
      <span className="fst-slide-num">{mark || String(num).padStart(2, "0")}</span>
      <span className="fst-slide-name">{children}</span>
    </button>
  );
}
