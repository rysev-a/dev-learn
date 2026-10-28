//! Pure logic of the block board: layout of rectangles with ports, pin lookup, connecting with buses.
//! No interface — covered by tests.

use std::collections::{HashMap, HashSet};

use archlab::{
    blocks::{connection_error, end_info, is_source_end, BlockInstance, BlockInterface, BlockLibrary, BlockPort, BusEnd, BusWire, PortsOf, TOP},
    interfaces::Iface,
    layout::{layout_box, side_boxes, BoxKind, PinRow, PinSide, BLOCK_W, SIDE_W},
    model::NodeValue,
};

use crate::components::labs::board_view::{js_round, Point};

/// Default block board size.
pub const BLOCKS_BOARD_W: f64 = 880.0;
pub const BLOCKS_BOARD_H: f64 = 560.0;

/// Row of a port (or its field) in a rectangle: everything needed for drawing and pin lookup.
#[derive(Clone, Debug, PartialEq)]
pub struct RowInfo {
    /// unique key `node|port|field` — it also marks the expansion
    pub key: String,
    pub end: BusEnd,
    pub name: String,
    pub ty: Iface,
    /// nesting depth: 0 is the whole port, 1 is its field, etc.
    pub depth: usize,
    /// pin on the left (block input) or on the right (block output)
    pub side_in: bool,
    /// row center from the top of the rectangle
    pub y: f64,
    pub expandable: bool,
    pub expanded: bool,
    /// circuit nodes carried by the row, in bit order
    pub nodes: Vec<String>,
}

/// Rectangle with ports: a block or the port column of the exercise itself.
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
    /// Rectangle key: the input and output columns share the same node, so the key also includes the kind.
    pub fn key(&self) -> (String, u8) {
        (self.node.clone(), kind_tag(self.kind))
    }
}

/// A number instead of the rectangle kind: `BoxKind` is not hashable, but the on-screen list key must be.
pub fn kind_tag(kind: BoxKind) -> u8 {
    match kind {
        BoxKind::TopIn => 0,
        BoxKind::TopOut => 1,
        BoxKind::Block => 2,
    }
}

/// Rectangle kind from the number given by [`kind_tag`].
pub fn kind_of(tag: u8) -> BoxKind {
    match tag {
        0 => BoxKind::TopIn,
        1 => BoxKind::TopOut,
        _ => BoxKind::Block,
    }
}

/// Row pin on the board: the pin center and the row itself.
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

/// Spreading a tight circuit when viewing: coordinates are multiplied from the top-left corner of the work area.
pub fn spread_x(x: f64, spread: f64) -> f64 {
    js_round(SIDE_W + 18.0 + (x - (SIDE_W + 18.0)) * spread)
}

pub fn spread_y(y: f64, spread: f64) -> f64 {
    js_round(20.0 + (y - 20.0) * spread)
}

/// Board size: in the normal view as given; when spread, it grows together with the blocks.
pub fn board_size(instances: &[BlockInstance], spread: f64, height: f64) -> (f64, f64) {
    if spread == 1.0 {
        return (BLOCKS_BOARD_W, height);
    }
    let max_x = instances.iter().map(|i| spread_x(i.x, spread)).fold(0.0, f64::max);
    let max_y = instances.iter().map(|i| spread_y(i.y, spread) + 290.0).fold(0.0, f64::max);
    (BLOCKS_BOARD_W.max(js_round(max_x + BLOCK_W + 30.0 + SIDE_W + 6.0)), height.max(js_round(max_y)))
}

/// Layout of all rectangles: the exercise's input and output columns and the blocks (`moved` are blocks shifted on screen).
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
            def.map_or(i18n::tr("Unknown block"), |d| d.title.as_str()),
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

/// Pins of all rows by row key.
pub fn pin_map(boxes: &[BoxInfo]) -> HashMap<String, PinHit> {
    let mut map = HashMap::new();
    for b in boxes {
        for row in &b.rows {
            map.insert(row.key.clone(), PinHit { pos: center_of(b, row), row: row.clone(), kind: b.kind });
        }
    }
    map
}

/// Pin for a bus end; if the field is collapsed, the bus goes to the nearest expanded ancestor (`a.b.c` → `a.b` → `a` → port).
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

/// Node ports: for [`TOP`] the exercise's own ports, for an instance the ports of its block.
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

/// Ends in "from → to" order: the source is the one that supplies the signal.
pub fn orient(a: &BusEnd, b: &BusEnd, ports: &PortsOf) -> (BusEnd, BusEnd) {
    match end_info(a, ports) {
        Some(info) if is_source_end(a, &info) => (a.clone(), b.clone()),
        _ => (b.clone(), a.clone()),
    }
}

/// Reason the ends cannot be connected; `None` means they can.
pub fn join_error(a: &BusEnd, b: &BusEnd, ports: &PortsOf) -> Option<String> {
    let (from, to) = orient(a, b, ports);
    connection_error(&from, &to, ports)
}

/// First free bus id of the form `b<n>`, starting from `bus count + 1`.
pub fn next_bus_id(wires: &[BusWire]) -> String {
    let mut n = wires.len() + 1;
    while wires.iter().any(|w| w.id == format!("b{n}")) {
        n += 1;
    }
    format!("b{n}")
}

/// Expand or collapse a row; collapsing also closes all its nested fields.
pub fn toggle_expanded(set: &mut HashSet<String>, key: &str) {
    if set.contains(key) {
        let nested = format!("{key}.");
        set.retain(|k| k != key && !k.starts_with(&nested));
    } else {
        set.insert(key.to_string());
    }
}

/// Bus class by its bit values: one bit — by value, several — `bus` (with `vx` while there are unknowns).
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

/// Row pin center in board coordinates: on the left, the rectangle edge; on the right, the edge plus the width.
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
        let _ru = locales::guard(i18n::Locale::Ru);
        let lib = BlockLibrary::builtin();
        let boxes = layout_boxes(&iface(), &lib, &[inst("i1", "adapter-w2a", 200.0, 20.0)], &HashSet::new(), &HashMap::new(), BLOCKS_BOARD_W, 1.0);
        assert_eq!(boxes.len(), 3);
        assert_eq!((boxes[0].kind, boxes[1].kind, boxes[2].kind), (BoxKind::TopIn, BoxKind::TopOut, BoxKind::Block));
        assert_eq!(boxes[2].title, "Слово → адрес");
        assert_eq!(boxes[2].w, BLOCK_W);
        // a block has two ports: input on the left, output on the right
        assert!(boxes[2].rows.iter().any(|r| r.side_in && r.name == "in"));
        assert!(boxes[2].rows.iter().any(|r| !r.side_in && r.name == "out"));
    }

    #[test]
    fn expanding_a_port_adds_its_fields_and_pins_resolve_to_the_nearest_visible_row() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let lib = BlockLibrary::builtin();
        let ins = [inst("i1", "adapter-w2a", 200.0, 20.0)];
        let closed = layout_boxes(&iface(), &lib, &ins, &HashSet::new(), &HashMap::new(), BLOCKS_BOARD_W, 1.0);
        let pins = pin_map(&closed);
        // field collapsed: the bus to `in.D1` arrives at the whole port's row
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
        let _ru = locales::guard(i18n::Locale::Ru);
        let lib = BlockLibrary::builtin();
        let ins = [inst("i1", "adapter-w2a", 200.0, 20.0)];
        let moved = HashMap::from([("i1".to_string(), Point::new(333.0, 77.0))]);
        let boxes = layout_boxes(&iface(), &lib, &ins, &HashSet::new(), &moved, BLOCKS_BOARD_W, 1.0);
        assert_eq!((boxes[2].x, boxes[2].y), (333.0, 77.0));
    }

    #[test]
    fn collapsing_a_row_closes_its_nested_fields_only() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mut set: HashSet<String> = ["n|p|", "n|p|op", "n|p|op.x", "n|q|"].iter().map(|s| s.to_string()).collect();
        toggle_expanded(&mut set, "n|p|op");
        assert!(set.contains("n|p|") && set.contains("n|q|"));
        assert!(!set.contains("n|p|op") && !set.contains("n|p|op.x"));
        toggle_expanded(&mut set, "n|p|op");
        assert!(set.contains("n|p|op"));
    }

    #[test]
    fn box_kinds_survive_the_round_trip_through_a_tag() {
        let _ru = locales::guard(i18n::Locale::Ru);
        for kind in [BoxKind::TopIn, BoxKind::TopOut, BoxKind::Block] {
            assert_eq!(kind_of(kind_tag(kind)), kind);
        }
    }

    #[test]
    fn bus_ids_skip_taken_ones() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let w = |id: &str| BusWire { id: id.into(), from: BusEnd::new("a", "b", ""), to: BusEnd::new("c", "d", "") };
        assert_eq!(next_bus_id(&[]), "b1");
        assert_eq!(next_bus_id(&[w("b2")]), "b3");
    }

    #[test]
    fn joining_is_checked_in_either_order_and_types_must_match() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let lib = BlockLibrary::builtin();
        let ins = [inst("i1", "adapter-w2a", 200.0, 20.0)];
        let iface = iface();
        let ports = ports_of(&iface, &lib, &ins);
        let top_in = BusEnd::new(TOP, "x", "");
        let block_in = BusEnd::new("i1", "in", "");
        // exercise input (Word2) → adapter input (Word2): allowed, in any order
        assert_eq!(join_error(&top_in, &block_in, &ports), None);
        assert_eq!(join_error(&block_in, &top_in, &ports), None);
        // adapter output (Addr2) → exercise output (Addr2) is allowed; to Word2 an adapter is needed
        let block_out = BusEnd::new("i1", "out", "");
        assert_eq!(join_error(&block_out, &BusEnd::new(TOP, "y", ""), &ports), None);
        assert!(join_error(&block_out, &top_in, &ports).is_some());
        // input to input is not allowed
        assert!(join_error(&block_in, &BusEnd::new(TOP, "y", ""), &ports).is_some());
    }

    #[test]
    fn spread_grows_the_board_with_the_blocks() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let ins = [inst("i1", "x", 200.0, 20.0), inst("i2", "x", 600.0, 400.0)];
        assert_eq!(board_size(&ins, 1.0, 560.0), (BLOCKS_BOARD_W, 560.0));
        let (w, h) = board_size(&ins, 1.7, 560.0);
        assert!(w > BLOCKS_BOARD_W && h > 560.0);
        assert_eq!(spread_x(SIDE_W + 18.0, 1.7), SIDE_W + 18.0, "the origin does not move");
        assert_eq!(spread_y(20.0, 1.7), 20.0);
    }

    #[test]
    fn wire_class_follows_the_width() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(wire_class(&[Some(1)], 1), "v1");
        assert_eq!(wire_class(&[Some(0)], 1), "v0");
        assert_eq!(wire_class(&[None], 1), "vx");
        assert_eq!(wire_class(&[Some(1), Some(0)], 2), "bus");
        assert_eq!(wire_class(&[Some(1), None], 2), "bus vx");
        assert_eq!(wire_class(&[], 2), "bus vx");
    }
}
