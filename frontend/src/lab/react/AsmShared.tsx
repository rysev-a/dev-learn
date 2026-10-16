import { useEffect, useRef, useState, type KeyboardEvent, type ReactNode } from "react";
import ResultAlert from "./ResultAlert.tsx";

/* Общие части лабораторий на ассемблере (Мини-8 — AsmLab, RISC-V — RvLab): сеанс решения, карточка программы,
   кнопки запуска, итог проверки, сетка памяти и таблица псевдокоманд. */

export const hexByte = (n: number) => n.toString(16).toUpperCase().padStart(2, "0");

/** Что нужно сеансу от задания */
interface SessionTask {
  id: string;
  starter: string;
  solution: string;
}

/** Состояние одного решения: подсказка, выбранная строка листинга, отчёт о решении, правка текста. */
export function useAsmSession(opts: {
  task: SessionTask;
  source: string;
  solvedBefore: boolean;
  /** задание выполнено (результат проверки после остановки машины) */
  ok: boolean | undefined;
  onCode: (code: string) => void;
  onSolved?: ((code: string) => void) | undefined;
}) {
  const { task, source, solvedBefore, ok, onCode, onSolved } = opts;
  const [, bump] = useState(0);
  const [hintOpen, setHintOpen] = useState(false);
  const [selected, setSelected] = useState<number | null>(null);
  const reported = useRef(false);

  useEffect(() => {
    reported.current = !!solvedBefore;
    setHintOpen(false);
    setSelected(null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [task.id]);
  useEffect(() => {
    if (ok && !reported.current) {
      reported.current = true;
      onSolved?.(source);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ok]);

  /** Tab в редакторе — два пробела, а не уход фокуса */
  const onKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key !== "Tab") return;
    e.preventDefault();
    const el = e.currentTarget;
    const { selectionStart: s, selectionEnd: en, value } = el;
    onCode(`${value.slice(0, s)}  ${value.slice(en)}`);
    requestAnimationFrame(() => (el.selectionStart = el.selectionEnd = s + 2));
  };
  const showSolution = () => {
    if (window.confirm("Показать эталонное решение? Ваш текущий код в этом задании будет заменён решением."))
      onCode(task.solution);
  };

  return {
    /** перерисовать после шага машины (состояние машины лежит вне React) */
    rerender: () => bump((n) => n + 1),
    hintOpen,
    toggleHint: () => setHintOpen((v) => !v),
    selected,
    select: (addr: number) => setSelected((cur) => (cur === addr ? null : addr)),
    clearSelection: () => setSelected(null),
    showSolution,
    restart: () => onCode(task.starter),
    onKey,
  };
}

export interface AsmError {
  line: number;
  message: string;
}

/** Карточка «Программа»: кнопки, подсказка, редактор, ошибки ассемблера */
export function ProgramCard(props: {
  session: ReturnType<typeof useAsmSession>;
  hint: string;
  source: string;
  errors: AsmError[];
  ariaLabel: string;
  onChange: (code: string) => void;
}) {
  const { session, hint, source, errors, ariaLabel, onChange } = props;
  return (
    <div className="lab-card">
      <div className="lab-card-head">
        <h3>Программа</h3>
        <div className="lab-actions">
          <button type="button" className="quiz-btn ghost" onClick={session.toggleHint}>
            {session.hintOpen ? "Скрыть подсказку" : "Подсказка"}
          </button>
          <button type="button" className="quiz-btn ghost" onClick={session.showSolution}>
            Показать решение
          </button>
          <button type="button" className="quiz-btn ghost" onClick={session.restart}>
            Начать заново
          </button>
        </div>
      </div>
      {session.hintOpen && <p className="ex-hint">{hint}</p>}
      <textarea
        className="lab-editor"
        spellCheck={false}
        rows={16}
        value={source}
        onChange={(e) => (onChange(e.target.value), session.clearSelection())}
        onKeyDown={session.onKey}
        aria-label={ariaLabel}
      />
      {errors.length > 0 && (
        <ul className="lab-errors" role="alert">
          {errors.map((e, i) => (
            <li key={i}>
              <strong>Строка {e.line}:</strong> {e.message}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

/** Кнопки «Шаг», «Выполнить», «Сбросить» */
export function RunButtons({ canStep, step, run, reset }: { canStep: boolean; step: () => void; run: () => void; reset: () => void }) {
  return (
    <div className="lab-actions">
      <button type="button" className="quiz-btn" onClick={step} disabled={!canStep}>
        Шаг ▸
      </button>
      <button type="button" className="quiz-btn ghost" onClick={run} disabled={!canStep}>
        Выполнить
      </button>
      <button type="button" className="quiz-btn ghost" onClick={reset}>
        Сбросить
      </button>
    </div>
  );
}

/** Итог проверки задания; плашка видна, только когда программа остановилась */
export function TaskResult({
  result,
  hasNext,
  onNext,
  nextLabel,
}: {
  result: { ok: boolean; message: string } | null;
  hasNext: boolean;
  onNext?: (() => void) | undefined;
  nextLabel: string;
}) {
  if (!result) return null;
  return (
    <ResultAlert
      ok={result.ok}
      title={result.ok ? "Задание выполнено!" : "Пока не то"}
      onNext={result.ok && hasNext ? onNext : undefined}
      nextLabel={nextLabel}
    >
      {result.message}
    </ResultAlert>
  );
}

/** Ячейка сетки памяти */
export interface MemCell {
  addr: number;
  hex: string;
  char: string;
  changed?: boolean;
  read?: boolean;
  written?: boolean;
  /** номер области диска (Мини-8); меньше нуля или не задан — вне областей */
  region?: number;
}

/** Строки по 16 байт из массива памяти, начиная с адреса base */
export function memRows(mem: ArrayLike<number>, base: number, rows: number, cellOf: (addr: number, byte: number) => Omit<MemCell, "addr" | "hex" | "char">): { addr: number; cells: MemCell[] }[] {
  return Array.from({ length: rows }, (_, row) => ({
    addr: base + row * 16,
    cells: Array.from({ length: 16 }, (_, col) => {
      const addr = base + row * 16 + col;
      const b = mem[addr] ?? 0;
      return { addr, hex: hexByte(b), char: b >= 32 && b < 127 ? String.fromCharCode(b) : "·", ...cellOf(addr, b) };
    }),
  }));
}

const cellClass = (c: MemCell) =>
  [
    "lab-cell",
    c.region !== undefined && c.region >= 0 ? `rg${c.region}` : "",
    c.changed ? "changed" : "",
    c.read ? "read" : "",
    c.written ? "written" : "",
  ]
    .filter(Boolean)
    .join(" ");

/** Сетка памяти: адрес строки, шестнадцатеричные байты и текстовое представление */
export function MemoryGrid({ rows, addrWidth, className = "" }: { rows: { addr: number; cells: MemCell[] }[]; addrWidth: number; className?: string }) {
  const addrHex = (n: number) => n.toString(16).toUpperCase().padStart(addrWidth, "0");
  return (
    <div className={`lab-disk ${className} mono`}>
      <div className="lab-disk-head">
        <span />
        {rows[0]?.cells.map((_, i) => (
          <span key={i}>{i.toString(16).toUpperCase()}</span>
        ))}
        <span className="lab-ascii-head">текст</span>
      </div>
      {rows.map((row) => (
        <div key={row.addr} className="lab-disk-row">
          <span className="lab-addr">{addrHex(row.addr)}</span>
          {row.cells.map((c) => (
            <span key={c.addr} className={cellClass(c)} title={`адрес 0x${addrHex(c.addr)}`}>
              {c.hex}
            </span>
          ))}
          <span className="lab-ascii">
            {row.cells.map((c) => (
              <span key={c.addr} className={c.char === "·" ? "dot" : ""}>
                {c.char}
              </span>
            ))}
          </span>
        </div>
      ))}
    </div>
  );
}

/** Таблица псевдокоманд: ассемблер разворачивает их сам */
export function PseudoTable({ items }: { items: readonly { example: string; becomes: string }[] }): ReactNode {
  return (
    <>
      <h4 className="lab-ref-sub">Псевдокоманды — сокращения, которые ассемблер разворачивает сам</h4>
      <table className="lab-table ref">
        <tbody>
          {items.map((p) => (
            <tr key={p.example}>
              <td className="left mono">
                <strong>{p.example}</strong>
              </td>
              <td className="left mono">= {p.becomes}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
