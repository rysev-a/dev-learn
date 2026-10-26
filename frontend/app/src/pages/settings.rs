//! Страница настроек: внешний вид хранится в браузере (`localStorage`) и применяется сразу, прогресс и аккаунт — в кабинете.

use api::dto::ResetScope;
use leptos::{prelude::*, task::spawn_local};

use crate::{
    components::aside::AsideState,
    hooks::client,
    player::Player,
    progress::ProgressStore,
    session::Session,
    settings::{self, Flag, Theme},
    themes,
};
use highlight::{highlight, Lang};

/// Тексты строки сброса: название, пояснение, вопрос в подтверждении и подпись кнопки.
#[derive(Clone, Copy)]
struct ResetCopy {
    title: &'static str,
    text: &'static str,
    confirm: &'static str,
    button: &'static str,
}

fn reset_copy(scope: ResetScope) -> ResetCopy {
    match scope {
        ResetScope::Practice => ResetCopy {
            title: "Сбросить прогресс упражнений",
            text: "Удаляет статусы задач, черновики кода и историю попыток. Вопросы и слайды не затрагиваются.",
            confirm: "Удалить решения, черновики и историю попыток во всех упражнениях?",
            button: "Сбросить",
        },
        ResetScope::All => ResetCopy {
            title: "Сбросить весь прогресс",
            text: "Обнуляет дашборд на главной: просмотренные слайды, ответы на вопросы и упражнения.",
            confirm: "Обнулить весь прогресс: слайды, вопросы и упражнения?",
            button: "Сбросить всё",
        },
    }
}

/// Подтверждение браузера; без окна (или при отказе) — «нет».
fn confirm(question: &str) -> bool {
    web_sys::window().and_then(|w| w.confirm_with_message(question).ok()).unwrap_or(false)
}

#[component]
pub fn SettingsPage(theme: RwSignal<Theme>) -> impl IntoView {
    let aside = expect_context::<AsideState>();
    // какой сброс только что выполнен и чем закончился неудачный
    let done = RwSignal::new(None::<ResetScope>);
    let failure = RwSignal::new(None::<String>);
    view! {
        <main class="set-page">
            <section class="set-card">
                <h2>"Настройки"</h2>
                <p class="set-sub">"Внешний вид хранится в этом браузере и применяется сразу; прогресс — в вашем кабинете на сервере."</p>

                <h3 class="set-group">"Аккаунт"</h3>
                <AccountRow />

                <h3 class="set-group">"Внешний вид"</h3>
                <SwitchRow
                    title="Светлая тема"
                    text="Переключает тёмную и светлую палитру интерфейса и слайдов."
                    on=Signal::derive(move || theme.get() == Theme::Light)
                    on_toggle=Callback::new(move |()| settings::switch_theme(theme, theme.get_untracked().toggled()))
                />
                <PalettePicker theme=theme />
                <SwitchRow
                    title="Свёрнутое меню разделов"
                    text="Вместо названий в левом меню — колонка иконок. Можно переключать и кнопкой над меню."
                    on=Signal::derive(move || aside.is_collapsed())
                    on_toggle=Callback::new(move |()| aside.set(!aside.is_collapsed()))
                />

                <h3 class="set-group">"Слайды"</h3>
                <FlagRow
                    flag=settings::ANIM_FLAG
                    title="Автопроигрывание анимаций"
                    text="Схемы на слайдах сами проходят шаги по таймеру, когда озвучка выключена. Если отключить, схема сразу показывает итог, а шаги переключаются вручную."
                />

                <h3 class="set-group">"Упражнения"</h3>
                <FlagRow
                    flag=settings::AUTO_NEXT_FLAG
                    title="Автопереход к следующему упражнению"
                    text="Когда проверка кода прошла успешно, через секунду открывается следующее упражнение (после последнего — первое упражнение следующей главы). По умолчанию выключено: решение остаётся на экране, дальше — по кнопке или Ctrl+Enter."
                />

                <h3 class="set-group">"Диаграммы"</h3>
                <FlagRow
                    flag=settings::AUTOWIRE_LAB_FLAG
                    title="Автосвязывание в «Архитектуре компьютера»"
                    text="Пока вы двигаете вентиль или блок, подходящие выводы соседей показываются пунктиром и соединяются сами при отпускании. Если выключить, провода тянутся только вручную."
                />
                <FlagRow
                    flag=settings::AUTOWIRE_SD_FLAG
                    title="Автосвязывание в «Системном дизайне»"
                    text="Новый или перетаскиваемый компонент сам подключается к подходящим соседям (пунктир-подсказка). Если выключить, связи тянутся от выходного порта к входному вручную."
                />

                <h3 class="set-group">"Прогресс"</h3>
                <ResetRow scope=ResetScope::Practice done=done failure=failure />
                <ResetRow scope=ResetScope::All done=done failure=failure />
                {move || failure.get().map(|e| view! { <p class="error">{e}</p> })}
            </section>
        </main>
    }
}

/// Кто вошёл и кнопка «Выйти».
#[component]
fn AccountRow() -> impl IntoView {
    let session = expect_context::<Session>();
    let player = expect_context::<Player>();
    let name = move || session.identity.get().map(|i| i.user.display()).unwrap_or_default();
    let email = move || session.identity.get().map(|i| i.user.email).unwrap_or_default();
    view! {
        <div class="set-row">
            <div class="set-row-text">
                <span class="set-row-title">{name}</span>
                <span class="set-row-desc">{email}". Прогресс, ответы и история попыток хранятся в кабинете и доступны с любого браузера."</span>
            </div>
            <button
                class="quiz-btn ghost"
                on:click=move |_| {
                    player.stop();
                    session.logout(client());
                }
            >
                "Выйти"
            </button>
        </div>
    }
}

/// Образец кода на карточке темы: цвета берутся из переменных карточки (`data-palette`), как в редакторе.
const SAMPLE: [&str; 3] = ["def total(xs):  # сумма", "    return sum(xs) + 42", "print(\"итого\", total([1, 2]))"];

/// Выбор цветовой темы: интерфейс, слайды и редактор кода. Карточки показывают тему вживую, выбор переключает и светлый или тёмный режим.
#[component]
fn PalettePicker(theme: RwSignal<Theme>) -> impl IntoView {
    let dark = RwSignal::new(settings::read_palette(Theme::Dark));
    let light = RwSignal::new(settings::read_palette(Theme::Light));
    let group = move |title: &'static str, mode: Theme, chosen: RwSignal<String>| {
        let cards = themes::of_mode(mode)
            .map(|p| {
                let id = p.id;
                let active = move || theme.get() == mode && chosen.get() == id;
                let code = SAMPLE
                    .iter()
                    .map(|line| {
                        let tokens = highlight(Lang::Python, line)
                            .into_iter()
                            .map(|t| match t.kind.css() {
                                Some(color) => view! { <span style=format!("color: {color}")>{t.text}</span> }.into_any(),
                                None => t.text.into_any(),
                            })
                            .collect_view();
                        view! { <div>{tokens}" "</div> }
                    })
                    .collect_view();
                view! {
                    <button
                        type="button"
                        class="palette-card"
                        class:on=active
                        data-palette=themes::card_id(p)
                        aria-pressed=move || active().to_string()
                        on:click=move |_| {
                            chosen.set(id.to_string());
                            settings::choose_palette(theme, mode, id);
                        }
                    >
                        <span class="palette-name">{p.name}</span>
                        <span class="palette-code">{code}</span>
                        <span class="palette-chips"><i style="background: var(--accent)"></i><i style="background: var(--green)"></i><i style="background: var(--amber)"></i><i style="background: var(--error)"></i><i style="background: var(--syn-keyword, var(--s-blue))"></i><i style="background: var(--syn-string, var(--s-amber))"></i></span>
                    </button>
                }
            })
            .collect_view();
        view! {
            <div class="palette-group">
                <span class="set-row-title">{title}</span>
                <div class="palette-grid">{cards}</div>
            </div>
        }
    };
    view! {
        <div class="set-row palette-row">
            <div class="set-row-text">
                <span class="set-row-title">"Цветовая тема"</span>
                <span class="set-row-desc">"Цвета интерфейса, слайдов и редактора кода. Выбор темы переключает светлый или тёмный режим; для каждого режима тема запоминается отдельно."</span>
            </div>
            {group("Тёмные", Theme::Dark, dark)}
            {group("Светлые", Theme::Light, light)}
        </div>
    }
}

/// Строка с переключателем.
#[component]
fn SwitchRow(title: &'static str, text: &'static str, #[prop(into)] on: Signal<bool>, on_toggle: Callback<()>) -> impl IntoView {
    view! {
        <div class="set-row">
            <div class="set-row-text">
                <span class="set-row-title">{title}</span>
                <span class="set-row-desc">{text}</span>
            </div>
            <button
                type="button"
                role="switch"
                aria-checked=move || on.get().to_string()
                aria-label=title
                class="set-switch"
                class:on=move || on.get()
                on:click=move |_| on_toggle.run(())
            >
                <i></i>
            </button>
        </div>
    }
}

/// Переключатель настройки из `localStorage`: значение читается при открытии, запись — при каждом щелчке.
#[component]
fn FlagRow(flag: Flag, title: &'static str, text: &'static str) -> impl IntoView {
    let on = RwSignal::new(flag.read());
    let toggle = Callback::new(move |()| {
        let next = !on.get_untracked();
        flag.write(next);
        on.set(next);
    });
    view! { <SwitchRow title=title text=text on=on on_toggle=toggle /> }
}

/// Строка сброса прогресса: подтверждение, запрос на сервер, пометка «Готово».
#[component]
fn ResetRow(scope: ResetScope, done: RwSignal<Option<ResetScope>>, failure: RwSignal<Option<String>>) -> impl IntoView {
    let progress = expect_context::<ProgressStore>();
    let copy = reset_copy(scope);
    let busy = RwSignal::new(false);
    let reset = move |_| {
        if busy.get_untracked() || !confirm(copy.confirm) {
            return;
        }
        busy.set(true);
        failure.set(None);
        spawn_local(async move {
            match progress.reset(scope).await {
                Ok(()) => done.set(Some(scope)),
                Err(e) => failure.set(Some(e.message)),
            }
            busy.set(false);
        });
    };
    view! {
        <div class="set-row">
            <div class="set-row-text">
                <span class="set-row-title">{copy.title}</span>
                <span class="set-row-desc">
                    {copy.text}
                    {move || (done.get() == Some(scope)).then(|| view! { <b class="set-done">" Готово."</b> })}
                </span>
            </div>
            <button class="quiz-btn ghost" disabled=move || busy.get() on:click=reset>{copy.button}</button>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn each_reset_has_its_own_wording_and_asks_before_deleting() {
        let (practice, all) = (reset_copy(ResetScope::Practice), reset_copy(ResetScope::All));
        assert_ne!(practice.title, all.title);
        assert_ne!(practice.confirm, all.confirm);
        assert!(practice.confirm.ends_with('?') && all.confirm.ends_with('?'));
        assert!(practice.text.contains("Вопросы и слайды не затрагиваются"), "сброс упражнений не трогает вопросы и слайды");
    }
}
