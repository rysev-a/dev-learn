//! Язык ответа. Базовое содержимое курса — русское; переводы лежат в таблицах `<таблица>_i18n` (поле `lang`) и покрывают
//! книгу целиком: у книги либо есть перевод на язык запроса, либо она отдаётся по-русски (`translated` → `false`).

use axum::{
    extract::FromRequestParts,
    http::{header, request::Parts},
};

use crate::db::Db;

/// Языки интерфейса. Русский — язык основного содержимого.
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

    /// Язык для движков лабораторий (общий крейт `i18n`).
    pub fn locale(self) -> i18n::Locale {
        match self {
            Lang::Ru => i18n::Locale::Ru,
            Lang::En => i18n::Locale::En,
        }
    }

    /// Код языка из `ru`, `en-US`, `ru_RU` и т. п.; неизвестный язык — `None`.
    pub fn parse(tag: &str) -> Option<Lang> {
        let primary = tag.trim().split(['-', '_']).next()?.to_ascii_lowercase();
        Lang::ALL.into_iter().find(|l| l.code() == primary)
    }

    /// Язык по заголовку `Accept-Language`: первый из известных тегов (качество `q` не разбираем — порядок важнее для двух языков).
    pub fn from_accept_language(header: &str) -> Option<Lang> {
        header.split(',').filter_map(|part| Lang::parse(part.split(';').next().unwrap_or(""))).next()
    }
}

/// `?lang=en` важнее заголовка `Accept-Language`; без них — русский.
impl<S: Send + Sync> FromRequestParts<S> for Lang {
    type Rejection = std::convert::Infallible;

    async fn from_request_parts(parts: &mut Parts, _: &S) -> Result<Self, Self::Rejection> {
        let from_query = parts.uri.query().and_then(|q| q.split('&').find_map(|kv| kv.strip_prefix("lang=")).and_then(Lang::parse));
        let from_header = parts.headers.get(header::ACCEPT_LANGUAGE).and_then(|v| v.to_str().ok()).and_then(Lang::from_accept_language);
        Ok(from_query.or(from_header).unwrap_or(Lang::Ru))
    }
}

/// Переведена ли книга на язык (для русского — всегда «базовое»).
pub async fn translated(db: &Db, lang: Lang, book: i64) -> Result<bool, surrealdb::Error> {
    if lang == Lang::Ru {
        return Ok(false);
    }
    let mut res = db.query("SELECT VALUE bid FROM books_i18n WHERE bid = $b AND lang = $l LIMIT 1").bind(("b", book)).bind(("l", lang.code())).await?;
    let rows: Vec<i64> = res.take(0)?;
    Ok(!rows.is_empty())
}

/// Подставляет переведённые поля в строки задач главы: `table` — `tasks_i18n` или `lab_tasks_i18n`, строки связываются по `tid`.
/// Книга без перевода (или русский язык) отдаётся как есть.
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

/// Таблица и условие выборки: базовая таблица без условия или `<таблица>_i18n` с условием на язык (`$l` привязывает вызывающий).
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
