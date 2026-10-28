//! Русский словарь: ключ — английский текст, значение — русский перевод. Записи лежат по областям, чтобы файлы оставались обозримыми.

mod ui;
mod archlab;
mod labs_ui;
mod netlab;
mod riscvlab;
mod server;
mod sdlab;
mod virtlab;
mod weblab;

/// Словари всех областей.
const DICTS: &[&[(&str, &str)]] = &[ui::RU, archlab::RU, labs_ui::RU, netlab::RU, riscvlab::RU, server::RU, sdlab::RU, virtlab::RU, weblab::RU];

/// Все записи словаря: (английский ключ, русский перевод).
pub fn entries() -> impl Iterator<Item = (&'static str, &'static str)> {
    DICTS.iter().flat_map(|d| d.iter().copied())
}
