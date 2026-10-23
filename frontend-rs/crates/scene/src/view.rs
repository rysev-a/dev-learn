//! Компоненты Leptos: оболочка сцены (кнопки шагов, холст, подпись), плавные узлы SVG и отрисовка элементов [`Item`].
//!
//! Все элементы сцены существуют на экране всё время: на каждом шаге меняются только их свойства (положение, цвет, прозрачность),
//! а плавность дают CSS-переходы класса `.a-t` из `App.css`.

use std::sync::Arc;

use gloo_timers::callback::Timeout;
use highlight::highlight;
use leptos::prelude::*;

use content::{
    item::{Bar, Cell, Channel, Circle, Code, Dir, Dot, Gate, GateKind, Item, Lamp, Line, Lnode, Path, Ptr, Region, RegionOp, Switch, Text, Transistor, Zone},
    tone::{Tone, ARROW_HEADS},
    Scene,
};

use crate::{env::use_env, paint::Paint};

/// Сцена невидима первые кадры и всплывает на CSS; движение внутри стартует после этой паузы.
pub const REVEAL_MS: u32 = 800;

/// Список строк для подписей сцены: принимает и `vec!["…"]`, и `Vec<String>` из данных.
#[derive(Clone, Debug, Default)]
pub struct Strings(pub Vec<String>);

impl From<Vec<&str>> for Strings {
    fn from(v: Vec<&str>) -> Self {
        Strings(v.into_iter().map(String::from).collect())
    }
}

impl From<Vec<String>> for Strings {
    fn from(v: Vec<String>) -> Self {
        Strings(v)
    }
}

/// Управление шагами сцены.
#[derive(Clone, Copy)]
pub struct StepsCtl {
    /// текущий шаг (0 — начало)
    pub step: Signal<usize>,
    /// номер последнего шага
    pub last: usize,
    manual: RwSignal<bool>,
    auto: RwSignal<bool>,
    raw: RwSignal<usize>,
}

impl StepsCtl {
    /// Ручной выбор шага: автосмена и привязка к голосу отключаются до нового запуска звука.
    pub fn pick(&self, i: usize) {
        self.manual.set(true);
        self.auto.set(false);
        self.raw.set(i);
    }
}

/// Шаг сцены. `cues` — секунды от начала абзаца, когда наступают шаги 1, 2, …; пока слайд озвучивается, шаг берётся
/// из времени голоса, иначе сцена сама проходит шаги по таймеру (`ms` на шаг) и останавливается на последнем.
pub fn use_steps(cues: Vec<f64>, ms: u32) -> StepsCtl {
    let env = use_env();
    let last = cues.len();
    let raw = RwSignal::new(if env.motion_off { last } else { 0 });
    let manual = RwSignal::new(false);
    let auto = RwSignal::new(!env.motion_off);
    let had_audio = StoredValue::new(false);

    // новый запуск звука возвращает управление голосу
    Effect::new(move |_| {
        let has = env.audio_time.get().is_some();
        if has && !had_audio.get_value() {
            manual.set(false);
        }
        had_audio.set_value(has);
    });
    let synced = Memo::new(move |_| env.audio_time.get().is_some() && !manual.get());

    let timer: StoredValue<Option<Timeout>, LocalStorage> = StoredValue::new_local(None);
    Effect::new(move |_| {
        let (step, auto, synced) = (raw.get(), auto.get(), synced.get());
        timer.set_value(None); // отмена прежнего таймера
        if synced || !auto || step >= last {
            return;
        }
        let delay = if step == 0 { REVEAL_MS + 900 } else { ms };
        timer.set_value(Some(Timeout::new(delay, move || raw.update(|s| *s += 1))));
    });
    on_cleanup(move || timer.set_value(None));

    let step = Signal::derive(move || match (synced.get(), env.audio_time.get()) {
        (true, Some(t)) => cues.iter().filter(|c| t >= **c).count(),
        _ => raw.get(),
    });
    StepsCtl { step, last, manual, auto, raw }
}

/// Становится `true` через [`REVEAL_MS`] после показа сцены: с этого момента стартуют входные движения (появление фигур, рисование кривой).
pub fn use_reveal() -> Signal<bool> {
    let shown = RwSignal::new(use_env().motion_off);
    let timer: StoredValue<Option<Timeout>, LocalStorage> = StoredValue::new_local(None);
    if !shown.get_untracked() {
        timer.set_value(Some(Timeout::new(REVEAL_MS, move || shown.set(true))));
    }
    on_cleanup(move || timer.set_value(None));
    shown.into()
}

/// Оболочка сцены: кнопки шагов, холст SVG (ширина 360, высота `height`), подпись шага.
#[component]
pub fn Stage(ctl: StepsCtl, #[prop(into)] labels: Strings, #[prop(into)] captions: Strings, #[prop(default = 170.0)] height: f64, children: Children) -> impl IntoView {
    let step = ctl.step;
    let (labels, captions) = (labels.0, captions.0);
    let chips = labels
        .into_iter()
        .enumerate()
        .map(|(i, label)| {
            view! {
                <button class="a-chip" class:on=move || step.get() == i on:click=move |_| ctl.pick(i)>
                    <span class="a-chip-lbl">{label}</span>
                </button>
            }
        })
        .collect_view();
    let heads = ARROW_HEADS
        .iter()
        .map(|(id, color)| {
            view! {
                <marker id=*id viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                    <path d="M0 1 L10 5 L0 9 z" style=format!("fill: {color}") />
                </marker>
            }
        })
        .collect_view();
    view! {
        <div class="a-stage">
            <div class="a-chips" role="tablist">{chips}</div>
            <svg viewBox=format!("0 0 360 {height}") class="a-svg" aria-hidden="true">
                <defs>{heads}</defs>
                {children()}
            </svg>
            // новый элемент на каждом шаге — подпись появляется заново (CSS-анимация)
            {move || {
                let note = captions.get(step.get()).cloned().unwrap_or_default();
                view! { <div class="a-result"><span class="a-result-note">{note}</span></div> }
            }}
        </div>
    }
}

/// Плавно движущийся узел SVG: положение, прозрачность, масштаб.
#[component]
pub fn G(
    #[prop(into, default = 0.0.into())] x: Signal<f64>,
    #[prop(into, default = 0.0.into())] y: Signal<f64>,
    #[prop(into, default = 1.0.into())] o: Signal<f64>,
    #[prop(into, default = 1.0.into())] s: Signal<f64>,
    /// задержка перехода, мс
    #[prop(into, default = 0.0.into())] delay: Signal<f64>,
    #[prop(into, optional)] class: String,
    children: Children,
) -> impl IntoView {
    view! {
        <g class=format!("a-t {class}") style=move || format!("transform: translate({}px, {}px) scale({}); opacity: {}; transition-delay: {}ms", x.get(), y.get(), s.get(), o.get(), delay.get())>
            {children()}
        </g>
    }
}

/// Плашка с текстом по центру, (x, y) — центр.
#[component]
pub fn Pill(
    #[prop(into)] x: Signal<f64>,
    #[prop(into)] y: Signal<f64>,
    #[prop(default = 50.0)] w: f64,
    #[prop(default = 20.0)] h: f64,
    #[prop(into, default = 1.0.into())] o: Signal<f64>,
    #[prop(into, default = 1.0.into())] s: Signal<f64>,
    #[prop(into, default = Tone::Muted.into())] tone: Signal<Tone>,
    #[prop(default = 10.5)] size: f64,
    #[prop(into, default = Paint::default().into())] paint: Signal<Paint>,
    #[prop(into, optional)] text: String,
) -> impl IntoView {
    let look = move || paint.get().apply(tone.get().look());
    view! {
        <G x=x y=y o=o s=s>
            <rect x=-w / 2.0 y=-h / 2.0 width=w height=h rx="6" style=move || {
                let l = look();
                format!("stroke: {}; fill: {}; fill-opacity: {}; stroke-width: 1.4", l.stroke, l.fill, l.fill_opacity)
            } />
            <text y="3.7" text-anchor="middle" class="a-mono" style=move || format!("fill: {}; font-size: {size}px", look().text)>{text}</text>
        </G>
    }
}

/// Кружок-элемент с подписью, (x, y) — центр.
#[component]
pub fn DotView(
    #[prop(into)] x: Signal<f64>,
    #[prop(into)] y: Signal<f64>,
    #[prop(into, default = 11.0.into())] r: Signal<f64>,
    #[prop(into, default = 1.0.into())] o: Signal<f64>,
    #[prop(into, default = 1.0.into())] s: Signal<f64>,
    #[prop(into, default = Tone::Muted.into())] tone: Signal<Tone>,
    #[prop(default = 10.5)] size: f64,
    #[prop(into, default = Paint::default().into())] paint: Signal<Paint>,
    #[prop(into, optional)] text: String,
) -> impl IntoView {
    let look = move || paint.get().apply(tone.get().look());
    let text = (!text.is_empty()).then_some(text);
    view! {
        <G x=x y=y o=o s=s>
            <circle r=move || r.get() style=move || {
                let l = look();
                format!("stroke: {}; fill: {}; fill-opacity: {}; stroke-width: 1.6", l.stroke, l.fill, l.fill_opacity)
            } />
            {text.map(|t| view! { <text y="3.7" text-anchor="middle" class="a-mono" style=move || format!("fill: {}; font-size: {size}px", look().text)>{t}</text> })}
        </G>
    }
}

/// Подпись; `o` — прозрачность (плавное появление).
#[component]
pub fn Txt(
    #[prop(into)] x: f64,
    #[prop(into)] y: f64,
    #[prop(into, default = 1.0.into())] o: Signal<f64>,
    #[prop(default = "middle")] anchor: &'static str,
    #[prop(optional)] mono: bool,
    /// цвет подписи; пусто — как у класса
    #[prop(default = "")] color: &'static str,
    /// размер шрифта; 0 — как у класса
    #[prop(default = 0.0)] size: f64,
    children: Children,
) -> impl IntoView {
    let style = move || {
        let mut s = format!("opacity: {}", o.get());
        if !color.is_empty() {
            s.push_str(&format!("; fill: {color}"));
        }
        if size > 0.0 {
            s.push_str(&format!("; font-size: {size}px"));
        }
        s
    };
    view! { <text x=x y=y text-anchor=anchor class=format!("a-t {}", if mono { "a-mono" } else { "a-cap" }) style=style>{children()}</text> }
}

// --- отрисовка элементов сцены ---------------------------------------------------------------

/// Подпись с переносами: `\n` — новая строка, несколько строк центрируются по вертикали.
fn lines_view(text: String, anchor: &'static str, lh: f64) -> AnyView {
    let parts: Vec<String> = text.split('\n').map(String::from).collect();
    if parts.len() == 1 {
        return text.into_any();
    }
    let n = parts.len();
    parts
        .into_iter()
        .enumerate()
        .map(|(i, p)| {
            let dy = if i == 0 { -((n - 1) as f64) * lh * 0.5 } else { lh };
            view! { <tspan x="0" dy=format!("{dy}em") text-anchor=anchor>{p}</tspan> }
        })
        .collect_view()
        .into_any()
}

fn dash_css(dash: bool, pattern: &str) -> String {
    if dash {
        format!("; stroke-dasharray: {pattern}")
    } else {
        String::new()
    }
}

/// Производные сигналы по полям элемента: `at!(c, x)` → `Signal<f64>`.
macro_rules! sig {
    ($m:ident . $f:ident) => {
        Signal::derive(move || $m.get().$f)
    };
}

/// Подпись под элементом: `y` — базовая линия.
fn sub_view(sub: Option<String>, y: f64) -> Option<impl IntoView> {
    sub.map(|sub| view! { <text y=y text-anchor="middle" class="a-cap" style="font-size: 8.5px">{sub}</text> })
}

fn cell_view(c: Memo<Cell>) -> impl IntoView {
    let shape = move || {
        let c = c.get();
        let k = c.tone.look();
        format!("fill: {}; fill-opacity: {}; stroke: {}; stroke-width: 1.5{}", k.fill, k.fill_opacity, k.stroke, dash_css(c.dash, "3 3"))
    };
    view! {
        <G x=sig!(c.x) y=sig!(c.y) o=sig!(c.o) s=sig!(c.s) delay=sig!(c.delay)>
            <rect x=move || -c.get().w / 2.0 y=move || -c.get().h / 2.0 width=move || c.get().w height=move || c.get().h rx="5" style=shape />
            <text y=move || c.get().size * 0.36 text-anchor="middle" class="a-mono" style=move || {
                let c = c.get();
                format!("fill: {}; font-size: {}px", c.text_color.clone().unwrap_or_else(|| c.tone.look().text.to_string()), c.size)
            }>{move || lines_view(c.get().text, "middle", 1.25)}</text>
            {move || {
                let c = c.get();
                c.sub.map(|sub| view! { <text y=c.h / 2.0 + 10.0 text-anchor="middle" class="a-cap" style=format!("font-size: {}px", c.sub_size)>{sub}</text> })
            }}
        </G>
    }
}

fn dot_view(d: Memo<Dot>) -> impl IntoView {
    view! {
        <G x=sig!(d.x) y=sig!(d.y) o=sig!(d.o) s=sig!(d.s) delay=sig!(d.delay)>
            <circle r=move || d.get().r style=move || {
                let d = d.get();
                let k = d.tone.look();
                format!("fill: {}; fill-opacity: {}; stroke: {}; stroke-width: 1.7{}", k.fill, k.fill_opacity, k.stroke, dash_css(d.dash, "3 3"))
            } />
            <text y=move || d.get().size * 0.36 text-anchor="middle" class="a-mono" style=move || {
                let d = d.get();
                format!("fill: {}; font-size: {}px", d.text_color.clone().unwrap_or_else(|| d.tone.look().text.to_string()), d.size)
            }>{move || d.get().text}</text>
            {move || {
                let d = d.get();
                sub_view(d.sub, d.r + 10.0)
            }}
        </G>
    }
}

/// Узел списка: значение | ссылка (точка или перечёркнутая пустая ссылка).
fn lnode_view(n: Memo<Lnode>) -> impl IntoView {
    view! {
        <G x=sig!(n.x) y=sig!(n.y) o=sig!(n.o) s=sig!(n.s) delay=sig!(n.delay)>
            <rect x=move || -n.get().w / 2.0 y=move || -n.get().h / 2.0 width=move || n.get().w height=move || n.get().h rx="5" style=move || {
                let k = n.get().tone.look();
                format!("fill: {}; fill-opacity: {}; stroke: {}; stroke-width: 1.5", k.fill, k.fill_opacity, k.stroke)
            } />
            <line x1=move || n.get().w / 2.0 - 14.0 y1=move || -n.get().h / 2.0 x2=move || n.get().w / 2.0 - 14.0 y2=move || n.get().h / 2.0 style=move || format!("stroke: {}; stroke-width: 1.2", n.get().tone.look().stroke) />
            <text x="-7" y="3.8" text-anchor="middle" class="a-mono" style=move || {
                let n = n.get();
                format!("fill: {}; font-size: {}px", n.tone.look().text, n.size)
            }>{move || n.get().text}</text>
            {move || {
                let n = n.get();
                let (w, h) = (n.w, n.h);
                if n.nil {
                    view! { <path d=format!("M{} {} L{} {}", w / 2.0 - 11.0, h / 2.0 - 5.0, w / 2.0 - 3.0, -h / 2.0 + 5.0) style="stroke: var(--s-muted); stroke-width: 1.3" /> }.into_any()
                } else {
                    view! { <circle cx=w / 2.0 - 7.0 cy="0" r="2.4" style="fill: var(--s-accent)" /> }.into_any()
                }
            }}
            {move || {
                let n = n.get();
                sub_view(n.sub, n.h / 2.0 + 10.0)
            }}
        </G>
    }
}

fn text_view(t: Memo<Text>) -> impl IntoView {
    view! {
        <G x=sig!(t.x) y=sig!(t.y) o=sig!(t.o) s=sig!(t.s) delay=sig!(t.delay)>
            <text text-anchor=move || t.get().anchor.css() class=move || if t.get().mono { "a-mono" } else { "a-cap" } style=move || {
                let t = t.get();
                let fill = match (t.fill(), t.mono) {
                    (Some(c), _) => format!("fill: {c}; "),
                    (None, true) => String::new(),
                    (None, false) => "fill: var(--s-muted); ".to_string(),
                };
                format!("{fill}font-size: {}px{}", t.size, if t.bold { "; font-weight: 600" } else { "" })
            }>{move || { let t = t.get(); lines_view(t.text, t.anchor.css(), 1.25) }}</text>
        </G>
    }
}

/// Указатель: стрелка к точке (x, y) и имя.
fn ptr_view(p: Memo<Ptr>) -> impl IntoView {
    let hue = move || p.get().tone.hue().unwrap_or("var(--s-muted)");
    view! {
        <G x=sig!(p.x) y=sig!(p.y) o=sig!(p.o) s=sig!(p.s) delay=sig!(p.delay)>
            <line
                x1="0"
                y1=move || if p.get().dir == Dir::Down { -17.0 } else { 17.0 }
                x2="0"
                y2=move || if p.get().dir == Dir::Down { -2.0 } else { 2.0 }
                marker-end=move || format!("url(#{})", p.get().tone.marker())
                style=move || format!("stroke: {}; stroke-width: 1.6", hue())
            />
            <text y=move || if p.get().dir == Dir::Down { -21.0 } else { 27.0 } text-anchor="middle" class="a-mono" style=move || format!("fill: {}; font-size: {}px; font-weight: 600", hue(), p.get().size)>{move || p.get().text}</text>
        </G>
    }
}

/// Путь линии: прямая или дуга (смещение середины перпендикулярно линии).
fn line_path(l: &Line) -> String {
    if l.bend == 0.0 {
        return format!("M{} {} L{} {}", l.x1, l.y1, l.x2, l.y2);
    }
    let (mx, my) = ((l.x1 + l.x2) / 2.0, (l.y1 + l.y2) / 2.0);
    let (dx, dy) = (l.x2 - l.x1, l.y2 - l.y1);
    let n = dx.hypot(dy).max(1e-9);
    format!("M{} {} Q{} {} {} {}", l.x1, l.y1, mx - dy / n * l.bend, my + dx / n * l.bend, l.x2, l.y2)
}

fn line_view(l: Memo<Line>) -> impl IntoView {
    view! {
        <path
            class="a-t"
            d=move || line_path(&l.get())
            marker-end=move || l.get().arrow.then(|| format!("url(#{})", l.get().tone.marker()))
            style=move || {
                let l = l.get();
                let stroke = l.tone.hue().unwrap_or("var(--s-border)");
                // `d: path()` в стиле нужен для плавного движения линии (CSS-переход свойства d)
                format!("d: path(\"{}\"); fill: none; stroke: {stroke}; stroke-width: {}; opacity: {}; transition-delay: {}ms{}", line_path(&l), l.width, l.o, l.delay, l.dash.as_deref().map(|d| format!("; stroke-dasharray: {d}")).unwrap_or_default())
            }
        />
    }
}

/// Кривая по пути SVG; `draw` — доля прорисованной линии.
fn path_view(p: Memo<Path>) -> impl IntoView {
    view! {
        <path
            class="a-t"
            d=move || p.get().d
            marker-end=move || p.get().arrow.then(|| format!("url(#{})", p.get().tone.marker()))
            pathLength=move || p.get().draw.map(|_| "1")
            style=move || {
                let p = p.get();
                let stroke = p.tone.hue().unwrap_or("var(--s-muted)");
                let (dash, offset) = match p.draw {
                    Some(d) => ("1 1".to_string(), 1.0 - d),
                    None => (p.dash.clone().unwrap_or_else(|| "none".into()), 0.0),
                };
                format!(
                    "fill: {}; fill-opacity: {}; stroke: {stroke}; stroke-width: {}; stroke-dasharray: {dash}; stroke-dashoffset: {offset}; opacity: {}; transition-delay: {}ms",
                    p.fill.as_deref().unwrap_or("none"),
                    p.fill_opacity.map_or_else(|| "1".to_string(), |o| o.to_string()),
                    p.width,
                    p.o,
                    p.delay
                )
            }
        />
    }
}

fn bar_view(b: Memo<Bar>) -> impl IntoView {
    view! {
        <G x=sig!(b.x) y=sig!(b.y) o=sig!(b.o) delay=sig!(b.delay)>
            <g class="a-t" style=move || {
                let b = b.get();
                let h = b.hh.clamp(0.5, b.max);
                format!("transform: scaleY({}); transform-origin: 50% 100%; transform-box: fill-box", h / b.max)
            }>
                <rect x=move || -b.get().w / 2.0 y=move || -b.get().max width=move || b.get().w height=move || b.get().max rx="3" style=move || {
                    let k = b.get().tone.look();
                    let fo = if k.fill_opacity == 1.0 { 1.0 } else { 0.35 };
                    format!("fill: {}; fill-opacity: {fo}; stroke: {}; stroke-width: 1.3", k.fill, k.stroke)
                } />
            </g>
            {move || b.get().text.map(|t| view! { <text y="11" text-anchor="middle" class="a-mono" style="font-size: 9.5px">{t}</text> })}
        </G>
    }
}

fn zone_view(z: Memo<Zone>) -> impl IntoView {
    view! {
        <G x=sig!(z.x) y=sig!(z.y) o=sig!(z.o) s=sig!(z.s) delay=sig!(z.delay)>
            <rect x=move || -z.get().w / 2.0 y=move || -z.get().h / 2.0 width=move || z.get().w height=move || z.get().h rx="8" style=move || {
                let z = z.get();
                let k = z.tone.look();
                let stroke = if z.tone == Tone::Outline { "var(--s-border)" } else { k.stroke };
                format!("fill: {}; fill-opacity: {}; stroke: {stroke}; stroke-width: 1.3{}", k.fill, k.fill_opacity, dash_css(z.dash, "4 3"))
            } />
            {move || {
                let z = z.get();
                z.label.map(|label| view! { <text x=-z.w / 2.0 + 6.0 y=-z.h / 2.0 - 4.0 class="a-cap" style="font-size: 8.5px">{label}</text> })
            }}
        </G>
    }
}

fn code_view(c: Memo<Code>) -> impl IntoView {
    view! {
        <G x=sig!(c.x) y=sig!(c.y) o=sig!(c.o) delay=sig!(c.delay)>
            {move || {
                let c = c.get();
                c.lines
                    .iter()
                    .enumerate()
                    .map(|(i, line)| {
                        let (is_hl, is_bad) = (c.hl.contains(&i), c.bad.contains(&i));
                        let (fill, opacity) = if is_bad { ("var(--s-red)", 0.22) } else if is_hl { ("var(--s-accent)", 0.2) } else { ("var(--s-accent)", 0.0) };
                        let tokens = highlight(c.lang, line)
                            .into_iter()
                            .map(|t| match t.kind.css() {
                                Some(color) => view! { <tspan style=format!("fill: {color}")>{t.text}</tspan> }.into_any(),
                                None => t.text.into_any(),
                            })
                            .collect_view();
                        view! {
                            <g>
                                <rect class="a-t" x="-4" y=i as f64 * c.lh - c.lh * 0.78 width=c.w height=c.lh rx="3" style=format!("fill: {fill}; fill-opacity: {opacity}") />
                                <text y=i as f64 * c.lh class="a-mono" style=format!("font-size: {}px; white-space: pre; fill: {}", c.size, if is_hl || is_bad { "var(--s-text)" } else { "var(--s-muted)" })>{tokens}</text>
                            </g>
                        }
                    })
                    .collect_view()
            }}
        </G>
    }
}

// --- элементы схем из вентилей ---------------------------------------------------------------

fn gate_body(kind: GateKind) -> &'static str {
    match kind {
        GateKind::And | GateKind::Nand => "M-14 -11 H2 A12 11 0 0 1 2 11 H-14 Z",
        GateKind::Or | GateKind::Nor | GateKind::Xor | GateKind::Xnor => "M-14 -11 Q4 -11 14 0 Q4 11 -14 11 Q-8 0 -14 -11 Z",
        GateKind::Not => "M-12 -10 L8 0 L-12 10 Z",
        GateKind::Buf => "M-12 -10 L12 0 L-12 10 Z",
    }
}

/// Вентиль: тело, кружок инверсии, выводы; подпись внутри и под ним.
fn gate_view(g: Memo<Gate>) -> impl IntoView {
    view! {
        <G x=sig!(g.x) y=sig!(g.y) o=sig!(g.o) s=sig!(g.s) delay=sig!(g.delay)>
            {move || {
                let g = g.get();
                let k = g.tone.look();
                let stroke = format!("stroke: {}; stroke-width: 1.7; fill: none", k.stroke);
                let kind = g.gate;
                let body_x = if kind == GateKind::Not { 11.0 } else { 17.0 };
                let out_from = if kind.bubble() { body_x + 3.0 } else { 14.0 };
                let text_x = if kind.or_shaped() { -2.0 } else { -4.0 };
                view! {
                    <path d=gate_body(kind) style=format!("{stroke}; fill: {}; fill-opacity: {}", k.fill, k.fill_opacity) />
                    {matches!(kind, GateKind::Xor | GateKind::Xnor).then(|| view! { <path d="M-19 -11 Q-13 0 -19 11" style=stroke.clone() /> })}
                    {kind.bubble().then(|| view! { <circle cx=body_x cy="0" r="3" style=format!("{stroke}; fill: var(--s-bg)") /> })}
                    {if kind.single_input() {
                        view! { <path d="M-22 0 H-12" style=stroke.clone() /> }.into_any()
                    } else {
                        view! { <path d="M-22 -6 H-15 M-22 6 H-15" style=stroke.clone() /> }.into_any()
                    }}
                    <path d=format!("M{out_from} 0 H22") style=stroke />
                    {g.text.map(|t| view! { <text y="3.5" x=text_x text-anchor="middle" class="a-mono" style=format!("fill: {}; font-size: {}px", k.text, g.size)>{t}</text> })}
                    {sub_view(g.sub, 23.0)}
                }
            }}
        </G>
    }
}

/// Транзистор КМОП: затвор, канал (сплошной, если открыт), выводы; у p-канала кружок на затворе.
fn transistor_view(t: Memo<Transistor>) -> impl IntoView {
    view! {
        <G x=sig!(t.x) y=sig!(t.y) o=sig!(t.o) s=sig!(t.s) delay=sig!(t.delay)>
            {move || {
                let t = t.get();
                let k = t.tone.look();
                let stroke = format!("stroke: {}; stroke-width: 1.7; fill: none", k.stroke);
                let p = t.channel == Channel::P;
                let (width, dash) = if t.on { ("2.8", "none") } else { ("1.7", "3 2.5") };
                view! {
                    <path d="M-5 -8 V8" style=stroke.clone() />
                    <path d="M0 -9 V9" style=format!("{stroke}; stroke-width: {width}; stroke-dasharray: {dash}") />
                    <path d="M0 -8 H10 V-16 M0 8 H10 V16" style=stroke.clone() />
                    {p.then(|| view! { <circle cx="-8" cy="0" r="2.5" style=format!("{stroke}; fill: var(--s-bg)") /> })}
                    <path d=if p { "M-16 0 H-10.5" } else { "M-16 0 H-5" } style=stroke />
                    {sub_view(t.sub, 27.0)}
                }
            }}
        </G>
    }
}

/// Выключатель: два контакта и рычаг (замкнут или поднят).
fn switch_view(w: Memo<Switch>) -> impl IntoView {
    view! {
        <G x=sig!(w.x) y=sig!(w.y) o=sig!(w.o) s=sig!(w.s) delay=sig!(w.delay)>
            {move || {
                let w = w.get();
                let k = w.tone.look();
                let stroke = format!("stroke: {}; stroke-width: 1.7; fill: none", k.stroke);
                view! {
                    <circle cx="-14" cy="0" r="2.4" style=format!("{stroke}; fill: var(--s-bg)") />
                    <circle cx="14" cy="0" r="2.4" style=format!("{stroke}; fill: var(--s-bg)") />
                    <path class="a-t" d=if w.on { "M-14 0 L14 0" } else { "M-14 0 L11 -11" } style=format!("{stroke}; stroke-width: 2.2") />
                    {sub_view(w.sub, 16.0)}
                }
            }}
        </G>
    }
}

/// Лампочка: горит (зелёная) или погашена (крест).
fn lamp_view(l: Memo<Lamp>) -> impl IntoView {
    view! {
        <G x=sig!(l.x) y=sig!(l.y) o=sig!(l.o) s=sig!(l.s) delay=sig!(l.delay)>
            <circle r=move || l.get().r class="a-t" style=move || {
                let l = l.get();
                let (fill, fo, stroke) = if l.on { ("var(--s-accent)", 0.55, "var(--s-accent)") } else { ("var(--s-panel2)", 1.0, l.tone.look().stroke) };
                format!("fill: {fill}; fill-opacity: {fo}; stroke: {stroke}; stroke-width: 1.7")
            } />
            <path
                d=move || {
                    let r = l.get().r * 0.65;
                    format!("M{} {} L{r} {r} M{r} {} L{} {r}", -r, -r, -r, -r)
                }
                style=move || {
                    let l = l.get();
                    format!("stroke: {}; stroke-width: 1.3", if l.on { "var(--s-text)" } else { l.tone.look().stroke })
                }
            />
            {move || {
                let l = l.get();
                sub_view(l.sub, l.r + 10.0)
            }}
        </G>
    }
}

/// Круг-контур: рамка цветом оттенка, при `filled` — лёгкая заливка.
fn circle_view(c: Memo<Circle>) -> impl IntoView {
    view! {
        <G x=sig!(c.x) y=sig!(c.y) o=sig!(c.o) s=sig!(c.s) delay=sig!(c.delay)>
            <circle r=move || c.get().r style=move || {
                let c = c.get();
                let hue = c.tone.hue().unwrap_or("var(--s-border)");
                let (fill, fo) = if c.filled { (hue, 0.28) } else { ("none", 0.0) };
                format!("fill: {fill}; fill-opacity: {fo}; stroke: {hue}; stroke-width: {}{}", c.width, c.dash.as_deref().map(|d| format!("; stroke-dasharray: {d}")).unwrap_or_default())
            } />
        </G>
    }
}

/// Область из операции над кругами; маски и обрезка строятся тут же (идентификаторы — от `id` элемента).
fn region_view(r: Memo<Region>) -> impl IntoView {
    view! {
        <g class="a-t" style=move || format!("opacity: {}; transition-delay: {}ms", r.get().o, r.get().delay)>
            {move || {
                let r = r.get();
                let uid: String = r.id.chars().map(|c| if c.is_ascii_alphanumeric() { c } else { '_' }).collect();
                let fill = format!("fill: {}; fill-opacity: {}", r.tone.hue().unwrap_or("var(--s-muted)"), r.opacity);
                let circle = |d: &content::item::Disc, color: &'static str| view! { <circle cx=d.x cy=d.y r=d.r fill=color /> };
                match (r.op, r.discs.as_slice()) {
                    (RegionOp::Union, discs) => discs.iter().map(|d| view! { <circle cx=d.x cy=d.y r=d.r style=fill.clone() /> }).collect_view().into_any(),
                    (RegionOp::Intersect, [a, b, ..]) => view! {
                        <defs><clipPath id=format!("rg-{uid}")><circle cx=a.x cy=a.y r=a.r /></clipPath></defs>
                        <circle cx=b.x cy=b.y r=b.r clip-path=format!("url(#rg-{uid})") style=fill />
                    }
                    .into_any(),
                    (RegionOp::Minus, [first, rest @ ..]) => view! {
                        <defs>
                            <mask id=format!("rg-{uid}")>
                                <rect width="360" height="400" fill="#000" />
                                {circle(first, "#fff")}
                                {rest.iter().map(|d| circle(d, "#000")).collect_view()}
                            </mask>
                        </defs>
                        <rect width="360" height="400" mask=format!("url(#rg-{uid})") style=fill />
                    }
                    .into_any(),
                    (RegionOp::Outside, discs) => {
                        let b = r.bounds.unwrap_or(content::item::Rect { x: 0.0, y: 0.0, w: 360.0, h: 170.0 });
                        view! {
                            <defs>
                                <mask id=format!("rg-{uid}")>
                                    <rect x=b.x y=b.y width=b.w height=b.h rx="10" fill="#fff" />
                                    {discs.iter().map(|d| circle(d, "#000")).collect_view()}
                                </mask>
                            </defs>
                            <rect x=b.x y=b.y width=b.w height=b.h rx="10" mask=format!("url(#rg-{uid})") style=fill />
                        }
                        .into_any()
                    }
                    _ => ().into_any(),
                }
            }}
        </g>
    }
}

/// Отрисовка одного элемента: вид задаёт первое состояние (у одного `id` он не меняется — это проверяет `Scene::compile`).
fn item_view(it: Memo<Item>) -> AnyView {
    macro_rules! typed {
        ($variant:ident, $render:ident) => {{
            let typed = Memo::new(move |_| match it.get() {
                Item::$variant(v) => v,
                other => unreachable!("вид элемента изменился: {other:?}"),
            });
            $render(typed).into_any()
        }};
    }
    match it.get_untracked() {
        Item::Cell(_) => typed!(Cell, cell_view),
        Item::Dot(_) => typed!(Dot, dot_view),
        Item::Lnode(_) => typed!(Lnode, lnode_view),
        Item::Text(_) => typed!(Text, text_view),
        Item::Ptr(_) => typed!(Ptr, ptr_view),
        Item::Line(_) => typed!(Line, line_view),
        Item::Zone(_) => typed!(Zone, zone_view),
        Item::Path(_) => typed!(Path, path_view),
        Item::Bar(_) => typed!(Bar, bar_view),
        Item::Code(_) => typed!(Code, code_view),
        Item::Gate(_) => typed!(Gate, gate_view),
        Item::Transistor(_) => typed!(Transistor, transistor_view),
        Item::Switch(_) => typed!(Switch, switch_view),
        Item::Lamp(_) => typed!(Lamp, lamp_view),
        Item::Circle(_) => typed!(Circle, circle_view),
        Item::Region(_) => typed!(Region, region_view),
    }
}

/// Сцена целиком: оболочка и все её элементы (компилируются при создании). `cues` перекрывают метки шагов сцены.
#[component]
pub fn SceneView(spec: content::SceneSpec, #[prop(optional)] cues: Option<Vec<f64>>) -> impl IntoView {
    let scene = match Scene::compile(&spec) {
        Ok(s) => Arc::new(s),
        Err(e) => return view! { <p class="error">{e.to_string()}</p> }.into_any(),
    };
    let ctl = use_steps(cues.unwrap_or_else(|| scene.cues.clone()), scene.step_ms);
    let step = ctl.step;
    let last = scene.steps() - 1;
    let items = (0..scene.item_count())
        .map(|i| {
            let scene = Arc::clone(&scene);
            item_view(Memo::new(move |_| scene.states[step.get().min(last)][i].clone()))
        })
        .collect_view();
    view! {
        <Stage ctl=ctl labels=scene.labels.clone() captions=scene.captions.clone() height=scene.height>{items}</Stage>
    }
    .into_any()
}
