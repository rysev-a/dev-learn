//! Where a new object goes on the board: every kind has a column (the layers run from the disks on the left to the VMs on the right), and a
//! new object takes the first free place of its column. The UI and the scenario builder use the same function, so a hand-placed object and a
//! built one land on the same grid.

use super::{Kind, Topology};

/// Width of an object on the board (board units).
pub const NODE_W: f64 = 92.0;
/// Height of an object on the board (board units).
pub const NODE_H: f64 = 60.0;
/// Distance between the rows of a column.
const ROW: f64 = 80.0;

/// Column of a kind (x) and the first row (y). Thin pools and thin volumes sit in the band below the logical volumes.
pub fn column(kind: Kind) -> (f64, f64) {
    match kind {
        Kind::Disk => (70.0, 60.0),
        Kind::Pv => (190.0, 60.0),
        Kind::Vg => (310.0, 60.0),
        Kind::Lv => (450.0, 60.0),
        Kind::Snapshot => (590.0, 60.0),
        Kind::Fs => (730.0, 60.0),
        Kind::Vm => (870.0, 60.0),
        Kind::ThinPool => (450.0, 380.0),
        Kind::ThinLv => (590.0, 380.0),
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
