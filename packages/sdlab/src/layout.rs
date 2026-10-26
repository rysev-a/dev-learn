//! Раскладка схемы по колонкам слева направо: пользователи → CDN → шлюзы → серверы → кэш/очередь → хранилища.
//! Окно просмотра — `BOARD_W × BOARD_H` единиц (по нему считается масштаб), сама схема шире: колонки стоят через 150,
//! а при открытии поле «вписывает» схему в окно.

use crate::jsfmt;
use crate::types::{SdNode, SdState};

pub const BOARD_W: f64 = 780.0;
pub const BOARD_H: f64 = 560.0;
const LAYOUT_H: f64 = 470.0;
const COL_STEP: f64 = 150.0;
const COLS: usize = 8;

/// Координата x колонки (за пределами — 70).
pub fn col_x(col: usize) -> f64 {
    if col < COLS {
        70.0 + col as f64 * COL_STEP
    } else {
        70.0
    }
}

/// Расставляет узлы без положения (`x < 0` или `y < 0`) по колонкам своего вида; остальные не трогает.
pub fn place(state: &SdState) -> SdState {
    let mut seen = [0usize; 16];
    let mut count = [0usize; 16];
    for n in &state.nodes {
        count[n.col().min(15)] += 1;
    }
    let nodes: Vec<SdNode> = state
        .nodes
        .iter()
        .map(|n| {
            let col = n.col().min(15);
            let i = seen[col];
            seen[col] += 1;
            if n.x >= 0.0 && n.y >= 0.0 {
                return n.clone();
            }
            let step = LAYOUT_H / (count[col] + 1) as f64;
            SdNode { x: col_x(n.col()), y: jsfmt::round(step * (i + 1) as f64), ..n.clone() }
        })
        .collect();
    SdState { nodes, edges: state.edges.clone() }
}

/// Куда ставить новый компонент в колонке: ниже самого нижнего или посередине пустой колонки.
pub fn next_y(state: &SdState, col: usize) -> f64 {
    state.nodes.iter().filter(|n| n.col() == col).map(|n| n.y).fold(None, |m: Option<f64>, y| Some(m.map_or(y, |m| m.max(y)))).map_or(LAYOUT_H / 2.0, |y| y + 80.0)
}

impl SdNode {
    /// Колонка раскладки по виду компонента.
    pub fn col(&self) -> usize {
        crate::kinds::spec(self.kind).col
    }
}
