//! Response language. The base course content is Russian; translations live in the `<table>_i18n` tables (field `lang`) and cover
//! a whole book: a book either has a translation into the request language or is served in Russian (`translated` -> `false`).

use axum::{
    extract::FromRequestParts,
    http::{header, request::Parts},
};

use crate::db::Db;

/// Interface languages. Russian is the language of the main content.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Lang {
    Ru,
    En,
}

impl Lang {
    pub const ALL: [Lang; 2] = [Lang::Ru, Lang::En];

    pub fn code(self) -> &'static str {
        match self {
            Lang::Ru => "ru",
            Lang::En => "en",
        }
    }

    /// Language for the lab engines (shared `i18n` crate).
    pub fn locale(self) -> i18n::Locale {
        match self {
            Lang::Ru => i18n::Locale::Ru,
            Lang::En => i18n::Locale::En,
        }
    }

    /// Language code from `ru`, `en-US`, `ru_RU` etc.; an unknown language - `None`.
    pub fn parse(tag: &str) -> Option<Lang> {
        let primary = tag.trim().split(['-', '_']).next()?.to_ascii_lowercase();
        Lang::ALL.into_iter().find(|l| l.code() == primary)
    }

    /// Language from the `Accept-Language` header: the first known tag (quality `q` is not parsed - order matters more for two languages).
    pub fn from_accept_language(header: &str) -> Option<Lang> {
        header.split(',').filter_map(|part| Lang::parse(part.split(';').next().unwrap_or(""))).next()
    }
}

/// `?lang=en` overrides the `Accept-Language` header; without them - Russian.
impl<S: Send + Sync> FromRequestParts<S> for Lang {
    type Rejection = std::convert::Infallible;

    async fn from_request_parts(parts: &mut Parts, _: &S) -> Result<Self, Self::Rejection> {
        let from_query = parts.uri.query().and_then(|q| q.split('&').find_map(|kv| kv.strip_prefix("lang=")).and_then(Lang::parse));
        let from_header = parts.headers.get(header::ACCEPT_LANGUAGE).and_then(|v| v.to_str().ok()).and_then(Lang::from_accept_language);
        Ok(from_query.or(from_header).unwrap_or(Lang::Ru))
    }
}

/// Whether the book is translated into the language (for Russian - always "base").
pub async fn translated(db: &Db, lang: Lang, book: i64) -> Result<bool, surrealdb::Error> {
    if lang == Lang::Ru {
        return Ok(false);
    }
    let mut res = db.query("SELECT VALUE bid FROM books_i18n WHERE bid = $b AND lang = $l LIMIT 1").bind(("b", book)).bind(("l", lang.code())).await?;
    let rows: Vec<i64> = res.take(0)?;
    Ok(!rows.is_empty())
}

/// Substitutes translated fields into the chapter's task rows: `table` - `tasks_i18n` or `lab_tasks_i18n`, rows are linked by `tid`.
/// A book without a translation (or the Russian language) is returned as is.
pub async fn overlay(db: &Db, table: &str, lang: Lang, book: i64, chapter: i64, rows: &mut [serde_json::Value], fields: &[&str]) -> Result<(), surrealdb::Error> {
    if rows.is_empty() || !translated(db, lang, book).await? {
        return Ok(());
    }
    let mut res = db.query(format!("SELECT * FROM {table} WHERE book = $b AND chapter = $c AND lang = $l")).bind(("b", book)).bind(("c", chapter)).bind(("l", lang.code())).await?;
    let texts: Vec<serde_json::Value> = res.take(0)?;
    for row in rows.iter_mut() {
        let Some(t) = texts.iter().find(|t| t["tid"] == row["tid"]) else { continue };
        for f in fields {
            if let Some(v) = t.get(*f).filter(|v| v.is_string()) {
                row[*f] = v.clone();
            }
        }
    }
    Ok(())
}

/// Table and selection condition: the base table without a condition or `<table>_i18n` with a language condition (`$l` is bound by the caller).
pub fn source(table: &str, translated: bool) -> (String, &'static str) {
    if translated {
        (format!("{table}_i18n"), " AND lang = $l")
    } else {
        (table.to_string(), "")
    }
}

#[cfg(test)]
mod tests {
    use super::Lang;

    #[test]
    fn parses_tags() {
        assert_eq!(Lang::parse("en-US"), Some(Lang::En));
        assert_eq!(Lang::parse("RU"), Some(Lang::Ru));
        assert_eq!(Lang::parse("de"), None);
        assert_eq!(Lang::from_accept_language("de-DE,de;q=0.9,en;q=0.8"), Some(Lang::En));
        assert_eq!(Lang::from_accept_language("fr"), None);
    }
}
