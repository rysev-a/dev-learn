//! Лаборатория книги «Виртуализация» (книга 17): шесть симуляторов как чистые модели на Rust.
//!
//! * [`hv`] — мини-гипервизор: ловушки, виртуальные регистры, команда POPF и двоичная трансляция (глава 2);
//! * [`ept`] — трансляция адресов гостя: теневые таблицы и EPT/NPT, TLB, стоимость в обращениях к памяти (глава 4);
//! * [`virtq`] — кольца virtio и подавление оповещений (глава 6);
//! * [`qcow2`] — цепочка слоёв образа: снимки, запись с копированием, слияние и откат (глава 9);
//! * [`migration`] — живая миграция: круги pre-copy, auto-converge, сжатие, post-copy (глава 10);
//! * [`numa`] — размещение машин по узлам NUMA (глава 11).
//!
//! Результаты моделей совпадают с прежними TypeScript-моделями (`frontend/src/virtlab`) бит в бит — это проверяют
//! дифференциальные тесты по «золотым» данным (`tests/golden/virt.json`, выгрузка `frontend/scripts/virt-export.mjs`).
//!
//! Устройство:
//! * в каждом модуле — типы состояния (serde), чистые функции модели и **цели** упражнений как данные (`*Goal`/сценарии),
//!   а где цель зависит от истории действий ученика (hv, virtq, qcow2) — «сессия» (`Session`), повторяющая обработчики
//!   интерфейса и сообщающая достигнутые цели;
//! * [`spec::Spec`] — описание упражнения (какой симулятор, сценарии, цели) как данные: лежит в файле главы
//!   ([`labfile::LabChapter`], `backend/data/labs/virt/17-NN.json`) и приходит клиенту; интерфейс по нему строит симулятор;
//! * [`verify::verify`] — серверная проверка присланного решения (достигнутые цели с данными), см. [`verify::Verdict`].
//!
//! Зависимости — только `serde`/`serde_json`, wasm-специфики нет: крейт собирается и нативно, и под `wasm32-unknown-unknown`.

pub mod ept;
pub mod error;
pub mod goal;
pub mod hv;
pub mod labfile;
pub mod migration;
pub mod numa;
pub mod qcow2;
pub mod spec;
pub mod verify;
pub mod virtq;

pub use error::SpecError;
pub use goal::Goal;
pub use labfile::{LabChapter, Task};
pub use spec::{builtin, Spec, LAB_IDS};
pub use verify::{verify, verify_with, GoalStatus, GoalVerdict, Strictness, Verdict};
