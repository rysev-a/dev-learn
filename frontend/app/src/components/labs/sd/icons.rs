//! Значки компонентов на поле схемы: содержимое `<svg>` 24×24 (контур, как у остальных значков приложения).

use sdlab::Kind;

/// Разметка значка вида компонента (внутренность элемента `<g>`).
pub fn markup(kind: Kind) -> &'static str {
    match kind {
        Kind::Clients => r#"<circle cx="12" cy="8" r="3.5"/><path d="M5 20a7 7 0 0 1 14 0"/>"#,
        Kind::Cdn => r#"<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/>"#,
        Kind::Limiter => r#"<path d="M4 5h16l-6 8v6l-4-2v-4L4 5Z"/>"#,
        Kind::Gateway => r#"<path d="M4 20V10l8-6 8 6v10"/><path d="M9 20v-6h6v6"/>"#,
        Kind::Lb => r#"<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="19" r="2.2"/><circle cx="19" cy="19" r="2.2"/><path d="M12 7v4M12 11l-6 6M12 11l6 6"/>"#,
        Kind::Ws => r#"<path d="M4 8l4 4-4 4M20 8l-4 4 4 4"/><path d="M13 6l-2 12"/>"#,
        Kind::App => r#"<rect x="3" y="3" width="18" height="8" rx="2"/><rect x="3" y="13" width="18" height="8" rx="2"/><path d="M7 7h.01M7 17h.01"/>"#,
        Kind::Cache => r#"<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/>"#,
        Kind::Queue => r#"<rect x="3" y="7" width="5" height="10" rx="1"/><rect x="9.5" y="7" width="5" height="10" rx="1"/><rect x="16" y="7" width="5" height="10" rx="1"/>"#,
        Kind::Worker => r#"<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>"#,
        Kind::Db => r#"<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>"#,
        Kind::Blob => r#"<path d="M21 8 12 3 3 8v8l9 5 9-5V8Z"/><path d="M3 8l9 5 9-5M12 13v8"/>"#,
        Kind::Search => r#"<circle cx="11" cy="11" r="6.5"/><path d="m16 16 5 5"/>"#,
        Kind::Monitor => r#"<path d="M3 12h4l3-7 4 14 3-7h4"/>"#,
        Kind::Auth => r#"<circle cx="8" cy="12" r="4"/><path d="M12 12h9M18 12v3M21 12v2"/>"#,
        Kind::Geo => r#"<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/>"#,
        Kind::Ml => r#"<circle cx="6" cy="7" r="2"/><circle cx="6" cy="17" r="2"/><circle cx="18" cy="12" r="2.4"/><path d="M8 7l8 4M8 17l8-4"/>"#,
        Kind::Pay => r#"<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h3"/>"#,
        Kind::Stream => r#"<path d="M3 8h13l-3-3M21 16H8l3 3"/>"#,
        Kind::Notify => r#"<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4l2-2Z"/><path d="M10 21a2 2 0 0 0 4 0"/>"#,
        Kind::Analytics => r#"<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>"#,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_kind_has_a_balanced_icon() {
        for k in Kind::ALL {
            let m = markup(k);
            assert!(m.starts_with('<') && m.ends_with("/>"), "{k}: {m}");
            assert_eq!(m.matches('<').count(), m.matches("/>").count(), "{k}: каждый элемент закрыт");
            assert_eq!(m.matches('"').count() % 2, 0, "{k}: кавычки парные");
        }
    }
}
