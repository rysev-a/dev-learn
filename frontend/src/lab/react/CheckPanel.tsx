import { inputsForRow } from "../exercises/logic-gates/circuit.model.ts";

/* Проверка решения: таблица истинности или сценарий по шагам (для защёлок и регистров) */
export default function CheckPanel({
  exercise: ex,
  inputState,
  valueAt,
  passedSteps,
  solved,
  matched,
  tableRows,
  currentRow,
}) {
  const labels = ex.labels ?? ex.inputs;
  const labelOf = (id: any) => labels[ex.inputs.indexOf(id)] ?? id;
  if (ex.mode === "steps") {
    const total = ex.steps?.length ?? 0;
    return (
      <div className="lab-card">
        <div className="lab-card-head">
          <div>
            <h3>Сценарий проверки</h3>
            <p>
              Выполняйте шаги по порядку: устанавливайте тумблеры и добивайтесь
              нужных значений на выходах
            </p>
          </div>
          <span className={`lab-badge ${solved ? "ok" : ""}`}>
            Шаг {Math.min(passedSteps + 1, total)} / {total}
          </span>
        </div>
        <div className="lab-steps">
          {ex.steps.map((st, i) => (
            <div
              key={i}
              className={`lab-step ${i < passedSteps ? "done" : ""} ${i === passedSteps ? "active" : ""}`}
            >
              <span className="lab-step-no">
                {i < passedSteps ? "✓" : i + 1}
              </span>
              <div>
                <p className="lab-step-text">{st.text}</p>
                <div className="lab-step-req">
                  {st.pulses > 1 && (
                    <span className="lab-chip pulses">тактов: {st.pulses}</span>
                  )}
                  {ex.inputs.map((id) => (
                    <span
                      key={id}
                      className={`lab-chip ${inputState[id] === st.inputs[id] ? "hit" : ""}`}
                    >
                      {labelOf(id)} = {st.inputs[id]}
                    </span>
                  ))}
                  <span className="lab-chip-sep">→</span>
                  {ex.outputs.map(
                    (o) =>
                      st.expect[o] !== undefined && (
                        <span
                          key={o}
                          className={`lab-chip out ${valueAt(o) === st.expect[o] ? "hit" : ""}`}
                        >
                          {o} = {st.expect[o]}
                        </span>
                      ),
                  )}
                  {ex.outputs.every((o: string|number) => st.expect[o] === undefined) && (
                    <span className="lab-chip out hit">
                      выход пока не проверяется
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }
  return (
    <div className="lab-card">
      <div className="lab-card-head">
        <h3 title="Строка с подсветкой — текущее положение тумблеров на доске">
          Таблица истинности
        </h3>
        <span className={`lab-badge ${solved ? "ok" : ""}`}>
          {matched} / {ex.target.length}
        </span>
      </div>
      <div className="lab-tt-scroll">
        <table className="lab-tt">
          <thead>
            <tr>
              {labels.map((l, i) => (
                <th key={i}>{l}</th>
              ))}
              {ex.outputs.map((o) => (
                <th key={o} className="sep">
                  Цель {o}
                </th>
              ))}
              {ex.outputs.map((o) => (
                <th key={`a${o}`}>Схема {o}</th>
              ))}
              <th />
            </tr>
          </thead>
          <tbody>
            {tableRows.map((row, i) => {
              const st = inputsForRow(ex.inputs, i);
              return (
                <tr key={i} className={i === currentRow ? "current" : ""}>
                  {ex.inputs.map((id) => (
                    <td key={id} className="in">
                      {st[id]}
                    </td>
                  ))}
                  {row.targets.map((t, k) => (
                    <td key={k} className="sep target">
                      {t}
                    </td>
                  ))}
                  {row.actuals.map((a, k) => (
                    <td
                      key={k}
                      className={`actual ${a === row.targets[k] ? "ok" : a !== undefined ? "bad" : "na"}`}
                    >
                      {a === undefined ? "—" : a}
                    </td>
                  ))}
                  <td className="mark">
                    {row.actuals[0] === undefined ? (
                      <span className="na-mark">·</span>
                    ) : row.ok ? (
                      <span className="ok-mark">✓</span>
                    ) : (
                      <span className="bad-mark">✕</span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
