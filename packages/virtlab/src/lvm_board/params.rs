//! Parameters of the objects of the board: the table of what an object of a kind may be told ([`param_specs`]). The UI draws the inspector from
//! the table, [`param_error`] validates the values (the server rejects what the table does not allow), and
//! [`Node::param_text`](super::Node::param_text) reads a value with the default when it is unset.
//!
//! The value sets are small and fixed on purpose (a student chooses from a list, as in a form): sizes are in GiB, the extent size and the pool
//! metadata in MiB.

use super::{Kind, Node, Param};

/// One choice of a [`ParamTy::Select`] parameter.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct ParamOption {
    /// The value as it is stored (`Param::Str`).
    pub value: &'static str,
    /// The text for the student.
    pub label: &'static str,
}

/// What kind of value a parameter takes.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ParamTy {
    /// A switch (`Param::Bool`).
    Bool,
    /// One of the listed values (`Param::Str`).
    Select(Vec<ParamOption>),
}

/// A parameter an object of a kind has.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ParamSpec {
    /// Key in the data files.
    pub key: &'static str,
    /// Caption for the student.
    pub label: &'static str,
    /// Value type.
    pub ty: ParamTy,
    /// The value while the parameter is unset.
    pub default: Param,
}

impl ParamSpec {
    fn flag(key: &'static str, label: &'static str, default: bool) -> ParamSpec {
        ParamSpec { key, label, ty: ParamTy::Bool, default: Param::Bool(default) }
    }

    /// A choice whose options read as their values (numbers).
    fn numbers(key: &'static str, label: &'static str, default: &'static str, values: &[&'static str]) -> ParamSpec {
        let options = values.iter().map(|v| ParamOption { value: v, label: v }).collect();
        ParamSpec { key, label, ty: ParamTy::Select(options), default: Param::Str(default.into()) }
    }

    fn select(key: &'static str, label: &'static str, default: &'static str, options: &[(&'static str, &'static str)]) -> ParamSpec {
        let options = options.iter().map(|(value, label)| ParamOption { value, label }).collect();
        ParamSpec { key, label, ty: ParamTy::Select(options), default: Param::Str(default.into()) }
    }

    /// The value is allowed for this parameter.
    pub fn accepts(&self, v: &Param) -> bool {
        match (&self.ty, v) {
            (ParamTy::Bool, Param::Bool(_)) => true,
            (ParamTy::Select(options), Param::Str(s)) => options.iter().any(|o| o.value == s),
            _ => false,
        }
    }

    /// The default as text (`true` / `false` for a switch).
    pub fn default_text(&self) -> String {
        param_to_text(&self.default)
    }

    /// The options of a select parameter (empty for a switch).
    pub fn options(&self) -> &[ParamOption] {
        match &self.ty {
            ParamTy::Select(o) => o,
            ParamTy::Bool => &[],
        }
    }
}

/// A parameter without the texts for the student: the key, the allowed values (empty for a switch) and the default as text. This is what the
/// model reads on every evaluation, so it allocates nothing; [`param_specs`] adds the captions, and a test keeps the two in step.
pub(crate) struct Raw {
    pub(crate) key: &'static str,
    pub(crate) options: &'static [&'static str],
    pub(crate) default: &'static str,
}

const SWITCH: &[&str] = &[];
const DISK_GIB: &[&str] = &["10", "20", "50", "100", "200", "500", "1000"];
const LV_GIB: &[&str] = &["1", "2", "5", "10", "20", "50", "100", "200"];
const POOL_GIB: &[&str] = &["10", "20", "50", "100", "200"];
const THIN_GIB: &[&str] = &["10", "20", "50", "100", "200", "500", "1000"];
const SNAP_GIB: &[&str] = &["1", "2", "5", "10", "20", "50"];
const FS_GIB: &[&str] = &["1", "2", "5", "10", "20", "50", "100", "200", "500", "1000"];
const META_MIB: &[&str] = &["64", "128", "256", "512", "1024"];

pub(crate) fn raw_specs(kind: Kind) -> &'static [Raw] {
    match kind {
        Kind::Disk => &[Raw { key: "size", options: DISK_GIB, default: "100" }],
        Kind::Vg => &[Raw { key: "pe", options: &["4", "32", "128"], default: "4" }],
        Kind::Lv => &[
            Raw { key: "size", options: LV_GIB, default: "10" },
            Raw { key: "mirror", options: &["1", "2"], default: "1" },
        ],
        Kind::ThinPool => &[
            Raw { key: "size", options: POOL_GIB, default: "50" },
            Raw { key: "meta", options: META_MIB, default: "128" },
            Raw { key: "autoextend", options: SWITCH, default: "false" },
        ],
        Kind::ThinLv => &[Raw { key: "size", options: THIN_GIB, default: "50" }],
        Kind::Snapshot => &[Raw { key: "size", options: SNAP_GIB, default: "5" }],
        Kind::Fs => &[
            Raw { key: "type", options: &["ext4", "xfs"], default: "ext4" },
            Raw { key: "size", options: FS_GIB, default: "10" },
        ],
        Kind::Pv | Kind::Vm => &[],
    }
}

impl Raw {
    /// The value is allowed.
    pub(crate) fn accepts(&self, v: &Param) -> bool {
        match v {
            Param::Bool(_) => self.options.is_empty(),
            Param::Str(s) => self.options.contains(&s.as_str()),
        }
    }
}

/// A parameter value as text.
pub fn param_to_text(p: &Param) -> String {
    match p {
        Param::Bool(b) => b.to_string(),
        Param::Str(s) => s.clone(),
    }
}

/// The parameters an object of the kind has, in the order the inspector shows them.
pub fn param_specs(kind: Kind) -> Vec<ParamSpec> {
    match kind {
        Kind::Disk => vec![ParamSpec::numbers("size", i18n::tr("Size, GiB"), "100", DISK_GIB)],
        Kind::Vg => vec![ParamSpec::numbers("pe", i18n::tr("Extent size, MiB"), "4", &["4", "32", "128"])],
        Kind::Lv => vec![
            ParamSpec::numbers("size", i18n::tr("Size, GiB"), "10", LV_GIB),
            ParamSpec::select(
                "mirror",
                i18n::tr("Copies"),
                "1",
                &[("1", i18n::tr("1: one copy")), ("2", i18n::tr("2: a mirror, each copy on its own physical volume"))],
            ),
        ],
        Kind::ThinPool => vec![
            ParamSpec::numbers("size", i18n::tr("Data size, GiB"), "50", POOL_GIB),
            ParamSpec::numbers("meta", i18n::tr("Metadata size, MiB"), "128", META_MIB),
            ParamSpec::flag("autoextend", i18n::tr("Autoextend: grow by 20% when 80% is used"), false),
        ],
        Kind::ThinLv => vec![ParamSpec::numbers("size", i18n::tr("Virtual size, GiB"), "50", THIN_GIB)],
        Kind::Snapshot => vec![ParamSpec::numbers("size", i18n::tr("Snapshot size, GiB"), "5", SNAP_GIB)],
        Kind::Fs => vec![
            ParamSpec::select("type", i18n::tr("Type"), "ext4", &[("ext4", "ext4"), ("xfs", "XFS")]),
            ParamSpec::numbers("size", i18n::tr("Filesystem size, GiB"), "10", FS_GIB),
        ],
        Kind::Pv | Kind::Vm => vec![],
    }
}

/// Why a parameter of the object is not allowed (`None`: all fine): an unknown key, or a value the parameter does not take.
pub fn param_error(n: &Node) -> Option<String> {
    let specs = raw_specs(n.kind);
    for (key, value) in &n.params {
        match specs.iter().find(|s| s.key == key) {
            None => return Some(i18n::trf!("“{0}” is not a parameter of a {1}", key, n.kind.label())),
            Some(s) if !s.accepts(value) => {
                return Some(i18n::trf!("“{0}” is not a valid value of the parameter “{1}”", param_to_text(value), key));
            }
            Some(_) => {}
        }
    }
    None
}
