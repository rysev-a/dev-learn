//! Object icons on the board: contents of a 24×24 `<svg>` (outline, like the app's other icons).

use virtlab::lvm_board::Kind;

/// Markup of an object kind's icon (the inside of a `<g>` element).
pub fn markup(kind: Kind) -> &'static str {
    match kind {
        Kind::Disk => r#"<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6"/><path d="M16 17h.01"/>"#,
        Kind::Pv => r#"<rect x="3" y="7" width="18" height="10" rx="2"/><path d="M7 7v10M17 12h.01"/>"#,
        Kind::Vg => r#"<rect x="3" y="3" width="8" height="8" rx="1.5"/><rect x="13" y="3" width="8" height="8" rx="1.5"/><rect x="3" y="13" width="18" height="8" rx="1.5"/>"#,
        Kind::Lv => r#"<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M3 14h18"/>"#,
        Kind::ThinPool => r#"<path d="M5 4h14l-2 16H7z"/><path d="M6.5 12h11"/>"#,
        Kind::ThinLv => r#"<rect x="3" y="5" width="18" height="14" rx="2" stroke-dasharray="3 2.5"/><path d="M3 12h18"/>"#,
        Kind::Snapshot => r#"<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7l1.5-3h5L16 7"/><circle cx="12" cy="13.5" r="3"/>"#,
        Kind::Fs => r#"<path d="M4 4h10l6 6v10H4z"/><path d="M14 4v6h6M8 14h8M8 17h5"/>"#,
        Kind::Vm => r#"<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>"#,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_kind_has_a_balanced_icon() {
        let _ru = locales::guard(i18n::Locale::Ru);
        for k in Kind::ALL {
            let m = markup(k);
            assert!(m.starts_with('<') && m.ends_with("/>"), "{k:?}: {m}");
            assert_eq!(m.matches('<').count(), m.matches("/>").count(), "{k:?}: every element is closed");
            assert_eq!(m.matches('"').count() % 2, 0, "{k:?}: quotes are paired");
        }
    }
}
