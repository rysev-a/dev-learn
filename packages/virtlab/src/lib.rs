//! Lab for the "Virtualization" book (book 17): nine simulators as pure Rust models.
//!
//! * [`hv`] — mini-hypervisor: traps, virtual registers, the POPF instruction and binary translation (chapter 2);
//! * [`ept`] — guest address translation: shadow page tables and EPT/NPT, TLB, cost in memory accesses (chapter 4);
//! * [`virtq`] — virtio rings and notification suppression (chapter 6);
//! * [`qcow2`] — image layer chain: snapshots, copy-on-write, merging and rollback (chapter 9);
//! * [`migration`] — live migration: pre-copy rounds, auto-converge, compression, post-copy (chapter 10);
//! * [`numa`] — placing machines on NUMA nodes (chapter 11);
//! * [`ovirt_dc`] — bringing up an oVirt data center: cluster, hosts, network, storage domain, VM (chapter 17);
//! * [`ovirt_fence`] — fencing a non-responsive oVirt host: soft fencing, cluster policy, power management (chapter 19);
//! * [`ovirt_sched`] — the oVirt scheduler: filters, weights and anti-affinity (chapter 22).
//!
//! Model results of the first six simulators match the former TypeScript models (`frontend/src/virtlab`) bit for bit — this is checked by
//! differential tests against "golden" data (`tests/golden/virt.json`, exported by `frontend/scripts/virt-export.mjs`).
//!
//! Layout:
//! * each module has state types (serde), pure model functions and exercise **goals** as data (`*Goal`/scenarios),
//!   and where a goal depends on the student's action history (hv, virtq, qcow2) — a "session" (`Session`) that mirrors
//!   the UI handlers and reports achieved goals;
//! * [`spec::Spec`] — exercise description (which simulator, scenarios, goals) as data: lives in the chapter file
//!   ([`labfile::LabChapter`], `backend/data/labs/virt/17-NN.json`) and is sent to the client; the UI builds the simulator from it;
//! * [`verify::verify`] — server-side check of a submitted solution (achieved goals with data), see [`verify::Verdict`].
//!
//! Dependencies are only `serde`/`serde_json`, nothing wasm-specific: the crate builds both natively and for `wasm32-unknown-unknown`.

pub mod ept;
pub mod error;
pub mod goal;
pub mod hv;
pub mod labfile;
pub mod migration;
pub mod numa;
pub mod ovirt_dc;
pub mod ovirt_fence;
pub mod ovirt_sched;
pub mod qcow2;
pub mod spec;
pub mod verify;
pub mod virtq;

pub use error::SpecError;
pub use goal::Goal;
pub use labfile::{LabChapter, Task};
pub use spec::{builtin, Spec, LAB_IDS};
pub use verify::{verify, verify_with, GoalStatus, GoalVerdict, Strictness, Verdict};
