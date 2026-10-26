//! Модель виртуальной очереди virtio (глава 6).
//!
//! В очереди `size` дескрипторов; буфер занимает дескриптор от «положил гость» до «забрал гость готовым». Устройство
//! «спит» (ждёт оповещения) или «занято» (само просматривает доступное кольцо). Оповещение — выход в гипервизор.
//! Без подавления драйвер звонит после каждой отправки; с подавлением — только если устройство спит.
//!
//! Цели ([`VirtqGoal`]) проверяются после каждого действия ученика — этим занят [`Session`] (то же, что `VirtqLab.tsx`);
//! для серверной перепроверки действия записываются как [`Action`] и воспроизводятся [`replay`].

use serde::{Deserialize, Serialize};

use crate::goal::Goal;

/// Число дескрипторов очереди в упражнении главы 6.
pub const SIZE: u32 = 8;

/// Состояние очереди.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct QueueState {
    /// Буферы, ожидающие устройство.
    pub avail: u32,
    /// Обработанные, ещё не забранные гостем.
    pub used: u32,
    /// Устройство занято (не спит).
    pub busy: bool,
    /// Оповещения (выходы в гипервизор).
    pub notifies: u32,
    /// Положено буферов всего.
    pub posted: u32,
    /// Обработано буферов всего.
    pub processed: u32,
    /// Последняя попытка положить буфер упёрлась в переполнение.
    pub overflow: bool,
}

/// Пустая очередь.
pub fn initial() -> QueueState {
    QueueState { avail: 0, used: 0, busy: false, notifies: 0, posted: 0, processed: 0, overflow: false }
}

impl Default for QueueState {
    fn default() -> Self {
        initial()
    }
}

/// Свободные дескрипторы.
pub fn free(size: u32, s: &QueueState) -> u32 {
    size.saturating_sub(s.avail + s.used)
}

/// Гость кладёт `n` буферов (пачкой — один раз оповещая). Всё или ничего: не хватает места — флаг переполнения.
pub fn post(size: u32, s: &QueueState, n: u32, suppress: bool) -> QueueState {
    if n > free(size, s) {
        return QueueState { overflow: true, ..s.clone() };
    }
    let mut t = QueueState { avail: s.avail + n, posted: s.posted + n, overflow: false, ..s.clone() };
    if !suppress || !s.busy {
        t.notifies += 1;
    }
    t.busy = true;
    t
}

/// Устройство обрабатывает один буфер; когда доступное кольцо опустело, засыпает.
pub fn device(s: &QueueState) -> QueueState {
    if !s.busy || s.avail == 0 {
        return s.clone();
    }
    let mut t = QueueState { avail: s.avail - 1, used: s.used + 1, processed: s.processed + 1, ..s.clone() };
    if t.avail == 0 {
        t.busy = false;
    }
    t
}

/// Гость забирает готовые буферы.
pub fn reap(s: &QueueState) -> QueueState {
    QueueState { used: 0, ..s.clone() }
}

/// Цель: выполнены все заданные условия на состоянии очереди (незаданные не проверяются).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct VirtqGoal {
    /// Идентификатор цели.
    pub id: String,
    /// Текст цели.
    pub text: String,
    /// Подавление оповещений должно быть включено (`true`) или выключено (`false`).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub suppress: Option<bool>,
    /// Положено буферов не меньше.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub min_posted: Option<u32>,
    /// Оповещений не больше.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max_notifies: Option<u32>,
    /// Очередь должна быть в состоянии переполнения.
    #[serde(default, skip_serializing_if = "std::ops::Not::not")]
    pub overflow: bool,
}

impl VirtqGoal {
    /// Выполнена ли цель на состоянии `s` при настройке подавления `suppress`.
    pub fn check(&self, s: &QueueState, suppress: bool) -> bool {
        self.suppress.is_none_or(|x| x == suppress)
            && self.min_posted.is_none_or(|n| s.posted >= n)
            && self.max_notifies.is_none_or(|n| s.notifies <= n)
            && (!self.overflow || s.overflow)
    }

    /// Цель для показа.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.text.clone())
    }
}

/// Действие ученика.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "op", rename_all = "snake_case")]
pub enum Action {
    /// Гость кладёт `n` буферов.
    Post {
        /// Сколько буферов.
        n: u32,
    },
    /// Устройство обрабатывает один буфер.
    Device,
    /// Гость забирает готовые.
    Reap,
    /// Сбросить очередь (цели, уже достигнутые, остаются достигнутыми).
    Reset,
    /// Переключить подавление оповещений.
    Suppress {
        /// Включено ли.
        on: bool,
    },
}

/// Что произошло на действии (для подписи под схемой).
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Note {
    /// Очередь переполнена: положить `need` буферов нельзя, свободно `free`.
    Overflow {
        /// Нужно дескрипторов.
        need: u32,
        /// Свободно.
        free: u32,
    },
    /// Положено `n` буферов, оповещение отправлено.
    Notified {
        /// Сколько положено.
        n: u32,
    },
    /// Положено `n` буферов, оповещение не нужно (устройство занято).
    Quiet {
        /// Сколько положено.
        n: u32,
    },
    /// Устройство спит или нечего обрабатывать.
    DeviceIdle,
    /// Устройство обработало один буфер.
    Processed,
    /// Гость забрал готовые.
    Reaped,
    /// Очередь сброшена.
    Reset,
    /// Подавление переключено.
    SuppressSet,
}

/// Ход упражнения: очередь, настройка подавления и достигнутые цели — как в `VirtqLab.tsx`.
#[derive(Clone, Debug)]
pub struct Session {
    size: u32,
    goals: Vec<VirtqGoal>,
    state: QueueState,
    suppress: bool,
    done: Vec<String>,
}

impl Session {
    /// Новое упражнение с очередью из `size` дескрипторов.
    pub fn new(size: u32, goals: &[VirtqGoal]) -> Session {
        Session { size, goals: goals.to_vec(), state: initial(), suppress: false, done: vec![] }
    }

    /// Состояние очереди.
    pub fn state(&self) -> &QueueState {
        &self.state
    }

    /// Включено ли подавление.
    pub fn suppress(&self) -> bool {
        self.suppress
    }

    /// Идентификаторы достигнутых целей (в порядке достижения).
    pub fn done(&self) -> &[String] {
        &self.done
    }

    /// Достигнуты ли все цели.
    pub fn solved(&self) -> bool {
        self.goals.iter().all(|g| self.done.contains(&g.id))
    }

    fn check_goals(&mut self) {
        for g in &self.goals {
            if g.check(&self.state, self.suppress) && !self.done.contains(&g.id) {
                self.done.push(g.id.clone());
            }
        }
    }

    /// Переключить подавление оповещений (цели при этом не проверяются).
    pub fn set_suppress(&mut self, on: bool) -> Note {
        self.suppress = on;
        Note::SuppressSet
    }

    /// Гость кладёт `n` буферов.
    pub fn post(&mut self, n: u32) -> Note {
        let before = self.state.clone();
        self.state = post(self.size, &before, n, self.suppress);
        let note = if self.state.overflow {
            Note::Overflow { need: n, free: free(self.size, &before) }
        } else if self.state.notifies > before.notifies {
            Note::Notified { n }
        } else {
            Note::Quiet { n }
        };
        self.check_goals();
        note
    }

    /// Устройство обрабатывает один буфер (спит — ничего, цели не проверяются).
    pub fn device(&mut self) -> Note {
        if !self.state.busy || self.state.avail == 0 {
            return Note::DeviceIdle;
        }
        self.state = device(&self.state);
        self.check_goals();
        Note::Processed
    }

    /// Гость забирает готовые буферы.
    pub fn reap(&mut self) -> Note {
        self.state = reap(&self.state);
        self.check_goals();
        Note::Reaped
    }

    /// Сбросить очередь.
    pub fn reset(&mut self) -> Note {
        self.state = initial();
        Note::Reset
    }

    /// Выполнить записанное действие.
    pub fn act(&mut self, a: &Action) -> Note {
        match a {
            Action::Post { n } => self.post(*n),
            Action::Device => self.device(),
            Action::Reap => self.reap(),
            Action::Reset => self.reset(),
            Action::Suppress { on } => self.set_suppress(*on),
        }
    }
}

/// Воспроизвести записанные действия и вернуть достигнутые цели.
pub fn replay(size: u32, goals: &[VirtqGoal], actions: &[Action]) -> Vec<String> {
    let mut s = Session::new(size, goals);
    for a in actions {
        s.act(a);
    }
    s.done
}

/// Цели по умолчанию (упражнение главы 6).
pub fn default_goals() -> Vec<VirtqGoal> {
    let g = |id: &str, text: &str| VirtqGoal {
        id: id.into(),
        text: text.into(),
        suppress: None,
        min_posted: None,
        max_notifies: None,
        overflow: false,
    };
    vec![
        VirtqGoal {
            suppress: Some(false),
            min_posted: Some(6),
            max_notifies: Some(2),
            ..g("batch", "Отправьте 6 буферов и более не больше чем двумя оповещениями (без подавления)")
        },
        VirtqGoal {
            overflow: true,
            ..g(
                "overflow",
                "Доведите очередь до переполнения: попробуйте положить буфер, когда свободных дескрипторов нет",
            )
        },
        VirtqGoal {
            suppress: Some(true),
            min_posted: Some(10),
            max_notifies: Some(2),
            ..g(
                "suppress",
                "Включите подавление оповещений и отправьте 10 буферов и более не больше чем двумя оповещениями",
            )
        },
    ]
}
