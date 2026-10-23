//! Модель живой миграции (глава 10).
//!
//! Единицы: память — МиБ, время — секунды, простой — миллисекунды. Круг pre-copy передаёт остаток, за это время гость
//! портит `dirty * время` МиБ (не больше всей памяти) — это и есть следующий остаток. Миграция сходится, когда остаток
//! помещается в допустимый простой.
//!
//! Сценарий ([`Scenario`]) задаёт скорость записи гостя и сети и цель (условие [`MigrationGoal`]); остальное подбирает
//! ученик ([`MigrationInput`]). Цель сценария проверяется по результату запуска.

use serde::{Deserialize, Serialize};

use crate::goal::Goal;

/// Память гостя, МиБ (16 ГиБ).
pub const MEM_MIB: f64 = 16384.0;
/// Передача состояния процессоров и устройств при остановке, мс.
pub const STATE_MS: f64 = 20.0;
/// Предел кругов pre-copy.
pub const MAX_ROUNDS: u32 = 12;
/// Условный выигрыш канала от сжатия (нулевые страницы и дельты).
pub const COMPRESS_FACTOR: f64 = 1.5;

/// Параметры миграции (формат полей — как в прежнем TypeScript-клиенте: `downtimeMs`, `autoConverge`, `postcopyAfter`).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct MigrationInput {
    /// Скорость записи гостя, МиБ/с.
    pub dirty: f64,
    /// Пропускная способность сети, МиБ/с.
    pub bw: f64,
    /// Допустимый простой, мс.
    pub downtime_ms: f64,
    /// Притормаживать vCPU (старт 20%, +10% за круг, не больше 99%).
    #[serde(default)]
    pub auto_converge: bool,
    /// Сжатие страниц.
    #[serde(default)]
    pub compress: bool,
    /// `None` — только pre-copy, иначе число кругов pre-copy до переключения на post-copy.
    #[serde(default)]
    pub postcopy_after: Option<u32>,
    /// Память гостя, МиБ (по умолчанию [`MEM_MIB`]).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub mem: Option<f64>,
}

/// Чем кончилась миграция.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Outcome {
    /// Остаток поместился в простой: обычная pre-copy.
    Precopy,
    /// Переключились на post-copy.
    Postcopy,
    /// Круги кончились, остановка с большим остатком.
    Failed,
}

/// Один круг pre-copy.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Round {
    /// Номер круга (с 1).
    pub k: u32,
    /// Передано в этом круге, МиБ.
    pub sent: f64,
    /// Длительность круга, с.
    pub secs: f64,
    /// Замедление vCPU, %.
    pub throttle: f64,
    /// Остаток после круга, МиБ.
    pub next: f64,
}

/// Результат симуляции.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Simulation {
    /// Исход.
    pub outcome: Outcome,
    /// Круги pre-copy.
    pub rounds: Vec<Round>,
    /// Остаток к моменту остановки/переключения, МиБ.
    pub remaining: f64,
    /// Простой, мс (округлён).
    pub downtime: u64,
    /// Общее время миграции, с (округлено до десятых).
    pub total: f64,
    /// Условное число ошибок страниц при post-copy.
    pub faults: u64,
    /// Порог остановки: сколько МиБ успевает уйти за допустимый простой.
    pub limit: f64,
}

/// Симулировать миграцию.
pub fn simulate(input: &MigrationInput) -> Simulation {
    let mem = input.mem.unwrap_or(MEM_MIB);
    let eff = input.bw * if input.compress { COMPRESS_FACTOR } else { 1.0 };
    let limit = (eff * input.downtime_ms) / 1000.0; // сколько МиБ можно передать за допустимый простой
    let mut rounds: Vec<Round> = vec![];
    let mut remaining = mem;
    let mut elapsed = 0.0;
    let mut throttle = 0.0;
    let mut switched = false;

    for k in 1..=MAX_ROUNDS {
        if remaining <= limit {
            break;
        }
        if let Some(after) = input.postcopy_after {
            if k > after {
                switched = true;
                break;
            }
        }
        let secs = remaining / eff;
        if input.auto_converge && k >= 2 {
            throttle = f64::min(99.0, 20.0 + 10.0 * f64::from(k - 2));
        }
        let rate = input.dirty * (1.0 - throttle / 100.0);
        let next = f64::min(mem, rate * secs);
        rounds.push(Round { k, sent: remaining, secs, throttle, next });
        elapsed += secs;
        remaining = next;
    }

    let fit = remaining <= limit;
    let (outcome, downtime, total, faults);
    if fit {
        outcome = Outcome::Precopy;
        downtime = (remaining / eff) * 1000.0 + STATE_MS;
        total = elapsed + downtime / 1000.0;
        faults = 0.0;
    } else if switched {
        // гость уже на цели, страницы подтягиваются по требованию и фоном
        outcome = Outcome::Postcopy;
        downtime = STATE_MS;
        total = elapsed + remaining / eff;
        faults = (remaining / 64.0).round(); // условно: одна ошибка на 64 МиБ остатка
    } else {
        // предел кругов исчерпан: машину всё равно приходится остановить с большим остатком
        outcome = Outcome::Failed;
        downtime = (remaining / eff) * 1000.0 + STATE_MS;
        total = elapsed + downtime / 1000.0;
        faults = 0.0;
    }
    Simulation {
        outcome,
        rounds,
        remaining,
        downtime: downtime.round() as u64,
        total: (total * 10.0).round() / 10.0,
        faults: faults as u64,
        limit,
    }
}

/// Условие достижения цели сценария по результату симуляции (незаданные не проверяются).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct MigrationGoal {
    /// Требуемый исход.
    pub outcome: Outcome,
    /// Простой не больше, мс.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max_downtime: Option<u64>,
    /// Общее время не больше, с.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max_total: Option<f64>,
}

impl MigrationGoal {
    /// Достигнута ли цель на результате `r`.
    pub fn check(&self, r: &Simulation) -> bool {
        r.outcome == self.outcome
            && self.max_downtime.is_none_or(|d| r.downtime <= d)
            && self.max_total.is_none_or(|t| r.total <= t)
    }
}

/// Сценарий: скорости гостя и сети заданы, остальное подбирает ученик.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Scenario {
    /// Идентификатор (он же идентификатор цели).
    pub id: String,
    /// Название вкладки.
    pub title: String,
    /// Скорость записи гостя, МиБ/с.
    pub dirty: f64,
    /// Пропускная способность сети, МиБ/с.
    pub bw: f64,
    /// Текст цели.
    pub goal: String,
    /// Подсказка сценария.
    pub hint: String,
    /// Условие достижения цели.
    pub check: MigrationGoal,
}

impl Scenario {
    /// Цель упражнения по этому сценарию.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.goal.clone())
    }

    /// Параметры запуска: скорости сценария и настройки ученика.
    pub fn input(
        &self,
        downtime_ms: f64,
        auto_converge: bool,
        compress: bool,
        postcopy_after: Option<u32>,
    ) -> MigrationInput {
        MigrationInput {
            dirty: self.dirty,
            bw: self.bw,
            downtime_ms,
            auto_converge,
            compress,
            postcopy_after,
            mem: None,
        }
    }

    /// Достигнута ли цель сценария запуском с настройками `input` (скорости берутся из сценария, не из `input`).
    pub fn reached(&self, input: &MigrationInput) -> bool {
        let p = MigrationInput { dirty: self.dirty, bw: self.bw, ..input.clone() };
        self.check.check(&simulate(&p))
    }
}

/// Сценарии по умолчанию (упражнение главы 10).
pub fn default_scenarios() -> Vec<Scenario> {
    vec![
        Scenario {
            id: "calm".into(),
            title: "Спокойный гость".into(),
            dirty: 300.0,
            bw: 1250.0,
            goal: "Pre-copy сошёлся, простой не больше 100 мс".into(),
            hint: "Допустимый простой — это порог остановки: чем он меньше, тем больше кругов, но тем короче пауза."
                .into(),
            check: MigrationGoal { outcome: Outcome::Precopy, max_downtime: Some(100), max_total: None },
        },
        Scenario {
            id: "busy".into(),
            title: "Активный гость".into(),
            dirty: 2000.0,
            bw: 1250.0,
            goal: "Без post-copy: миграция сошлась, простой не больше 600 мс".into(),
            hint: "Гость пишет быстрее, чем уходит по сети, — остаток не уменьшается. Нужно притормозить vCPU.".into(),
            check: MigrationGoal { outcome: Outcome::Precopy, max_downtime: Some(600), max_total: None },
        },
        Scenario {
            id: "wild".into(),
            title: "Очень активный гость".into(),
            dirty: 6000.0,
            bw: 1250.0,
            goal: "Гибрид: простой не больше 100 мс, общее время не больше 60 с".into(),
            hint: "Переключайтесь на post-copy раньше: каждый круг pre-copy здесь стоит около 13 секунд.".into(),
            check: MigrationGoal { outcome: Outcome::Postcopy, max_downtime: Some(100), max_total: Some(60.0) },
        },
    ]
}
