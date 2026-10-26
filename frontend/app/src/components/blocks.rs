//! Блоки тела слайда из данных ([`content::Block`]) и рамка слайда: один общий компонент на все главы.

use content::{
    slide::{Card, Cell, Topic},
    Block, Lang, Slide,
};
use highlight::{highlight, Kind};
use leptos::prelude::*;
use scene::SceneView;

/// Класс подсветки из `App.css` (`rs-*`) для токена.
fn token_class(lang: Lang, kind: Kind, text: &str) -> Option<&'static str> {
    Some(match kind {
        Kind::Plain => return None,
        Kind::Comment => "rs-com",
        Kind::Str => "rs-str",
        Kind::Number => "rs-num",
        Kind::Keyword => "rs-kw",
        Kind::Builtin => {
            if lang == Lang::Rust {
                if text.starts_with('\'') {
                    "rs-life"
                } else {
                    "rs-ty"
                }
            } else {
                "rs-kw"
            }
        }
        Kind::Accent => {
            if text.ends_with('!') {
                "rs-mac"
            } else {
                "rs-fn"
            }
        }
    })
}

/// Врезка кода: строки подсвечиваются по языку.
#[component]
fn CodeBlock(lang: Lang, text: String) -> impl IntoView {
    let lines = text
        .split('\n')
        .map(|line| {
            highlight(lang, line)
                .into_iter()
                .map(|t| match token_class(lang, t.kind, &t.text) {
                    Some(c) => view! { <span class=c>{t.text}</span> }.into_any(),
                    None => t.text.into_any(),
                })
                .collect_view()
        })
        .collect::<Vec<_>>();
    let last = lines.len().saturating_sub(1);
    view! {
        <pre class="rs-code">
            {lines.into_iter().enumerate().map(|(i, l)| view! { {l}{(i < last).then_some("\n")} }).collect_view()}
        </pre>
    }
}

/// Текст с вставками кода: `` `код` `` — моноширинная вставка.
pub fn inline(text: &str) -> impl IntoView {
    text.split('`')
        .enumerate()
        .map(|(i, part)| if i % 2 == 1 { view! { <span class="s-path">{part.to_string()}</span> }.into_any() } else { part.to_string().into_any() })
        .collect_view()
}

fn card_view(c: Card) -> impl IntoView {
    let title_class = if c.mono { "s-node-mono" } else { "s-node-title" };
    view! {
        <div class=format!("s-node {}", c.kind)>
            <span class=title_class>{c.title}</span>
            {c.sub.map(|s| view! { <span class="s-node-sub">{s}</span> })}
        </div>
    }
}

fn topic_view(t: Topic) -> impl IntoView {
    view! {
        <div class="s-topic">
            <span class="s-topic-big">{t.big}</span>
            <span class="s-divider"></span>
            <span class="s-node-title">{t.title}</span>
            <span class="s-node-sub">{t.sub}</span>
        </div>
    }
}

/// Один блок тела слайда.
#[component]
pub fn BlockView(block: Block) -> impl IntoView {
    match block {
        Block::Scene(spec) => view! { <SceneView spec=spec /> }.into_any(),
        Block::Code { lang, text } => view! { <CodeBlock lang=lang text=text /> }.into_any(),
        Block::Cmd { text } => view! { <div class="s-cmd"><pre>{text}</pre></div> }.into_any(),
        Block::Label { text } => view! { <div class="s-label">{text}</div> }.into_any(),
        Block::Note { text } => view! { <div class="s-note">{inline(&text)}</div> }.into_any(),
        Block::Hint { text } => view! { <p class="s-hint">{inline(&text)}</p> }.into_any(),
        Block::Topics { items } => view! { <div class="s-grid2">{items.into_iter().map(topic_view).collect_view()}</div> }.into_any(),
        Block::Grid { cards } => view! { <div class="s-grid2">{cards.into_iter().map(card_view).collect_view()}</div> }.into_any(),
        Block::Cols { cells } => view! {
            <div class="s-cols">
                {cells.into_iter().map(|c| match c {
                    Cell::Card(card) => card_view(card).into_any(),
                    Cell::Arrow => view! { <span class="s-arr">"→"</span> }.into_any(),
                }).collect_view()}
            </div>
        }
        .into_any(),
        Block::Table { rows } => view! {
            <div class="s-table">
                {rows.into_iter().map(|(l, r)| view! { <div><span class="s-path accent">{l}</span><span>{r}</span></div> }).collect_view()}
            </div>
        }
        .into_any(),
    }
}

/// Рамка слайда: рубрика с номером, заголовок, подзаголовок, тело (блоки) и блок «ГЛАВНОЕ».
#[component]
pub fn DataSlide(rubric: String, n: usize, total: usize, slide: Slide) -> impl IntoView {
    let body = slide.body.into_iter().map(|block| view! { <BlockView block=block /> }).collect_view();
    view! {
        <div class="slide">
            <div class="s-rubric">
                <span>{rubric}</span>
                <span>{format!("{n:02} / {total}")}</span>
            </div>
            <h3 class="s-title">{slide.title}</h3>
            {slide.sub.map(|s| view! { <p class="s-sub">{s}</p> })}
            <div class="s-divider"></div>
            <div class="s-body">{body}</div>
            <div class="s-main">
                <span class="s-main-label">"ГЛАВНОЕ"</span>
                <span class="s-main-text">{slide.main}</span>
            </div>
        </div>
    }
}
