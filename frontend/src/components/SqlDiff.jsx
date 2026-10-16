/* Сравнение результата SQL-запроса с эталоном: слева результат ученика, справа верный.
   Отличающиеся значения подсвечены в обеих таблицах, лишние и недостающие строки помечены,
   у столбцов, которых не хватает или которые лишние, подсвечены заголовки.

   Проверка на сервере сравнивает значения по позиции (имена столбцов не важны), поэтому и
   здесь сопоставление идёт по позициям; различие имён показано мягко. */

const key = (row) => JSON.stringify(row);
const same = (a, b) => a === b || (a == null && b == null);

// Сопоставление строк: для каждой строки результата и эталона — статус и «пара» для поячеечной подсветки
function align(got, exp, ordered) {
  const gs = got.map(() => ({ st: "ok", pair: null }));
  const es = exp.map(() => ({ st: "ok", pair: null }));
  if (ordered) {
    const n = Math.min(got.length, exp.length);
    for (let i = 0; i < n; i++) {
      if (key(got[i]) !== key(exp[i])) {
        gs[i] = { st: "diff", pair: i };
        es[i] = { st: "diff", pair: i };
      }
    }
    for (let i = n; i < got.length; i++) gs[i] = { st: "extra", pair: null };
    for (let i = n; i < exp.length; i++) es[i] = { st: "missing", pair: null };
    return { gs, es };
  }
  // без порядка: сначала убираем совпавшие строки (с учётом повторов), остаток парим по очереди
  const pool = new Map();
  exp.forEach((r, i) => {
    const k = key(r);
    if (!pool.has(k)) pool.set(k, []);
    pool.get(k).push(i);
  });
  const extraIdx = [];
  got.forEach((r, i) => {
    const k = key(r);
    const list = pool.get(k);
    if (list && list.length) list.shift();
    else extraIdx.push(i);
  });
  const missingIdx = [];
  for (const list of pool.values()) missingIdx.push(...list);
  missingIdx.sort((a, b) => a - b);
  const n = Math.min(extraIdx.length, missingIdx.length);
  for (let k = 0; k < n; k++) {
    gs[extraIdx[k]] = { st: "diff", pair: missingIdx[k] };
    es[missingIdx[k]] = { st: "diff", pair: extraIdx[k] };
  }
  for (let k = n; k < extraIdx.length; k++)
    gs[extraIdx[k]] = { st: "extra", pair: null };
  for (let k = n; k < missingIdx.length; k++)
    es[missingIdx[k]] = { st: "missing", pair: null };
  return { gs, es };
}

const show = (v) => (v === null || v === undefined ? "NULL" : String(v));

function Table({
  title,
  total,
  shown,
  cols,
  width,
  rows,
  status,
  other,
  side,
}) {
  return (
    <div className={`sd-side ${side}`}>
      <div className="sd-title">
        <span className="s-label">{title}</span>
        <span className="sd-count">
          {total} {total === 1 ? "строка" : "строк"}
        </span>
      </div>
      <div className="sd-scroll">
        <table className="sd-t">
          <thead>
            <tr>
              <th className="sd-n">#</th>
              {Array.from({ length: width }, (_, j) => {
                const name = cols[j];
                const lack = j >= (side === "got" ? other.width : other.width);
                return (
                  <th
                    key={j}
                    className={
                      lack ? (side === "got" ? "extra" : "missing") : ""
                    }
                    title={
                      lack
                        ? side === "got"
                          ? "лишний столбец"
                          : "этого столбца нет в вашем результате"
                        : undefined
                    }
                  >
                    {name ?? `col${j + 1}`}
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 && (
              <tr>
                <td className="sd-empty" colSpan={width + 1}>
                  пусто
                </td>
              </tr>
            )}
            {rows.map((r, i) => {
              const s = status[i];
              const peer = s.pair != null ? other.rows[s.pair] : null;
              return (
                <tr key={i} className={`sd-${s.st}`}>
                  <td className="sd-n">{i + 1}</td>
                  {Array.from({ length: width }, (_, j) => {
                    const v = r[j];
                    let cls = "";
                    if (s.st === "extra" || s.st === "missing") cls = s.st;
                    else if (s.st === "diff") {
                      const pv = peer ? peer[j] : undefined;
                      if (j >= (peer ? peer.length : 0) || !same(v, pv))
                        cls = side === "got" ? "extra" : "missing";
                    }
                    return (
                      <td
                        key={j}
                        className={`${cls} ${typeof v === "number" ? "num" : ""}`}
                      >
                        {j < r.length ? show(v) : ""}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      {total > shown && (
        <p className="sd-more">
          Показаны первые {shown} из {total} строк.
        </p>
      )}
    </div>
  );
}

export default function SqlDiff({ r }) {
  const gotRows = r.got_rows || [];
  const expRows = r.exp_rows || [];
  const gotCols = r.got_cols || [];
  const expCols =
    r.exp_cols && r.exp_cols.length ? r.exp_cols : gotCols.length ? [] : [];
  const gw = Math.max(gotCols.length, ...gotRows.map((x) => x.length), 0);
  const ew = Math.max(expCols.length, ...expRows.map((x) => x.length), 0);
  const width = Math.max(gw, ew);
  const { gs, es } = align(gotRows, expRows, !!r.ordered);

  const extra = gs.filter((s) => s.st === "extra").length;
  const missing = es.filter((s) => s.st === "missing").length;
  const diff = gs.filter((s) => s.st === "diff").length;

  // мягкое различие имён: проверка имён не делает, но ученику полезно увидеть
  const renamed =
    expCols.length > 0 &&
    gotCols.length === expCols.length &&
    gotCols.some(
      (c, j) => String(c).toLowerCase() !== String(expCols[j]).toLowerCase(),
    );

  const parts = [];
  if (gw !== ew)
    parts.push(
      gw > ew
        ? `столбцов у вас больше: ${gw} вместо ${ew}`
        : `не хватает столбцов: ${gw} вместо ${ew}`,
    );
  if (r.got_total !== r.exp_total)
    parts.push(`строк у вас ${r.got_total}, ожидается ${r.exp_total}`);
  if (diff) parts.push(`отличается строк: ${diff}`);
  if (extra) parts.push(`лишних строк: ${extra}`);
  if (missing) parts.push(`не хватает строк: ${missing}`);
  if (r.ordered) parts.push("порядок строк важен");

  return (
    <div className="sd">
      {parts.length > 0 && <p className="sd-sum">{parts.join(" · ")}</p>}
      <div className="sd-grid">
        <Table
          side="got"
          title="ваш результат"
          total={r.got_total ?? gotRows.length}
          shown={gotRows.length}
          cols={gotCols}
          width={width}
          rows={gotRows}
          status={gs}
          other={{ rows: expRows, width: ew }}
        />
        <Table
          side="exp"
          title="верный результат"
          total={r.exp_total ?? expRows.length}
          shown={expRows.length}
          cols={expCols.length ? expCols : gotCols}
          width={width}
          rows={expRows}
          status={es}
          other={{ rows: gotRows, width: gw }}
        />
      </div>
      <p className="sd-legend">
        <span className="sd-key extra" /> лишнее или неверное значение у вас
        <span className="sd-key missing" /> чего не хватает или что должно быть
        {renamed && (
          <span className="sd-note">
            Имена столбцов отличаются от эталона — проверка их не учитывает.
          </span>
        )}
      </p>
    </div>
  );
}
