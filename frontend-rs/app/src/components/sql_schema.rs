//! Виджет «База данных» в SQL-упражнении: ERD-диаграмма (таблицы можно перетаскивать, связи подсвечиваются при наведении)
//! и просмотр данных таблиц. Схема приходит с сервером вместе с задачами главы (`ChapterTasks::datasets`).
//!
//! Раскладка, геометрия связей и подписи — чистые функции вверху файла (с тестами); компоненты только связывают их с сигналами.

use std::{collections::HashMap, sync::Arc};

use api::dto::{SqlDataset, SqlRelation, SqlTable};
use leptos::prelude::*;
use serde_json::Value;
use wasm_bindgen::JsCast;

use crate::settings;

const BOX_W: f64 = 176.0;
const HEAD_H: f64 = 24.0;
const ROW_H: f64 = 19.0;
const GAP_X: f64 = 96.0;
const GAP_Y: f64 = 22.0;
const PAD: f64 = 16.0;
/// Запас справа от самой правой таблицы: сюда заходят петли связей.
const MARGIN_RIGHT: f64 = 40.0;
/// Таблицу нельзя утащить ближе к краю холста.
const MIN_POS: f64 = 4.0;
/// Сдвиг меньше этого — клик (открывает данные таблицы), а не перетаскивание.
const CLICK_SLOP: f64 = 3.0;

const KEY_OPEN: &str = "say-sx-open";
const KEY_VIEW: &str = "say-sx-view";

// --- чистая логика ------------------------------------------------------------------------------

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Point {
    pub x: f64,
    pub y: f64,
}

/// Положения таблиц на холсте по именам.
pub type Layout = HashMap<String, Point>;

fn box_h(t: &SqlTable) -> f64 {
    HEAD_H + t.columns.len() as f64 * ROW_H + 6.0
}

/// Начальная раскладка: родители (на кого ссылаются) слева, дети справа; внутри колонки — в порядке таблиц схемы.
pub fn auto_layout(schema: &SqlDataset) -> Layout {
    let mut level: HashMap<&str, usize> = schema.tables.iter().map(|t| (t.name.as_str(), 0)).collect();
    for _ in 0..schema.tables.len() {
        for r in schema.relations.iter().filter(|r| r.from != r.to) {
            if let Some(parent) = level.get(r.to.as_str()).copied() {
                if let Some(child) = level.get_mut(r.from.as_str()) {
                    *child = (*child).max(parent + 1);
                }
            }
        }
    }
    let mut columns: std::collections::BTreeMap<usize, Vec<&SqlTable>> = Default::default();
    for t in &schema.tables {
        columns.entry(level[t.name.as_str()]).or_default().push(t);
    }
    let mut out = Layout::new();
    for (lv, tables) in columns {
        let mut y = PAD;
        for t in tables {
            out.insert(t.name.clone(), Point { x: PAD + lv as f64 * (BOX_W + GAP_X), y });
            y += box_h(t) + GAP_Y;
        }
    }
    out
}

/// Размер области viewBox: все таблицы с полями и запасом справа.
pub fn canvas_size(tables: &[SqlTable], layout: &Layout) -> (f64, f64) {
    let right = layout.values().map(|p| p.x).fold(0.0, f64::max) + BOX_W + PAD;
    let bottom = tables.iter().map(|t| layout.get(&t.name).map_or(0.0, |p| p.y) + box_h(t)).fold(0.0, f64::max) + PAD;
    (right + MARGIN_RIGHT, bottom)
}

/// Стиль `<svg>`: растягивается по ширине, но не мельче трёх четвертей и не крупнее натурального размера.
fn svg_style(width: f64) -> String {
    format!("width: 100%; min-width: {}px; max-width: {width}px; height: auto;", (width * 0.75).round())
}

/// Связь на холсте: кривая и места подписей «N» (у ребёнка) и «1» (у родителя).
#[derive(Clone, Debug, PartialEq)]
pub struct Link {
    pub d: String,
    pub child: Point,
    pub parent: Point,
}

/// Кривая связи от столбца ребёнка (`from`, `ya` — высота столбца на холсте) к столбцу родителя (`to`, `yb`).
/// Таблицы рядом — дуга между ними; друг над другом — обход справа; ссылка таблицы на себя — петля справа.
pub fn link_geometry(from: Point, ya: f64, to: Point, yb: f64, same_table: bool) -> Link {
    if same_table {
        let x = from.x + BOX_W;
        return Link { d: format!("M{x},{ya} C{},{ya} {},{yb} {x},{yb}", x + 46.0, x + 46.0), child: Point { x: x + 8.0, y: ya }, parent: Point { x: x + 8.0, y: yb } };
    }
    if from.x >= to.x + BOX_W {
        let (x1, x2) = (from.x, to.x + BOX_W);
        let k = ((x1 - x2) / 2.0).max(30.0);
        return Link { d: format!("M{x1},{ya} C{},{ya} {},{yb} {x2},{yb}", x1 - k, x2 + k), child: Point { x: x1 - 10.0, y: ya }, parent: Point { x: x2 + 10.0, y: yb } };
    }
    if to.x >= from.x + BOX_W {
        let (x1, x2) = (from.x + BOX_W, to.x);
        let k = ((x2 - x1) / 2.0).max(30.0);
        return Link { d: format!("M{x1},{ya} C{},{ya} {},{yb} {x2},{yb}", x1 + k, x2 - k), child: Point { x: x1 + 10.0, y: ya }, parent: Point { x: x2 - 10.0, y: yb } };
    }
    let bulge = from.x.max(to.x) + BOX_W + 50.0;
    Link {
        d: format!("M{},{ya} C{bulge},{ya} {bulge},{yb} {},{yb}", from.x + BOX_W, to.x + BOX_W),
        child: Point { x: from.x + BOX_W + 10.0, y: ya },
        parent: Point { x: to.x + BOX_W + 10.0, y: yb },
    }
}

/// Высота столбца внутри таблицы (от её верха); `None` — такого столбца нет.
fn column_offset(t: &SqlTable, column: &str) -> Option<f64> {
    t.columns.iter().position(|c| c.name == column).map(|i| HEAD_H + i as f64 * ROW_H + ROW_H / 2.0)
}

/// Таблица подсвечена как «связанная», если на неё и на наведённую таблицу есть общая связь.
fn is_linked(relations: &[SqlRelation], hovered: Option<&str>, name: &str) -> bool {
    hovered.is_some_and(|h| relations.iter().any(|r| (r.from == h && r.to == name) || (r.to == h && r.from == name)))
}

fn table_class(is_view: bool, hovered: bool, linked: bool) -> String {
    let mut class = String::from("sx-tbl");
    for (on, name) in [(is_view, "view"), (hovered, "on"), (linked, "linked")] {
        if on {
            class.push(' ');
            class.push_str(name);
        }
    }
    class
}

/// Перетаскиваемая таблица: смещение указателя внутри неё и признак «сдвинули».
#[derive(Clone, Debug, PartialEq)]
struct Drag {
    name: String,
    dx: f64,
    dy: f64,
    moved: bool,
}

impl Drag {
    /// Начало перетаскивания: указатель `pointer` над таблицей, стоящей в `at`.
    fn start(name: &str, pointer: Point, at: Point) -> Self {
        Drag { name: name.to_string(), dx: pointer.x - at.x, dy: pointer.y - at.y, moved: false }
    }

    /// Новое место таблицы для указателя `pointer`; запоминает, что таблицу действительно сдвинули.
    fn to(&mut self, pointer: Point, current: Point) -> Point {
        let next = Point { x: (pointer.x - self.dx).max(MIN_POS), y: (pointer.y - self.dy).max(MIN_POS) };
        if (next.x - current.x).abs() + (next.y - current.y).abs() > CLICK_SLOP {
            self.moved = true;
        }
        next
    }
}

/// «1 таблица», «2 таблицы», «5 таблиц», «21 таблица».
pub fn plural(n: usize, one: &'static str, few: &'static str, many: &'static str) -> &'static str {
    match (n % 10, n % 100) {
        (_, 11..=14) => many,
        (1, _) => one,
        (2..=4, _) => few,
        _ => many,
    }
}

/// Подпись в заголовке виджета: «5 таблиц · 2 представл.».
fn summary(schema: &SqlDataset) -> String {
    let tables = schema.tables.iter().filter(|t| !t.is_view()).count();
    let views = schema.tables.len() - tables;
    let base = format!("{tables} {}", plural(tables, "таблица", "таблицы", "таблиц"));
    if views > 0 {
        format!("{base} · {views} представл.")
    } else {
        base
    }
}

/// Значение ячейки как текст: `NULL` для пустого, строки без кавычек, целые вещественные — без «.0» (как показал бы браузер).
pub fn cell_text(v: &Value) -> String {
    match v {
        Value::Null => "NULL".to_string(),
        Value::String(s) => s.clone(),
        Value::Number(n) => match (n.as_i64(), n.as_f64()) {
            (Some(i), _) => i.to_string(),
            (None, Some(f)) => f.to_string(),
            (None, None) => n.to_string(),
        },
        other => other.to_string(),
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum View {
    Erd,
    Data,
}

impl View {
    fn from_setting(v: Option<&str>) -> Self {
        if v == Some("data") {
            View::Data
        } else {
            View::Erd
        }
    }
    fn name(self) -> &'static str {
        match self {
            View::Erd => "erd",
            View::Data => "data",
        }
    }
}

// --- компоненты ---------------------------------------------------------------------------------

/// Точка указателя в системе координат viewBox: по границам `<svg>` и размеру холста (высота `auto` сохраняет пропорции).
fn pointer_in_svg(ev: &web_sys::PointerEvent, canvas: (f64, f64)) -> Option<Point> {
    let svg = ev.current_target()?.dyn_into::<web_sys::Element>().ok()?.closest("svg").ok()??;
    let rect = svg.get_bounding_client_rect();
    if rect.width() <= 0.0 || rect.height() <= 0.0 {
        return None;
    }
    Some(Point { x: (f64::from(ev.client_x()) - rect.left()) * canvas.0 / rect.width(), y: (f64::from(ev.client_y()) - rect.top()) * canvas.1 / rect.height() })
}

/// Связь между двумя таблицами; кривая пересчитывается, только когда сдвинули одну из них.
#[component]
fn RelationLine(rel: SqlRelation, from: SqlTable, to: SqlTable, layout: RwSignal<Layout>, hovered: RwSignal<Option<String>>) -> impl IntoView {
    let (Some(ya), Some(yb)) = (column_offset(&from, &rel.from_col), column_offset(&to, &rel.to_col)) else {
        return ().into_any();
    };
    let same = from.name == to.name;
    let link = Memo::new(move |_| {
        layout.with(|l| {
            let (a, b) = (l.get(&from.name)?, l.get(&to.name)?);
            Some(link_geometry(*a, a.y + ya, *b, b.y + yb, same))
        })
    });
    let on = Memo::new(move |_| hovered.with(|h| h.as_deref().is_some_and(|h| h == rel.from || h == rel.to)));
    view! {
        <g class="sx-rel" class:on=move || on.get()>
            <path fill="none" d=move || link.get().map(|l| l.d).unwrap_or_default() />
            <text class="sx-card" x=move || link.get().map_or(0.0, |l| l.child.x) y=move || link.get().map_or(0.0, |l| l.child.y - 4.0)>"N"</text>
            <text class="sx-card" x=move || link.get().map_or(0.0, |l| l.parent.x) y=move || link.get().map_or(0.0, |l| l.parent.y - 4.0)>"1"</text>
        </g>
    }
    .into_any()
}

/// Таблица на диаграмме: рамка, заголовок и строки столбцов с отметками PK/FK.
#[component]
fn TableBox(
    table: SqlTable,
    schema: Arc<SqlDataset>,
    layout: RwSignal<Layout>,
    hovered: RwSignal<Option<String>>,
    on_down: Callback<(web_sys::PointerEvent, String)>,
) -> impl IntoView {
    let name = table.name.clone();
    let at = {
        let name = name.clone();
        Memo::new(move |_| layout.with(|l| l.get(&name).copied()))
    };
    let linked = {
        let name = name.clone();
        Memo::new(move |_| hovered.with(|h| is_linked(&schema.relations, h.as_deref(), &name)))
    };
    let is_hovered = {
        let name = name.clone();
        Memo::new(move |_| hovered.with(|h| h.as_deref() == Some(name.as_str())))
    };
    let is_view = table.is_view();
    let head = format!("M0,{HEAD_H} V7 a7,7 0 0 1 7,-7 H{} a7,7 0 0 1 7,7 V{HEAD_H} Z", BOX_W - 7.0);
    let columns = table
        .columns
        .iter()
        .enumerate()
        .map(|(i, c)| {
            let key = if c.pk { "PK" } else if c.fk.is_some() { "FK" } else { "" };
            let class = if c.pk { "pk" } else if c.fk.is_some() { "fk" } else { "" };
            view! {
                <g transform=format!("translate(0,{})", HEAD_H + i as f64 * ROW_H) class=class>
                    <text class="sx-key" x="10" y={ROW_H - 6.0}>{key}</text>
                    <text class="sx-col" x="32" y={ROW_H - 6.0}>{c.name.clone()}</text>
                    <text class="sx-type" x={BOX_W - 10.0} y={ROW_H - 6.0} text-anchor="end">{c.data_type.to_lowercase()}</text>
                </g>
            }
        })
        .collect_view();
    let title = format!("{}{}", if is_view { "◇ " } else { "" }, table.name);
    let height = box_h(&table);
    let own_name = name.clone();
    let enter_name = name.clone();
    view! {
        <g
            transform=move || at.get().map(|p| format!("translate({},{})", p.x, p.y)).unwrap_or_default()
            class=move || table_class(is_view, is_hovered.get(), linked.get())
            on:pointerdown=move |ev| on_down.run((ev, own_name.clone()))
            on:pointerenter=move |_| hovered.set(Some(enter_name.clone()))
            on:pointerleave=move |_| hovered.set(None)
        >
            <rect class="sx-frame" width=BOX_W height=height rx="7" />
            <path class="sx-head" d=head />
            <text class="sx-name" x="10" y="16">{title}</text>
            <text class="sx-count" x={BOX_W - 10.0} y="16" text-anchor="end">{table.total}</text>
            {columns}
        </g>
    }
}

/// ERD: таблицы перетаскиваются, клик без сдвига открывает данные таблицы (`on_open_table`).
#[component]
fn Erd(schema: Arc<SqlDataset>, on_open_table: Callback<String>) -> impl IntoView {
    let initial = StoredValue::new(auto_layout(&schema));
    let layout = RwSignal::new(initial.get_value());
    let hovered = RwSignal::new(None::<String>);
    let drag = StoredValue::new(None::<Drag>);
    let canvas = {
        let schema = schema.clone();
        Memo::new(move |_| layout.with(|l| canvas_size(&schema.tables, l)))
    };

    let on_down = Callback::new(move |(ev, name): (web_sys::PointerEvent, String)| {
        let (Some(pointer), Some(at)) = (pointer_in_svg(&ev, canvas.get_untracked()), layout.with_untracked(|l| l.get(&name).copied())) else {
            return;
        };
        drag.set_value(Some(Drag::start(&name, pointer, at)));
        if let Some(el) = ev.current_target().and_then(|t| t.dyn_into::<web_sys::Element>().ok()) {
            let _ = el.set_pointer_capture(ev.pointer_id());
        }
    });
    let on_move = move |ev: web_sys::PointerEvent| {
        let Some(pointer) = pointer_in_svg(&ev, canvas.get_untracked()) else { return };
        drag.update_value(|d| {
            let Some(d) = d else { return };
            let Some(current) = layout.with_untracked(|l| l.get(&d.name).copied()) else { return };
            let next = d.to(pointer, current);
            layout.update(|l| {
                l.insert(d.name.clone(), next);
            });
        });
    };
    let on_up = move |_| {
        if let Some(d) = drag.try_update_value(Option::take).flatten() {
            if !d.moved {
                on_open_table.run(d.name);
            }
        }
    };

    let by_name: HashMap<&str, &SqlTable> = schema.tables.iter().map(|t| (t.name.as_str(), t)).collect();
    let relations = schema
        .relations
        .iter()
        .filter_map(|r| {
            let (from, to) = ((*by_name.get(r.from.as_str())?).clone(), (*by_name.get(r.to.as_str())?).clone());
            Some(view! { <RelationLine rel=r.clone() from=from to=to layout=layout hovered=hovered /> })
        })
        .collect_view();
    let tables = schema
        .tables
        .iter()
        .map(|t| view! { <TableBox table=t.clone() schema=schema.clone() layout=layout hovered=hovered on_down=on_down /> })
        .collect_view();

    view! {
        <div class="sx-erd">
            <svg
                viewBox=move || { let (w, h) = canvas.get(); format!("0 0 {w} {h}") }
                style=move || svg_style(canvas.get().0)
                role="img"
                aria-label="ERD-диаграмма учебной базы"
                on:pointermove=on_move
                on:pointerup=on_up
                on:pointercancel=on_up
            >
                {relations}
                {tables}
            </svg>
            <div class="sx-erd-foot">
                <span>"PK — первичный ключ · FK — внешний ключ · N : 1 — связь"</span>
                <button class="sx-link" title="Вернуть таблицы на места" on:click=move |_| layout.set(initial.get_value())>"расставить заново"</button>
            </div>
        </div>
    }
}

fn cell_view(v: &Value) -> impl IntoView {
    if v.is_null() {
        view! { <i class="sx-null">"NULL"</i> }.into_any()
    } else {
        view! { <span class=if v.is_number() { "sx-num" } else { "" }>{cell_text(v)}</span> }.into_any()
    }
}

/// Таблица данных: имя столбца с отметкой ключа и типом, строки, пометка об обрезанном списке.
fn grid_view(t: &SqlTable) -> impl IntoView {
    let head = t
        .columns
        .iter()
        .map(|c| {
            let class = if c.pk { "pk" } else if c.fk.is_some() { "fk" } else { "" };
            let key = if c.pk { Some("PK") } else if c.fk.is_some() { Some("FK") } else { None };
            view! { <th class=class>{key.map(|k| view! { <b>{k}</b> })}{c.name.clone()}<small>{c.data_type.to_lowercase()}</small></th> }
        })
        .collect_view();
    let body = if t.rows.is_empty() {
        view! { <tr><td colspan=t.columns.len() class="sx-empty">"таблица пуста"</td></tr> }.into_any()
    } else {
        t.rows.iter().map(|r| view! { <tr>{r.iter().map(|v| view! { <td>{cell_view(v)}</td> }).collect_view()}</tr> }).collect_view().into_any()
    };
    let more = (t.total > t.rows.len()).then(|| view! { <p class="sx-more">{format!("Показаны первые {} из {} строк.", t.rows.len(), t.total)}</p> });
    view! {
        <div class="sx-scroll">
            <table class="sx-grid">
                <thead><tr>{head}</tr></thead>
                <tbody>{body}</tbody>
            </table>
        </div>
        {more}
    }
}

/// Просмотр данных: вкладки таблиц и выбранная таблица; `selected` — имя, `None` — первая.
#[component]
fn Data(schema: Arc<SqlDataset>, selected: RwSignal<Option<String>>) -> impl IntoView {
    let current = {
        let schema = schema.clone();
        Memo::new(move |_| selected.with(|s| s.as_deref().and_then(|n| schema.tables.iter().position(|t| t.name == n)).unwrap_or(0)))
    };
    let tabs = schema
        .tables
        .iter()
        .enumerate()
        .map(|(i, t)| {
            let name = t.name.clone();
            view! {
                <button
                    class="sx-tab"
                    role="tab"
                    class:on=move || current.get() == i
                    aria-selected=move || (current.get() == i).to_string()
                    on:click=move |_| selected.set(Some(name.clone()))
                >
                    {if t.is_view() { "◇ " } else { "" }}
                    {t.name.clone()}
                    <em>{t.total}</em>
                </button>
            }
        })
        .collect_view();
    view! {
        <div class="sx-data">
            <div class="sx-tabs" role="tablist">{tabs}</div>
            {move || schema.tables.get(current.get()).map(grid_view)}
        </div>
    }
}

/// Виджет целиком: заголовок со сворачиванием, переключатель «ERD / Данные» и выбранный вид. Вид и «развёрнуто» помнятся в настройках.
#[component]
pub fn SqlSchema(schema: SqlDataset) -> impl IntoView {
    if schema.tables.is_empty() {
        return ().into_any();
    }
    let open = RwSignal::new(settings::read(KEY_OPEN).as_deref() != Some("0"));
    let mode = RwSignal::new(View::from_setting(settings::read(KEY_VIEW).as_deref()));
    let selected = RwSignal::new(None::<String>);
    let label = summary(&schema);
    let schema = Arc::new(schema);

    let show = move |v: View| {
        mode.set(v);
        settings::write(KEY_VIEW, Some(v.name()));
        if !open.get_untracked() {
            open.set(true);
            settings::write(KEY_OPEN, Some("1"));
        }
    };
    let fold = move |_| {
        let next = !open.get_untracked();
        open.set(next);
        settings::write(KEY_OPEN, Some(if next { "1" } else { "0" }));
    };
    let open_table = Callback::new(move |name: String| {
        selected.set(Some(name));
        show(View::Data);
    });
    let seg = move |v: View, title: &'static str| view! { <button class:on=move || open.get() && mode.get() == v on:click=move |_| show(v)>{title}</button> };

    view! {
        <section class="sx" aria-label="Учебная база">
            <div class="sx-bar">
                <button class="sx-fold" aria-expanded=move || open.get().to_string() on:click=fold>
                    <span class="sx-chev" class:on=move || open.get()>"▸"</span>
                    "База данных"
                    <em>{label}</em>
                </button>
                <div class="sx-seg" role="group" aria-label="Вид">
                    {seg(View::Erd, "ERD")}
                    {seg(View::Data, "Данные")}
                </div>
            </div>
            {move || {
                open.get().then(|| match mode.get() {
                    View::Erd => view! { <Erd schema=schema.clone() on_open_table=open_table /> }.into_any(),
                    View::Data => view! { <Data schema=schema.clone() selected=selected /> }.into_any(),
                })
            }}
        </section>
    }
    .into_any()
}

#[cfg(test)]
mod tests {
    use super::*;
    use api::dto::{SqlColumn, SqlForeignKey};
    use serde_json::json;

    fn col(name: &str, pk: bool, fk: Option<(&str, &str)>) -> SqlColumn {
        SqlColumn { name: name.into(), data_type: "INTEGER".into(), pk, notnull: false, fk: fk.map(|(t, c)| SqlForeignKey { table: t.into(), column: c.into() }) }
    }

    fn table(name: &str, cols: Vec<SqlColumn>) -> SqlTable {
        SqlTable { name: name.into(), kind: "table".into(), columns: cols, rows: Vec::new(), total: 0 }
    }

    fn rel(from: &str, from_col: &str, to: &str, to_col: &str) -> SqlRelation {
        SqlRelation { from: from.into(), from_col: from_col.into(), to: to.into(), to_col: to_col.into() }
    }

    /// Магазин: customers ← orders ← order_items → products.
    fn shop() -> SqlDataset {
        SqlDataset {
            tables: vec![
                table("customers", vec![col("id", true, None), col("name", false, None)]),
                table("products", vec![col("id", true, None)]),
                table("orders", vec![col("id", true, None), col("customer_id", false, Some(("customers", "id")))]),
                table("order_items", vec![col("order_id", false, Some(("orders", "id"))), col("product_id", false, Some(("products", "id")))]),
            ],
            relations: vec![rel("orders", "customer_id", "customers", "id"), rel("order_items", "order_id", "orders", "id"), rel("order_items", "product_id", "products", "id")],
        }
    }

    #[test]
    fn layout_puts_parents_left_and_children_right() {
        let l = auto_layout(&shop());
        let x = |n: &str| l[n].x;
        assert_eq!(x("customers"), PAD);
        assert_eq!(x("products"), PAD);
        assert_eq!(x("orders"), PAD + BOX_W + GAP_X);
        assert_eq!(x("order_items"), PAD + 2.0 * (BOX_W + GAP_X));
        // в одной колонке таблицы идут друг под другом с зазором
        let customers_h = HEAD_H + 2.0 * ROW_H + 6.0;
        assert_eq!(l["customers"].y, PAD);
        assert_eq!(l["products"].y, PAD + customers_h + GAP_Y);
    }

    #[test]
    fn layout_is_deterministic_and_survives_self_references_and_unknown_tables() {
        let mut s = shop();
        s.relations.push(rel("customers", "id", "customers", "id"));
        s.relations.push(rel("ghost", "id", "customers", "id"));
        s.relations.push(rel("orders", "id", "ghost", "id"));
        assert_eq!(auto_layout(&s), auto_layout(&s));
        assert_eq!(auto_layout(&s)["customers"].x, PAD);
        assert_eq!(auto_layout(&s).len(), 4);
    }

    #[test]
    fn cyclic_references_do_not_hang_the_layout() {
        let s = SqlDataset {
            tables: vec![table("a", vec![col("id", true, None)]), table("b", vec![col("id", true, None)])],
            relations: vec![rel("a", "id", "b", "id"), rel("b", "id", "a", "id")],
        };
        assert_eq!(auto_layout(&s).len(), 2);
    }

    #[test]
    fn canvas_covers_every_table_with_margins() {
        let s = shop();
        let l = auto_layout(&s);
        let (w, h) = canvas_size(&s.tables, &l);
        assert_eq!(w, PAD + 2.0 * (BOX_W + GAP_X) + BOX_W + PAD + MARGIN_RIGHT);
        let tallest = s.tables.iter().map(|t| l[&t.name].y + box_h(t)).fold(0.0, f64::max);
        assert_eq!(h, tallest + PAD);
    }

    #[test]
    fn svg_style_never_shrinks_below_three_quarters() {
        assert_eq!(svg_style(400.0), "width: 100%; min-width: 300px; max-width: 400px; height: auto;");
    }

    #[test]
    fn link_between_neighbours_leaves_the_child_and_enters_the_parent() {
        let parent = Point { x: 16.0, y: 16.0 };
        let child = Point { x: 16.0 + BOX_W + GAP_X, y: 16.0 };
        // ребёнок справа от родителя: кривая от левого края ребёнка к правому краю родителя
        let l = link_geometry(child, 60.0, parent, 40.0, false);
        assert!(l.d.starts_with(&format!("M{},60 ", child.x)));
        assert!(l.d.ends_with(&format!(" {},40", parent.x + BOX_W)));
        assert_eq!((l.child.x, l.parent.x), (child.x - 10.0, parent.x + BOX_W + 10.0));
        // ребёнок слева: зеркально
        let l = link_geometry(parent, 40.0, child, 60.0, false);
        assert!(l.d.starts_with(&format!("M{},40 ", parent.x + BOX_W)));
        assert_eq!((l.child.x, l.parent.x), (parent.x + BOX_W + 10.0, child.x - 10.0));
    }

    #[test]
    fn link_handles_stacked_and_self_references() {
        let a = Point { x: 16.0, y: 16.0 };
        let b = Point { x: 40.0, y: 200.0 };
        let l = link_geometry(a, 50.0, b, 230.0, false);
        let bulge = 40.0 + BOX_W + 50.0;
        assert_eq!(l.d, format!("M{},50 C{bulge},50 {bulge},230 {},230", a.x + BOX_W, b.x + BOX_W));
        let own = link_geometry(a, 50.0, a, 70.0, true);
        assert_eq!(own.child, Point { x: a.x + BOX_W + 8.0, y: 50.0 });
        assert_eq!(own.parent, Point { x: a.x + BOX_W + 8.0, y: 70.0 });
    }

    #[test]
    fn far_links_bend_at_least_thirty_units() {
        let a = Point { x: 400.0, y: 0.0 };
        let b = Point { x: 400.0 - BOX_W - 20.0, y: 0.0 };
        assert!(link_geometry(a, 10.0, b, 10.0, false).d.contains(&format!("C{},10", a.x - 30.0)));
    }

    #[test]
    fn column_offset_points_at_the_middle_of_the_row() {
        let t = table("t", vec![col("a", false, None), col("b", false, None)]);
        assert_eq!(column_offset(&t, "a"), Some(HEAD_H + ROW_H / 2.0));
        assert_eq!(column_offset(&t, "b"), Some(HEAD_H + ROW_H + ROW_H / 2.0));
        assert_eq!(column_offset(&t, "zzz"), None);
    }

    #[test]
    fn linked_tables_are_neighbours_of_the_hovered_one() {
        let s = shop();
        assert!(is_linked(&s.relations, Some("orders"), "customers"));
        assert!(is_linked(&s.relations, Some("customers"), "orders"));
        assert!(!is_linked(&s.relations, Some("customers"), "products"));
        assert!(!is_linked(&s.relations, None, "orders"));
    }

    #[test]
    fn table_classes_follow_state() {
        assert_eq!(table_class(false, false, false), "sx-tbl");
        assert_eq!(table_class(true, true, false), "sx-tbl view on");
        assert_eq!(table_class(false, false, true), "sx-tbl linked");
    }

    #[test]
    fn a_drag_follows_the_pointer_keeps_margins_and_tells_a_click_from_a_move() {
        let at = Point { x: 100.0, y: 50.0 };
        let mut d = Drag::start("t", Point { x: 120.0, y: 60.0 }, at);
        assert_eq!((d.dx, d.dy), (20.0, 10.0));
        // дрожание в пределах трёх единиц — ещё клик
        assert_eq!(d.to(Point { x: 121.0, y: 61.0 }, at), Point { x: 101.0, y: 51.0 });
        assert!(!d.moved);
        // уход за левый край упирается в поля
        assert_eq!(d.to(Point { x: 5.0, y: 100.0 }, at), Point { x: MIN_POS, y: 90.0 });
        assert!(d.moved);
    }

    #[test]
    fn plurals_in_russian() {
        let p = |n| plural(n, "таблица", "таблицы", "таблиц");
        assert_eq!([p(1), p(2), p(4), p(5), p(11), p(14), p(21), p(22), p(25)], ["таблица", "таблицы", "таблицы", "таблиц", "таблиц", "таблиц", "таблица", "таблицы", "таблиц"]);
    }

    #[test]
    fn summary_counts_tables_and_views_separately() {
        let mut s = shop();
        assert_eq!(summary(&s), "4 таблицы");
        s.tables[3].kind = "view".into();
        assert_eq!(summary(&s), "3 таблицы · 1 представл.");
    }

    #[test]
    fn cells_show_null_strings_and_integral_floats() {
        assert_eq!(cell_text(&Value::Null), "NULL");
        assert_eq!(cell_text(&json!("Аня")), "Аня");
        assert_eq!(cell_text(&json!(7)), "7");
        assert_eq!(cell_text(&json!(3.0)), "3");
        assert_eq!(cell_text(&json!(2.5)), "2.5");
    }

    #[test]
    fn view_setting_defaults_to_the_diagram() {
        assert_eq!(View::from_setting(None), View::Erd);
        assert_eq!(View::from_setting(Some("data")), View::Data);
        assert_eq!(View::from_setting(Some("мусор")), View::Erd);
        assert_eq!(View::from_setting(Some(View::Data.name())), View::Data);
    }
}
