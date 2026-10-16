import { useMemo, useState } from "react";
import { ABI_NAMES, OPS, PSEUDO, fieldsOf, type BitField } from "../riscv/rv-isa.ts";
import { STACK_TOP, assemble } from "../riscv/rv-asm.ts";
import { MMIO_MAP, RvMachine } from "../riscv/rv-machine.ts";
import { fullSource, type RvTask } from "../riscv/rv-tasks.ts";
import { projectFiles, projectZip } from "../riscv/rv-project.ts";
import { makeZip } from "../riscv/zip.ts";
import { MemoryGrid, ProgramCard, PseudoTable, RunButtons, TaskResult, memRows, useAsmSession } from "./AsmShared.tsx";

/* Настоящие 32-битные команды RISC-V на «мягком» процессоре с памятью и периферией. В режиме real —
   целые настоящие программы, которые можно собрать на своём компьютере (проект скачивается архивом). */

const RUN_LIMIT = 200_000;
const hexAddr = (n: number) => n.toString(16).toUpperCase().padStart(4, "0");
const LEDS = [7, 6, 5, 4, 3, 2, 1, 0];
const WINDOWS = [
  { id: "text", title: "Команды (0x0000)", from: 0x0000 },
  { id: "data", title: "Данные (0x1000)", from: 0x1000 },
  { id: "stack", title: "Стек (вершина)", from: STACK_TOP - 0x100 },
];

function saveBlob(blob: Blob|MediaSource, name: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

interface RvLabProps {
  task: RvTask;
  code: string | undefined;
  onCode: (code: string) => void;
  solvedBefore: boolean;
  onSolved?: (code: string) => void;
  onNext?: () => void;
  hasNext: boolean;
  nextLabel: string;
  real?: boolean;
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
}: RvLabProps) {
  const [resetKey, setResetKey] = useState(0);
  const [windowId, setWindowId] = useState("text");
  const [openFile, setOpenFile] = useState("program.s");
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
    [asm, resetKey, task],
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
  const session = useAsmSession({ task, source, solvedBefore, ok: result?.ok, onCode, onSolved });

  /* окно памяти перескакивает туда, где команда только что читала или писала */
  const follow = () => {
    if (!machine) return;
    const addr = machine.lastWrite ?? machine.lastRead;
    if (addr === null) return;
    const w = WINDOWS.find((x) => addr >= x.from && addr < x.from + 0x100);
    if (w) setWindowId(w.id);
  };
  const step = () => (machine?.step(), follow(), session.rerender());
  const run = () => (machine?.run(RUN_LIMIT), follow(), session.rerender());

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
  const base = (WINDOWS.find((w) => w.id === windowId) ?? WINDOWS[0]!).from;
  const mem = view?.mem ?? asm.image;
  const grid = memRows(mem, base, 16, (addr) => ({
    read: view?.lastRead === addr,
    written: view?.lastWrite === addr,
  }));
  const switches = task.switches ?? 0;
  const files = useMemo(() => projectFiles(source), [source]);
  const shown = files.find((f) => f.name === openFile) ?? files[0]!;

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
          <ProgramCard
            session={session}
            hint={task.hint}
            source={source}
            errors={asm.errors}
            ariaLabel="Текст программы на ассемблере RISC-V"
            onChange={onCode}
          />

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
                        selected={session.selected === l.addr}
                        onClick={() => session.select(l.addr)}
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
              <RunButtons canStep={canStep} step={step} run={run} reset={() => setResetKey((n) => n + 1)} />
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

          <TaskResult result={result} hasNext={hasNext} onNext={onNext} nextLabel={nextLabel} />

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
            <MemoryGrid rows={grid} addrWidth={4} className="lab-mem" />
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
                  new Blob([makeZip(projectZip(files)) as BlobPart], {
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
          <PseudoTable items={PSEUDO} />
        </div>
      </div>
    </div>
  );
}

interface ListingRow {
  addr: number;
  addrHex: string;
  wordHex: string;
  text: string;
  current: boolean;
  pseudo?: boolean;
  parts: { fmt: string; fields: BitField[] };
}

function RowFragment({ l, selected, onClick }: { l: ListingRow; selected: boolean; onClick: () => void }) {
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
