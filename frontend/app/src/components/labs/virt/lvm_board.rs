//! LVM board (book 19, chapters 16 and 20): the student assembles the storage of a server — disks, physical volumes, a volume group, logical
//! volumes, thin pools, snapshots, filesystems and VMs — and connects the objects like gates on the boards of the "Computer architecture" lab.
//! The rules of the links, the derived statuses (does the volume fit, did the snapshot overflow, how full is the thin pool, what does a lost disk
//! take with it) and the scenario goals come from `virtlab::lvm_board` (shared with the server, which re-checks the whole board); this module
//! is the interface only.
//!
//! * `lab.rs` — state of one scenario: the board, selection, the shown loss, statuses and board actions;
//! * `logic.rs` — pure logic (draft, placing, links, wires, statuses, tree, loss report) with tests;
//! * `board.rs` — the SVG board: palette, objects, pins, links, pan and zoom (`board_view.rs`);
//! * `panels.rs` — story, inspector, "if a disk fails", summary, tree and goals;
//! * `icons.rs` — object icons.
//!
//! Every scenario has its own board. The draft is the JSON object `{scenario id: board}` and goes to the owner on every edit (not while
//! dragging); the goal data of a scenario is its board, so the solution has the same shape.

use std::sync::Arc;

use leptos::prelude::*;
use virtlab::lvm_board::{Scenario, Topology};

mod board;
mod icons;
mod lab;
mod logic;
mod panels;

use board::Board;
use lab::Lab;
use panels::{GoalsPanel, Inspector, LossPanel, Story, SummaryPanel, TreePanel};

use super::common::{data, Goals, Tab};

#[component]
pub fn LvmBoardLab(
    scenarios: Vec<Scenario>,
    goals: Goals,
    /// the saved boards (a draft string), empty to start from the scenarios
    draft: Signal<String>,
    /// write the draft
    on_draft: Callback<String>,
) -> impl IntoView {
    let initial = logic::restore(&scenarios, &draft.get_untracked());
    let boards: Vec<(String, RwSignal<Topology>)> = scenarios.iter().zip(initial).map(|(s, t)| (s.id.clone(), RwSignal::new(t))).collect();
    let persist = {
        let boards = boards.clone();
        Callback::new(move |()| {
            let snapshot: Vec<(String, Topology)> = boards.iter().map(|(id, b)| (id.clone(), b.get_untracked())).collect();
            on_draft.run(logic::draft_json(&snapshot));
        })
    };
    let labs: Vec<Lab> = scenarios.iter().cloned().zip(boards).map(|(sc, (_, board))| Lab::new(Arc::new(sc), board, persist)).collect();

    // a scenario is marked once, when its goals first hold on a board the rules accept; the goal data is the board
    for lab in labs.iter().copied() {
        Effect::new(move |was: Option<bool>| {
            let now = lab.solved_now.get();
            if now && was != Some(true) {
                goals.mark(&lab.id(), data(&lab.board.get_untracked()));
            }
            now
        });
    }

    let active = RwSignal::new(0usize);
    let tabs = scenarios
        .iter()
        .enumerate()
        .map(|(i, s)| view! { <Tab title=s.title.clone() id=s.id.clone() index=i active=active.into() goals=goals on_pick=Callback::new(move |i| active.set(i)) /> })
        .collect_view();
    let labs = StoredValue::new(labs);

    view! {
        <div class="vl vl-lvm">
            <div class="vl-tabs" role="tablist">{tabs}</div>
            {move || labs.with_value(|l| l.get(active.get()).copied()).map(|lab| view! { <ScenarioView lab=lab /> })}
        </div>
    }
}

/// One scenario: the story, the board with the message under it, and the panels beside it.
#[component]
fn ScenarioView(lab: Lab) -> impl IntoView {
    view! {
        <Story lab=lab />
        <div class="vl-lvm-main">
            <div class="vl-lvm-work">
                <Board lab=lab />
                {move || {
                    let n = lab.notice.get();
                    (!n.is_empty()).then(|| view! { <p class="vl-lvm-notice" role="status">{n}</p> })
                }}
            </div>
            <div class="vl-lvm-side">
                <GoalsPanel lab=lab />
                <Inspector lab=lab />
                <LossPanel lab=lab />
                <SummaryPanel lab=lab />
                <TreePanel lab=lab />
            </div>
        </div>
    }
}
