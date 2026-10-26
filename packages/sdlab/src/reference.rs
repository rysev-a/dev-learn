//! Справочник чисел модели: ёмкость, цены, доступность и задержки компонентов (его же показывает справка в лаборатории).
//! Единицы: ёмкость — условных запросов в секунду на экземпляр, цена — $ в месяц, задержка — мс.

/// Размер экземпляра.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Size {
    S,
    M,
    L,
}

impl Size {
    /// Размер из значения параметра `size`; пустое или неизвестное — `S`.
    pub fn parse(s: &str) -> Size {
        match s {
            "M" => Size::M,
            "L" => Size::L,
            _ => Size::S,
        }
    }
}

/// Значение по размерам S/M/L.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct BySize {
    pub s: f64,
    pub m: f64,
    pub l: f64,
}

impl BySize {
    pub const fn new(s: f64, m: f64, l: f64) -> BySize {
        BySize { s, m, l }
    }
    pub fn get(&self, size: Size) -> f64 {
        match size {
            Size::S => self.s,
            Size::M => self.m,
            Size::L => self.l,
        }
    }
}

/// Класс хранения объектов.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Tier {
    /// цена за ТБ в месяц
    pub price: f64,
    /// задержка доступа, мс
    pub lat: f64,
}

/// Ёмкость, цена и доступность простого компонента.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Basic {
    pub cap: f64,
    pub cost: f64,
    pub avail: f64,
}

/// Задержки узлов, мс.
pub mod lat {
    pub const CDN: f64 = 12.0;
    pub const LIMITER: f64 = 1.0;
    pub const GATEWAY: f64 = 4.0;
    pub const LB_L4: f64 = 1.5;
    pub const LB_L7: f64 = 3.0;
    pub const WS: f64 = 5.0;
    pub const APP: f64 = 25.0;
    pub const APP_STATIC: f64 = 6.0;
    pub const CACHE: f64 = 1.5;
    pub const QUEUE: f64 = 4.0;
    pub const BLOB: f64 = 45.0;
    pub const SEARCH: f64 = 30.0;
    pub const DB_READ: f64 = 9.0;
    pub const DB_WRITE: f64 = 16.0;
    pub const AUTH: f64 = 6.0;
    pub const GEO: f64 = 4.0;
    pub const ML: f64 = 35.0;
    pub const PAY: f64 = 180.0;
}

pub const APP_CAP: BySize = BySize::new(300.0, 700.0, 1500.0);
pub const APP_COST: BySize = BySize::new(60.0, 120.0, 240.0);
pub const APP_AVAIL: f64 = 0.995;
pub const LB: Basic = Basic { cap: 20000.0, cost: 25.0, avail: 0.9995 };
pub const GATEWAY: Basic = Basic { cap: 8000.0, cost: 40.0, avail: 0.999 };
pub const LIMITER: Basic = Basic { cap: 100000.0, cost: 15.0, avail: 0.9995 };
pub const CDN: Basic = Basic { cap: 1000000.0, cost: 60.0, avail: 0.9999 };
/// Кэш: ёмкость узла, цена за ГБ, доступность.
pub const CACHE_CAP: f64 = 60000.0;
pub const CACHE_COST_PER_GB: f64 = 12.0;
pub const DB_READ: BySize = BySize::new(1000.0, 3000.0, 8000.0);
pub const DB_WRITE: BySize = BySize::new(200.0, 600.0, 1500.0);
pub const DB_COST: BySize = BySize::new(100.0, 250.0, 600.0);
pub const DB_AVAIL: f64 = 0.999;
/// Во сколько раз NoSQL быстрее SQL.
pub const DB_NOSQL: f64 = 1.8;
pub const QUEUE_CAP_PER_PARTITION: f64 = 20000.0;
pub const QUEUE_COST: f64 = 60.0;
pub const QUEUE_COST_PER_PARTITION: f64 = 10.0;
pub const QUEUE_AVAIL: f64 = 0.9995;
pub const WORKER_CAP: BySize = BySize::new(150.0, 400.0, 400.0);
pub const WORKER_COST: BySize = BySize::new(40.0, 80.0, 80.0);
pub const WORKER_AVAIL: f64 = 0.995;
pub const BLOB: Basic = Basic { cap: 100000.0, cost: 25.0, avail: 0.9999 };
pub const AUTH: Basic = Basic { cap: 4000.0, cost: 50.0, avail: 0.999 };
pub const GEO: Basic = Basic { cap: 6000.0, cost: 90.0, avail: 0.999 };
pub const ML: Basic = Basic { cap: 300.0, cost: 200.0, avail: 0.995 };
pub const PAY: Basic = Basic { cap: 400.0, cost: 40.0, avail: 0.999 };
pub const NOTIFY: Basic = Basic { cap: 1500.0, cost: 45.0, avail: 0.999 };
pub const ANALYTICS: Basic = Basic { cap: 6000.0, cost: 140.0, avail: 0.999 };
pub const STREAM_CAP_PER_PARTITION: f64 = 50000.0;
pub const STREAM_COST: f64 = 100.0;
pub const STREAM_COST_PER_PARTITION: f64 = 15.0;
pub const STREAM_AVAIL: f64 = 0.9999;
pub const SEARCH_CAP: f64 = 1200.0;
pub const SEARCH_COST: f64 = 150.0;
pub const SEARCH_MAX_GB_PER_SHARD: f64 = 40.0;
pub const SEARCH_AVAIL: f64 = 0.999;
pub const WS: Basic = Basic { cap: 15000.0, cost: 90.0, avail: 0.995 };
pub const MONITOR_COST: f64 = 40.0;
/// Вес статического запроса, обслуженного самим приложением.
pub const STATIC_WEIGHT: f64 = 0.1;
/// Во сколько раз тяжелее запрос «поиск» в базе без индекса.
pub const HEAVY_SEARCH: f64 = 5.0;
/// Какую долю записей оставляет в БД write-back кэш.
pub const WRITE_BACK: f64 = 0.4;

/// Класс хранения объектов по значению параметра `tier` (`hot`, `mix`, `cold`).
pub fn blob_tier(tier: &str) -> Option<Tier> {
    match tier {
        "hot" => Some(Tier { price: 23.0, lat: 45.0 }),
        "mix" => Some(Tier { price: 10.0, lat: 70.0 }),
        "cold" => Some(Tier { price: 4.0, lat: 150.0 }),
        _ => None,
    }
}

/// Множитель цены тарифа (`ondemand`, `reserved`, `spot`); неизвестный — 1.
pub fn price_factor(pricing: &str) -> f64 {
    match pricing {
        "reserved" => 0.6,
        "spot" => 0.3,
        _ => 1.0,
    }
}
