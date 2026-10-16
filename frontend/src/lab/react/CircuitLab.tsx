import ResultAlert from "./ResultAlert.tsx";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { Section } from "../sections/sections.ts";
import type { Exercise } from "../exercises/logic-gates/exercises.ts";
import type { BoardHandle } from "./BlockBoard.tsx";
import type { PaletteItem } from "./GateBoard.tsx";
import {
  COMPOSITE_GATES,
  evaluateCircuit,
  inputsForRow,
  outputValue,
  reserveUids,
  settleCircuit,
  zeroInputs,
  type Bit,
  type GateInstance,
  type GateType,
  type InputId,
  type NodeValue,
  type Wire,
} from "../exercises/logic-gates/circuit.model.ts";
import { RU_NAMES } from "../exercises/logic-gates/gate-shapes.ts";
import {
  childScope,
  createLibrary,
  expand,
  interfaceOfExercise,
  isBlockSolution,
  isGateSolution,
  localSolutionStore,
  type BlockDef,
  type BlockInstance,
  type BlockInterface,
  type BusWire,
  type Expansion,
  type Solution,
  type ValueScope,
} from "../exercises/logic-gates/blocks.ts";
import { freeSpot } from "../exercises/logic-gates/block-layout.ts";
import { SECTIONS } from "../sections/sections.ts";
import {
  gateLockHint,
  isGateUnlocked,
  loadProgress,
  saveProgress,
} from "../exercises/logic-gates/lab/exercise-progress.ts";
import { HISTORY_MAX, buildWave, type Sample } from "../exercises/logic-gates/lab/wave.ts";
import GateBoard from "./GateBoard.tsx";
import CheckPanel from "./CheckPanel.tsx";
import WaveDiagram from "./WaveDiagram.tsx";
import BlockBoard, { BLOCKS_BOARD_W } from "./BlockBoard.tsx";
import CircuitView from "./CircuitView.tsx";
import { CLOCK_RATES, Clock } from "./clock.ts";

/* Одно упражнение со схемой: доска из вентилей, таблица истинности или сценарий по шагам,
   такт и временная диаграмма. Порт CircuitLab: состояние — в React, расчёт — в общем ядре.
   Решённое упражнение запоминает схему (localStorage + кабинет), см. LabPractice. */

/** один уровень просмотра: верхняя схема или блок, в который «заглянули» */
interface Level {
  title: string;
  def: BlockDef | null;
  iface: BlockInterface;
  solution: Solution;
  expansion: Expansion;
  scope: ValueScope;
}

interface CircuitLabProps {
  section: Section;
  exercise: Exercise;
  index: number;
  solvedBefore: boolean;
  onSolved?: (solution: string) => void;
  onNext?: () => void;
  hasNext: boolean;
  nextLabel: string;
  progressVersion: number;
  fullscreen?: boolean;
  onOpenSource?: (source: { sectionSlug: string; exerciseId: string }) => void;
}

export default function CircuitLab({
  section,
  exercise: ex,
  index,
  solvedBefore,
  onSolved,
  onNext,
  hasNext,
  nextLabel,
  progressVersion,
  fullscreen,
  onOpenSource,
}: CircuitLabProps) {
  const blocksMode = ex.kind === "blocks";
  const [gates, setGates] = useState<GateInstance[]>([]);
  const [wires, setWires] = useState<Wire[]>([]);
  const [instances, setInstances] = useState<BlockInstance[]>([]);
  const [busWires, setBusWires] = useState<BusWire[]>([]);
  const [inspectPath, setInspectPath] = useState<string[]>([]);
  const [editUnlocked, setEditUnlocked] = useState(false);
  const [inputState, setInputState] = useState(zeroInputs());
  const [passed, setPassed] = useState(0);
  const [history, setHistory] = useState<Sample[]>([]);
  const [flash, setFlash] = useState<string | null>(null);
  const [hintOpen, setHintOpen] = useState(false);
  const [, redraw] = useState(0);
  const boardRef = useRef<BoardHandle | null>(null);
  const lastStable = useRef<Map<string, NodeValue>>(new Map());
  const flashTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  const reported = useRef(false);
  const stepsMode = ex.mode === "steps";
  const clockId = ex.clock ?? null;

  /* блоки: библиотека читает решения один раз; новая — после каждого решённого упражнения */
  const library = useMemo(
    () => createLibrary(SECTIONS),
    [ex.id, progressVersion],
  ); // eslint-disable-line react-hooks/exhaustive-deps
  const iface = useMemo(() => interfaceOfExercise(ex), [ex]);
  const expansion = useMemo(
    () =>
      blocksMode
        ? expand({ instances, busWires }, iface, library.lookup)
        : null,
    [blocksMode, instances, busWires, iface, library],
  );
  const circuit = useMemo(
    () => (expansion ? expansion.circuit : { gates, wires }),
    [expansion, gates, wires],
  );

  /* ---------- значения узлов ---------- */
  const tableValues = useMemo(
    () => evaluateCircuit(circuit, inputState),
    [circuit, inputState],
  );
  const seqValues = useMemo(() => {
    if (!stepsMode) return new Map<string, NodeValue>();
    const res = settleCircuit(circuit, inputState, lastStable.current);
    lastStable.current = res.stable ? res.values : new Map();
    return res.values;
  }, [circuit, inputState, stepsMode]);
  const valueAt = useCallback(
    (node: string) => (stepsMode ? seqValues.get(node) : tableValues.get(node)),
    [stepsMode, seqValues, tableValues],
  );

  /* ---------- проверка ---------- */
  const tableRows = useMemo(() => {
    if (stepsMode) return [];
    return ex.target.map((targetRow, row) => {
      const inputs = inputsForRow(ex.inputs, row);
      const actuals = ex.outputs.map((o) => outputValue(circuit, inputs, o));
      return {
        targets: targetRow,
        actuals,
        ok: actuals.every((a, i) => a === targetRow[i]),
      };
    });
  }, [circuit, ex, stepsMode]);
  const matched = tableRows.filter((r) => r.ok).length;
  const totalSteps = ex.steps?.length ?? 0;
  const solved = stepsMode
    ? totalSteps > 0 && passed === totalSteps
    : tableRows.length > 0 && tableRows.every((r) => r.ok);
  const currentRow = ex.inputs.reduce(
    (acc: number, id) => (acc << 1) | inputState[id],
    0,
  );

  /* ---------- сценарий: проверка текущего шага ---------- */
  useEffect(() => {
    if (!stepsMode || !ex.steps) return;
    const step = ex.steps[passed];
    if (!step) return;
    if (!ex.inputs.every((id) => inputState[id] === step.inputs[id])) return;
    if (
      ex.outputs.every(
        (o) =>
          step.expect[o] === undefined || seqValues.get(o) === step.expect[o],
      )
    )
      setPassed((n) => n + 1);
  }, [stepsMode, ex, passed, inputState, seqValues]);

  /* ---------- временная диаграмма ---------- */
  const snapshot = useCallback(
    (): Sample => ({
      inputs: Object.fromEntries(ex.inputs.map((id) => [id, inputState[id]])) as Sample["inputs"],
      outputs: Object.fromEntries(ex.outputs.map((o) => [o, seqValues.get(o)])),
    }),
    [ex, inputState, seqValues],
  );
  const snapRef = useRef(snapshot);
  snapRef.current = snapshot;
  const sampleOnInput = useRef(false);
  // новый столбец — после каждого изменения тумблеров
  useEffect(() => {
    if (!stepsMode) return;
    setHistory((h) => [...h, snapRef.current()].slice(-HISTORY_MAX));
    sampleOnInput.current = true;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [inputState, stepsMode]);
  // схема изменилась, тумблеры — нет: обновить последний столбец
  useEffect(() => {
    if (!stepsMode) return;
    if (sampleOnInput.current) {
      sampleOnInput.current = false;
      return;
    }
    setHistory((h) =>
      h.length === 0 ? h : [...h.slice(0, -1), snapRef.current()],
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [circuit, seqValues]);
  const wave = useMemo(() => buildWave(history, ex), [history, ex]);

  /* ---------- такт ---------- */
  const inputRef = useRef(inputState);
  inputRef.current = inputState;
  const setInput = useCallback((id: InputId, level: Bit) => {
    setInputState((s) => (s[id] === level ? s : { ...s, [id]: level }));
    inputRef.current = { ...inputRef.current, [id]: level };
  }, []);
  // такт создаётся один раз; id тактового входа обновляется на каждом рендере
  const [clock] = useState(() => {
    const c: Clock = new Clock(
      {
        clockId: () => clockId,
        level: (id) => inputRef.current[id as InputId],
        setLevel: (id, level) => {
          if (id === clockId && level === 1 && inputRef.current[id as InputId] !== 1)
            c.edges += 1;
          setInput(id as InputId, level as Bit);
        },
      },
      () => redraw((n) => n + 1),
    );
    return c;
  });
  clock.host.clockId = () => clockId;
  useEffect(() => () => clock.dispose(), [clock]);

  const notify = (text: string) => {
    setFlash(text);
    clearTimeout(flashTimer.current);
    flashTimer.current = setTimeout(() => setFlash(null), 2800);
  };

  /* ---------- смена упражнения: чистая доска, затем сохранённое решение ---------- */
  useEffect(() => {
    clock.stop();
    clock.set({ edges: 0 });
    lastStable.current = new Map();
    reported.current = false;
    setInputState(zeroInputs());
    inputRef.current = zeroInputs();
    setPassed(0);
    setHistory([]);
    setHintOpen(false);
    boardRef.current?.resetView?.();
    setInspectPath([]);
    setEditUnlocked(false);
    const sol = solvedBefore
      ? localSolutionStore.load(section.progressKey, ex.id)
      : undefined;
    setGates([]);
    setWires([]);
    setInstances([]);
    setBusWires([]);
    if (sol && isBlockSolution(sol)) {
      reserveUids([
        ...sol.instances.map((i) => i.id),
        ...sol.busWires.map((w) => w.id),
      ]);
      setInstances(sol.instances);
      setBusWires(sol.busWires);
    } else if (sol && isGateSolution(sol)) {
      reserveUids([
        ...sol.gates.map((g) => g.id),
        ...sol.wires.map((w) => w.id),
      ]);
      setGates(sol.gates);
      setWires(sol.wires);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ex.id, section.slug]);

  /* ---------- решено: запомнить схему, сообщить наверх ---------- */
  useEffect(() => {
    if (!solved || reported.current) return;
    reported.current = true;
    const sol = blocksMode ? { instances, busWires } : { gates, wires };
    localSolutionStore.save(section.progressKey, ex.id, sol);
    const p = loadProgress(section);
    if (!p.solved.has(index))
      saveProgress(section, new Set(p.solved).add(index), index);
    onSolved?.(JSON.stringify(sol));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [solved]);
  // схема решённого упражнения обновляется, если её переделали и она снова верна
  useEffect(() => {
    if (solved && reported.current)
      localSolutionStore.save(
        section.progressKey,
        ex.id,
        blocksMode ? { instances, busWires } : { gates, wires },
      );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [gates, wires, instances, busWires]);

  const toggleInput = (id: InputId) => {
    const next = (inputState[id] ^ 1) as Bit;
    if (id === clockId && next === 1) clock.edges += 1;
    setInputState((s) => ({ ...s, [id]: next }));
  };

  const reset = () => {
    clock.stop();
    setGates([]);
    setWires([]);
    setInstances([]);
    setBusWires([]);
    setInspectPath([]);
    setPassed(0);
    lastStable.current = new Map();
    reported.current = false;
  };

  /* ---------- блоки: палитра и «заглянуть внутрь» ---------- */
  const blockPalette = useMemo(
    () =>
      (ex.blocks ?? []).flatMap((id: string) => {
        const def = library.def(id);
        if (!def) return [];
        const ins = def.ports.filter((p) => p.dir === "in").map((p) => p.name);
        const outs = def.ports
          .filter((p) => p.dir === "out")
          .map((p) => p.name);
        return [
          {
            id,
            title: def.title,
            available: library.available(id),
            hint: library.lockHint(id),
            summary: `${ins.join(", ")} → ${outs.join(", ")}`,
          },
        ];
      }),
    [ex, library],
  );
  const addBlock = (blockId: string) => {
    if (!library.available(blockId)) {
      notify(`${library.lockHint(blockId)} — и блок откроется`);
      return;
    }
    setInstances((list) => {
      let n = list.length + 1;
      while (list.some((i) => i.id === `i${n}`)) n++;
      return [
        ...list,
        { id: `i${n}`, blockId, ...freeSpot(list, BLOCKS_BOARD_W) },
      ];
    });
  };
  const levels = useMemo(() => {
    if (!expansion) return [];
    const out: Level[] = [
      {
        title: ex.title,
        def: null,
        iface,
        solution: { instances, busWires },
        expansion,
        scope: valueAt,
      },
    ];
    for (const id of inspectPath) {
      const cur = out[out.length - 1];
      const sub = cur.expansion.subs.get(id);
      if (!sub) break;
      out.push({
        title: sub.def.title,
        def: sub.def,
        iface: sub.def,
        solution: sub.solution,
        expansion: sub.expansion,
        scope: childScope(cur.scope, cur.expansion, id, sub.def),
      });
    }
    return out;
  }, [expansion, ex, iface, instances, busWires, inspectPath, valueAt]);
  const current =
    inspectPath.length > 0 && levels.length > 1
      ? levels[levels.length - 1]
      : null;
  const inspectInto = (id: string) => (
    setInspectPath((p) => [...p, id]),
    setEditUnlocked(false)
  );
  const inspectTo = (n?: number) => (
    setInspectPath((p) => p.slice(0, n)),
    setEditUnlocked(false)
  );
  const toggleNode = (node: string) =>
    (ex.inputs as readonly string[]).includes(node) && toggleInput(node as InputId);

  /* ---------- палитра ---------- */
  const palette = useMemo(
    (): PaletteItem[] =>
      ex.allowed.map((type) => {
        const locked = !isGateUnlocked(type);
        return {
          type,
          locked,
          title: locked
            ? gateLockHint(type)
            : `${type} — ${RU_NAMES[type]}${COMPOSITE_GATES[type] ? " (составной)" : ""}`,
          label: `Добавить элемент ${type}, ${RU_NAMES[type]}`,
        };
      }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [ex, progressVersion],
  );
  const onLockedPick = (type: GateType) => {
    notify(`${gateLockHint(type)} — и элемент откроется`);
    setHintOpen(true);
  };

  const clk = clock;
  const clockLevel = clockId ? inputState[clockId] : 0;
  const labels = ex.labels ?? ex.inputs;
  const what = blocksMode ? "Соедините блоки шинами" : "Соберите схему";
  const hint = stepsMode
    ? `${what} и выполняйте шаги сценария — ${blocksMode ? "на вход подаётся такт" : "сигналы меняются тумблерами"}`
    : `${what} так, чтобы столбцы «Схема» совпали со столбцами «Цель»`;

  return (
    <div className="lab">
      <div className="lab-work">
        <div className="lab-card lab-board-card">
          <div className="lab-card-head">
            <div>
              <h3>Доска</h3>
              <p>{hint}</p>
            </div>
            <div className="lab-actions">
              {clockId && (
                <div
                  className="lab-clock"
                  role="group"
                  aria-label="Тактовый генератор"
                >
                  <button
                    type="button"
                    className="quiz-btn"
                    onClick={() => clk.tick()}
                    disabled={clk.ticking || clk.auto || clockLevel === 1}
                    title={
                      clockLevel === 1 && !clk.ticking && !clk.auto
                        ? "Сначала опустите CLK в 0"
                        : "Один такт: CLK поднимается в 1 и опускается в 0"
                    }
                  >
                    Такт ▸
                  </button>
                  <button
                    type="button"
                    className={`quiz-btn ghost ${clk.auto ? "running" : ""}`}
                    onClick={() => clk.toggleAuto()}
                    disabled={clk.ticking}
                    title="Автоматический генератор тактов"
                  >
                    {clk.auto ? "⏸ Пауза" : "▶ Авто"}
                  </button>
                  <select
                    value={clk.rate}
                    onChange={(e) => clk.setRate(Number(e.target.value))}
                    aria-label="Частота генератора"
                    title="Частота генератора"
                  >
                    {CLOCK_RATES.map((hz) => (
                      <option key={hz} value={hz}>
                        {hz} Гц
                      </option>
                    ))}
                  </select>
                  <span
                    className="lab-edges"
                    title="Сколько фронтов (0 → 1) подано с начала упражнения"
                  >
                    тактов: {clk.edges}
                  </span>
                </div>
              )}
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
                onClick={reset}
                title="Очистить доску"
              >
                Очистить
              </button>
            </div>
          </div>
          {hintOpen && (
            <p className="ex-hint">
              {ex.hint}
              {palette
                .filter((p) => p.locked)
                .map((p) => (
                  <span key={p.type} className="lab-lock-hint">
                    <br />
                    🔒 {p.title}
                  </span>
                ))}
            </p>
          )}
          {blocksMode && (
            <div
              className="lab-blocks"
              role="toolbar"
              aria-label="Блоки: кликните, чтобы добавить на доску"
            >
              {blockPalette.map((b) => (
                <button
                  key={b.id}
                  type="button"
                  className={`lab-block-item ${b.available ? "" : "locked"}`}
                  title={b.available ? b.summary : b.hint}
                  onClick={() => addBlock(b.id)}
                >
                  <span className="lab-block-name">
                    {b.available ? "" : "🔒 "}
                    {b.title}
                  </span>
                  <span className="lab-block-sub">
                    {b.available ? b.summary : b.hint}
                  </span>
                </button>
              ))}
            </div>
          )}
          <div className="lab-board-wrap">
            {blocksMode ? (
              current ? (
                <div className="lab-inspector">
                  <div className="lab-inspector-bar">
                    <nav className="lab-crumbs" aria-label="Где вы находитесь">
                      {levels.map((lvl, i) =>
                        i === levels.length - 1 ? (
                          <strong key={i}>{lvl.title}</strong>
                        ) : (
                          <span key={i}>
                            <button
                              type="button"
                              className="lab-crumb"
                              onClick={() => inspectTo(i)}
                            >
                              {lvl.title}
                            </button>
                            <span className="lab-crumb-sep"> › </span>
                          </span>
                        ),
                      )}
                    </nav>
                    <div className="lab-actions">
                      <button
                        type="button"
                        className="quiz-btn ghost"
                        onClick={() => inspectTo(inspectPath.length - 1)}
                      >
                        ← Назад
                      </button>
                      {current.def?.source && onOpenSource && (
                        <button
                          type="button"
                          className="quiz-btn ghost"
                          onClick={() => setEditUnlocked((v) => !v)}
                          title="Схему блока меняют в упражнении, где вы её собрали"
                        >
                          {editUnlocked
                            ? "🔓 Редактирование разрешено"
                            : "🔒 Только просмотр"}
                        </button>
                      )}
                    </div>
                  </div>
                  {editUnlocked && current.def?.source && onOpenSource && (
                    <div className="lab-inspector-edit">
                      <p>
                        Схему блока меняют в упражнении, где вы её собрали:
                        изменённое решение должно по-прежнему проходить
                        проверку. Пока оно не решено, блок работает по последней
                        верной версии.
                      </p>
                      <button
                        type="button"
                        className="quiz-btn"
                        onClick={() => onOpenSource(current.def!.source!)}
                      >
                        Открыть в редакторе →
                      </button>
                    </div>
                  )}
                  {current.solution && isBlockSolution(current.solution) ? (
                    <BlockBoard
                      iface={current.iface}
                      library={library}
                      instances={current.solution.instances}
                      setInstances={() => {}}
                      busWires={current.solution.busWires}
                      setBusWires={() => {}}
                      expansion={current.expansion}
                      scope={current.scope}
                      readonly
                      fullscreen={fullscreen}
                      onInspect={inspectInto}
                      resetKey={inspectPath.join("/")}
                    />
                  ) : current.solution && isGateSolution(current.solution) ? (
                    <CircuitView
                      gates={current.solution.gates}
                      wires={current.solution.wires}
                      iface={current.iface}
                      scope={current.scope}
                      fullscreen={fullscreen}
                      resetKey={inspectPath.join("/")}
                    />
                  ) : null}
                </div>
              ) : (
                <BlockBoard
                  iface={iface}
                  library={library}
                  instances={instances}
                  setInstances={setInstances}
                  busWires={busWires}
                  setBusWires={setBusWires}
                  expansion={expansion}
                  scope={valueAt}
                  clockNode={clockId}
                  onToggle={toggleNode}
                  onInspect={inspectInto}
                  onMessage={notify}
                  boardRef={boardRef}
                  fullscreen={fullscreen}
                  resetKey={ex.id}
                />
              )
            ) : (
              <GateBoard
                gates={gates}
                setGates={setGates}
                wires={wires}
                setWires={setWires}
                circuit={circuit}
                inputs={ex.inputs}
                labels={labels}
                outputs={ex.outputs}
                inputState={inputState}
                clockId={clockId}
                stepsMode={stepsMode}
                valueFn={valueAt}
                palette={palette}
                guideFocus={null}
                fullscreen={fullscreen}
                onToggleInput={toggleInput}
                onEdited={() => {}}
                onMessage={notify}
                onLockedPick={onLockedPick}
                boardRef={boardRef}
              />
            )}
            {flash && (
              <div className="lab-flash" role="alert">
                {flash}
              </div>
            )}
          </div>
        </div>

        <CheckPanel
          exercise={ex}
          inputState={inputState}
          valueAt={valueAt}
          passedSteps={passed}
          solved={solved}
          matched={matched}
          tableRows={tableRows}
          currentRow={currentRow}
        />
      </div>

      {solved && (
        <ResultAlert
          title={
            <>
              {stepsMode
                ? "Схема работает как надо!"
                : `Схема работает — ${matched} из ${ex.target.length}!`}{" "}
              Формула: <strong>{ex.formula}</strong>
            </>
          }
          onNext={hasNext ? onNext : undefined}
          nextLabel={nextLabel}
        >
          {ex.success}
        </ResultAlert>
      )}

      {stepsMode && <WaveDiagram wave={wave} onClear={() => setHistory([])} />}
    </div>
  );
}
