//! Boards beside the results of the Python tasks of the oVirt book: a read-only picture of a board with the statuses derived by the model.
//!
//! * level 2 — a task whose answer is data (`host_statuses(board)`): the board of every test; the picture shows what the model says about it, so a wrong answer can
//!   be compared with the board;
//! * level 3 — a task whose code repairs the board (`fix(board)`): the starting board of every scenario, and after a run the board the code returned, with the links the
//!   code added marked and the goals of the scenario checked by the same model the server judges with.

use leptos::prelude::*;
use serde_json::Value;
use virtlab::ovirt_topo::{auto_layout, evaluate, scenario_of, Edge, Scenario, Topology, NODE_H, NODE_W};

use super::{icons, logic};

/// A board from task data (positions are optional).
fn parse(v: &Value) -> Option<Topology> {
    let mut t: Topology = serde_json::from_value(v.clone()).ok()?;
    if t.nodes.iter().all(|n| n.x == 0.0 && n.y == 0.0) {
        auto_layout(&mut t);
    }
    Some(t)
}

/// A read-only board: objects with their statuses, links with their names; links in `fresh` are drawn as added.
#[component]
pub fn BoardPicture(board: Topology, #[prop(optional)] fresh: Vec<Edge>) -> impl IntoView {
    let ev = evaluate(&board);
    let (w, h) = (NODE_W, NODE_H);
    let (min_x, max_x) = board.nodes.iter().fold((f64::MAX, f64::MIN), |(lo, hi), n| (lo.min(n.x), hi.max(n.x)));
    let (min_y, max_y) = board.nodes.iter().fold((f64::MAX, f64::MIN), |(lo, hi), n| (lo.min(n.y), hi.max(n.y)));
    let view_box = format!("{} {} {} {}", min_x - w / 2.0 - 12.0, min_y - h / 2.0 - 12.0, max_x - min_x + w + 24.0, max_y - min_y + h + 24.0);
    let edges = board
        .edges
        .iter()
        .filter_map(|e| {
            let (d, mid) = logic::edge_geom(&board, e)?;
            let label = logic::edge_rel(&board, e).map(|r| r.label()).unwrap_or_default();
            let new = fresh.contains(e);
            Some(view! {
                <g class="vl-topo-edge" class:path=new data-from=e.from.clone() data-to=e.to.clone()>
                    <path class="line" d=d></path>
                    <text class="lbl" x=mid.x y=mid.y - 6.0 text-anchor="middle">{label}</text>
                </g>
            })
        })
        .collect_view();
    let nodes = board
        .nodes
        .iter()
        .map(|n| {
            let info = logic::node_info(&board, &ev, &n.id);
            let class = format!("vl-topo-node {} {}", n.kind.as_str(), logic::status_class(&info));
            let chip = info.chip.clone().map(|c| view! { <span class=format!("vl-chip {}", c.class)>{c.text}</span> });
            let badge = logic::badge_text(&info);
            view! {
                <g class=class data-id=n.id.clone() data-kind=n.kind.as_str() transform=format!("translate({},{})", n.x, n.y)>
                    <title>{logic::describe_node(n, &info)}</title>
                    <rect x={-w / 2.0} y={-h / 2.0} width=w height=h rx="9"></rect>
                    <g class="vl-topo-ico" transform=format!("translate({},{}) scale(0.5)", -w / 2.0 + 6.0, -h / 2.0 + 5.0) inner_html=icons::markup(n.kind)></g>
                    <text class="vl-topo-badge" x={w / 2.0 - 6.0} y={-h / 2.0 + 15.0} text-anchor="end">{badge}</text>
                    <text class="vl-topo-name" x="0" y="-2" text-anchor="middle">{logic::short_name(&n.name)}</text>
                    <foreignObject class="vl-topo-chipbox" x={-w / 2.0 + 3.0} y="6" width={w - 6.0} height="20">
                        <div class="vl-topo-status">{chip}</div>
                    </foreignObject>
                </g>
            }
        })
        .collect_view();
    view! {
        <div class="vl-pic-scroll">
            <svg class="vl-pic-svg" viewBox=view_box preserveAspectRatio="xMidYMid meet">
                <g>{edges}</g>
                <g>{nodes}</g>
            </svg>
        </div>
    }
}

/// Goals of a scenario on a board, with marks.
fn goals_view(sc: &Scenario, board: &Topology) -> impl IntoView {
    let results = sc.results(board);
    let invalid = sc.invalid(board);
    view! {
        <ul class="vl-goals">
            {results
                .into_iter()
                .map(|g| view! { <li class:ok=g.ok><span class="vl-gm">{if g.ok { "✓" } else { "○" }}</span><span>{i18n::tr_dyn(&g.text)}</span></li> })
                .collect_view()}
        </ul>
        {invalid.map(|t| view! { <p class="vl-no vl-topo-invalid">{i18n::tr_dyn(&t)}</p> })}
    }
}

/// The body of the boards panel for the test (level 2) or the scenario (level 3) number `i` of an oVirt task; the tabs around it are `TaskBoards`.
pub fn task_body(boards: &api::dto::TaskBoards, i: usize, after: RwSignal<bool>, res: Signal<Option<api::dto::RunResult>>) -> Option<AnyView> {
    if !boards.checks.is_empty() {
        let check = boards.checks.get(i)?;
        let sc = scenario_of(&check.pack, &check.scenario)?;
        let start = sc.start.clone();
        let returned = res.get().and_then(|r| r.results.get(i).and_then(|t| t.board.as_ref().and_then(parse)));
        let (board, fresh) = match (&returned, after.get()) {
            (Some(b), true) => (b.clone(), b.edges.iter().filter(|e| !start.edges.contains(e)).cloned().collect::<Vec<_>>()),
            _ => (start.clone(), Vec::new()),
        };
        let toggle = returned.is_some().then(|| {
            view! {
                <div class="vl-pic-toggle">
                    <button type="button" class="vl-tab" class:on=move || !after.get() on:click=move |_| after.set(false)>{i18n::tr("Before")}</button>
                    <button type="button" class="vl-tab" class:on=move || after.get() on:click=move |_| after.set(true)>{i18n::tr("After your fix")}</button>
                </div>
            }
        });
        Some(
            view! {
                <div class="vl-pic-body">
                    <p class="vl-goal">{i18n::tr_dyn(&sc.story)}</p>
                    {toggle}
                    <BoardPicture board=board.clone() fresh=fresh />
                    {goals_view(&sc, &board)}
                </div>
            }
            .into_any(),
        )
    } else {
        let board = boards.boards.get(i).and_then(parse)?;
        Some(
            view! {
                <div class="vl-pic-body">
                    <p class="vl-pic-note">{i18n::tr("The board of this test, with the statuses the model derives from its links.")}</p>
                    <BoardPicture board=board />
                </div>
            }
            .into_any(),
        )
    }
}
