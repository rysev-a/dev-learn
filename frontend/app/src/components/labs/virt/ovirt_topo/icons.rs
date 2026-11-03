//! Object icons on the board: contents of a 24×24 `<svg>` (outline, like the app's other icons).

use virtlab::ovirt_topo::Kind;

/// Markup of an object kind's icon (the inside of a `<g>` element).
pub fn markup(kind: Kind) -> &'static str {
    match kind {
        Kind::Engine => r#"<rect x="4" y="3" width="16" height="12" rx="2"/><path d="M8 21h8M12 15v6M8 8l2 2-2 2M13 12h3"/>"#,
        Kind::DataCenter => r#"<path d="M3 21V9l6-4v16M9 21V12l6-3v12M15 21V8l6 3v10M2 21h20"/>"#,
        Kind::Cluster => r#"<rect x="3" y="3" width="8" height="8" rx="1.5"/><rect x="13" y="3" width="8" height="8" rx="1.5"/><rect x="3" y="13" width="8" height="8" rx="1.5"/><rect x="13" y="13" width="8" height="8" rx="1.5"/>"#,
        Kind::Host => r#"<rect x="3" y="3" width="18" height="8" rx="2"/><rect x="3" y="13" width="18" height="8" rx="2"/><path d="M7 7h.01M7 17h.01"/>"#,
        Kind::Network => r#"<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="19" r="2.2"/><circle cx="19" cy="19" r="2.2"/><path d="M12 7v4M12 11l-6 6M12 11l6 6"/>"#,
        Kind::StorageDomain => r#"<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>"#,
        Kind::Vm => r#"<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>"#,
        Kind::FenceAgent => r#"<path d="M12 3v8"/><path d="M6.4 6.6a8 8 0 1 0 11.2 0"/>"#,
        Kind::AffinityGroup => r#"<circle cx="8" cy="12" r="5"/><circle cx="16" cy="12" r="5"/>"#,
        Kind::Backup => r#"<path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/><path d="M12 8v4l3 2"/>"#,
        Kind::User => r#"<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>"#,
        Kind::Permission => r#"<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M16 7l3 3M14 9l2 2"/>"#,
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
