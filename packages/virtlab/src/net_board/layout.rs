//! Where a new object goes on the board: every kind has a column (from the namespaces and their rules on the left, where the «lives in» links start, to the outside network on the right),
//! and a new object takes the first free place of its column. The UI and the scenario builder use the same function, so a hand-placed object and a
//! built one land on the same grid.

use super::{Kind, Topology};

/// Width of an object on the board (board units).
pub const NODE_W: f64 = 92.0;
/// Height of an object on the board (board units).
pub const NODE_H: f64 = 60.0;
/// Distance between the rows of a column.
const ROW: f64 = 80.0;

/// Column of a kind (x) and the first row (y). VLAN interfaces and VMs sit in the band below.
pub fn column(kind: Kind) -> (f64, f64) {
    match kind {
        Kind::Netns => (70.0, 60.0),
        Kind::Nat => (70.0, 380.0),
        Kind::Eth => (190.0, 60.0),
        Kind::Bond => (310.0, 60.0),
        Kind::Vlan => (310.0, 380.0),
        Kind::Bridge => (430.0, 60.0),
        Kind::Veth => (550.0, 60.0),
        Kind::Vm => (550.0, 380.0),
        Kind::External => (670.0, 60.0),
    }
}

/// The first free place of a new object in the column of its kind: no other object closer than a node width across or 70 down.
pub fn next_pos(t: &Topology, kind: Kind) -> (f64, f64) {
    let (x, y0) = column(kind);
    (0..)
        .map(|i| (x, y0 + ROW * f64::from(i)))
        .find(|(x, y)| !t.nodes.iter().any(|n| (n.x - x).abs() < NODE_W && (n.y - y).abs() < 70.0))
        .unwrap_or((x, y0))
}

/// Places the objects of a board that has no positions (task data): every object takes the first free place of its column, in the order of the list.
pub fn auto_layout(t: &mut Topology) {
    let mut placed = Topology { nodes: Vec::new(), edges: Vec::new() };
    for n in &mut t.nodes {
        let (x, y) = next_pos(&placed, n.kind);
        n.x = x;
        n.y = y;
        placed.nodes.push(n.clone());
    }
}
