//! Чистая логика доски с блоками: раскладка прямоугольников с портами, поиск контактов, соединение шинами.
//! Без интерфейса — проверяется тестами.

use std::collections::{HashMap, HashSet};

use archlab::{
    blocks::{connection_error, end_info, is_source_end, BlockInstance, BlockInterface, BlockLibrary, BlockPort, BusEnd, BusWire, PortsOf, TOP},
    interfaces::Iface,
    layout::{layout_box, side_boxes, BoxKind, PinRow, PinSide, BLOCK_W, SIDE_W},
    model::NodeValue,
};

use crate::components::labs::board_view::{js_round, Point};

/// Размеры доски блоков по умолчанию.
pub const BLOCKS_BOARD_W: f64 = 880.0;
pub const BLOCKS_BOARD_H: f64 = 560.0;

/// Строка порта (или его поля) в прямоугольнике: всё, что нужно для отрисовки и поиска контакта.
#[derive(Clone, Debug, PartialEq)]
pub struct RowInfo {
    /// уникальный ключ `узел|порт|поле` — им же помечается раскрытие
    pub key: String,
    pub end: BusEnd,
    pub name: String,
    pub ty: Iface,
    /// глубина вложенности: 0 — порт целиком, 1 — его поле и т. д.
    pub depth: usize,
    /// контакт слева (вход блока) или справа (выход блока)
    pub side_in: bool,
    /// центр строки от верха прямоугольника
    pub y: f64,
    pub expandable: bool,
    pub expanded: bool,
    /// узлы схемы, которые несёт строка, по порядку бит
    pub nodes: Vec<String>,
}

/// Прямоугольник с портами: блок или колонка портов самого упражнения.
#[derive(Clone, Debug, PartialEq)]
pub struct BoxInfo {
    pub node: String,
    pub kind: BoxKind,
    pub title: String,
    pub x: f64,
    pub y: f64,
    pub w: f64,
    pub h: f64,
    pub rows: Vec<RowInfo>,
}

impl BoxInfo {
    /// Ключ прямоугольника: у колонок входов и выходов один и тот же узел, поэтому в ключе ещё и вид.
    pub fn key(&self) -> (String, u8) {
        (self.node.clone(), kind_tag(self.kind))
    }
}

/// Число вместо вида прямоугольника: `BoxKind` не хешируется, а ключ списка на экране должен.
pub fn kind_tag(kind: BoxKind) -> u8 {
    match kind {
        BoxKind::TopIn => 0,
        BoxKind::TopOut => 1,
        BoxKind::Block => 2,
    }
}

/// Вид прямоугольника по числу из [`kind_tag`].
pub fn kind_of(tag: u8) -> BoxKind {
    match tag {
        0 => BoxKind::TopIn,
        1 => BoxKind::TopOut,
        _ => BoxKind::Block,
    }
}

/// Контакт строки на доске: центр пина и сама строка.
#[derive(Clone, Debug, PartialEq)]
pub struct PinHit {
    pub pos: Point,
    pub row: RowInfo,
    pub kind: BoxKind,
}

fn row_info(r: &PinRow) -> RowInfo {
    RowInfo {
        key: r.key.clone(),
        end: r.end.clone(),
        name: r.name.clone(),
        ty: r.ty,
        depth: r.depth,
        side_in: r.side == PinSide::In,
        y: r.y,
        expandable: r.expandable,
        expanded: r.expanded,
        nodes: r.nodes.clone(),
    }
}

/// Раздвигание тесной схемы при просмотре: координаты умножаются от левого верхнего угла рабочей области.
pub fn spread_x(x: f64, spread: f64) -> f64 {
    js_round(SIDE_W + 18.0 + (x - (SIDE_W + 18.0)) * spread)
}

pub fn spread_y(y: f64, spread: f64) -> f64 {
    js_round(20.0 + (y - 20.0) * spread)
}

/// Размер доски: при обычном виде — как задан; при раздвигании растёт вместе с блоками.
pub fn board_size(instances: &[BlockInstance], spread: f64, height: f64) -> (f64, f64) {
    if spread == 1.0 {
        return (BLOCKS_BOARD_W, height);
    }
    let max_x = instances.iter().map(|i| spread_x(i.x, spread)).fold(0.0, f64::max);
    let max_y = instances.iter().map(|i| spread_y(i.y, spread) + 290.0).fold(0.0, f64::max);
    (BLOCKS_BOARD_W.max(js_round(max_x + BLOCK_W + 30.0 + SIDE_W + 6.0)), height.max(js_round(max_y)))
}

/// Раскладка всех прямоугольников: колонки входов и выходов упражнения и блоки (`moved` — сдвинутые на экране блоки).
pub fn layout_boxes(
    iface: &BlockInterface,
    lib: &BlockLibrary,
    instances: &[BlockInstance],
    expanded: &HashSet<String>,
    moved: &HashMap<String, Point>,
    board_w: f64,
    spread: f64,
) -> Vec<BoxInfo> {
    let (in_box, out_box) = side_boxes(&iface.ports, expanded, board_w, 16.0);
    let mut layouts = vec![in_box, out_box];
    for inst in instances {
        let def = lib.def(&inst.block_id);
        let (x, y) = moved.get(&inst.id).map_or((spread_x(inst.x, spread), spread_y(inst.y, spread)), |p| (p.x, p.y));
        let empty: &[BlockPort] = &[];
        layouts.push(layout_box(
            &inst.id,
            def.map_or("Неизвестный блок", |d| d.title.as_str()),
            def.map_or(empty, |d| d.iface.ports.as_slice()),
            expanded,
            (x, y, BLOCK_W),
            BoxKind::Block,
        ));
    }
    layouts
        .into_iter()
        .map(|b| BoxInfo { node: b.node.clone(), kind: b.kind, title: b.title.clone(), x: b.x, y: b.y, w: b.w, h: b.h, rows: b.rows.iter().map(row_info).collect() })
        .collect()
}

/// Контакты всех строк по ключу строки.
pub fn pin_map(boxes: &[BoxInfo]) -> HashMap<String, PinHit> {
    let mut map = HashMap::new();
    for b in boxes {
        for row in &b.rows {
            map.insert(row.key.clone(), PinHit { pos: center_of(b, row), row: row.clone(), kind: b.kind });
        }
    }
    map
}

/// Контакт для конца шины; если поле свёрнуто, шина идёт к ближайшему раскрытому предку (`a.b.c` → `a.b` → `a` → порт).
pub fn pin_for<'a>(pins: &'a HashMap<String, PinHit>, end: &BusEnd) -> Option<&'a PinHit> {
    let mut path = end.path.clone();
    loop {
        let key = format!("{}|{}|{}", end.node, end.port, path);
        if let Some(hit) = pins.get(&key) {
            return Some(hit);
        }
        if path.is_empty() {
            return None;
        }
        path = match path.rfind('.') {
            Some(dot) => path[..dot].to_string(),
            None => String::new(),
        };
    }
}

/// Порты узла: у [`TOP`] — порты самого упражнения, у экземпляра — порты его блока.
pub fn ports_of<'a>(iface: &'a BlockInterface, lib: &'a BlockLibrary, instances: &'a [BlockInstance]) -> impl Fn(&str) -> Option<&'a [BlockPort]> + 'a {
    move |node: &str| {
        if node == TOP {
            Some(iface.ports.as_slice())
        } else {
            let inst = instances.iter().find(|i| i.id == node)?;
            lib.def(&inst.block_id).map(|d| d.iface.ports.as_slice())
        }
    }
}

/// Концы в порядке «откуда → куда»: источником считается тот, что отдаёт сигнал.
pub fn orient(a: &BusEnd, b: &BusEnd, ports: &PortsOf) -> (BusEnd, BusEnd) {
    match end_info(a, ports) {
        Some(info) if is_source_end(a, &info) => (a.clone(), b.clone()),
        _ => (b.clone(), a.clone()),
    }
}

/// Причина, по которой концы нельзя соединить; `None` — можно.
pub fn join_error(a: &BusEnd, b: &BusEnd, ports: &PortsOf) -> Option<String> {
    let (from, to) = orient(a, b, ports);
    connection_error(&from, &to, ports)
}

/// Первый свободный id шины вида `b<n>`, начиная с `число шин + 1`.
pub fn next_bus_id(wires: &[BusWire]) -> String {
    let mut n = wires.len() + 1;
    while wires.iter().any(|w| w.id == format!("b{n}")) {
        n += 1;
    }
    format!("b{n}")
}

/// Раскрыть или свернуть строку; при сворачивании закрываются и все её вложенные поля.
pub fn toggle_expanded(set: &mut HashSet<String>, key: &str) {
    if set.contains(key) {
        let nested = format!("{key}.");
        set.retain(|k| k != key && !k.starts_with(&nested));
    } else {
        set.insert(key.to_string());
    }
}

/// Класс шины по значениям её бит: один бит — по значению, несколько — `bus` (с `vx`, пока есть неизвестные).
pub fn wire_class(values: &[NodeValue], width: usize) -> &'static str {
    let known = !values.is_empty() && values.iter().all(Option::is_some);
    match (width, values.first().copied().flatten()) {
        (1, Some(1)) => "v1",
        (1, Some(_)) => "v0",
        (1, None) => "vx",
        _ if known => "bus",
        _ => "bus vx",
    }
}

/// Центр пина строки в координатах доски: слева — край прямоугольника, справа — край плюс ширина.
pub fn center_of(b: &BoxInfo, row: &RowInfo) -> Point {
    Point::new(if row.side_in { b.x } else { b.x + b.w }, b.y + row.y)
}

#[cfg(test)]
mod tests {
    use super::*;
    use archlab::blocks::Dir;

    fn port(name: &str, ty: Iface, dir: Dir, nodes: &[&str]) -> BlockPort {
        BlockPort { name: name.into(), ty, dir, nodes: nodes.iter().map(|n| n.to_string()).collect() }
    }

    fn iface() -> BlockInterface {
        BlockInterface {
            inputs: vec!["A".into(), "B".into()],
            outputs: vec!["Y1".into(), "Y0".into()],
            labels: None,
            ports: vec![port("x", Iface::Word2, Dir::In, &["A", "B"]), port("y", Iface::Addr2, Dir::Out, &["Y1", "Y0"])],
        }
    }

    fn inst(id: &str, block: &str, x: f64, y: f64) -> BlockInstance {
        BlockInstance { id: id.into(), block_id: block.into(), x, y }
    }

    #[test]
    fn layout_has_two_side_columns_and_one_box_per_block() {
        let lib = BlockLibrary::builtin();
        let boxes = layout_boxes(&iface(), &lib, &[inst("i1", "adapter-w2a", 200.0, 20.0)], &HashSet::new(), &HashMap::new(), BLOCKS_BOARD_W, 1.0);
        assert_eq!(boxes.len(), 3);
        assert_eq!((boxes[0].kind, boxes[1].kind, boxes[2].kind), (BoxKind::TopIn, BoxKind::TopOut, BoxKind::Block));
        assert_eq!(boxes[2].title, "Слово → адрес");
        assert_eq!(boxes[2].w, BLOCK_W);
        // у блока два порта: вход слева, выход справа
        assert!(boxes[2].rows.iter().any(|r| r.side_in && r.name == "in"));
        assert!(boxes[2].rows.iter().any(|r| !r.side_in && r.name == "out"));
    }

    #[test]
    fn expanding_a_port_adds_its_fields_and_pins_resolve_to_the_nearest_visible_row() {
        let lib = BlockLibrary::builtin();
        let ins = [inst("i1", "adapter-w2a", 200.0, 20.0)];
        let closed = layout_boxes(&iface(), &lib, &ins, &HashSet::new(), &HashMap::new(), BLOCKS_BOARD_W, 1.0);
        let pins = pin_map(&closed);
        // поле свёрнуто: шина на `in.D1` приходит к строке всего порта
        let hit = pin_for(&pins, &BusEnd::new("i1", "in", "D1")).map(|h| h.row.key.clone());
        assert_eq!(hit.as_deref(), Some("i1|in|"));
        let mut open = HashSet::new();
        open.insert("i1|in|".to_string());
        let wide = layout_boxes(&iface(), &lib, &ins, &open, &HashMap::new(), BLOCKS_BOARD_W, 1.0);
        assert!(wide[2].rows.len() > closed[2].rows.len());
        let hit = pin_for(&pin_map(&wide), &BusEnd::new("i1", "in", "D1")).map(|h| h.row.key.clone());
        assert_eq!(hit.as_deref(), Some("i1|in|D1"));
        assert!(pin_for(&pins, &BusEnd::new("zzz", "in", "")).is_none());
    }

    #[test]
    fn moved_blocks_keep_the_screen_position() {
        let lib = BlockLibrary::builtin();
        let ins = [inst("i1", "adapter-w2a", 200.0, 20.0)];
        let moved = HashMap::from([("i1".to_string(), Point::new(333.0, 77.0))]);
        let boxes = layout_boxes(&iface(), &lib, &ins, &HashSet::new(), &moved, BLOCKS_BOARD_W, 1.0);
        assert_eq!((boxes[2].x, boxes[2].y), (333.0, 77.0));
    }

    #[test]
    fn collapsing_a_row_closes_its_nested_fields_only() {
        let mut set: HashSet<String> = ["n|p|", "n|p|op", "n|p|op.x", "n|q|"].iter().map(|s| s.to_string()).collect();
        toggle_expanded(&mut set, "n|p|op");
        assert!(set.contains("n|p|") && set.contains("n|q|"));
        assert!(!set.contains("n|p|op") && !set.contains("n|p|op.x"));
        toggle_expanded(&mut set, "n|p|op");
        assert!(set.contains("n|p|op"));
    }

    #[test]
    fn box_kinds_survive_the_round_trip_through_a_tag() {
        for kind in [BoxKind::TopIn, BoxKind::TopOut, BoxKind::Block] {
            assert_eq!(kind_of(kind_tag(kind)), kind);
        }
    }

    #[test]
    fn bus_ids_skip_taken_ones() {
        let w = |id: &str| BusWire { id: id.into(), from: BusEnd::new("a", "b", ""), to: BusEnd::new("c", "d", "") };
        assert_eq!(next_bus_id(&[]), "b1");
        assert_eq!(next_bus_id(&[w("b2")]), "b3");
    }

    #[test]
    fn joining_is_checked_in_either_order_and_types_must_match() {
        let lib = BlockLibrary::builtin();
        let ins = [inst("i1", "adapter-w2a", 200.0, 20.0)];
        let iface = iface();
        let ports = ports_of(&iface, &lib, &ins);
        let top_in = BusEnd::new(TOP, "x", "");
        let block_in = BusEnd::new("i1", "in", "");
        // вход упражнения (Word2) → вход адаптера (Word2): можно, в любом порядке
        assert_eq!(join_error(&top_in, &block_in, &ports), None);
        assert_eq!(join_error(&block_in, &top_in, &ports), None);
        // выход адаптера (Addr2) → выход упражнения (Addr2) можно; к Word2 — нужен переходник
        let block_out = BusEnd::new("i1", "out", "");
        assert_eq!(join_error(&block_out, &BusEnd::new(TOP, "y", ""), &ports), None);
        assert!(join_error(&block_out, &top_in, &ports).is_some());
        // вход к входу нельзя
        assert!(join_error(&block_in, &BusEnd::new(TOP, "y", ""), &ports).is_some());
    }

    #[test]
    fn spread_grows_the_board_with_the_blocks() {
        let ins = [inst("i1", "x", 200.0, 20.0), inst("i2", "x", 600.0, 400.0)];
        assert_eq!(board_size(&ins, 1.0, 560.0), (BLOCKS_BOARD_W, 560.0));
        let (w, h) = board_size(&ins, 1.7, 560.0);
        assert!(w > BLOCKS_BOARD_W && h > 560.0);
        assert_eq!(spread_x(SIDE_W + 18.0, 1.7), SIDE_W + 18.0, "точка отсчёта не уезжает");
        assert_eq!(spread_y(20.0, 1.7), 20.0);
    }

    #[test]
    fn wire_class_follows_the_width() {
        assert_eq!(wire_class(&[Some(1)], 1), "v1");
        assert_eq!(wire_class(&[Some(0)], 1), "v0");
        assert_eq!(wire_class(&[None], 1), "vx");
        assert_eq!(wire_class(&[Some(1), Some(0)], 2), "bus");
        assert_eq!(wire_class(&[Some(1), None], 2), "bus vx");
        assert_eq!(wire_class(&[], 2), "bus vx");
    }
}
