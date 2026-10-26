//! «Заглянуть внутрь»: просмотр схемы блока и процессора только для чтения — крошки пути, спуск в блоки вплоть до
//! вентилей, живые значения на проводах (`CircuitView.tsx`, часть `CircuitLab.tsx` и `CpuInspector.tsx`).

use std::{collections::HashMap, sync::Arc};

use archlab::{
    blocks::{BlockInstance, BlockInterface, BlockSolution, GateSolution, Solution},
    model::{
        out_pin_x, output_ys, pin_pos, wire_path, GateInstance, GateType, NodeValue, PinKind, PinRef, Wire, YMap, BOARD_H, BOARD_W, GATE_H, GATE_W,
        INPUT_X, OUT_X,
    },
};
use leptos::{ev, prelude::*, svg};

use super::{
    block_board::BlockBoard,
    block_logic::BLOCKS_BOARD_H,
    common::{levels_along, node_class, node_text, Exp, GateShape, Level, Lib, Scope, BOARD},
};
use crate::{
    components::labs::board_view::{is_background, js_round, use_fullscreen, BoardView, ItemDrag, Point, ZoomControls},
    dom,
};

/// Равномерная раскладка узлов по высоте доски `h` (для схем с многими входами и выходами).
pub fn spread_ys(names: &[String], h: f64) -> YMap {
    let n = names.len();
    let step = if n > 1 { (h - 80.0) / (n as f64 - 1.0) } else { 0.0 };
    YMap(names.iter().enumerate().map(|(i, name)| (name.clone(), if n == 1 { h / 2.0 } else { 40.0 + i as f64 * step })).collect())
}

/// Y входов по их именам (имена бывают любыми, не только `A`…`F`): до трёх — 80/200/320, до четырёх — по высоте
/// 50…390 (как на обычной доске), больше — равномерно по `h`.
pub fn named_input_ys(names: &[String], h: f64) -> YMap {
    if names.len() > 4 {
        return spread_ys(names, h);
    }
    if names.len() <= 3 {
        return YMap(names.iter().enumerate().map(|(i, n)| (n.clone(), [80.0, 200.0, 320.0][i])).collect());
    }
    let step = (390.0 - 50.0) / (names.len() as f64 - 1.0);
    YMap(names.iter().enumerate().map(|(i, n)| (n.clone(), 50.0 + i as f64 * step)).collect())
}

/// Размеры доски просмотра схемы из вентилей: (ширина, высота, на сколько колонка выходов уехала вправо).
pub fn gate_view_size(gates: &[GateInstance], inputs: usize, outputs: usize, spread: f64) -> (f64, f64, f64) {
    let sx = |x: f64| js_round(150.0 + (x - 150.0) * spread);
    let sy = |y: f64| js_round(20.0 + (y - 20.0) * spread);
    let w = if spread == 1.0 { BOARD_W } else { BOARD_W.max(gates.iter().map(|g| sx(g.x)).fold(0.0, f64::max) + 110.0 + 160.0) };
    let lowest = gates.iter().map(|g| sy(g.y)).fold(0.0, f64::max) + 110.0;
    let ports = inputs.max(outputs) as f64 * 50.0 + 40.0;
    (w, BOARD_H.max(lowest).max(ports), w - BOARD_W)
}

/// Во сколько раз раздвинуть схему блоков процессора, чтобы она читалась.
pub fn spread_for_blocks(instances: usize) -> f64 {
    match instances {
        n if n > 8 => 1.7,
        n if n > 3 => 1.4,
        _ => 1.2,
    }
}

/// Во сколько раз раздвинуть схему из вентилей процессора.
pub fn spread_for_gates(gates: usize) -> f64 {
    match gates {
        n if n > 40 => 1.9,
        n if n > 20 => 1.6,
        n if n > 8 => 1.35,
        _ => 1.15,
    }
}

/// Высота доски блоков процессора: все блоки помещаются.
pub fn block_board_height(instances: &[BlockInstance]) -> f64 {
    instances.iter().map(|i| i.y + 290.0).fold(BLOCKS_BOARD_H, f64::max)
}

/// Значение сигнала на входном контакте элемента: по узлу и контакту.
type PinValue = Arc<dyn Fn(&str, PinKind) -> NodeValue + Send + Sync>;

/// Схема из вентилей только для просмотра — «внутренность» блока. Значения берутся из общей симуляции, сигналы
/// живые. Вентили можно двигать и раздвигать: схема от этого не меняется.
#[component]
pub fn CircuitView(gates: Arc<Vec<GateInstance>>, wires: Arc<Vec<Wire>>, iface: Arc<BlockInterface>, scope: Scope, #[prop(default = 1.0)] spread: f64) -> impl IntoView {
    let fullscreen = use_fullscreen();
    let svg_ref = NodeRef::<svg::Svg>::new();
    let (w, h, extra_w) = gate_view_size(&gates, iface.inputs.len(), iface.outputs.len(), spread);
    let view = BoardView::new(svg_ref, BOARD, Signal::stored((w, h)));
    let moved = RwSignal::new(HashMap::<String, Point>::new());
    let dragging = RwSignal::new(None::<(String, ItemDrag)>);

    let in_y = Arc::new(named_input_ys(&iface.inputs, h));
    let out_y = Arc::new(if iface.outputs.len() > 4 { spread_ys(&iface.outputs, h) } else { output_ys(&iface.outputs) });
    // вентили на экране: сдвинутые рукой или раздвинутые
    let placed = {
        let gates = gates.clone();
        Memo::new(move |_| {
            moved.with(|mv| {
                gates
                    .iter()
                    .map(|g| {
                        let (x, y) = mv.get(&g.id).map_or((js_round(150.0 + (g.x - 150.0) * spread), js_round(20.0 + (g.y - 20.0) * spread)), |p| (p.x, p.y));
                        GateInstance { x, y, ..g.clone() }
                    })
                    .collect::<Vec<_>>()
            })
        })
    };
    let pos = {
        let (in_y, out_y, outputs) = (in_y.clone(), out_y.clone(), iface.outputs.clone());
        move |r: &PinRef| {
            let p = placed.with(|g| pin_pos(r, g, &out_y, &in_y));
            // колонка выходов при раздвигании уехала вправо вместе с доской
            if r.pin != PinKind::Out && outputs.contains(&r.node) {
                (p.x + extra_w, p.y)
            } else {
                (p.x, p.y)
            }
        }
    };
    let pos = Arc::new(pos);
    let pin_val = {
        let (wires, scope) = (wires.clone(), scope.clone());
        move |node: &str, pin: PinKind| -> NodeValue { wires.iter().find(|x| x.to.node == node && x.to.pin == pin).and_then(|x| scope(&x.from.node)) }
    };
    let pin_val: PinValue = Arc::new(pin_val);

    let on_move = move |e: web_sys::PointerEvent| {
        let c = Point::new(f64::from(e.client_x()), f64::from(e.client_y()));
        if view.move_pan(c.x, c.y) {
            return;
        }
        if let Some((id, item)) = dragging.get_untracked() {
            let o = BOARD.items.clamp(item.at(view.to_board(c.x, c.y)), (GATE_W, GATE_H));
            moved.update(|m| {
                m.insert(id, o);
            });
        }
    };
    dom::on_window(ev::pointermove, on_move);
    dom::on_window(ev::pointerup, move |_| {
        view.end_pan();
        dragging.set(None);
    });

    let wire_paths = wires
        .iter()
        .map(|wire| {
            let (from, to, pos, scope) = (wire.from.clone(), wire.to.clone(), pos.clone(), scope.clone());
            let src = wire.from.node.clone();
            let d = {
                let pos = pos.clone();
                move || {
                    let (a, b) = (pos(&from), pos(&to));
                    wire_path(archlab::model::Point { x: a.0, y: a.1 }, archlab::model::Point { x: b.0, y: b.1 })
                }
            };
            view! { <path class=move || format!("wire-line {}", node_class(scope(&src))) d=d></path> }
        })
        .collect_view();

    let input_nodes = iface
        .inputs
        .iter()
        .map(|id| {
            let y = in_y.get(id).unwrap_or(200.0);
            let label = iface.labels.as_ref().and_then(|l| iface.inputs.iter().position(|n| n == id).and_then(|i| l.get(i).cloned())).unwrap_or_else(|| id.clone());
            let (s1, s2, s3, id1, id2, id3) = (scope.clone(), scope.clone(), scope.clone(), id.clone(), id.clone(), id.clone());
            view! {
                <g class="node">
                    <rect class="node-box" x="10" y=y - 22.0 width="86" height="44" rx="10"></rect>
                    <text class="node-label" x="30" y=y + 5.0>{label}</text>
                    <rect class=move || format!("node-chip {}", node_class(s1(&id1))) x="56" y=y - 12.0 width="26" height="24" rx="7"></rect>
                    <text class="node-chip-text" x="69" y=y + 5.0>{move || node_text(s2(&id2))}</text>
                    <circle class=move || format!("pin-dot {}", node_class(s3(&id3))) cx=INPUT_X cy=y r="5.5"></circle>
                </g>
            }
        })
        .collect_view();
    let output_nodes = iface
        .outputs
        .iter()
        .map(|o| {
            let y = out_y.get(o).unwrap_or(200.0);
            let (s1, s2, s3, o1, o2, o3) = (scope.clone(), scope.clone(), scope.clone(), o.clone(), o.clone(), o.clone());
            view! {
                <g class="node" transform=format!("translate({extra_w} 0)")>
                    <rect class="node-box out-box" x="788" y=y - 22.0 width="86" height="44" rx="10"></rect>
                    <text class="node-label" x="812" y=y + 5.0>{o.clone()}</text>
                    <rect class=move || format!("node-chip {}", node_class(s1(&o1))) x="834" y=y - 12.0 width="26" height="24" rx="7"></rect>
                    <text class="node-chip-text" x="847" y=y + 5.0>{move || node_text(s2(&o2))}</text>
                    <circle class=move || format!("pin-dot {}", node_class(s3(&o3))) cx=OUT_X cy=y r="5.5"></circle>
                </g>
            }
        })
        .collect_view();
    let gate_nodes = gates
        .iter()
        .map(|g| {
            let (id, ty) = (g.id.clone(), g.ty);
            gate_node(view, placed, dragging, pin_val.clone(), scope.clone(), id, ty)
        })
        .collect_view();

    view! {
        <div class="lab-board" class:fill=fullscreen>
            <ZoomControls
                view=view
                changed=Signal::derive(move || view.changed() || moved.with(|m| !m.is_empty()))
                on_reset=Callback::new(move |()| {
                    view.reset();
                    moved.set(HashMap::new());
                })
            />
            <svg
                node_ref=svg_ref
                class="lab-board-svg cv"
                class:panning=move || view.panning.get()
                viewBox=move || view.view_box()
                role="img"
                aria-label="Схема внутри блока (только просмотр)"
                on:pointerdown=move |e| {
                    view.on_pointer_down(&e, is_background(e.target(), "cv-bg"));
                }
                on:wheel=move |e| view.on_wheel(&e, fullscreen())
                on:mousedown=|e| {
                    if e.button() == 1 {
                        e.prevent_default();
                    }
                }
                on:auxclick=|e| {
                    if e.button() == 1 {
                        e.prevent_default();
                    }
                }
            >
                <defs>
                    <pattern id="cv-dots" width="22" height="22" patternUnits="userSpaceOnUse">
                        <circle cx="1.5" cy="1.5" r="1.5" class="grid-dot"></circle>
                    </pattern>
                </defs>
                <rect
                    class="cv-bg"
                    x=move || view.pan.get().x.to_string()
                    y=move || view.pan.get().y.to_string()
                    width=move || (w / view.zoom.get()).to_string()
                    height=move || (h / view.zoom.get()).to_string()
                    fill="url(#cv-dots)"
                ></rect>
                {wire_paths}
                {input_nodes}
                {output_nodes}
                {gate_nodes}
            </svg>
        </div>
    }
}

/// Вентиль просмотра: контур, точки сигналов на контактах и «щуп» со значением выхода; его можно двигать.
#[allow(clippy::too_many_arguments)]
fn gate_node(
    view: BoardView,
    placed: Memo<Vec<GateInstance>>,
    dragging: RwSignal<Option<(String, ItemDrag)>>,
    pin_val: PinValue,
    scope: Scope,
    id: String,
    ty: GateType,
) -> impl IntoView {
    let at = {
        let id = id.clone();
        Memo::new(move |_| placed.with(|l| l.iter().find(|g| g.id == id).map_or((0.0, 0.0), |g| (g.x, g.y))))
    };
    let out_x = out_pin_x(ty);
    let pins = ty
        .pins()
        .iter()
        .map(|pin| {
            let (pin, node, pv) = (*pin, id.clone(), pin_val.clone());
            let py = archlab::layout::gate_pin_y(ty, pin);
            view! { <circle class=move || format!("pin-dot {}", node_class(pv(&node, pin))) cx="-8" cy=py r="5.5"></circle> }
        })
        .collect_view();
    let (s1, s2, i1, i2, i3) = (scope.clone(), scope, id.clone(), id.clone(), id.clone());
    view! {
        <g
            class="gate"
            transform=move || format!("translate({} {})", at.get().0, at.get().1)
            on:pointerdown=move |e| {
                if e.button() != 0 {
                    return;
                }
                e.prevent_default();
                let p = view.to_board(f64::from(e.client_x()), f64::from(e.client_y()));
                let (x, y) = at.get_untracked();
                dragging.set(Some((i3.clone(), ItemDrag::start(p, Point::new(x, y)))));
            }
        >
            <GateShape ty=ty />
            {pins}
            <circle class=move || format!("pin-dot {}", node_class(s1(&i1))) cx=out_x cy="24" r="5.5"></circle>
            <g class="probe" transform=format!("translate({} 24)", out_x + 20.0)>
                <circle r="9"></circle>
                <text y="3.5" text-anchor="middle">{move || node_text(s2(&i2))}</text>
            </g>
        </g>
    }
}

/// Просмотр схемы блока или процессора: крошки пути, «← Назад» и сама схема уровня. Путь (`path`) — id экземпляров,
/// в которые спустились; `top` — самый верхний уровень. `cpu` — раздвигать схемы и показывать сводку по вентилям.
#[component]
pub fn Inspector(top: Signal<Level>, library: Signal<Lib>, path: RwSignal<Vec<String>>, #[prop(default = false)] cpu: bool) -> impl IntoView {
    move || {
        let lvls = levels_along(top.get(), &path.get(), cpu);
        let Some(cur) = lvls.last().cloned() else { return ().into_any() };
        let stats = cpu.then(|| {
            let dffs = cur.expansion.circuit.gates.iter().filter(|g| g.ty == GateType::Dff).count();
            format!("внутри: {} вентилей, {dffs} триггеров", cur.expansion.circuit.gates.len() - dffs)
        });
        let crumbs = lvls
            .iter()
            .enumerate()
            .map(|(i, l)| {
                if i + 1 == lvls.len() {
                    view! { <strong>{l.title.clone()}</strong> }.into_any()
                } else {
                    view! {
                        <span>
                            <button type="button" class="lab-crumb" on:click=move |_| path.update(|p| p.truncate(i))>{l.title.clone()}</button>
                            <span class="lab-crumb-sep">" › "</span>
                        </span>
                    }
                    .into_any()
                }
            })
            .collect_view();
        let inspect = Callback::new(move |id: String| path.update(|p| p.push(id)));
        let scene = match &*cur.solution {
            Solution::Block(BlockSolution { instances, bus_wires }) => {
                let (spread, height) = if cpu { (spread_for_blocks(instances.len()), block_board_height(instances)) } else { (1.0, BLOCKS_BOARD_H) };
                let (instances, bus_wires) = (RwSignal::new(instances.clone()), RwSignal::new(bus_wires.clone()));
                view! {
                    <BlockBoard
                        iface=cur.iface.clone()
                        library=library
                        instances=instances
                        bus_wires=bus_wires
                        expansion=Signal::stored(Some(Exp(cur.expansion.clone())))
                        scope=cur.scope.clone()
                        readonly=true
                        height=height
                        spread=spread
                        on_inspect=inspect
                    />
                }
                .into_any()
            }
            Solution::Gate(GateSolution { gates, wires }) => {
                let spread = if cpu { spread_for_gates(gates.len()) } else { 1.0 };
                view! { <CircuitView gates=Arc::new(gates.clone()) wires=Arc::new(wires.clone()) iface=cur.iface.clone() scope=cur.scope.clone() spread=spread /> }.into_any()
            }
            Solution::Native(_) => view! {
                <p class="lab-native">
                    "Это встроенная память: ячейки здесь не из вентилей — как настоящая микросхема, у неё есть адрес, данные и (у диска) запись по такту. "
                    "Содержимое — на карточке «Виртуальный диск» выше (для программы — в машинном коде слева)."
                </p>
            }
            .into_any(),
        };
        let can_back = !path.with(Vec::is_empty);
        view! {
            <div class="lab-inspector">
                <div class="lab-inspector-bar">
                    <nav class="lab-crumbs" aria-label="Где вы находитесь">{crumbs}</nav>
                    <div class="lab-actions">
                        {stats.map(|s| view! { <span class="lab-edges">{s}</span> })}
                        {can_back.then(|| view! { <button type="button" class="quiz-btn ghost" on:click=move |_| path.update(|p| { p.pop(); })>"← Назад"</button> })}
                    </div>
                </div>
                {scene}
            </div>
        }
        .into_any()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn names(n: usize) -> Vec<String> {
        (0..n).map(|i| format!("n{i}")).collect()
    }

    #[test]
    fn up_to_three_inputs_use_the_classic_rows() {
        let ys = named_input_ys(&names(3), 440.0);
        assert_eq!(ys.get("n0"), Some(80.0));
        assert_eq!(ys.get("n2"), Some(320.0));
    }

    #[test]
    fn four_inputs_spread_over_the_board_and_many_inputs_over_its_height() {
        let four = named_input_ys(&names(4), 440.0);
        assert_eq!((four.get("n0"), four.get("n3")), (Some(50.0), Some(390.0)));
        let many = named_input_ys(&names(9), 800.0);
        assert_eq!((many.get("n0"), many.get("n8")), (Some(40.0), Some(760.0)));
        assert_eq!(spread_ys(&names(1), 440.0).get("n0"), Some(220.0));
    }

    #[test]
    fn view_size_grows_with_spread_and_ports() {
        let g = |x: f64, y: f64| GateInstance { id: "g".into(), ty: GateType::And, x, y };
        assert_eq!(gate_view_size(&[g(200.0, 100.0)], 2, 1, 1.0), (BOARD_W, BOARD_H, 0.0));
        let (w, h, extra) = gate_view_size(&[g(700.0, 400.0)], 2, 1, 2.0);
        assert!(w > BOARD_W && h > BOARD_H && extra == w - BOARD_W);
        // много выходов — доска выше, чтобы все поместились
        assert_eq!(gate_view_size(&[], 2, 12, 1.0).1, 640.0);
    }

    #[test]
    fn processor_spread_depends_on_the_size_of_the_scheme() {
        assert_eq!(spread_for_blocks(2), 1.2);
        assert_eq!(spread_for_blocks(5), 1.4);
        assert_eq!(spread_for_blocks(12), 1.7);
        assert_eq!(spread_for_gates(5), 1.15);
        assert_eq!(spread_for_gates(30), 1.6);
        assert_eq!(spread_for_gates(100), 1.9);
    }

    #[test]
    fn block_board_is_tall_enough_for_the_lowest_block() {
        let i = |y: f64| BlockInstance { id: "i".into(), block_id: "b".into(), x: 0.0, y };
        assert_eq!(block_board_height(&[i(10.0)]), BLOCKS_BOARD_H);
        assert_eq!(block_board_height(&[i(10.0), i(500.0)]), 790.0);
    }
}
