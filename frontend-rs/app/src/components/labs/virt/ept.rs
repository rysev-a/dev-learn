//! Симулятор трансляции адресов (глава 4): режим (теневые таблицы или EPT), размеры страниц гостя и хозяина, нагрузка.
//! Показывает цену обхода (двумерная сетка обращений), промахи TLB и общую стоимость в обращениях к памяти. Решено, когда
//! достигнуты все цели. В данных цели — настройки запуска; сервер заново запускает модель.

use leptos::prelude::*;
use virtlab::ept::{
    self, EptGoal, Mode, PageSize, SimInput, SimRun, Workload, EXIT_COST, TLB_ENTRIES,
};

use super::common::{data, fmt_ru, GoalItem, GoalList, Goals};

/// Подпись размера страницы в списке выбора.
fn size_text(p: PageSize) -> &'static str {
    match p {
        PageSize::K4 => "4 КиБ",
        PageSize::M2 => "2 МиБ",
        PageSize::G1 => "1 ГиБ",
    }
}

/// Короткое имя размера (как в данных: `4K`, `2M`, `1G`).
fn size_key(p: PageSize) -> &'static str {
    match p {
        PageSize::K4 => "4K",
        PageSize::M2 => "2M",
        PageSize::G1 => "1G",
    }
}

fn parse_size(s: &str) -> Option<PageSize> {
    PageSize::ALL.into_iter().find(|p| size_key(*p) == s)
}

/// Сетка обращений одного промаха: число столбцов и клетки (`true` — сами данные).
#[derive(Debug, PartialEq, Eq)]
pub struct WalkGrid {
    pub cols: u32,
    pub cells: Vec<bool>,
}

/// Двумерная сетка обхода: теневые таблицы — ряд из `walk_cost` уровней (запись TLB описывает меньшую из двух страниц);
/// EPT — `(g+1)×(h+1)` клеток, последняя — данные.
pub fn walk_grid(mode: Mode, guest: PageSize, host: PageSize) -> WalkGrid {
    match mode {
        Mode::Shadow => {
            let n = ept::walk_cost(Mode::Shadow, guest, host);
            WalkGrid { cols: n, cells: vec![false; n as usize] }
        }
        Mode::Ept => {
            let (g, h) = (guest.levels() + 1, host.levels() + 1);
            let mut cells = vec![false; (g * h) as usize];
            if let Some(last) = cells.last_mut() {
                *last = true;
            }
            WalkGrid { cols: h, cells }
        }
    }
}

/// Формула цены промаха над сеткой.
pub fn walk_formula(mode: Mode, guest: PageSize, host: PageSize) -> String {
    match mode {
        Mode::Ept => format!("({}+1)×({}+1)−1", guest.levels(), host.levels()),
        Mode::Shadow => format!("{} уровня", ept::walk_cost(Mode::Shadow, guest, host)),
    }
}

/// Цели, достигнутые запуском: те, что привязаны к этой нагрузке и выполнены на результате `r`.
pub fn reached<'a>(goals: &'a [EptGoal], r: &SimRun, cfg: &SimInput) -> Vec<&'a EptGoal> {
    goals.iter().filter(|g| g.workload == cfg.workload && g.check(r, cfg)).collect()
}

#[component]
pub fn EptLab(workloads: Vec<Workload>, targets: Vec<EptGoal>, goals: Goals) -> impl IntoView {
    let mode = RwSignal::new(Mode::Ept);
    let guest = RwSignal::new(PageSize::K4);
    let host = RwSignal::new(PageSize::K4);
    let first = workloads.first().map(|w| w.id.clone()).unwrap_or_default();
    let workload = RwSignal::new(first);
    let res: RwSignal<Option<SimRun>> = RwSignal::new(None);

    let items: Vec<GoalItem> = targets
        .iter()
        .map(|g| {
            let title = workloads.iter().find(|w| w.id == g.workload).map(|w| w.title.clone()).unwrap_or_default();
            GoalItem::new(g.id.clone(), g.text.clone()).with_note(format!("нагрузка «{title}»"))
        })
        .collect();
    let options = workloads
        .iter()
        .map(|w| {
            let id = w.id.clone();
            view! { <option value=w.id.clone() selected=move || workload.get() == id>{w.title.clone()}</option> }
        })
        .collect_view();
    let workloads = StoredValue::new(workloads);
    let targets = StoredValue::new(targets);
    let note = move || {
        workloads.with_value(|ws| {
            let id = workload.get();
            let note = ws.iter().find(|w| w.id == id).map(|w| w.note.clone()).unwrap_or_default();
            format!("{note}. TLB — {TLB_ENTRIES} записей; запись описывает страницу меньшего из двух размеров.")
        })
    };

    let run = move |_| {
        let cfg = SimInput { mode: mode.get_untracked(), guest: guest.get_untracked(), host: host.get_untracked(), workload: workload.get_untracked() };
        let Ok(r) = workloads.with_value(|ws| ept::simulate(ws, &cfg)) else { return };
        let ids: Vec<String> = targets.with_value(|ts| reached(ts, &r, &cfg).into_iter().map(|g| g.id.clone()).collect());
        res.set(Some(r));
        for id in ids {
            goals.mark(&id, data(&cfg));
        }
    };

    view! {
        <div class="vl">
            <div class="vl-grid">
                <div class="vl-card">
                    <div class="vl-field">
                        <span class="s-label">"режим"</span>
                        <div class="vl-seg">
                            <ModeButton mode=mode value=Mode::Shadow title="теневые таблицы" />
                            <ModeButton mode=mode value=Mode::Ept title="EPT / NPT" />
                        </div>
                    </div>
                    <div class="vl-row">
                        <SizeSelect label="страница гостя" value=guest />
                        <SizeSelect label="страница хозяина" value=host />
                    </div>
                    <label class="vl-field">
                        <span>"нагрузка"</span>
                        <select on:change=move |ev| workload.set(event_target_value(&ev))>{options}</select>
                    </label>
                    <p class="vl-hint">{note}</p>
                    <div class="vl-actions">
                        <button class="quiz-btn" on:click=run>"Запустить нагрузку"</button>
                    </div>
                    <GoalList goals=goals items=items />
                </div>

                <div class="vl-card">
                    <div class="pr-res-head">
                        <span class="s-label">"промах TLB"</span>
                        <span class="pr-res-time">{move || walk_formula(mode.get(), guest.get(), host.get())}</span>
                    </div>
                    <Grid mode=mode guest=guest host=host />
                    <p class="vl-hint">"Каждая клетка — одно обращение к памяти при промахе; зелёная — сами данные."</p>
                    {move || res.get().map(|r| view! { <RunResult run=r /> })}
                </div>
            </div>
        </div>
    }
}

/// Кнопка переключателя режима.
#[component]
fn ModeButton(mode: RwSignal<Mode>, value: Mode, title: &'static str) -> impl IntoView {
    view! {
        <button class="vl-segbtn" class:on=move || mode.get() == value on:click=move |_| mode.set(value)>
            {title}
        </button>
    }
}

/// Выбор размера страницы.
#[component]
fn SizeSelect(label: &'static str, value: RwSignal<PageSize>) -> impl IntoView {
    let options = PageSize::ALL
        .into_iter()
        .map(|p| view! { <option value=size_key(p) selected=move || value.get() == p>{size_text(p)}</option> })
        .collect_view();
    view! {
        <label class="vl-field">
            <span>{label}</span>
            <select on:change=move |ev| {
                if let Some(p) = parse_size(&event_target_value(&ev)) {
                    value.set(p);
                }
            }>{options}</select>
        </label>
    }
}

/// Сетка обращений одного промаха.
#[component]
fn Grid(mode: RwSignal<Mode>, guest: RwSignal<PageSize>, host: RwSignal<PageSize>) -> impl IntoView {
    move || {
        let grid = walk_grid(mode.get(), guest.get(), host.get());
        view! {
            <div class="vl-grid2" style=format!("grid-template-columns: repeat({}, 22px)", grid.cols)>
                {grid.cells.into_iter().map(|data| view! { <i class={if data { "data" } else { "on" }}></i> }).collect_view()}
            </div>
        }
    }
}

/// Итог последнего запуска.
#[component]
fn RunResult(run: SimRun) -> impl IntoView {
    view! {
        <div class="vl-final">
            <table class="vl-stat">
                <tbody>
                    <tr><td>"обращений гостя"</td><td>{fmt_ru(run.accesses as f64)}</td></tr>
                    <tr>
                        <td>"промахов TLB"</td>
                        <td>{format!("{} (страница в TLB: {})", fmt_ru(run.misses as f64), size_key(run.eff_page))}</td>
                    </tr>
                    <tr><td>"цена одного промаха"</td><td>{format!("{} обращ.", run.walk)}</td></tr>
                    <tr><td>"выходов из-за правок таблиц"</td><td>{fmt_ru(run.exits as f64)}</td></tr>
                    <tr>
                        <td><b>"всего обращений к памяти"</b></td>
                        <td><b>{fmt_ru(run.cost as f64)}</b></td>
                    </tr>
                </tbody>
            </table>
            <p class="vl-hint">
                {format!("Выход стоит {} обращений; попадание в TLB — одно обращение к данным.", fmt_ru(EXIT_COST as f64))}
            </p>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use virtlab::ept::{default_goals, default_workloads};

    use super::*;

    #[test]
    fn grid_for_ept_has_data_cell_last() {
        let g = walk_grid(Mode::Ept, PageSize::K4, PageSize::K4);
        assert_eq!(g.cols, 5);
        assert_eq!(g.cells.len(), 25);
        assert_eq!(g.cells.iter().filter(|d| **d).count(), 1);
        assert_eq!(g.cells.last(), Some(&true));
        let g = walk_grid(Mode::Ept, PageSize::G1, PageSize::M2);
        assert_eq!((g.cols, g.cells.len()), (4, 12));
    }

    #[test]
    fn grid_for_shadow_is_one_row_of_min_levels() {
        // обход идёт по таблицам меньшей из двух страниц, то есть по большему числу уровней
        let g = walk_grid(Mode::Shadow, PageSize::K4, PageSize::M2);
        assert_eq!(g, WalkGrid { cols: 4, cells: vec![false; 4] });
        let g = walk_grid(Mode::Shadow, PageSize::M2, PageSize::G1);
        assert_eq!(g, WalkGrid { cols: 3, cells: vec![false; 3] });
        // число клеток сетки совпадает с ценой обхода модели
        for mode in [Mode::Shadow, Mode::Ept] {
            for g in PageSize::ALL {
                for h in PageSize::ALL {
                    let grid = walk_grid(mode, g, h);
                    let data = grid.cells.iter().filter(|d| **d).count() as u32;
                    assert_eq!(grid.cells.len() as u32 - data, ept::walk_cost(mode, g, h), "{mode:?} {g:?} {h:?}");
                }
            }
        }
    }

    #[test]
    fn formula_matches_mode() {
        assert_eq!(walk_formula(Mode::Ept, PageSize::K4, PageSize::K4), "(4+1)×(4+1)−1");
        assert_eq!(walk_formula(Mode::Shadow, PageSize::M2, PageSize::G1), "3 уровня");
    }

    #[test]
    fn size_keys_roundtrip() {
        for p in PageSize::ALL {
            assert_eq!(parse_size(size_key(p)), Some(p));
        }
        assert_eq!(parse_size("8K"), None);
    }

    #[test]
    fn default_walk_goal_is_reached_with_ept() {
        let (ws, gs) = (default_workloads(), default_goals());
        // 4 КиБ × 4 КиБ: промах стоит 24 обращения — цель «не больше 15» не достигается; 2 МиБ × 2 МиБ — ровно 15
        let cfg = SimInput { mode: Mode::Ept, guest: PageSize::K4, host: PageSize::K4, workload: "one".into() };
        let r = ept::simulate(&ws, &cfg).expect("запуск");
        assert!(reached(&gs, &r, &cfg).is_empty());
        let cfg = SimInput { guest: PageSize::M2, host: PageSize::M2, ..cfg };
        let r = ept::simulate(&ws, &cfg).expect("запуск");
        let ids: Vec<&str> = reached(&gs, &r, &cfg).iter().map(|g| g.id.as_str()).collect();
        assert_eq!(ids, ["walk"]);
        // цели других нагрузок не засчитываются
        let cfg = SimInput { workload: "scan".into(), ..cfg };
        let r = ept::simulate(&ws, &cfg).expect("запуск");
        assert!(reached(&gs, &r, &cfg).iter().all(|g| g.workload == "scan"));
    }
}
