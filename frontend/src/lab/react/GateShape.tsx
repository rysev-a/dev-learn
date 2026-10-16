import { GATE_W } from "../exercises/logic-gates/circuit.model.ts";
import { gateBodyPath, gateBubbleCx, gateExtraArc } from "../exercises/logic-gates/gate-shapes.ts";
import type { GateType } from "../exercises/logic-gates/circuit.model.ts";

/** Контур вентиля: тело, дополнительная дуга (XOR), кружок инверсии и (по умолчанию) подпись типа */
export default function GateShape({ type, label = true }: { type: GateType; label?: boolean }) {
  const bubble = gateBubbleCx(type);
  const arc = gateExtraArc(type);
  return (
    <>
      <path className="gate-body" d={gateBodyPath(type)} />
      {arc && <path className="gate-extra" d={arc} />}
      {bubble !== null && <circle className="gate-bubble" cx={bubble} cy="24" r="5" />}
      {label && (
        <text className={`gate-label ${type === "NOT" ? "small" : ""}`} x={type === "NOT" ? 13 : GATE_W / 2} y="29">
          {type}
        </text>
      )}
    </>
  );
}
