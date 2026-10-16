import ResultAlert from "./ResultAlert.tsx";
import { useEffect, useMemo, useRef, useState, type KeyboardEvent } from "react";
import { assemble } from "../asm/assembler.ts";
import { OPS, PSEUDO, REG_COUNT, fields } from "../asm/isa.ts";
import { Machine } from "../asm/machine.ts";
import { GateMachine } from "../cpu8/gate-machine.ts";
import { hex, type AsmTask } from "../asm/tasks.ts";
import CpuInspector from "./CpuInspector.tsx";

/* Ассемблер процессора «Мини-8»: пишем программу, смотрим машинный код и запускаем её на виртуальном диске
   в эмуляторе или на процессоре, собранном из вентилей. */

const RUN_LIMIT = 100_000;
const hexByte = (n: number) => n.toString(16).toUpperCase().padStart(2, "0");
const regNames = Array.from({ length: REG_COUNT }, (_, i) => `r${i}`);

interface AsmLabProps {
  task: AsmTask;
  code: string | undefined;
  onCode: (code: string) => void;
  solvedBefore: boolean;
  onSolved?: (code: string) => void;
  onNext?: () => void;
  hasNext: boolean;
  nextLabel: string;
}

export default function AsmLab({
  task,
  code,
  onCode,
  solvedBefore,
  onSolved,
  onNext,
  hasNext,
  nextLabel,
}: AsmLabProps) {
  const [engine, setEngine] = useState("emu");
  const [resets, setResets] = useState(0);
  const [, bump] = useState(0);
  const [hintOpen, setHintOpen] = useState(false);
  const [selected, setSelected] = useState<number | null>(null);
  const reported = useRef(false);
  const source = code ?? task.starter;
  const asm = useMemo(() => assemble(source), [source]);

  const machine = useMemo(() => {
    if (asm.errors.length > 0) return null;
    return engine === "gates"
      ? new GateMachine(asm.words, task.disk)
      : new Machine(asm.words, task.disk);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [asm, engine, resets, task]);
  const view = machine?.view() ?? null;
  const result = view
    ? view.error
      ? { ok: false, message: view.error }
      : view.halted
        ? task.check(view.mem)
        : null
    : null;
  const canStep = !!view && !view.halted && !view.error;

  useEffect(() => {
    reported.current = !!solvedBefore;
    setHintOpen(false);
    setSelected(null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [task.id]);
  useEffect(() => {
    if (result?.ok && !reported.current) {
      reported.current = true;
      onSolved?.(source);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [result?.ok]);

  const step = () => (machine?.step(), bump((n) => n + 1));
  const run = () => (machine?.run(RUN_LIMIT), bump((n) => n + 1));

  const onKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key !== "Tab") return;
    e.preventDefault();
    const el = e.currentTarget;
    const { selectionStart: s, selectionEnd: en, value } = el;
    onCode(`${value.slice(0, s)}  ${value.slice(en)}`);
    requestAnimationFrame(() => (el.selectionStart = el.selectionEnd = s + 2));
  };
  const showSolution = () => {
    if (
      window.confirm(
        "Показать эталонное решение? Ваш текущий код в этом задании будет заменён решением.",
      )
    )
      onCode(task.solution);
  };

  const pc = view?.pc ?? -1;
  const listing = asm.lines.map((l) => ({
    ...l,
    bits: fields(l.word),
    wordHex: l.word.toString(16).padStart(4, "0"),
    current: l.addr === pc,
  }));
  const mem = view?.mem ?? task.disk;
  const regionOf = (i: number) =>
    task.regions.findIndex((r) => i >= r.from && i < r.from + r.length);
  const grid = Array.from({ length: 16 }, (_, row) => ({
    addr: row * 16,
    cells: Array.from({ length: 16 }, (_, col) => {
      const addr = row * 16 + col;
      const b = mem[addr];
      return {
        addr,
        hex: hexByte(b),
        char: b >= 32 && b < 127 ? String.fromCharCode(b) : "·",
        changed: b !== task.disk[addr],
        written: view?.lastWrite === addr,
        read: view?.lastRead === addr,
        region: regionOf(addr),
      };
    }),
  }));
  const cellClass = (c: { region: number; changed?: boolean; read?: boolean; written?: boolean }) =>
    [
      "lab-cell",
      c.region >= 0 ? `rg${c.region}` : "",
      c.changed ? "changed" : "",
      c.read ? "read" : "",
      c.written ? "written" : "",
    ]
      .filter(Boolean)
      .join(" ");

  return (
    <div className="lab lab-asm">
      <div className="lab-asm-grid">
        <section className="lab-col">
          <div className="lab-card">
            <div className="lab-card-head">
              <h3>Программа</h3>
              <div className="lab-actions">
                <button
                  type="button"
                  className="quiz-btn ghost"
                  onClick={() => setHintOpen((v) => !v)}
                >
                  {hintOpen ? "Скрыть подсказку" : "Подсказка"}
                </button>
                <button
                  type="button"
                  className="quiz-btn ghost"
                  onClick={showSolution}
                >
                  Показать решение
                </button>
                <button
                  type="button"
                  className="quiz-btn ghost"
                  onClick={() => onCode(task.starter)}
                >
                  Начать заново
                </button>
              </div>
            </div>
            {hintOpen && <p className="ex-hint">{task.hint}</p>}
            <textarea
              className="lab-editor"
              spellCheck={false}
              rows={16}
              value={source}
              onChange={(e) => (onCode(e.target.value), setSelected(null))}
              onKeyDown={onKey}
              aria-label="Текст программы на ассемблере"
            />
            {asm.errors.length > 0 && (
              <ul className="lab-errors" role="alert">
                {asm.errors.map((e, i) => (
                  <li key={i}>
                    <strong>Строка {e.line}:</strong> {e.message}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="lab-card">
            <div className="lab-card-head">
              <div>
                <h3>Машинный код</h3>
                <p>
                  Что ассемблер сделал из вашей программы: каждая команда — одно
                  16-битное слово из полей «код · A · B · C». Нажмите на строку,
                  чтобы разобрать её по битам.
                </p>
              </div>
            </div>
            {listing.length === 0 ? (
              <p className="lab-muted">Команд пока нет.</p>
            ) : (
              <div className="lab-scroll">
                <table className="lab-table">
                  <thead>
                    <tr>
                      <th>адрес</th>
                      <th>hex</th>
                      <th>код</th>
                      <th>A</th>
                      <th>B</th>
                      <th>C</th>
                      <th className="left">команда</th>
                    </tr>
                  </thead>
                  <tbody>
                    {listing.map((l) => (
                      <tr
                        key={l.addr}
                        className={`${l.current ? "current" : ""} ${selected === l.addr ? "selected" : ""}`}
                        onClick={() =>
                          setSelected(selected === l.addr ? null : l.addr)
                        }
                      >
                        <td>{l.addr}</td>
                        <td className="mono">{l.wordHex}</td>
                        <td className="mono f-op">{l.bits.opcode}</td>
                        <td className="mono f-a">{l.bits.a}</td>
                        <td className="mono f-b">{l.bits.b}</td>
                        <td className="mono f-c">{l.bits.c}</td>
                        <td className="left mono">{l.text}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            {selected !== null && (
              <p className="lab-explain">
                Первые четыре бита — <strong>код операции</strong>: по ним
                процессор понимает, что делать. Дальше поля A, B и C: в
                зависимости от команды это номера регистров, число или смещение
                перехода. Подробности — в справочнике ниже.
              </p>
            )}
          </div>
        </section>

        <section className="lab-col">
          <div className="lab-card">
            <div className="lab-card-head">
              <h3>Процессор</h3>
              <div
                className="lab-seg"
                role="group"
                aria-label="Чем выполнять программу"
              >
                <button
                  type="button"
                  className={engine === "emu" ? "on" : ""}
                  onClick={() => setEngine("emu")}
                  title="Быстрая программа-эмулятор"
                >
                  Эмулятор
                </button>
                <button
                  type="button"
                  className={engine === "gates" ? "on" : ""}
                  onClick={() => setEngine("gates")}
                  title="Тот же процессор, собранный из вентилей: каждая команда считается схемой"
                >
                  Схема из вентилей
                </button>
              </div>
              <div className="lab-actions">
                <button
                  type="button"
                  className="quiz-btn"
                  onClick={step}
                  disabled={!canStep}
                >
                  Шаг ▸
                </button>
                <button
                  type="button"
                  className="quiz-btn ghost"
                  onClick={run}
                  disabled={!canStep}
                >
                  Выполнить
                </button>
                <button
                  type="button"
                  className="quiz-btn ghost"
                  onClick={() => setResets((n) => n + 1)}
                >
                  Сбросить
                </button>
              </div>
            </div>
            {view ? (
              <>
                <div className="lab-regs">
                  {regNames.map((name, i) => (
                    <div
                      key={name}
                      className={`lab-reg ${view.lastReg === i ? "changed" : ""}`}
                    >
                      <span className="lab-reg-name">{name}</span>
                      <span className="lab-reg-val mono">{view.regs[i]}</span>
                      <span className="lab-reg-hex mono">
                        0x{hexByte(view.regs[i])}
                      </span>
                    </div>
                  ))}
                </div>
                <div className="lab-status">
                  <span className="lab-badge">
                    следующая команда: {view.pc}
                  </span>
                  <span className="lab-badge">
                    выполнено шагов: {view.steps}
                  </span>
                  {view.halted && (
                    <span className="lab-badge ok">остановлен (hlt)</span>
                  )}
                </div>
              </>
            ) : (
              <p className="lab-muted">
                Исправьте ошибки в программе — тогда её можно запустить.
              </p>
            )}
          </div>

          {result && (
            <ResultAlert
              ok={result.ok}
              title={result.ok ? "Задание выполнено!" : "Пока не то"}
              onNext={result.ok && hasNext ? onNext : undefined}
              nextLabel={nextLabel}
            >
              {result.message}
            </ResultAlert>
          )}

          <div className="lab-card">
            <div className="lab-card-head">
              <div>
                <h3>Виртуальный диск</h3>
                <p>
                  256 байт памяти. Жёлтым подсвечены байты, которые ваша
                  программа изменила; зелёным — записанный последним, синим —
                  прочитанный.
                </p>
              </div>
            </div>
            <div className="lab-regions">
              {task.regions.map((r, i) => (
                <span key={r.name} className={`lab-region rg${i}`}>
                  {r.name} · {hex(r.from)}
                </span>
              ))}
            </div>
            <div className="lab-disk mono">
              <div className="lab-disk-head">
                <span />
                {grid[0].cells.map((c) => (
                  <span key={c.addr}>{c.addr.toString(16).toUpperCase()}</span>
                ))}
                <span className="lab-ascii-head">текст</span>
              </div>
              {grid.map((row) => (
                <div key={row.addr} className="lab-disk-row">
                  <span className="lab-addr">{hexByte(row.addr)}</span>
                  {row.cells.map((c) => (
                    <span
                      key={c.addr}
                      className={cellClass(c)}
                      title={`адрес 0x${hexByte(c.addr)}`}
                    >
                      {c.hex}
                    </span>
                  ))}
                  <span className="lab-ascii">
                    {row.cells.map((c) => (
                      <span
                        key={c.addr}
                        className={c.char === "·" ? "dot" : ""}
                      >
                        {c.char}
                      </span>
                    ))}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>

      {engine === "gates" && machine instanceof GateMachine && (
        <div className="lab-card">
          <div className="lab-card-head">
            <div>
              <h3>Устройство процессора</h3>
              <p>
                Сейчас программу выполняет не эмулятор, а схема из вентилей:
                каждый такт в ней — целая команда. Кнопка с лупой на блоке
                показывает, из чего он собран, вплоть до отдельных вентилей;
                значения на проводах — живые, по текущему шагу.
              </p>
            </div>
          </div>
          <CpuInspector machine={machine} version={view?.steps ?? 0} />
        </div>
      )}

      <div className="lab-card">
        <div className="lab-card-head">
          <div>
            <h3>Справочник: команды процессора Мини-8</h3>
            <p>
              8 регистров r0…r7 (r0 всегда равен нулю), числа — байты 0…255.
              Команда занимает 16 бит:{" "}
              <span className="mono">код(4) · A(3) · B(3) · C(6)</span>.
              Комментарии — после «;». Метки — «имя:» в начале строки; константы
              — «.equ ИМЯ, число».
            </p>
          </div>
        </div>
        <div className="lab-scroll">
          <table className="lab-table ref">
            <thead>
              <tr>
                <th className="left">команда</th>
                <th className="left">пример</th>
                <th className="left">что делает</th>
                <th>код</th>
              </tr>
            </thead>
            <tbody>
              {OPS.map((o) => (
                <tr key={o.mnemonic}>
                  <td className="left mono">
                    <strong>{o.mnemonic}</strong>
                  </td>
                  <td className="left mono">{o.example}</td>
                  <td className="left">{o.meaning}</td>
                  <td className="mono">
                    {o.opcode.toString(2).padStart(4, "0")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <h4 className="lab-ref-sub">
            Псевдокоманды — сокращения, которые ассемблер разворачивает сам
          </h4>
          <table className="lab-table ref">
            <tbody>
              {PSEUDO.map((p) => (
                <tr key={p.name}>
                  <td className="left mono">
                    <strong>{p.example}</strong>
                  </td>
                  <td className="left mono">= {p.becomes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
