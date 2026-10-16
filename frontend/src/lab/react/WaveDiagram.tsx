import { JSXElementConstructor, Key, ReactPortal, ReactNode, ReactElement } from "react";
import { WAVE } from "../exercises/logic-gates/lab/wave.ts";

/* Временная диаграмма: история сигналов в упражнениях с защёлками и регистрами */
export default function WaveDiagram({ wave, onClear }) {
  return (
    <div className="lab-card">
      <div className="lab-card-head">
        <div>
          <h3>Временная диаграмма</h3>
          <p>
            История сигналов: каждый столбец — одно изменение. Пунктир —
            значение пока не определено
          </p>
        </div>
        <button type="button" className="quiz-btn ghost" onClick={onClear}>
          Очистить
        </button>
      </div>
      <svg
        className="lab-wave"
        viewBox={`0 0 ${WAVE.width} ${wave.height}`}
        role="img"
        aria-label="Временная диаграмма сигналов"
      >
        {wave.cols.map((x: string|number|undefined, i: Key|null|undefined) => (
          <line
            key={i}
            className="wave-grid"
            x1={x}
            x2={x}
            y1="0"
            y2={wave.height}
          />
        ))}
        {wave.cols.length > 0 && (
          <rect
            className="wave-now"
            x={wave.lastX}
            y="0"
            width={WAVE.step}
            height={wave.height}
          />
        )}
        {wave.rows.map((r: { label: boolean|Key|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|Promise<string|number|bigint|boolean|ReactPortal|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|null|undefined>|null|undefined; kind: any; top: number; dx: string|undefined; d: string|undefined; }) => (
          <g key={r.label} className={`wave-row ${r.kind}`}>
            <text className="wave-label" x="0" y={r.top + 18}>
              {r.label}
            </text>
            <path className="wave-x" d={r.dx} />
            <path className="wave-line" d={r.d} />
          </g>
        ))}
      </svg>
    </div>
  );
}
