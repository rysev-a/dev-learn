//! Справочник компонентов: русские названия, настраиваемые параметры, значения по умолчанию, палитра.
//! Числа ёмкости, цен и задержек — в [`crate::reference`].

use std::collections::BTreeMap;
use std::sync::LazyLock;

use serde::Serialize;

use crate::types::{Kind, ParamValue};

/// Тип поля параметра в панели компонента.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "lowercase")]
pub enum ParamType {
    Int,
    Select,
    Bool,
}

/// Вариант выбора.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct ParamOption {
    pub value: ParamValue,
    pub label: &'static str,
}

/// Описание параметра компонента.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct ParamSpec {
    pub key: &'static str,
    pub label: &'static str,
    #[serde(rename = "type")]
    pub ty: ParamType,
    pub min: Option<f64>,
    pub max: Option<f64>,
    pub options: Vec<ParamOption>,
    pub default: ParamValue,
    /// подсказка под полем
    pub help: Option<&'static str>,
    /// `false` — показывается только в упражнениях, где параметр перечислен в `show`
    pub basic: bool,
    /// движок параметр не читает: он нужен только для целей `param` (метка «как устроено», не рычаг расчёта)
    pub inert: bool,
}

impl ParamSpec {
    fn int(key: &'static str, label: &'static str, min: i32, max: i32, default: i32) -> ParamSpec {
        ParamSpec {
            key,
            label,
            ty: ParamType::Int,
            min: Some(f64::from(min)),
            max: Some(f64::from(max)),
            options: Vec::new(),
            default: default.into(),
            help: None,
            basic: true,
            inert: false,
        }
    }

    fn select(key: &'static str, label: &'static str, options: &[(ParamValue, &'static str)], default: ParamValue) -> ParamSpec {
        ParamSpec {
            key,
            label,
            ty: ParamType::Select,
            min: None,
            max: None,
            options: options.iter().map(|(v, l)| ParamOption { value: v.clone(), label: l }).collect(),
            default,
            help: None,
            basic: true,
            inert: false,
        }
    }

    fn flag(key: &'static str, label: &'static str) -> ParamSpec {
        ParamSpec { key, label, ty: ParamType::Bool, min: None, max: None, options: Vec::new(), default: false.into(), help: None, basic: true, inert: false }
    }

    fn help(mut self, h: &'static str) -> ParamSpec {
        self.help = Some(h);
        self
    }

    /// Параметр, который движок не читает (см. [`ParamSpec::inert`]).
    fn inert(mut self) -> ParamSpec {
        self.inert = true;
        self
    }

    /// Дополнительный параметр: виден только в упражнениях с ним в `show`.
    fn advanced(mut self) -> ParamSpec {
        self.basic = false;
        self
    }
}

/// Описание вида компонента.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct KindSpec {
    pub kind: Kind,
    pub label: &'static str,
    /// одна строка: чем занимается компонент
    pub about: &'static str,
    pub params: Vec<ParamSpec>,
    /// колонка раскладки слева направо
    pub col: usize,
}

fn s(v: &'static str) -> ParamValue {
    ParamValue::Str(v.to_owned())
}

fn n(v: i32) -> ParamValue {
    ParamValue::Num(f64::from(v))
}

fn size() -> ParamSpec {
    ParamSpec::select("size", "Размер", &[(s("S"), "S — малый"), (s("M"), "M — средний"), (s("L"), "L — большой")], s("S"))
}

fn zone() -> ParamSpec {
    ParamSpec::select(
        "zone",
        "Размещение",
        &[(s("single"), "одна зона"), (s("multi"), "три зоны региона"), (s("regions"), "два региона")],
        s("single"),
    )
    .help("отказ зоны: «одна зона» теряет всё, остальные — треть; отказ региона: два региона теряют половину")
}

fn ttl() -> ParamSpec {
    ParamSpec::select("ttl", "TTL, с", &[(n(30), "30"), (n(300), "300"), (n(3600), "3600")], n(300))
}

fn pricing(spot: &'static str) -> ParamSpec {
    ParamSpec::select(
        "pricing",
        "Тариф",
        &[(s("ondemand"), "по требованию"), (s("reserved"), "резерв (−40%)"), (s("spot"), spot)],
        s("ondemand"),
    )
    .advanced()
}

fn instances(max: i32) -> ParamSpec {
    ParamSpec::int("instances", "Экземпляры", 1, max, 1)
}

fn mk(kind: Kind, label: &'static str, about: &'static str, col: usize, params: Vec<ParamSpec>) -> KindSpec {
    KindSpec { kind, label, about, params, col }
}

fn build() -> Vec<KindSpec> {
    // порядок — как в `Kind::ALL`
    let mut v = vec![
        mk(Kind::Clients, "Пользователи", "источник нагрузки", 0, vec![]),
        mk(Kind::Cdn, "CDN", "раздаёт статику с ближайших серверов", 1, vec![ttl().help("чем больше TTL, тем выше доля попаданий")]),
        mk(Kind::Lb, "Балансировщик", "делит запросы между серверами", 3, vec![
            ParamSpec::int("instances", "Экземпляры", 1, 3, 1),
            ParamSpec::select("layer", "Уровень", &[(s("L4"), "L4 (TCP)"), (s("L7"), "L7 (HTTP)")], s("L4")),
        ]),
        mk(Kind::Gateway, "API-шлюз", "вход: авторизация, маршрутизация, лимиты", 2, vec![ParamSpec::int("instances", "Экземпляры", 1, 4, 1)]),
        mk(Kind::Limiter, "Ограничитель", "пропускает не больше N запросов в секунду", 2, vec![ParamSpec::int("limit", "Предел, запр/с", 100, 50000, 2000)]),
        mk(Kind::App, "Сервер приложения", "бизнес-логика без состояния", 4, vec![
            // верхний предел 40, а не 30, как в TypeScript-версии: эталоны итоговых заданий (глав 22–24) требуют 33–35 серверов
            instances(40),
            size(),
            ParamSpec::select("sessions", "Сессии", &[(s("local"), "в памяти сервера"), (s("external"), "во внешнем хранилище")], s("local")),
            zone(),
            ParamSpec::int("weight", "Доля трафика", 1, 10, 1).advanced().help("вес сервиса при делении трафика между сервисами"),
            ParamSpec::flag("idempotency", "Ключи идемпотентности").advanced().inert(),
            ParamSpec::int("retries", "Повторы к БД", 0, 3, 0).advanced().help("повторы без паузы усиливают перегрузку"),
            ParamSpec::flag("breaker", "Автомат разрыва").advanced().help("обрывает повторы, когда база перегружена"),
            ParamSpec::select(
                "feed",
                "Лента",
                &[(s("pull"), "pull — собирать при чтении"), (s("push"), "push — раскладывать при записи"), (s("hybrid"), "гибрид")],
                s("pull"),
            )
            .advanced(),
            ParamSpec::select(
                "deploy",
                "Выкладка",
                &[(s("all"), "всё сразу"), (s("rolling"), "по одному (rolling)"), (s("bluegreen"), "blue/green")],
                s("all"),
            )
            .advanced()
            .help("blue/green держит вторую копию — расход ×2"),
            pricing("спот (−70%, прерывается)"),
        ]),
        mk(Kind::Cache, "Кэш", "быстрая память для горячих данных", 5, vec![
            ParamSpec::int("size_gb", "Память, ГБ", 1, 128, 4),
            ttl(),
            ParamSpec::select(
                "policy",
                "Политика записи",
                &[(s("aside"), "cache-aside"), (s("through"), "write-through"), (s("back"), "write-back")],
                s("aside"),
            )
            .help("write-back снимает нагрузку записи с БД, но данные могут пропасть")
            .advanced(),
            ParamSpec::int("replicas", "Реплики", 0, 2, 0),
            zone(),
        ]),
        mk(Kind::Db, "База данных", "постоянное хранилище", 7, vec![
            size(),
            ParamSpec::int("replicas", "Реплики на шард", 0, 5, 0),
            ParamSpec::int("shards", "Шарды", 1, 16, 1),
            ParamSpec::flag("failover", "Автопереключение").help("при отказе лидера реплика занимает его место"),
            ParamSpec::select("engine", "Тип", &[(s("sql"), "SQL"), (s("nosql"), "NoSQL")], s("sql")),
            ParamSpec::select("sync", "Репликация", &[(s("async"), "асинхронная"), (s("sync"), "синхронная")], s("async"))
                .advanced()
                .help("синхронная: реплики не отстают, но запись медленнее"),
            ParamSpec::select("shard_key", "Ключ шардирования", &[(s("hash"), "хеш"), (s("range"), "диапазон")], s("hash")).advanced(),
            zone(),
        ]),
        mk(Kind::Queue, "Очередь", "буфер между производителями и обработчиками", 5, vec![
            ParamSpec::int("partitions", "Партиции", 1, 16, 1),
            ParamSpec::flag("dlq", "Очередь недоставленных").advanced().inert(),
        ]),
        mk(Kind::Worker, "Обработчик", "разбирает очередь", 6, vec![
            instances(30),
            ParamSpec::select("size", "Размер", &[(s("S"), "S — малый"), (s("M"), "M — средний")], s("S")),
            zone(),
            ParamSpec::flag("idempotent", "Идемпотентная обработка").advanced().inert().help("повторная доставка не портит данные"),
            pricing("спот (−70%)"),
        ]),
        mk(Kind::Blob, "Объектное хранилище", "файлы и медиа", 7, vec![ParamSpec::select(
            "tier",
            "Класс хранения",
            &[(s("hot"), "горячее ($23/ТБ)"), (s("mix"), "горячее + холодное ($10/ТБ)"), (s("cold"), "холодное ($4/ТБ)")],
            s("hot"),
        )
        .advanced()
        .help("холодное дешевле, но доступ к объектам медленнее")]),
        mk(Kind::Search, "Поиск", "полнотекстовый индекс", 7, vec![
            ParamSpec::int("shards", "Шарды", 1, 16, 1),
            ParamSpec::int("replicas", "Реплики", 1, 6, 1),
        ]),
        mk(Kind::Ws, "WebSocket-шлюз", "держит постоянные соединения", 3, vec![instances(40)]),
        mk(Kind::Monitor, "Мониторинг", "метрики, журналы, оповещения", 6, vec![]),
        mk(Kind::Auth, "Сервис входа", "аутентификация и права: проверка токенов и сессий", 5, vec![instances(20)]),
        mk(Kind::Geo, "Геосервис", "геопоиск и положения в памяти: ближайшие водители, курьеры, рестораны", 5, vec![instances(30)]),
        mk(Kind::Ml, "Сервис ранжирования", "модель рекомендаций и оценок: дорогие вычисления на запрос", 5, vec![instances(20)]),
        mk(Kind::Pay, "Платёжный шлюз", "внешний платёжный провайдер: медленный и дорогой вызов", 5, vec![ParamSpec::int("instances", "Каналы провайдера", 1, 4, 1)]),
        mk(Kind::Stream, "Поток событий", "журнал событий с партициями: каждый потребитель получает свою копию", 5, vec![ParamSpec::int("partitions", "Партиции", 1, 32, 1)]),
        mk(Kind::Notify, "Уведомления", "рассылка пушей и писем из очереди или потока", 6, vec![instances(20)]),
        mk(Kind::Analytics, "Аналитика", "хранилище событий для отчётов и метрик продукта", 6, vec![instances(10)]),
    ];
    // приводим к порядку Kind::ALL
    v.sort_by_key(|k| k.kind.index());
    v
}

static SPECS: LazyLock<Vec<KindSpec>> = LazyLock::new(build);

/// Описание вида компонента.
pub fn spec(kind: Kind) -> &'static KindSpec {
    // порядок в SPECS совпадает с Kind::ALL (build сортирует по индексу вида)
    &SPECS[kind.index()]
}

/// Описания всех видов в порядке [`Kind::ALL`].
pub fn all_specs() -> &'static [KindSpec] {
    &SPECS
}

/// Описание параметра вида по ключу.
pub fn param_spec(kind: Kind, key: &str) -> Option<&'static ParamSpec> {
    spec(kind).params.iter().find(|p| p.key == key)
}

/// Значение параметра по умолчанию.
pub fn default_param(kind: Kind, key: &str) -> Option<&'static ParamValue> {
    param_spec(kind, key).map(|p| &p.default)
}

/// Параметры нового компонента: все значения по умолчанию.
pub fn default_params(kind: Kind) -> BTreeMap<String, ParamValue> {
    spec(kind).params.iter().map(|p| (p.key.to_owned(), p.default.clone())).collect()
}

/// Порядок компонентов в палитре.
pub const KIND_ORDER: [Kind; 20] = [
    Kind::Cdn,
    Kind::Limiter,
    Kind::Gateway,
    Kind::Lb,
    Kind::Ws,
    Kind::App,
    Kind::Cache,
    Kind::Queue,
    Kind::Worker,
    Kind::Db,
    Kind::Blob,
    Kind::Search,
    Kind::Auth,
    Kind::Geo,
    Kind::Ml,
    Kind::Pay,
    Kind::Stream,
    Kind::Notify,
    Kind::Analytics,
    Kind::Monitor,
];

/// Ключ параметра в современной записи: прежние `sizeGB` и `shardKey` из TypeScript-версии переводятся в `size_gb` и `shard_key`.
pub fn canonical_param_key(key: &str) -> &str {
    match key {
        "sizeGB" => "size_gb",
        "shardKey" => "shard_key",
        other => other,
    }
}

/// Запись из списка `show` (`"db.shardKey"`) в современной записи (`"db.shard_key"`).
pub fn canonical_show_key(entry: &str) -> String {
    match entry.split_once('.') {
        Some((kind, key)) => format!("{kind}.{}", canonical_param_key(key)),
        None => entry.to_owned(),
    }
}
