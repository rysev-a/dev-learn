//! Схема и данные учебной базы SQL-задачи: таблицы, столбцы, ключи, связи и строки (как `exercises/schema_view.py`).
//! Базу собирает тот же `setup`, что и песочница, но здесь, в памяти: определения задач написаны нами.

use rusqlite::{types::ValueRef, Connection};
use serde_json::{json, Value};
use sha2::{Digest, Sha256};

const MAX_ROWS: i64 = 100;

pub fn dataset_key(setup: &str) -> String {
    Sha256::digest(setup.as_bytes()).iter().map(|b| format!("{b:02x}")).collect::<String>()[..12].to_string()
}

fn cell(v: ValueRef) -> Value {
    match v {
        ValueRef::Null => Value::Null,
        ValueRef::Integer(n) => json!(n),
        ValueRef::Real(f) => serde_json::Number::from_f64(f).map_or(Value::Null, Value::Number),
        ValueRef::Text(t) => Value::String(String::from_utf8_lossy(t).into_owned()),
        ValueRef::Blob(b) => Value::String(b.iter().map(|x| format!("{x:02x}")).collect()),
    }
}

/// `{tables: [{name, kind, columns: [{name, type, pk, notnull, fk}], rows, total}], relations: [...]}`
pub fn describe(setup: &str) -> anyhow::Result<Value> {
    let con = Connection::open_in_memory()?;
    // учебные базы заполняются в порядке «как удобно читать», а не по внешним ключам; песочница (sqlite3) их не проверяет
    con.execute_batch("PRAGMA foreign_keys = OFF")?;
    con.execute_batch(setup)?;
    let mut st = con.prepare("SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%' ORDER BY type DESC, rowid")?;
    let objects: Vec<(String, String)> = st.query_map([], |r| Ok((r.get(0)?, r.get(1)?)))?.collect::<Result<_, _>>()?;

    struct Col {
        name: String,
        typ: String,
        notnull: bool,
        pk: i64,
    }
    let mut info: Vec<Vec<Col>> = Vec::new();
    let mut pk_of: std::collections::HashMap<String, String> = std::collections::HashMap::new();
    for (name, _) in &objects {
        let mut st = con.prepare(&format!("PRAGMA table_info(\"{name}\")"))?;
        let cols: Vec<Col> = st
            .query_map([], |r| Ok(Col { name: r.get(1)?, typ: r.get::<_, Option<String>>(2)?.unwrap_or_default(), notnull: r.get::<_, i64>(3)? != 0, pk: r.get(5)? }))?
            .collect::<Result<_, _>>()?;
        if let Some(first) = cols.iter().filter(|c| c.pk > 0).min_by_key(|c| c.pk) {
            pk_of.insert(name.clone(), first.name.clone());
        }
        info.push(cols);
    }
    let (mut tables, mut relations) = (Vec::new(), Vec::new());
    for ((name, kind), cols) in objects.iter().zip(&info) {
        let mut fks: std::collections::HashMap<String, (String, String)> = std::collections::HashMap::new();
        if kind == "table" {
            let mut st = con.prepare(&format!("PRAGMA foreign_key_list(\"{name}\")"))?;
            let rows: Vec<(String, String, Option<String>)> = st.query_map([], |r| Ok((r.get(2)?, r.get(3)?, r.get(4)?)))?.collect::<Result<_, _>>()?;
            for (to_table, from, to) in rows {
                let to_col = to.filter(|t| !t.is_empty()).or_else(|| pk_of.get(&to_table).cloned()).unwrap_or_else(|| "id".into());
                relations.push(json!({ "from": name, "from_col": from, "to": to_table, "to_col": to_col }));
                fks.insert(from, (to_table, to_col));
            }
        }
        let mut st = con.prepare(&format!("SELECT * FROM \"{name}\" LIMIT {MAX_ROWS}"))?;
        let width = st.column_count();
        let rows: Vec<Value> = st
            .query_map([], |r| Ok(Value::Array((0..width).map(|n| r.get_ref(n).map(cell)).collect::<Result<Vec<_>, _>>()?)))?
            .collect::<Result<_, _>>()?;
        let total: i64 = con.query_row(&format!("SELECT COUNT(*) FROM \"{name}\""), [], |r| r.get(0))?;
        tables.push(json!({
            "name": name, "kind": kind,
            "columns": cols.iter().map(|c| json!({
                "name": c.name, "type": c.typ, "pk": c.pk > 0, "notnull": c.notnull,
                "fk": fks.get(&c.name).map(|(t, col)| json!({ "table": t, "column": col })),
            })).collect::<Vec<_>>(),
            "rows": rows, "total": total,
        }));
    }
    Ok(json!({ "tables": tables, "relations": relations }))
}
