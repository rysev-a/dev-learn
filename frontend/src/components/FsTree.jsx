import { useEffect, useState } from "react";

/* Левое дерево полноэкранного режима: разделы книги → главы. Под текущей
   главой — слот (`setItemsSlot`): активная вкладка (слайды, вопросы или
   упражнения) кладёт в него свои пункты через портал. */
export default function FsTree({ sections, chapterId, onOpenChapter, setItemsSlot }) {
  const curSec = sections.find((sec) =>
    sec.chapters.some((c) => String(c.id) === String(chapterId)),
  )?.id;
  const [open, setOpen] = useState(() => new Set(curSec != null ? [curSec] : []));
  // раздел с текущей главой раскрыт всегда, остальные — по клику
  useEffect(() => {
    if (curSec != null) setOpen((prev) => new Set(prev).add(curSec));
  }, [curSec]);
  const toggle = (id) =>
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
export function FsItem({ on, mark, num, children, onClick, status }) {
  return (
    <button className={`fst-slide ${on ? "on" : ""} ${status || ""}`} onClick={onClick}>
      <span className="fst-slide-num">{mark || String(num).padStart(2, "0")}</span>
      <span className="fst-slide-name">{children}</span>
    </button>
  );
}
