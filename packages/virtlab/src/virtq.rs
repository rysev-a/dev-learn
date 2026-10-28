//! virtio virtqueue model (chapter 6).
//!
//! The queue has `size` descriptors; a buffer occupies a descriptor from "posted by the guest" to "reaped by the guest as done". The device
//! is either "asleep" (waiting for a notification) or "busy" (polling the available ring itself). A notification is an exit to the hypervisor.
//! Without suppression the driver kicks after every post; with suppression — only if the device is asleep.
//!
//! Goals ([`VirtqGoal`]) are checked after every student action — that is the job of [`Session`] (same as `VirtqLab.tsx`);
//! for server-side re-checking actions are recorded as [`Action`] and replayed by [`replay`].

use serde::{Deserialize, Serialize};

use crate::goal::Goal;

/// Number of queue descriptors in the chapter 6 exercise.
pub const SIZE: u32 = 8;

/// Queue state.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct QueueState {
    /// Buffers waiting for the device.
    pub avail: u32,
    /// Processed, not yet reaped by the guest.
    pub used: u32,
    /// Device is busy (not asleep).
    pub busy: bool,
    /// Notifications (exits to the hypervisor).
    pub notifies: u32,
    /// Total buffers posted.
    pub posted: u32,
    /// Total buffers processed.
    pub processed: u32,
    /// The last attempt to post a buffer hit an overflow.
    pub overflow: bool,
}

/// Empty queue.
pub fn initial() -> QueueState {
    QueueState { avail: 0, used: 0, busy: false, notifies: 0, posted: 0, processed: 0, overflow: false }
}

impl Default for QueueState {
    fn default() -> Self {
        initial()
    }
}

/// Free descriptors.
pub fn free(size: u32, s: &QueueState) -> u32 {
    size.saturating_sub(s.avail + s.used)
}

/// The guest posts `n` buffers (as a batch — notifying once). All or nothing: not enough room — overflow flag.
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

/// The device processes one buffer; when the available ring is empty, it goes to sleep.
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

/// The guest reaps completed buffers.
pub fn reap(s: &QueueState) -> QueueState {
    QueueState { used: 0, ..s.clone() }
}

/// Goal: all specified conditions hold on the queue state (unspecified ones are not checked).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct VirtqGoal {
    /// Goal identifier.
    pub id: String,
    /// Goal text.
    pub text: String,
    /// Notification suppression must be enabled (`true`) or disabled (`false`).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub suppress: Option<bool>,
    /// At least this many buffers posted.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub min_posted: Option<u32>,
    /// At most this many notifications.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max_notifies: Option<u32>,
    /// The queue must be in the overflow state.
    #[serde(default, skip_serializing_if = "std::ops::Not::not")]
    pub overflow: bool,
}

impl VirtqGoal {
    /// Whether the goal holds on state `s` with suppression setting `suppress`.
    pub fn check(&self, s: &QueueState, suppress: bool) -> bool {
        self.suppress.is_none_or(|x| x == suppress)
            && self.min_posted.is_none_or(|n| s.posted >= n)
            && self.max_notifies.is_none_or(|n| s.notifies <= n)
            && (!self.overflow || s.overflow)
    }

    /// Goal for display.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.text.clone())
    }
}

/// Student action.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "op", rename_all = "snake_case")]
pub enum Action {
    /// The guest posts `n` buffers.
    Post {
        /// How many buffers.
        n: u32,
    },
    /// The device processes one buffer.
    Device,
    /// The guest reaps completed buffers.
    Reap,
    /// Reset the queue (already achieved goals stay achieved).
    Reset,
    /// Toggle notification suppression.
    Suppress {
        /// Whether enabled.
        on: bool,
    },
}

/// What happened on the action (for the caption under the diagram).
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Note {
    /// Queue overflow: cannot post `need` buffers, `free` are available.
    Overflow {
        /// Descriptors needed.
        need: u32,
        /// Free.
        free: u32,
    },
    /// `n` buffers posted, notification sent.
    Notified {
        /// How many posted.
        n: u32,
    },
    /// `n` buffers posted, no notification needed (device is busy).
    Quiet {
        /// How many posted.
        n: u32,
    },
    /// The device is asleep or there is nothing to process.
    DeviceIdle,
    /// The device processed one buffer.
    Processed,
    /// The guest reaped completed buffers.
    Reaped,
    /// Queue reset.
    Reset,
    /// Suppression toggled.
    SuppressSet,
}

/// Exercise progress: queue, suppression setting and achieved goals — as in `VirtqLab.tsx`.
#[derive(Clone, Debug)]
pub struct Session {
    size: u32,
    goals: Vec<VirtqGoal>,
    state: QueueState,
    suppress: bool,
    done: Vec<String>,
}

impl Session {
    /// New exercise with a queue of `size` descriptors.
    pub fn new(size: u32, goals: &[VirtqGoal]) -> Session {
        Session { size, goals: goals.to_vec(), state: initial(), suppress: false, done: vec![] }
    }

    /// Queue state.
    pub fn state(&self) -> &QueueState {
        &self.state
    }

    /// Whether suppression is enabled.
    pub fn suppress(&self) -> bool {
        self.suppress
    }

    /// Identifiers of achieved goals (in order of achievement).
    pub fn done(&self) -> &[String] {
        &self.done
    }

    /// Whether all goals are achieved.
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

    /// Toggle notification suppression (goals are not checked here).
    pub fn set_suppress(&mut self, on: bool) -> Note {
        self.suppress = on;
        Note::SuppressSet
    }

    /// The guest posts `n` buffers.
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

    /// The device processes one buffer (asleep — nothing happens, goals are not checked).
    pub fn device(&mut self) -> Note {
        if !self.state.busy || self.state.avail == 0 {
            return Note::DeviceIdle;
        }
        self.state = device(&self.state);
        self.check_goals();
        Note::Processed
    }

    /// The guest reaps completed buffers.
    pub fn reap(&mut self) -> Note {
        self.state = reap(&self.state);
        self.check_goals();
        Note::Reaped
    }

    /// Reset the queue.
    pub fn reset(&mut self) -> Note {
        self.state = initial();
        Note::Reset
    }

    /// Perform a recorded action.
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

/// Replay recorded actions and return the achieved goals.
pub fn replay(size: u32, goals: &[VirtqGoal], actions: &[Action]) -> Vec<String> {
    let mut s = Session::new(size, goals);
    for a in actions {
        s.act(a);
    }
    s.done
}

/// Default goals (chapter 6 exercise).
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
            ..g("batch", i18n::tr("Send 6 or more buffers with at most two notifications (without suppression)"))
        },
        VirtqGoal {
            overflow: true,
            ..g(
                "overflow",
                i18n::tr("Drive the queue to overflow: try to add a buffer when there are no free descriptors"),
            )
        },
        VirtqGoal {
            suppress: Some(true),
            min_posted: Some(10),
            max_notifies: Some(2),
            ..g(
                "suppress",
                i18n::tr("Enable notification suppression and send 10 or more buffers with at most two notifications"),
            )
        },
    ]
}
