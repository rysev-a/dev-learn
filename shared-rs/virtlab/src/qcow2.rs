//! Модель цепочки слоёв qcow2 (глава 9).
//!
//! Цепочка — вектор слоёв от верхнего (текущего, в него идут все записи) к базовому. Чтение идёт вниз до первого слоя,
//! где кластер есть; каждая проверка слоя — обращение к таблицам. Снимок — новый пустой верхний слой. Слияние (commit)
//! переносит кластеры верхнего слоя в нижний. Откат отбрасывает верхний слой.
//!
//! Цели зависят от истории действий ([`Qcow2Rule`]): глубокое чтение, сокращение цепочки, откат записей. Историю ведёт
//! [`Session`] (то же, что `Qcow2Lab.tsx`); для серверной перепроверки действия записываются как [`Action`]
//! и воспроизводятся [`replay`].

use std::collections::BTreeMap;

use serde::{Deserialize, Serialize};

use crate::goal::Goal;

/// Число кластеров в упражнении.
pub const CLUSTERS: u32 = 8;

/// Слой: кластеры, которые в нём выделены (номер → данные).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Layer {
    /// Название слоя.
    pub name: String,
    /// Выделенные кластеры.
    pub data: BTreeMap<u32, String>,
}

/// Цепочка из одного базового слоя с кластерами `base`.
pub fn initial_chain(base: &BTreeMap<u32, String>) -> Vec<Layer> {
    vec![Layer { name: "база".into(), data: base.clone() }]
}

/// Снимок: сверху добавляется пустой слой «слой n».
pub fn snapshot(chain: &[Layer], n: u32) -> Vec<Layer> {
    let mut v = Vec::with_capacity(chain.len() + 1);
    v.push(Layer { name: format!("слой {n}"), data: BTreeMap::new() });
    v.extend_from_slice(chain);
    v
}

/// Запись данных `d` в кластер `c`: идёт в верхний слой; `copy_up` — кластер уже лежал ниже или выше (копирование при записи).
pub fn write(chain: &[Layer], c: u32, d: &str) -> (Vec<Layer>, bool) {
    let Some((top, rest)) = chain.split_first() else {
        return (vec![], false);
    };
    let below = rest.iter().any(|l| l.data.contains_key(&c)) || top.data.contains_key(&c);
    let mut top = top.clone();
    top.data.insert(c, d.to_string());
    let mut v = Vec::with_capacity(chain.len());
    v.push(top);
    v.extend_from_slice(rest);
    (v, below)
}

/// Результат чтения кластера.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ReadResult {
    /// Данные (нет ни в одном слое — читаются нули, `None`).
    pub value: Option<String>,
    /// Глубина слоя, где найден кластер (0 — верхний).
    pub depth: Option<usize>,
    /// Обращений к таблицам слоёв.
    pub lookups: usize,
    /// Название слоя, где найден кластер.
    pub layer: Option<String>,
}

/// Прочитать кластер `c` вниз по цепочке.
pub fn read(chain: &[Layer], c: u32) -> ReadResult {
    for (i, l) in chain.iter().enumerate() {
        if let Some(v) = l.data.get(&c) {
            return ReadResult { value: Some(v.clone()), depth: Some(i), lookups: i + 1, layer: Some(l.name.clone()) };
        }
    }
    ReadResult { value: None, depth: None, lookups: chain.len(), layer: None }
}

/// Слияние: кластеры верхнего слоя переносятся в нижний; `None` — слой всего один.
pub fn commit(chain: &[Layer]) -> Option<Vec<Layer>> {
    if chain.len() < 2 {
        return None;
    }
    let mut next = chain[1].clone();
    for (k, v) in &chain[0].data {
        next.data.insert(*k, v.clone());
    }
    let mut v = Vec::with_capacity(chain.len() - 1);
    v.push(next);
    v.extend_from_slice(&chain[2..]);
    Some(v)
}

/// Откат: верхний слой отбрасывается; `None` — слой всего один.
pub fn revert(chain: &[Layer]) -> Option<Vec<Layer>> {
    if chain.len() < 2 {
        return None;
    }
    Some(chain[1..].to_vec())
}

/// Правило цели.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum Qcow2Rule {
    /// Прочитать найденный кластер при цепочке не короче `min_chain`, и чтение стоит не меньше `min_lookups` обращений.
    Deep {
        /// Минимальная длина цепочки при чтении.
        min_chain: usize,
        /// Минимум обращений к таблицам.
        min_lookups: usize,
    },
    /// Цепочка когда-то была не короче `min_chain`, а после слияния стала не длиннее `max_after`.
    Squash {
        /// Минимальная наибольшая длина цепочки за сессию.
        min_chain: usize,
        /// Длина цепочки после слияния не больше.
        max_after: usize,
    },
    /// Записать кластер в верхний слой, откатить слой и прочитать этот кластер: данные уже другие.
    Rollback,
}

/// Цель упражнения.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Qcow2Goal {
    /// Идентификатор цели.
    pub id: String,
    /// Текст цели.
    pub text: String,
    /// Правило.
    pub rule: Qcow2Rule,
}

impl Qcow2Goal {
    /// Цель для показа.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.text.clone())
    }
}

/// Действие ученика.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "op", rename_all = "snake_case")]
pub enum Action {
    /// Снимок.
    Snapshot,
    /// Запись данных в кластер.
    Write {
        /// Номер кластера.
        cluster: u32,
        /// Данные.
        data: String,
    },
    /// Чтение кластера.
    Read {
        /// Номер кластера.
        cluster: u32,
    },
    /// Слить верхний слой.
    Commit,
    /// Откатить верхний слой.
    Revert,
}

/// Что произошло на действии (для подписи под схемой).
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Note {
    /// Снимок сделан.
    Snapshot,
    /// Запись выполнена; `copy_up` — кластер лежал в какой-то слое (копирование при записи).
    Write {
        /// Копирование при записи.
        copy_up: bool,
    },
    /// Чтение выполнено.
    Read(ReadResult),
    /// Слияние выполнено.
    Committed,
    /// Слияние невозможно: слой один.
    CommitImpossible,
    /// Откат выполнен; `had_data` — в отброшенном слое были записи.
    Reverted {
        /// В отброшенном слое были записи.
        had_data: bool,
    },
    /// Откат невозможен: слой один.
    RevertImpossible,
}

/// Ход упражнения: цепочка слоёв, служебные счётчики и достигнутые цели — как в `Qcow2Lab.tsx`.
#[derive(Clone, Debug)]
pub struct Session {
    goals: Vec<Qcow2Goal>,
    chain: Vec<Layer>,
    max_len: usize,
    snaps: u32,
    dropped: Option<BTreeMap<u32, String>>,
    done: Vec<String>,
}

impl Session {
    /// Новое упражнение: базовый слой с кластерами `base`.
    pub fn new(base: &BTreeMap<u32, String>, goals: &[Qcow2Goal]) -> Session {
        Session { goals: goals.to_vec(), chain: initial_chain(base), max_len: 1, snaps: 0, dropped: None, done: vec![] }
    }

    /// Цепочка слоёв (верхний — первый).
    pub fn chain(&self) -> &[Layer] {
        &self.chain
    }

    /// Наибольшая длина цепочки за сессию.
    pub fn max_len(&self) -> usize {
        self.max_len
    }

    /// Идентификаторы достигнутых целей (в порядке достижения).
    pub fn done(&self) -> &[String] {
        &self.done
    }

    /// Достигнуты ли все цели.
    pub fn solved(&self) -> bool {
        self.goals.iter().all(|g| self.done.contains(&g.id))
    }

    fn mark(&mut self, pred: impl Fn(&Qcow2Rule) -> bool) {
        for g in &self.goals {
            if pred(&g.rule) && !self.done.contains(&g.id) {
                self.done.push(g.id.clone());
            }
        }
    }

    fn set_chain(&mut self, c: Vec<Layer>) {
        self.max_len = self.max_len.max(c.len());
        self.chain = c;
    }

    /// Снимок.
    pub fn snapshot(&mut self) -> Note {
        self.snaps += 1;
        let c = snapshot(&self.chain, self.snaps);
        self.set_chain(c);
        Note::Snapshot
    }

    /// Запись.
    pub fn write(&mut self, cluster: u32, data: &str) -> Note {
        let (c, copy_up) = write(&self.chain, cluster, data);
        self.set_chain(c);
        Note::Write { copy_up }
    }

    /// Чтение.
    pub fn read(&mut self, cluster: u32) -> Note {
        let r = read(&self.chain, cluster);
        let len = self.chain.len();
        if r.value.is_some() {
            let lookups = r.lookups;
            self.mark(|rule| matches!(rule, Qcow2Rule::Deep { min_chain, min_lookups } if lookups >= *min_lookups && len >= *min_chain));
        }
        // откат подтверждён, если кластер, записанный в отброшенный слой, теперь читается иначе (или не читается вовсе)
        if let Some(d) = &self.dropped {
            if let Some(old) = d.get(&cluster) {
                if r.value.as_ref() != Some(old) {
                    self.mark(|rule| matches!(rule, Qcow2Rule::Rollback));
                    self.dropped = None;
                }
            }
        }
        Note::Read(r)
    }

    /// Слияние верхнего слоя.
    pub fn commit(&mut self) -> Note {
        let Some(c) = commit(&self.chain) else {
            return Note::CommitImpossible;
        };
        self.set_chain(c);
        let (max_len, len) = (self.max_len, self.chain.len());
        self.mark(|rule| matches!(rule, Qcow2Rule::Squash { min_chain, max_after } if max_len >= *min_chain && len <= *max_after));
        Note::Committed
    }

    /// Откат верхнего слоя.
    pub fn revert(&mut self) -> Note {
        let Some(c) = revert(&self.chain) else {
            return Note::RevertImpossible;
        };
        let top = &self.chain[0].data;
        let had_data = !top.is_empty();
        self.dropped = if had_data { Some(top.clone()) } else { None };
        self.set_chain(c);
        Note::Reverted { had_data }
    }

    /// Выполнить записанное действие.
    pub fn act(&mut self, a: &Action) -> Note {
        match a {
            Action::Snapshot => self.snapshot(),
            Action::Write { cluster, data } => self.write(*cluster, data),
            Action::Read { cluster } => self.read(*cluster),
            Action::Commit => self.commit(),
            Action::Revert => self.revert(),
        }
    }
}

/// Воспроизвести записанные действия и вернуть достигнутые цели.
pub fn replay(base: &BTreeMap<u32, String>, goals: &[Qcow2Goal], actions: &[Action]) -> Vec<String> {
    let mut s = Session::new(base, goals);
    for a in actions {
        s.act(a);
    }
    s.done
}

/// Базовые кластеры по умолчанию: 0–3 = A–D.
pub fn default_base() -> BTreeMap<u32, String> {
    [(0, "A"), (1, "B"), (2, "C"), (3, "D")].into_iter().map(|(k, v)| (k, v.to_string())).collect()
}

/// Цели по умолчанию (упражнение главы 9).
pub fn default_goals() -> Vec<Qcow2Goal> {
    vec![
        Qcow2Goal {
            id: "deep".into(),
            text: "Прочитайте кластер из базы при цепочке в 4 слоя и больше: чтение стоит 4 обращения и больше".into(),
            rule: Qcow2Rule::Deep { min_chain: 4, min_lookups: 4 },
        },
        Qcow2Goal {
            id: "squash".into(),
            text: "Слейте слои (commit), чтобы цепочка из 4 слоёв сократилась до двух".into(),
            rule: Qcow2Rule::Squash { min_chain: 4, max_after: 2 },
        },
        Qcow2Goal {
            id: "rollback".into(),
            text: "Запишите кластер в верхний слой, откатите слой — и убедитесь, что старые данные вернулись".into(),
            rule: Qcow2Rule::Rollback,
        },
    ]
}
