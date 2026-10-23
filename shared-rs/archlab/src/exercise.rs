//! Упражнения лаборатории как данные: глава, задача, спецификация проверки.
//!
//! Файл данных — `backend/app/data/labs/arch/<книга>-<глава:02>.json` ([`LabChapter`]); поле `spec`
//! задачи содержит всё, что нужно клиенту и серверу. Эталонное решение (`solution`) бэкенд клиенту
//! не отдаёт — см. [`Task::for_client`].

use crate::blocks::{BlockInterface, BlockPort, Dir, Solution};
use crate::interfaces::Iface;
use crate::model::{Bit, GateType, InputId};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// Номер книги «Архитектура компьютера».
pub const ARCH_BOOK: u32 = 14;

/// Один файл данных: глава книги с упражнениями лаборатории.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct LabChapter {
    pub book: u32,
    pub chapter: u32,
    /// Всегда `"arch"` для этого крейта.
    pub lab: String,
    pub tasks: Vec<Task>,
}

/// Упражнение: заголовок, условие, подсказка и спецификация проверки.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Task {
    pub id: String,
    pub title: String,
    pub statement: String,
    pub hint: String,
    pub spec: Spec,
}

impl Task {
    /// Копия для клиента: без эталонного решения.
    pub fn for_client(&self) -> Task {
        let mut t = self.clone();
        match &mut t.spec {
            Spec::Circuit(c) => c.solution = None,
            Spec::Asm(a) => a.solution = String::new(),
        }
        t
    }
}

/// Спецификация упражнения: схема (главы 6–14) или программа ассемблера (глава 15).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
#[allow(clippy::large_enum_variant)]
pub enum Spec {
    Circuit(CircuitSpec),
    Asm(AsmSpec),
}

/// Как проверяется упражнение со схемой.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Mode {
    /// Сверка с таблицей истинности.
    Table,
    /// Пошаговый сценарий (последовательностная схема).
    Steps,
}

/// Из чего собирается решение.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Build {
    /// Из вентилей.
    Gates,
    /// Из готовых блоков, соединённых шинами.
    Blocks,
}

/// Один шаг сценария для последовательностных схем.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Step {
    /// Требуемое состояние тумблеров (перечислены все активные входы).
    pub inputs: BTreeMap<InputId, Bit>,
    /// Ожидаемые значения выходов; выход, которого здесь нет, на этом шаге не проверяется.
    pub expect: BTreeMap<String, Bit>,
    /// Пояснение шага.
    pub text: String,
    /// Сколько импульсов такта подать до этого шага (по умолчанию один; шаг с CLK = 0 — без такта).
    #[serde(default)]
    pub pulses: Option<u32>,
}

/// Группа узлов упражнения, объединённая в один порт заданного типа.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct PortDecl {
    pub name: String,
    #[serde(rename = "type")]
    pub ty: Iface,
    /// Узлы упражнения (входы A–F или имена выходов) по порядку бит типа: старший — первый.
    pub nodes: Vec<String>,
}

/// Решённое упражнение становится блоком с таким id.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BlockMeta {
    pub id: String,
    pub title: String,
}

/// Упражнение со схемой.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct CircuitSpec {
    /// Раздел (slug из реестра): `simple-circuits`, `mux`, …
    pub section: String,
    pub mode: Mode,
    pub build: Build,
    /// Входы на доске (физические узлы A–F).
    pub inputs: Vec<InputId>,
    /// Подписи входов (по порядку `inputs`); пусто — сами id.
    #[serde(default)]
    pub labels: Vec<String>,
    /// Имена выходов на доске.
    pub outputs: Vec<String>,
    /// Целевая таблица: строк 2^входов, в строке — по значению на каждый выход.
    #[serde(default)]
    pub target: Vec<Vec<Bit>>,
    /// Какие вентили доступны в палитре.
    #[serde(default)]
    pub allowed: Vec<GateType>,
    #[serde(default)]
    pub steps: Vec<Step>,
    #[serde(default)]
    pub ports: Vec<PortDecl>,
    #[serde(default)]
    pub block: Option<BlockMeta>,
    /// Какие блоки доступны в палитре (для `build = blocks`).
    #[serde(default)]
    pub blocks: Vec<String>,
    /// Какой из входов тактовый.
    #[serde(default)]
    pub clock: Option<InputId>,
    /// Шаги достигаются импульсами такта.
    #[serde(default)]
    pub ticks: bool,
    /// Формула для заголовка после победы.
    pub formula: String,
    /// Объяснение после победы.
    pub success: String,
    /// Эталонное решение — только на сервере.
    #[serde(default)]
    pub solution: Option<Solution>,
}

impl CircuitSpec {
    /// Подпись входа на доске.
    pub fn label_of(&self, id: InputId) -> String {
        let i = self.inputs.iter().position(|x| *x == id);
        i.and_then(|i| self.labels.get(i).cloned()).unwrap_or_else(|| id.as_str().to_string())
    }

    /// Подписи всех входов по порядку.
    pub fn labels_or_ids(&self) -> Vec<String> {
        self.inputs.iter().map(|i| self.label_of(*i)).collect()
    }

    /// Интерфейс упражнения: его узлы, сгруппированные в порты (`interfaceOfExercise`).
    pub fn interface(&self) -> BlockInterface {
        let inputs: Vec<String> = self.inputs.iter().map(|i| i.as_str().to_string()).collect();
        BlockInterface {
            labels: (!self.labels.is_empty()).then(|| self.labels.clone()),
            outputs: self.outputs.clone(),
            ports: self
                .ports
                .iter()
                .map(|p| BlockPort {
                    name: p.name.clone(),
                    ty: p.ty,
                    dir: if p.nodes.iter().all(|n| inputs.contains(n)) { Dir::In } else { Dir::Out },
                    nodes: p.nodes.clone(),
                })
                .collect(),
            inputs,
        }
    }
}

/// Область на диске, которую интерфейс подписывает над сеткой памяти.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct DiskRegion {
    pub name: String,
    pub from: usize,
    pub length: usize,
}

/// Байты как строка шестнадцатеричных пар (`"00ff"`) — компактно в JSON.
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct HexBytes(pub Vec<u8>);

impl Serialize for HexBytes {
    fn serialize<S: serde::Serializer>(&self, s: S) -> Result<S::Ok, S::Error> {
        let text: String = self.0.iter().map(|b| format!("{b:02x}")).collect();
        s.serialize_str(&text)
    }
}

impl<'de> Deserialize<'de> for HexBytes {
    fn deserialize<D: serde::Deserializer<'de>>(d: D) -> Result<Self, D::Error> {
        let text = String::deserialize(d)?;
        if text.len() % 2 != 0 || !text.is_ascii() {
            return Err(serde::de::Error::custom("нужна строка шестнадцатеричных пар"));
        }
        let bytes = (0..text.len() / 2)
            .map(|i| u8::from_str_radix(&text[2 * i..2 * i + 2], 16).map_err(serde::de::Error::custom))
            .collect::<Result<Vec<u8>, D::Error>>()?;
        Ok(HexBytes(bytes))
    }
}

/// Упражнение на ассемблере Мини-8: диск и ожидаемая память после остановки.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct AsmSpec {
    /// Заготовка программы.
    pub starter: String,
    /// Эталонное решение — только на сервере.
    #[serde(default)]
    pub solution: String,
    /// Исходное содержимое диска (256 байт).
    pub disk: HexBytes,
    /// Какой должна быть память после остановки (256 байт).
    pub expected: HexBytes,
    pub regions: Vec<DiskRegion>,
}
