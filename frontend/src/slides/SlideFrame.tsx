/* Общая рамка слайда: рубрика с номером, заголовок, подзаголовок, тело и блок «ГЛАВНОЕ».
   Раньше эти компоненты копировались в каждый файл главы. */
import type { ReactNode } from "react";

function Rubric({ text, n, total }: { text: string; n: number; total: number }) {
  return (
    <div className="s-rubric">
      <span>{text}</span>
      <span>
        {String(n).padStart(2, "0")} / {total}
      </span>
    </div>
  );
}

// makeSlide(рубрика, число слайдов главы) → компонент <Slide n title sub main>
export interface SlideProps {
  n: number;
  title: string;
  sub?: string;
  main?: ReactNode;
  children?: ReactNode;
}

export function makeSlide(rubric: string, total: number) {
  function Slide({ n, title, sub, main, children }: SlideProps) {
    return (
      <div className="slide">
        <Rubric text={rubric} n={n} total={total} />
        <h3 className="s-title">{title}</h3>
        {sub && <p className="s-sub">{sub}</p>}
        <div className="s-divider" />
        <div className="s-body">{children}</div>
        {main && (
          <div className="s-main">
            <span className="s-main-label">ГЛАВНОЕ</span>
            <span className="s-main-text">{main}</span>
          </div>
        )}
      </div>
    );
  }
  // рубрика и число слайдов нужны выгрузке слайдов в JSON (scripts/slides-export.mjs)
  return Object.assign(Slide, { rubric, total });
}
