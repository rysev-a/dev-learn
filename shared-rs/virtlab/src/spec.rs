//! Описание упражнения как данные: какой симулятор, его сценарии и цели.
//!
//! [`Spec`] лежит в поле `spec` задачи файла главы ([`crate::LabChapter`]); интерфейс строит по нему симулятор,
//! а сервер перепроверяет по нему присланное решение ([`mod@crate::verify`]).

use std::collections::BTreeMap;

use serde::{Deserialize, Serialize};

use crate::error::SpecError;
use crate::goal::Goal;
use crate::{ept, hv, migration, numa, qcow2, virtq};

/// Идентификаторы упражнений книги 17 (они же `Task::id`).
pub const LAB_IDS: [&str; 6] =
    ["virt-sim-hv", "virt-sim-ept", "virt-sim-virtqueue", "virt-sim-qcow2", "virt-sim-migration", "virt-sim-numa"];

/// Кластер базового слоя qcow2 (в данных — списком, а не словарём: ключи-числа в JSON строками не нужны).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct BaseCluster {
    /// Номер кластера.
    pub cluster: u32,
    /// Данные.
    pub data: String,
}

/// Описание симулятора упражнения (поле `sim` — какой модуль).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(tag = "sim", rename_all = "snake_case")]
pub enum Spec {
    /// Мини-гипервизор (глава 2): программы гостя.
    Hv {
        /// Программы; цель — пройти каждую.
        programs: Vec<hv::Program>,
    },
    /// Трансляция адресов (глава 4): нагрузки и цели.
    Ept {
        /// Нагрузки.
        workloads: Vec<ept::Workload>,
        /// Цели.
        goals: Vec<ept::EptGoal>,
    },
    /// Очередь virtio (глава 6).
    Virtq {
        /// Число дескрипторов.
        size: u32,
        /// Цели.
        goals: Vec<virtq::VirtqGoal>,
    },
    /// Размещение по узлам NUMA (глава 11).
    Numa {
        /// Узлы хоста.
        nodes: Vec<numa::Node>,
        /// Сценарии; цель — принять размещение каждого.
        scenarios: Vec<numa::Scenario>,
    },
    /// Слои qcow2 (глава 9).
    Qcow2 {
        /// Число кластеров.
        clusters: u32,
        /// Кластеры базового слоя.
        base: Vec<BaseCluster>,
        /// Цели.
        goals: Vec<qcow2::Qcow2Goal>,
    },
    /// Живая миграция (глава 10).
    Migration {
        /// Сценарии; цель — достичь условия каждого.
        scenarios: Vec<migration::Scenario>,
    },
}

/// Базовый слой qcow2 списком → словарь.
pub fn base_map(base: &[BaseCluster]) -> BTreeMap<u32, String> {
    base.iter().map(|c| (c.cluster, c.data.clone())).collect()
}

fn unique(kind: &str, ids: impl Iterator<Item = String>) -> Result<(), SpecError> {
    let mut seen = std::collections::BTreeSet::new();
    for id in ids {
        if id.is_empty() {
            return Err(SpecError::new(format!("{kind}: пустой идентификатор")));
        }
        if !seen.insert(id.clone()) {
            return Err(SpecError::new(format!("{kind}: повтор идентификатора «{id}»")));
        }
    }
    Ok(())
}

impl Spec {
    /// Имя симулятора (значение поля `sim`).
    pub fn sim(&self) -> &'static str {
        match self {
            Spec::Hv { .. } => "hv",
            Spec::Ept { .. } => "ept",
            Spec::Virtq { .. } => "virtq",
            Spec::Numa { .. } => "numa",
            Spec::Qcow2 { .. } => "qcow2",
            Spec::Migration { .. } => "migration",
        }
    }

    /// Цели упражнения по порядку. Упражнение решено, когда достигнуты все.
    pub fn goals(&self) -> Vec<Goal> {
        match self {
            Spec::Hv { programs } => programs.iter().map(hv::Program::as_goal).collect(),
            Spec::Ept { goals, .. } => goals.iter().map(ept::EptGoal::as_goal).collect(),
            Spec::Virtq { goals, .. } => goals.iter().map(virtq::VirtqGoal::as_goal).collect(),
            Spec::Numa { scenarios, .. } => scenarios.iter().map(numa::Scenario::as_goal).collect(),
            Spec::Qcow2 { goals, .. } => goals.iter().map(qcow2::Qcow2Goal::as_goal).collect(),
            Spec::Migration { scenarios, .. } => scenarios.iter().map(migration::Scenario::as_goal).collect(),
        }
    }

    /// Проверка целостности данных: идентификаторы уникальны, ссылки на нагрузки есть, команды разбираются.
    pub fn validate(&self) -> Result<(), SpecError> {
        unique("цели", self.goals().into_iter().map(|g| g.id))?;
        if self.goals().is_empty() {
            return Err(SpecError::new("нет целей"));
        }
        match self {
            Spec::Hv { programs } => {
                for p in programs {
                    p.validate()?;
                }
            }
            Spec::Ept { workloads, goals } => {
                unique("нагрузки", workloads.iter().map(|w| w.id.clone()))?;
                for g in goals {
                    if !workloads.iter().any(|w| w.id == g.workload) {
                        return Err(SpecError::new(format!("цель {}: нет нагрузки «{}»", g.id, g.workload)));
                    }
                }
            }
            Spec::Virtq { size, .. } => {
                if *size == 0 {
                    return Err(SpecError::new("очередь без дескрипторов"));
                }
            }
            Spec::Numa { nodes, scenarios } => {
                if nodes.is_empty() || nodes.len() > 255 {
                    return Err(SpecError::new("число узлов должно быть от 1 до 255"));
                }
                for s in scenarios {
                    unique("машины", s.vms.iter().map(|v| v.name.clone()))?;
                    if !s.max.is_finite() || s.max < 0.0 {
                        return Err(SpecError::new(format!("сценарий {}: недопустимая доля", s.id)));
                    }
                }
            }
            Spec::Qcow2 { clusters, base, .. } => {
                if base.iter().any(|c| c.cluster >= *clusters) {
                    return Err(SpecError::new("кластер базового слоя вне диапазона"));
                }
            }
            Spec::Migration { scenarios } => {
                for s in scenarios {
                    if !(s.dirty.is_finite() && s.bw.is_finite() && s.bw > 0.0 && s.dirty >= 0.0) {
                        return Err(SpecError::new(format!("сценарий {}: недопустимые скорости", s.id)));
                    }
                }
            }
        }
        Ok(())
    }
}

/// Описание упражнения по умолчанию по его идентификатору (`virt-sim-…`).
pub fn builtin(id: &str) -> Option<Spec> {
    Some(match id {
        "virt-sim-hv" => Spec::Hv { programs: hv::default_programs() },
        "virt-sim-ept" => Spec::Ept { workloads: ept::default_workloads(), goals: ept::default_goals() },
        "virt-sim-virtqueue" => Spec::Virtq { size: virtq::SIZE, goals: virtq::default_goals() },
        "virt-sim-qcow2" => Spec::Qcow2 {
            clusters: qcow2::CLUSTERS,
            base: qcow2::default_base().into_iter().map(|(cluster, data)| BaseCluster { cluster, data }).collect(),
            goals: qcow2::default_goals(),
        },
        "virt-sim-migration" => Spec::Migration { scenarios: migration::default_scenarios() },
        "virt-sim-numa" => Spec::Numa { nodes: numa::default_nodes(), scenarios: numa::default_scenarios() },
        _ => return None,
    })
}
