import { useMemo, useState } from "react";
import {
BlockSolution,
  childScope,
  GateSolution,
  isBlockSolution,
  isGateSolution,
  isNativeSolution,
} from "../exercises/logic-gates/blocks.ts";
import { CPU8_BLOCKS, cpu8Library } from "../cpu8/blocks.ts";
import BlockBoard from "./BlockBoard.tsx";
import CircuitView from "./CircuitView.tsx";

/* «Устройство процессора»: схема процессора из блоков, в которую можно спускаться вплоть до отдельных
   вентилей. Значения на проводах — живые, по текущему такту. */

const boardHeight = (s: BlockSolution) => Math.max(560, ...s.instances.map((i) => i.y + 290));
const spreadFor = (s: BlockSolution) =>
  s.instances.length > 8 ? 1.7 : s.instances.length > 3 ? 1.4 : 1.2;
const spreadForGates = (g: GateSolution) =>
  g.gates.length > 40
    ? 1.9
    : g.gates.length > 20
      ? 1.6
      : g.gates.length > 8
        ? 1.35
        : 1.15;

export default function CpuInspector({ machine, version }) {
  const [path, setPath] = useState([]);
  const scope = useMemo(
    () => (node: any) => machine.sim.get(node),
    [machine, version],
  ); // eslint-disable-line react-hooks/exhaustive-deps

  const levels = useMemo(() => {
    const cpu = CPU8_BLOCKS.get("c8-cpu");
    const out = [
      {
        title: cpu.def.title,
        def: cpu.def,
        iface: cpu.def,
        solution: cpu.solution,
        expansion: machine.expansion,
        scope,
      },
    ];
    for (const id of path) {
      const cur = out[out.length - 1];
      const sub = cur.expansion.subs.get(id);
      if (!sub) break;
      out.push({
        title: `${sub.def.title} (${id})`,
        def: sub.def,
        iface: sub.def,
        solution: sub.solution,
        expansion: sub.expansion,
        scope: childScope(cur.scope, cur.expansion, id, sub.def),
      });
    }
    return out;
  }, [machine, path, scope]);
  const current = levels[levels.length - 1];
  const stats = useMemo(() => {
    const c = current.expansion.circuit;
    const dffs = c.gates.filter((g) => g.type === "DFF").length;
    return { gates: c.gates.length - dffs, dffs };
  }, [current]);
  const sol = current.solution;
  const key = `${machine === undefined ? "" : "m"}:${path.join("/")}`;

  return (
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
                  onClick={() => setPath((p) => p.slice(0, i))}
                >
                  {lvl.title}
                </button>
                <span className="lab-crumb-sep"> › </span>
              </span>
            ),
          )}
        </nav>
        <div className="lab-actions">
          <span className="lab-edges">
            внутри: {stats.gates} вентилей, {stats.dffs} триггеров
          </span>
          {path.length > 0 && (
            <button
              type="button"
              className="quiz-btn ghost"
              onClick={() => setPath((p) => p.slice(0, -1))}
            >
              ← Назад
            </button>
          )}
        </div>
      </div>
      {isBlockSolution(sol) ? (
        <BlockBoard
          iface={current.iface}
          library={cpu8Library}
          instances={sol.instances}
          setInstances={() => {}}
          busWires={sol.busWires}
          setBusWires={() => {}}
          expansion={current.expansion}
          scope={current.scope}
          readonly
          height={boardHeight(sol)}
          spread={spreadFor(sol)}
          onInspect={(id: any) => setPath((p) => [...p, id])}
          resetKey={key}
        />
      ) : isGateSolution(sol) ? (
        <CircuitView
          gates={sol.gates}
          wires={sol.wires}
          iface={current.iface}
          scope={current.scope}
          spread={spreadForGates(sol)}
          resetKey={key}
        />
      ) : isNativeSolution(sol) ? (
        <p className="lab-native">
          Это встроенная память: ячейки здесь не из вентилей — как настоящая
          микросхема, у неё есть адрес, данные и (у диска) запись по такту.
          Содержимое — на карточке «Виртуальный диск» выше (для программы — в
          машинном коде слева).
        </p>
      ) : null}
    </div>
  );
}
