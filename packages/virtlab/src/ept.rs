//! Модель трансляции адресов гостя (глава 4, «Память гостя»).
//!
//! Стоимость измеряется в обращениях к памяти. Теневые таблицы: промах TLB стоит обход одной таблицы (уровней столько,
//! сколько у наименьшей страницы), но каждое изменение отображения — выход ([`EXIT_COST`]). Вложенные EPT/NPT: промах
//! стоит `(g+1)*(h+1)-1` обращений, изменений гостя гипервизор не видит. Запись TLB описывает страницу наименьшего из двух
//! размеров: крупная страница гостя на мелкой страничке хозяина «дробится».
//!
//! Нагрузки и цели — данные ([`Workload`], [`EptGoal`]); цель привязана к нагрузке и проверяется по результату запуска
//! и настройкам.

use serde::{Deserialize, Serialize};

use crate::error::SpecError;
use crate::goal::Goal;

/// Размер страницы.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum PageSize {
    /// 4 КиБ.
    #[serde(rename = "4K")]
    K4,
    /// 2 МиБ.
    #[serde(rename = "2M")]
    M2,
    /// 1 ГиБ.
    #[serde(rename = "1G")]
    G1,
}

impl PageSize {
    /// Все размеры от меньшего к большему.
    pub const ALL: [PageSize; 3] = [PageSize::K4, PageSize::M2, PageSize::G1];

    /// Размер страницы в байтах.
    pub fn bytes(self) -> u64 {
        match self {
            PageSize::K4 => 4096,
            PageSize::M2 => 2 * 1024 * 1024,
            PageSize::G1 => 1024 * 1024 * 1024,
        }
    }

    /// Число уровней таблиц при обходе до страницы такого размера.
    pub fn levels(self) -> u32 {
        match self {
            PageSize::K4 => 4,
            PageSize::M2 => 3,
            PageSize::G1 => 2,
        }
    }
}

/// Режим трансляции.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Mode {
    /// Теневые таблицы.
    Shadow,
    /// Вложенные таблицы EPT/NPT.
    Ept,
}

/// Число записей TLB.
pub const TLB_ENTRIES: usize = 64;
/// Стоимость выхода в гипервизор (в обращениях к памяти).
pub const EXIT_COST: u64 = 1000;

fn smaller(a: PageSize, b: PageSize) -> PageSize {
    if a.bytes() <= b.bytes() {
        a
    } else {
        b
    }
}

/// Цена одного промаха TLB в обращениях к памяти (обход таблиц; без самого обращения к данным).
pub fn walk_cost(mode: Mode, guest: PageSize, host: PageSize) -> u32 {
    match mode {
        Mode::Shadow => smaller(guest, host).levels(),
        Mode::Ept => (guest.levels() + 1) * (host.levels() + 1) - 1,
    }
}

const MIB: u64 = 1024 * 1024;

/// Линейный конгруэнтный генератор (тот же, что в TypeScript: `Math.imul(x, 1664525) + 1013904223 >>> 0`).
fn lcg(seed: u32) -> impl FnMut() -> u32 {
    let mut x = seed;
    move || {
        x = x.wrapping_mul(1664525).wrapping_add(1013904223);
        x
    }
}

fn random_addrs(n: usize, span: u64, seed: u32) -> Vec<u64> {
    let mut r = lcg(seed);
    (0..n).map(|_| (u64::from(r()) % (span / 8)) * 8).collect()
}

/// Как строятся адреса обращений нагрузки.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum Access {
    /// Одно обращение по адресу.
    Single {
        /// Адрес.
        addr: u64,
    },
    /// `count` обращений подряд с шагом `step` байт.
    Stride {
        /// Число обращений.
        count: usize,
        /// Шаг в байтах.
        step: u64,
    },
    /// `count` случайных обращений (по 8 байт) в пределах `span_mib` МиБ; генератор — `seed`.
    Random {
        /// Число обращений.
        count: usize,
        /// Размах адресов, МиБ.
        span_mib: u64,
        /// Начальное значение генератора.
        seed: u32,
    },
}

/// Нагрузка: обращения гостя к памяти и число изменений отображения гостем.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Workload {
    /// Идентификатор.
    pub id: String,
    /// Название.
    pub title: String,
    /// Пояснение под выбором нагрузки.
    pub note: String,
    /// Адреса обращений.
    pub access: Access,
    /// Сколько раз гость меняет отображение (в теневых режимах каждое — выход).
    pub maps: u64,
}

/// Развёрнутая нагрузка.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Trace {
    /// Адреса обращений по порядку.
    pub addrs: Vec<u64>,
    /// Число изменений отображения.
    pub maps: u64,
}

impl Workload {
    /// Развернуть нагрузку в список адресов.
    pub fn make(&self) -> Trace {
        let addrs = match self.access {
            Access::Single { addr } => vec![addr],
            Access::Stride { count, step } => (0..count as u64).map(|i| i * step).collect(),
            Access::Random { count, span_mib, seed } => random_addrs(count, span_mib * MIB, seed),
        };
        Trace { addrs, maps: self.maps }
    }
}

/// Настройки запуска.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SimInput {
    /// Режим трансляции.
    pub mode: Mode,
    /// Размер страницы гостя.
    pub guest: PageSize,
    /// Размер страницы хозяина.
    pub host: PageSize,
    /// Идентификатор нагрузки.
    pub workload: String,
}

/// Результат запуска нагрузки.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SimRun {
    /// Цена одного промаха.
    pub walk: u32,
    /// Число обращений гостя.
    pub accesses: u64,
    /// Промахи TLB.
    pub misses: u64,
    /// Попадания в TLB.
    pub hits: u64,
    /// Выходы в гипервизор из-за правок таблиц.
    pub exits: u64,
    /// Всего обращений к памяти.
    pub cost: u64,
    /// Размер страницы, которую описывает запись TLB.
    pub eff_page: PageSize,
}

/// Запустить нагрузку `w` с настройками `mode`, `guest`, `host`.
pub fn simulate_workload(w: &Workload, mode: Mode, guest: PageSize, host: PageSize) -> SimRun {
    let trace = w.make();
    let eff = smaller(guest, host).bytes();
    let walk = walk_cost(mode, guest, host);
    let mut tlb: Vec<u64> = Vec::with_capacity(TLB_ENTRIES + 1);
    let mut misses = 0u64;
    let mut cost = 0u64;
    for &a in &trace.addrs {
        let p = a / eff;
        if let Some(i) = tlb.iter().position(|&x| x == p) {
            tlb.remove(i);
            cost += 1;
        } else {
            misses += 1;
            cost += u64::from(walk) + 1;
            if tlb.len() >= TLB_ENTRIES {
                tlb.remove(0);
            }
        }
        tlb.push(p);
    }
    let exits = if mode == Mode::Shadow { trace.maps } else { 0 };
    cost += exits * EXIT_COST;
    let accesses = trace.addrs.len() as u64;
    SimRun { walk, accesses, misses, hits: accesses - misses, exits, cost, eff_page: smaller(guest, host) }
}

/// Запустить нагрузку из списка по идентификатору.
pub fn simulate(workloads: &[Workload], input: &SimInput) -> Result<SimRun, SpecError> {
    let w = workloads
        .iter()
        .find(|w| w.id == input.workload)
        .ok_or_else(|| SpecError::new(format!("нет нагрузки «{}»", input.workload)))?;
    Ok(simulate_workload(w, input.mode, input.guest, input.host))
}

/// Цель: на своей нагрузке выполнены все заданные условия (незаданные не проверяются).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct EptGoal {
    /// Идентификатор цели.
    pub id: String,
    /// Текст цели.
    pub text: String,
    /// Нагрузка, на которой цель проверяется.
    pub workload: String,
    /// Требуемый режим.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub mode: Option<Mode>,
    /// Требуемый размер страницы гостя.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub guest: Option<PageSize>,
    /// Требуемый размер страницы хозяина.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub host: Option<PageSize>,
    /// Цена промаха не больше.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max_walk: Option<u32>,
    /// Общая стоимость не больше.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max_cost: Option<u64>,
}

impl EptGoal {
    /// Достигнута ли цель при запуске `r` с настройками `cfg` (нагрузка не проверяется — см. [`achieved`]).
    pub fn check(&self, r: &SimRun, cfg: &SimInput) -> bool {
        self.mode.is_none_or(|m| m == cfg.mode)
            && self.guest.is_none_or(|g| g == cfg.guest)
            && self.host.is_none_or(|h| h == cfg.host)
            && self.max_walk.is_none_or(|w| r.walk <= w)
            && self.max_cost.is_none_or(|c| r.cost <= c)
    }

    /// Цель для показа.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.text.clone())
    }
}

/// Цели, достигнутые запуском `input` (то же, что делает кнопка «Запустить нагрузку»).
pub fn achieved(workloads: &[Workload], goals: &[EptGoal], input: &SimInput) -> Result<Vec<String>, SpecError> {
    let r = simulate(workloads, input)?;
    Ok(goals.iter().filter(|g| g.workload == input.workload && g.check(&r, input)).map(|g| g.id.clone()).collect())
}

/// Нагрузки по умолчанию (упражнение главы 4).
pub fn default_workloads() -> Vec<Workload> {
    let w = |id: &str, title: &str, note: &str, access: Access, maps: u64| Workload {
        id: id.into(),
        title: title.into(),
        note: note.into(),
        access,
        maps,
    };
    vec![
        w("one", "Один промах TLB", "один доступ к памяти: смотрим цену обхода", Access::Single { addr: 0 }, 0),
        w(
            "scan",
            "Сканирование 8 МиБ",
            "2048 обращений подряд с шагом 4 КиБ",
            Access::Stride { count: 2048, step: 4096 },
            0,
        ),
        w(
            "random",
            "Случайные доступы по 64 МиБ",
            "4000 случайных обращений; TLB на 64 записи",
            Access::Random { count: 4000, span_mib: 64, seed: 7 },
            0,
        ),
        w(
            "fork",
            "Частые изменения таблиц",
            "500 изменений отображения гостем и 2000 случайных обращений по 1 ГиБ",
            Access::Random { count: 2000, span_mib: 1024, seed: 11 },
            500,
        ),
    ]
}

/// Цели по умолчанию (упражнение главы 4).
pub fn default_goals() -> Vec<EptGoal> {
    let g = |id: &str, text: &str, workload: &str| EptGoal {
        id: id.into(),
        text: text.into(),
        workload: workload.into(),
        mode: None,
        guest: None,
        host: None,
        max_walk: None,
        max_cost: None,
    };
    vec![
        EptGoal {
            mode: Some(Mode::Ept),
            max_walk: Some(15),
            ..g("walk", "Один промах стоит не больше 15 обращений (вложенные таблицы)", "one")
        },
        EptGoal {
            mode: Some(Mode::Shadow),
            guest: Some(PageSize::K4),
            host: Some(PageSize::K4),
            max_cost: Some(15000),
            ..g("scan", "Сканирование 8 МиБ в 4 КиБ-страницах дешевле, чем в EPT: не больше 15 000", "scan")
        },
        EptGoal {
            max_cost: Some(10000),
            ..g("random", "Случайные доступы по 64 МиБ укладываются в 10 000 обращений", "random")
        },
        EptGoal {
            max_cost: Some(35000), ..g("fork", "Частые изменения таблиц: не больше 35 000 обращений", "fork")
        },
    ]
}
