import ResultAlert from "./ResultAlert.jsx";
import { useEffect, useMemo, useRef, useState } from "react";
import { ABI_NAMES, OPS, PSEUDO, fieldsOf } from "../riscv/rv-isa";
import { STACK_TOP, assemble } from "../riscv/rv-asm";
import { MMIO_MAP, RvMachine } from "../riscv/rv-machine";
import { fullSource } from "../riscv/rv-tasks";
import { projectFiles, projectZip } from "../riscv/rv-project";
import { makeZip } from "../riscv/zip";

/* Настоящие 32-битные команды RISC-V на «мягком» процессоре с памятью и периферией. В режиме real —
   целые настоящие программы, которые можно собрать на своём компьютере (проект скачивается архивом). */

const RUN_LIMIT = 200_000;
const hex8 = (n) => n.toString(16).toUpperCase().padStart(2, "0");
const hexAddr = (n) => n.toString(16).toUpperCase().padStart(4, "0");
const LEDS = [7, 6, 5, 4, 3, 2, 1, 0];
const WINDOWS = [
  { id: "text", title: "Команды (0x0000)", from: 0x0000 },
  { id: "data", title: "Данные (0x1000)", from: 0x1000 },
  { id: "stack", title: "Стек (вершина)", from: STACK_TOP - 0x100 },
];

function saveBlob(blob, name) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export default function RvLab({
  task,
  code,
  onCode,
  solvedBefore,
  onSolved,
  onNext,
  hasNext,
  nextLabel,
  real,
}) {
  const [resets, setResets] = useState(0);
  const [, bump] = useState(0);
  const [hintOpen, setHintOpen] = useState(false);
  const [selected, setSelected] = useState(null);
  const [windowId, setWindowId] = useState("text");
  const [openFile, setOpenFile] = useState("program.s");
  const reported = useRef(false);
  const source = code ?? task.starter;
  const asm = useMemo(() => assemble(fullSource(source, task)), [source, task]);
  const machine = useMemo(
    () =>
      asm.errors.length > 0
        ? null
        : new RvMachine(asm.image, {
            switches: task.switches,
            entry: asm.entry,
          }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [asm, resets, task],
  );
  const view = machine?.view() ?? null;
  const result = view
    ? view.error
      ? { ok: false, message: view.error }
      : view.halted
        ? task.check(view, asm.symbols)
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

  /* окно памяти перескакивает туда, где команда только что читала или писала */
  const follow = () => {
    if (!machine) return;
    const addr = machine.lastWrite ?? machine.lastRead;
    if (addr === null) return;
    const w = WINDOWS.find((x) => addr >= x.from && addr < x.from + 0x100);
    if (w) setWindowId(w.id);
  };
  const step = () => (machine?.step(), follow(), bump((n) => n + 1));
  const run = () => (machine?.run(RUN_LIMIT), follow(), bump((n) => n + 1));

  const onKey = (e) => {
    if (e.key !== "Tab") return;
    e.preventDefault();
    const el = e.target;
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
    parts: fieldsOf(l.word),
    wordHex: l.word.toString(16).padStart(8, "0"),
    addrHex: l.addr.toString(16).padStart(4, "0"),
    current: l.addr === pc,
  }));
  const regs = Array.from({ length: 32 }, (_, i) => {
    const u = view?.regs[i] ?? 0;
    return {
      num: i,
      name: ABI_NAMES[i],
      signed: u | 0,
      hex: (u >>> 0).toString(16).padStart(8, "0"),
      changed: view?.lastReg === i,
    };
  });
  const base = WINDOWS.find((w) => w.id === windowId).from;
  const mem = view?.mem ?? asm.image;
  const grid = Array.from({ length: 16 }, (_, row) => ({
    addr: base + row * 16,
    cells: Array.from({ length: 16 }, (_, col) => {
      const addr = base + row * 16 + col;
      const b = mem[addr] ?? 0;
      return {
        addr,
        hex: hex8(b),
        char: b >= 32 && b < 127 ? String.fromCharCode(b) : "·",
        read: view?.lastRead === addr,
        written: view?.lastWrite === addr,
      };
    }),
  }));
  const switches = task.switches ?? 0;
  const files = useMemo(() => projectFiles(source), [source]);
  const shown = files.find((f) => f.name === openFile) ?? files[0];

  return (
    <div className="lab lab-asm lab-rv">
      {task.data?.trim() && (
        <div className="lab-card">
          <p className="lab-data-title">
            Данные задания (доступны по меткам, менять нельзя):
          </p>
          <pre className="lab-data mono">{task.data}</pre>
        </div>
      )}
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
              aria-label="Текст программы на ассемблере RISC-V"
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
                  настоящее 32-битное слово RISC-V. Цветом выделены поля;
                  нажмите на строку, чтобы увидеть формат команды.
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
                      <th className="left">поля (старшие биты слева)</th>
                      <th className="left">команда</th>
                    </tr>
                  </thead>
                  <tbody>
                    {listing.map((l) => (
                      <RowFragment
                        key={l.addr}
                        l={l}
                        selected={selected === l.addr}
                        onClick={() =>
                          setSelected(selected === l.addr ? null : l.addr)
                        }
                      />
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </section>

        <section className="lab-col">
          <div className="lab-card">
            <div className="lab-card-head">
              <h3>Процессор RV32IM</h3>
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
                <div className="lab-regs rv32">
                  {regs.map((r) => (
                    <div
                      key={r.num}
                      className={`lab-reg ${r.changed ? "changed" : ""}`}
                      title={`x${r.num} = 0x${r.hex}`}
                    >
                      <span className="lab-reg-name">
                        {r.name} <small>x{r.num}</small>
                      </span>
                      <span className="lab-reg-val mono">{r.signed}</span>
                      <span className="lab-reg-hex mono">{r.hex}</span>
                    </div>
                  ))}
                </div>
                <div className="lab-status">
                  <span className="lab-badge">pc = 0x{hexAddr(view.pc)}</span>
                  <span className="lab-badge">
                    выполнено команд: {view.steps}
                  </span>
                  {view.lastInsn && (
                    <span className="lab-badge mono">{view.lastInsn}</span>
                  )}
                  {view.halted && (
                    <span className="lab-badge ok">остановлен</span>
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

          {real ? (
            <div className="lab-card">
              <div className="lab-card-head">
                <div>
                  <h3>Вывод программы</h3>
                  <p>
                    Всё, что программа отправила в стандартный вывод системным
                    вызовом write. Когда она вызывает exit, здесь же видно код
                    возврата.
                  </p>
                </div>
              </div>
              <pre className="lab-console mono">
                {view?.uart ?? ""}
                <span className="lab-caret">▮</span>
              </pre>
              {view && view.exitCode !== null && (
                <p className="lab-exit mono">
                  код возврата: {view.exitCode & 0xff}
                </p>
              )}
            </div>
          ) : (
            <div className="lab-card">
              <div className="lab-card-head">
                <div>
                  <h3>Периферия</h3>
                  <p>
                    Устройства подключены к тем же шинам, что и память, и видны
                    программе как обычные адреса. Запись или чтение по такому
                    адресу — это общение с устройством.
                  </p>
                </div>
              </div>
              <div className="lab-dev">
                <span className="lab-dev-name">Светодиоды</span>
                <span className="lab-leds" aria-label="Светодиоды">
                  {LEDS.map((i) => (
                    <span
                      key={i}
                      className={`lab-led ${((view?.leds ?? 0) >> i) & 1 ? "on" : ""}`}
                      title={`LED${i}`}
                    >
                      {i}
                    </span>
                  ))}
                </span>
              </div>
              <div className="lab-dev">
                <span className="lab-dev-name">Переключатели</span>
                <span className="lab-leds" aria-label="Переключатели">
                  {LEDS.map((i) => (
                    <span
                      key={i}
                      className={`lab-led sw ${(switches >> i) & 1 ? "on" : ""}`}
                      title={`SW${i}`}
                    >
                      {i}
                    </span>
                  ))}
                </span>
              </div>
              <div className="lab-dev">
                <span className="lab-dev-name">Таймер</span>
                <span className="mono">{view?.steps ?? 0}</span>
              </div>
              <p className="lab-data-title">Консоль (UART):</p>
              <pre className="lab-console mono">
                {view?.uart ?? ""}
                <span className="lab-caret">▮</span>
              </pre>
              <table className="lab-table ref">
                <tbody>
                  {MMIO_MAP.map((m) => (
                    <tr key={m.addr}>
                      <td className="left mono">0x{m.addr.toString(16)}</td>
                      <td className="left">
                        <strong>{m.name}</strong> — {m.note}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          <div className="lab-card">
            <div className="lab-card-head">
              <h3>Память</h3>
              <div className="lab-seg" role="group" aria-label="Окно памяти">
                {WINDOWS.map((w) => (
                  <button
                    key={w.id}
                    type="button"
                    className={windowId === w.id ? "on" : ""}
                    onClick={() => setWindowId(w.id)}
                  >
                    {w.title}
                  </button>
                ))}
              </div>
            </div>
            <p className="lab-muted">
              Окно в 256 байт. Зелёным — записанный последним байт, синим —
              прочитанный. Слова лежат «младшим байтом вперёд» (little-endian).
            </p>
            <div className="lab-disk lab-mem mono">
              <div className="lab-disk-head">
                <span />
                {grid[0].cells.map((c, i) => (
                  <span key={c.addr}>{i.toString(16).toUpperCase()}</span>
                ))}
                <span className="lab-ascii-head">текст</span>
              </div>
              {grid.map((row) => (
                <div key={row.addr} className="lab-disk-row">
                  <span className="lab-addr">{hexAddr(row.addr)}</span>
                  {row.cells.map((c) => (
                    <span
                      key={c.addr}
                      className={`lab-cell ${c.read ? "read" : ""} ${c.written ? "written" : ""}`}
                      title={`адрес 0x${hexAddr(c.addr)}`}
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

      {real && (
        <div className="lab-card">
          <div className="lab-card-head">
            <div>
              <h3>Собрать у себя на компьютере</h3>
              <p>
                Эта программа — обычный файл на ассемблере RISC-V. Скачайте
                проект, установите инструменты (команды — в README) и выполните{" "}
                <span className="mono">make run</span>: настоящий компилятор
                превратит текст в те же 32-битные слова, что в листинге выше, а
                qemu выполнит их.
              </p>
            </div>
            <button
              type="button"
              className="quiz-btn"
              onClick={() =>
                saveBlob(
                  new Blob([makeZip(projectZip(files))], {
                    type: "application/zip",
                  }),
                  "riscv-program.zip",
                )
              }
            >
              Скачать проект (.zip)
            </button>
          </div>
          <div className="lab-seg" role="group" aria-label="Файлы проекта">
            {files.map((f) => (
              <button
                key={f.name}
                type="button"
                className={openFile === f.name ? "on" : ""}
                onClick={() => setOpenFile(f.name)}
              >
                {f.name}
              </button>
            ))}
          </div>
          <p className="lab-muted">
            {shown.note}{" "}
            <button
              type="button"
              className="quiz-btn ghost"
              onClick={() =>
                saveBlob(
                  new Blob([shown.content], {
                    type: "text/plain;charset=utf-8",
                  }),
                  shown.name,
                )
              }
            >
              Скачать {shown.name}
            </button>
          </p>
          <pre className="lab-data mono lab-file">{shown.content}</pre>
        </div>
      )}

      <div className="lab-card">
        <div className="lab-card-head">
          <div>
            <h3>Справочник: команды RISC-V (RV32IM)</h3>
            <p>
              32 регистра по 32 бита; x0 (zero) всегда равен нулю. У регистров
              есть «ABI-имена»: a0…a7 — аргументы и результат, t0…t6 —
              временные, s0…s11 — «неприкосновенные» (функция обязана вернуть их
              как были), ra — адрес возврата, sp — стек. Комментарии — после
              «#». Метки — «имя:».
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
                <th>формат</th>
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
                    {o.fmt}
                    {o.ext === "M" ? " · M" : ""}
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
                <tr key={p.example}>
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

function RowFragment({ l, selected, onClick }) {
  return (
    <>
      <tr
        className={`${l.current ? "current" : ""} ${selected ? "selected" : ""} ${l.pseudo ? "pseudo" : ""}`}
        onClick={onClick}
      >
        <td className="mono">{l.addrHex}</td>
        <td className="mono">{l.wordHex}</td>
        <td className="left mono lab-fields">
          {l.parts.fields.map((f, i) => (
            <span key={i} className={`fld ${f.cls}`} title={f.name}>
              {f.bits}
            </span>
          ))}
        </td>
        <td className="left mono">{l.text}</td>
      </tr>
      {selected && (
        <tr className="explain-row">
          <td colSpan={4}>
            <div className="lab-legend">
              <strong>Формат {l.parts.fmt}.</strong>
              {l.parts.fields.map((f, i) => (
                <span key={i} className="lab-legend-item">
                  <span className={`fld ${f.cls}`}>{f.bits}</span> {f.name}
                </span>
              ))}
            </div>
          </td>
        </tr>
      )}
    </>
  );
}
