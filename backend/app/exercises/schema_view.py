"""Схема и данные учебной базы SQL-задачи: таблицы, столбцы, ключи, связи и строки.

Клиент рисует по ним ERD-диаграмму и показывает содержимое таблиц. Базу собирает тот же
`setup`, что и песочница, но здесь, в памяти бэкенда: определения задач написаны нами,
а ученик в этом процессе ничего не исполняет."""

import hashlib
import sqlite3

MAX_ROWS = 100  # строк таблицы, которые уходят клиенту


def dataset_key(setup: str) -> str:
    return hashlib.sha1(setup.encode("utf-8")).hexdigest()[:12]


def _value(v):
    if isinstance(v, bytes):
        return v.hex()
    return v


def describe(setup: str) -> dict:
    """{tables: [{name, kind, columns: [{name, type, pk, notnull}], rows, total}], relations: [...]}"""
    con = sqlite3.connect(":memory:")
    try:
        con.executescript(setup)
        rows = con.execute(
            "SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view') "
            "AND name NOT LIKE 'sqlite_%' ORDER BY type DESC, rowid"
        ).fetchall()
        tables, relations = [], []
        pk_of: dict[str, str] = {}
        info: dict[str, list] = {}
        for name, _ in rows:
            cols = con.execute(f'PRAGMA table_info("{name}")').fetchall()
            info[name] = cols
            pks = [c for c in cols if c[5]]
            if pks:
                pk_of[name] = sorted(pks, key=lambda c: c[5])[0][1]
        for name, kind in rows:
            cols = info[name]
            fks = {}
            if kind == "table":
                for fk in con.execute(f'PRAGMA foreign_key_list("{name}")').fetchall():
                    # id, seq, table, from, to, on_update, on_delete, match
                    to_col = fk[4] or pk_of.get(fk[2]) or "id"
                    fks[fk[3]] = (fk[2], to_col)
                    relations.append(
                        {"from": name, "from_col": fk[3], "to": fk[2], "to_col": to_col}
                    )
            data = con.execute(f'SELECT * FROM "{name}" LIMIT {MAX_ROWS}').fetchall()
            total = con.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
            tables.append(
                {
                    "name": name,
                    "kind": kind,
                    "columns": [
                        {
                            "name": c[1],
                            "type": c[2] or "",
                            "pk": bool(c[5]),
                            "notnull": bool(c[3]),
                            "fk": fks.get(c[1]) and {"table": fks[c[1]][0], "column": fks[c[1]][1]},
                        }
                        for c in cols
                    ],
                    "rows": [[_value(v) for v in r] for r in data],
                    "total": total,
                }
            )
        return {"tables": tables, "relations": relations}
    finally:
        con.close()


_cache: dict[str, dict] = {}


def dataset(setup: str) -> dict:
    key = dataset_key(setup)
    if key not in _cache:
        _cache[key] = describe(setup)
    return _cache[key]
