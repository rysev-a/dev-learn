//! Object icons on the board: contents of a 24×24 `<svg>` (outline, like the app's other icons).

use virtlab::net_board::Kind;

/// Markup of an object kind's icon (the inside of a `<g>` element).
pub fn markup(kind: Kind) -> &'static str {
    match kind {
        Kind::Netns => r#"<rect x="3" y="3" width="18" height="18" rx="3" stroke-dasharray="3 2.5"/><path d="M8 12h8M12 8v8"/>"#,
        Kind::Eth => r#"<rect x="3" y="8" width="18" height="10" rx="2"/><path d="M7 8V5M12 8V5M17 8V5M7 18v2M17 18v2"/>"#,
        Kind::Veth => r#"<path d="M3 8h8l2 8h8"/><circle cx="4" cy="8" r="1.4"/><circle cx="20" cy="16" r="1.4"/>"#,
        Kind::Bridge => r#"<rect x="3" y="9" width="18" height="6" rx="2"/><path d="M7 9V5M12 9V5M17 9V5M7 15v4M12 15v4M17 15v4"/>"#,
        Kind::Bond => r#"<path d="M4 6h6c4 0 4 12 8 12h2M4 18h6c4 0 4-12 8-12h2"/>"#,
        Kind::Vlan => r#"<rect x="3" y="4" width="18" height="6" rx="1.5"/><rect x="3" y="14" width="18" height="6" rx="1.5"/><path d="M8 7h.01M8 17h.01"/>"#,
        Kind::Vm => r#"<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>"#,
        Kind::External => r#"<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>"#,
        Kind::Nat => r#"<path d="M4 8h13l-3-3M20 16H7l3 3"/>"#,
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
