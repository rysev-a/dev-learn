//! Вкладка «Теория»: слайды главы с плеером и окном «За кадром». Для глав, ещё не перенесённых на Leptos, — текст уроков.

use std::sync::Arc;

use api::dto::Chapter;
use content::Chapter as SlideChapter;
use leptos::prelude::*;
use leptos_router::hooks::query_signal;
use scene::{provide_env, SceneEnv};

use super::ChapterCtx;
use crate::{
    components::{
        blocks::DataSlide,
        slides::SlidePanel,
        voice_popup::VoicePopup,
    },
    hooks::{use_load, Load},
    player::{estimate_seconds, Player},
    progress::ProgressStore,
    settings,
};

/// Длительности абзацев главы: озвучка, если файл есть, иначе виртуальные часы.
pub fn durations(ch: &Chapter) -> Vec<f64> {
    ch.lessons.iter().map(|l| if l.dur > 0.0 { l.dur } else { estimate_seconds(&l.text) }).collect()
}

/// Позиция в главе: сумма абзацев до показанного плюс время внутри него.
pub fn chapter_position(durations: &[f64], shown: usize, inside: Option<f64>) -> f64 {
    durations.iter().take(shown).sum::<f64>() + inside.unwrap_or(0.0)
}

/// Слайды главы: данные с бэкенда; у главы без слайдов — текст урока.
#[component]
pub fn Theory() -> impl IntoView {
    let ctx = expect_context::<ChapterCtx>();
    let book = ctx.book;
    let chapter = ctx.chapter;
    let slides = use_load(
        move || chapter.get().ready().map(|c| c.num),
        move |client, num| async move { client.slides(book, num).await },
    );
    move || match (chapter.get(), slides.get()) {
        (Load::Ready(ch), Load::Ready(Some(data))) => view! { <Slides book=book chapter=ch deck=Deck::data(data) /> }.into_any(),
        (Load::Ready(ch), Load::Ready(None)) => view! { <PlainText chapter=ch /> }.into_any(),
        (Load::Failed(e), _) | (_, Load::Failed(e)) => view! { <p class="error">{e}</p> }.into_any(),
        _ => view! { <p class="empty">"Загрузка…"</p> }.into_any(),
    }
}

/// Название слайда в списке полного экрана: короткое (`short`), если задано, иначе заголовок.
pub fn fs_title(short: Option<&str>, title: &str) -> String {
    short.filter(|s| !s.trim().is_empty()).unwrap_or(title).to_string()
}

/// Колода слайдов главы: число слайдов, их названия для списка полного экрана и функция «слайд i → вид».
#[derive(Clone)]
struct Deck {
    count: usize,
    titles: Vec<String>,
    frame: Arc<dyn Fn(usize) -> AnyView + Send + Sync>,
}

impl Deck {
    fn data(ch: SlideChapter) -> Self {
        let (rubric, slides) = (ch.rubric, ch.slides);
        let count = slides.len();
        Deck {
            count,
            titles: slides.iter().map(|s| fs_title(s.short.as_deref(), &s.title)).collect(),
            frame: Arc::new(move |i| view! { <DataSlide rubric=rubric.clone() n=i + 1 total=count slide=slides[i].clone() /> }.into_any()),
        }
    }
}

/// Глава без слайдов на Leptos: сам текст урока по абзацам.
#[component]
fn PlainText(chapter: Chapter) -> impl IntoView {
    let paragraphs = chapter.lessons.into_iter().map(|l| view! { <p class="s-hint">{l.text}</p> }).collect_view();
    view! {
        <p class="empty">"Слайды этой главы ещё не перенесены на Leptos — они есть в React-версии. Текст урока:"</p>
        {paragraphs}
    }
}

#[component]
fn Slides(book: i64, chapter: Chapter, deck: Deck) -> impl IntoView {
    let player = expect_context::<Player>();
    let progress = expect_context::<ProgressStore>();
    let count = deck.count;
    let titles = deck.titles;
    let (manual, set_manual) = query_signal::<usize>("slide");
    let durs = durations(&chapter);
    let total: f64 = durs.iter().sum();
    let num = chapter.num;
    on_cleanup(move || player.stop());

    // слайд следует за читаемым абзацем, иначе — ручной выбор (он живёт в адресе: перезагрузка возвращает на тот же слайд)
    let idx = Memo::new(move |_| player.playing.get().or_else(|| manual.get()).unwrap_or(0).min(count - 1));
    let playing = Signal::derive(move || player.playing.get().is_some() && !player.paused.get());
    // просмотренный слайд идёт в прогресс (дашборд на главной)
    Effect::new(move |_| progress.mark_slide(book, num, idx.get()));

    let start_from = {
        let durs = durs.clone();
        move |i: usize| {
            player.start(durs.clone(), i);
            set_manual.set(None);
        }
    };
    // клик по слайду: если глава играет — начинаем с этой части, иначе просто показываем слайд
    let on_pick = {
        let start_from = start_from.clone();
        Callback::new(move |i: usize| {
            if player.playing.get_untracked().is_some() {
                if player.playing.get_untracked() == Some(i) && player.paused.get_untracked() {
                    player.toggle_pause();
                } else {
                    start_from(i);
                }
            } else {
                set_manual.set(Some(i));
            }
        })
    };
    let on_play = Callback::new(move |()| {
        if player.playing.get_untracked().is_some() {
            if player.paused.get_untracked() {
                player.toggle_pause();
            }
        } else {
            start_from(manual.get_untracked().unwrap_or(0).min(count - 1));
        }
    });
    let on_pause = Callback::new(move |()| {
        if playing.get_untracked() {
            player.toggle_pause();
        }
    });

    let time = {
        let durs = durs.clone();
        Signal::derive(move || {
            let shown = idx.get();
            let inside = player.audio_time(shown);
            (chapter_position(&durs, shown, inside), total)
        })
    };
    let stage = {
        let frame = deck.frame.clone();
        Callback::new(move |i: usize| {
            // среда сцены: время озвучки этого слайда и режим «без движения»
            provide_env(SceneEnv { audio_time: Signal::derive(move || player.audio_time(i)), motion_off: settings::motion_off() });
            frame(i)
        })
    };
    let lessons = chapter.lessons;
    let popup = {
        let durs = durs.clone();
        move || {
            let i = idx.get();
            let lesson = lessons.iter().find(|l| l.ord == i)?;
            let (text, d) = (lesson.text.clone(), durs.get(i).copied().unwrap_or(3.0));
            Some(view! { <VoicePopup text=text t=Signal::derive(move || player.audio_time(i)) d=d /> })
        }
    };
    view! {
        <div>
            {popup}
            <SlidePanel idx=idx count=count titles=titles time=time playing=playing on_play=on_play on_pause=on_pause on_pick=on_pick stage=stage />
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn full_screen_list_prefers_the_short_title() {
        assert_eq!(fs_title(Some("Кратко"), "Длинный заголовок слайда"), "Кратко");
        assert_eq!(fs_title(None, "Заголовок"), "Заголовок");
        assert_eq!(fs_title(Some("  "), "Заголовок"), "Заголовок", "пустое короткое название не показываем");
    }

    #[test]
    fn position_is_the_sum_of_earlier_parts_plus_time_inside() {
        let d = [10.0, 20.0, 30.0];
        assert_eq!(chapter_position(&d, 0, None), 0.0);
        assert_eq!(chapter_position(&d, 2, None), 30.0);
        assert_eq!(chapter_position(&d, 2, Some(4.5)), 34.5);
        assert_eq!(chapter_position(&d, 9, None), 60.0, "слайд за концом не ломает сумму");
    }
}
