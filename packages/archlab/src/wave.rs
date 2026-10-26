//! Временная диаграмма по истории изменений сигналов (порт `lab/wave.ts`).

use crate::exercise::CircuitSpec;
use crate::model::{Bit, InputId, NodeValue};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// Сколько последних изменений хранит временная диаграмма.
pub const HISTORY_MAX: usize = 24;

/// Размеры диаграммы.
pub const LABEL_W: f64 = 56.0;
pub const STEP: f64 = 26.0;
pub const ROW_H: f64 = 30.0;
pub const HI: f64 = 8.0;
pub const LO: f64 = 22.0;

/// Ширина всей диаграммы.
pub const fn wave_width() -> f64 {
    LABEL_W + HISTORY_MAX as f64 * STEP
}

/// Снимок сигналов после очередного изменения — один столбец временной диаграммы.
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct Sample {
    pub inputs: BTreeMap<InputId, Bit>,
    pub outputs: BTreeMap<String, NodeValue>,
}

/// Вид строки диаграммы.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum RowKind {
    In,
    Clk,
    Out,
}

/// Строка диаграммы: подпись и пути SVG.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct WaveRow {
    pub label: String,
    pub kind: RowKind,
    pub top: f64,
    /// Определённые участки сигнала.
    pub d: String,
    /// Неопределённые («?») участки — пунктиром посередине.
    pub dx: String,
}

/// Готовая диаграмма.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Wave {
    pub rows: Vec<WaveRow>,
    pub height: f64,
    pub cols: Vec<f64>,
    pub last_x: f64,
}

fn wave_row(label: String, kind: RowKind, top: f64, values: &[NodeValue]) -> WaveRow {
    let mut d = String::new();
    let mut dx = String::new();
    let mut prev_y: Option<f64> = None;
    for (i, v) in values.iter().enumerate() {
        let x0 = LABEL_W + i as f64 * STEP;
        let x1 = x0 + STEP;
        match v {
            None => {
                dx.push_str(&format!("M {} {} H {} ", x0, top + (HI + LO) / 2.0, x1));
                prev_y = None;
            }
            Some(v) => {
                let y = top + if *v == 1 { HI } else { LO };
                match prev_y {
                    None => d.push_str(&format!("M {x0} {y} H {x1} ")),
                    Some(p) if p == y => d.push_str(&format!("H {x1} ")),
                    Some(_) => d.push_str(&format!("V {y} H {x1} ")),
                }
                prev_y = Some(y);
            }
        }
    }
    WaveRow { label, kind, top, d, dx }
}

/// Временная диаграмма по истории изменений: по строке на каждый вход и выход упражнения.
pub fn build_wave(samples: &[Sample], spec: &CircuitSpec) -> Wave {
    let mut rows: Vec<(String, RowKind, Vec<NodeValue>)> = Vec::new();
    for id in &spec.inputs {
        let kind = if spec.clock == Some(*id) { RowKind::Clk } else { RowKind::In };
        rows.push((spec.label_of(*id), kind, samples.iter().map(|s| s.inputs.get(id).copied()).collect()));
    }
    for o in &spec.outputs {
        rows.push((o.clone(), RowKind::Out, samples.iter().map(|s| s.outputs.get(o).copied().flatten()).collect()));
    }
    let rows: Vec<WaveRow> = rows
        .into_iter()
        .enumerate()
        .map(|(i, (label, kind, values))| wave_row(label, kind, i as f64 * ROW_H, &values))
        .collect();
    Wave {
        height: rows.len() as f64 * ROW_H,
        cols: (0..samples.len()).map(|i| LABEL_W + i as f64 * STEP).collect(),
        last_x: LABEL_W + (samples.len() as f64 - 1.0) * STEP,
        rows,
    }
}
