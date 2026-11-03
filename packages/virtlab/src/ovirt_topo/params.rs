//! Parameters of the objects of the board: the table of what an object of a kind may be told ([`param_specs`]) and the typed values some of them
//! have. The UI draws the inspector from the table, [`param_error`] validates the values (the server rejects what the table does not allow),
//! and [`Node::param_text`](super::Node::param_text) reads a value with the default when it is unset.

use super::{Kind, Node, Param, Role};

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

/// A parameter without the texts for the student: the key, the allowed values (empty for a switch) and the default as text. This is what
/// the model reads on every evaluation, so it allocates nothing; [`param_specs`] adds the captions, and a test keeps the two in step.
pub(crate) struct Raw {
    pub(crate) key: &'static str,
    pub(crate) options: &'static [&'static str],
    pub(crate) default: &'static str,
}

const SWITCH: &[&str] = &[];

pub(crate) fn raw_specs(kind: Kind) -> &'static [Raw] {
    match kind {
        Kind::Network => &[
            Raw { key: "role", options: &["vm", "management", "migration", "storage", "display"], default: "vm" },
            Raw { key: "required", options: SWITCH, default: "true" },
        ],
        Kind::StorageDomain => &[Raw { key: "type", options: &["nfs", "iscsi"], default: "nfs" }],
        Kind::Host => &[
            Raw { key: "mem", options: &["16", "32", "64"], default: "32" },
            Raw { key: "maintenance", options: SWITCH, default: "false" },
        ],
        Kind::Vm => &[
            Raw { key: "ha", options: SWITCH, default: "false" },
            Raw { key: "mem", options: &["2", "4", "8", "16"], default: "4" },
        ],
        Kind::AffinityGroup => &[
            Raw { key: "polarity", options: &["positive", "negative"], default: "negative" },
            Raw { key: "hard", options: SWITCH, default: "true" },
        ],
        Kind::Backup => &[Raw { key: "type", options: &["snapshot", "incremental", "full"], default: "snapshot" }],
        Kind::Permission => &[Raw {
            key: "role",
            options: &["SuperUser", "DataCenterAdmin", "ClusterAdmin", "HostAdmin", "UserRole"],
            default: "UserRole",
        }],
        Kind::Engine | Kind::DataCenter | Kind::Cluster | Kind::FenceAgent | Kind::User => &[],
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
        Kind::Network => vec![
            ParamSpec::select(
                "role",
                i18n::tr("Role"),
                Role::Vm.as_str(),
                &Role::ALL.map(|r| (r.as_str(), r.label())),
            ),
            ParamSpec::flag("required", i18n::tr("Required: every host of the cluster must have it"), true),
        ],
        Kind::StorageDomain => vec![ParamSpec::select(
            "type",
            i18n::tr("Type"),
            "nfs",
            &[("nfs", "NFS"), ("iscsi", "iSCSI")],
        )],
        Kind::Host => vec![
            ParamSpec::select("mem", i18n::tr("Memory"), "32", &[("16", i18n::tr("16 GB")), ("32", i18n::tr("32 GB")), ("64", i18n::tr("64 GB"))]),
            ParamSpec::flag("maintenance", i18n::tr("Maintenance mode: the host runs no VMs"), false),
        ],
        Kind::Vm => vec![
            ParamSpec::flag("ha", i18n::tr("Highly available: restarted on another host when its host fails"), false),
            ParamSpec::select(
                "mem",
                i18n::tr("Memory"),
                "4",
                &[("2", i18n::tr("2 GB")), ("4", i18n::tr("4 GB")), ("8", i18n::tr("8 GB")), ("16", i18n::tr("16 GB"))],
            ),
        ],
        Kind::AffinityGroup => vec![
            ParamSpec::select(
                "polarity",
                i18n::tr("Polarity"),
                "negative",
                &[
                    ("positive", i18n::tr("positive: the VMs run on one host")),
                    ("negative", i18n::tr("negative: the VMs run on different hosts")),
                ],
            ),
            ParamSpec::flag("hard", i18n::tr("Hard: a VM that breaks the rule cannot run"), true),
        ],
        Kind::Backup => vec![ParamSpec::select(
            "type",
            i18n::tr("Type"),
            "snapshot",
            &[("snapshot", i18n::tr("snapshot")), ("incremental", i18n::tr("incremental")), ("full", i18n::tr("full"))],
        )],
        Kind::Permission => vec![ParamSpec::select(
            "role",
            i18n::tr("Role"),
            "UserRole",
            &PermRole::ALL.map(|r| (r.as_str(), r.as_str())),
        )],
        Kind::Engine | Kind::DataCenter | Kind::Cluster | Kind::FenceAgent | Kind::User => vec![],
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

/// Type of a backup.
#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum BackupType {
    /// A snapshot: it lives on the disk domain of the VM, so it is lost with it.
    Snapshot,
    /// An incremental backup stored off the data center.
    Incremental,
    /// A full backup stored off the data center.
    Full,
}

impl BackupType {
    /// All types.
    pub const ALL: [BackupType; 3] = [BackupType::Snapshot, BackupType::Incremental, BackupType::Full];

    /// Name in data files.
    pub fn as_str(self) -> &'static str {
        match self {
            BackupType::Snapshot => "snapshot",
            BackupType::Incremental => "incremental",
            BackupType::Full => "full",
        }
    }

    /// Parse the name from a data file.
    pub fn parse(s: &str) -> Option<BackupType> {
        BackupType::ALL.into_iter().find(|t| t.as_str() == s)
    }

    /// Name for the student.
    pub fn label(self) -> &'static str {
        match self {
            BackupType::Snapshot => i18n::tr("snapshot"),
            BackupType::Incremental => i18n::tr("incremental"),
            BackupType::Full => i18n::tr("full"),
        }
    }

    /// The backup is stored off the data center, so it survives the loss of a storage domain or of the whole site.
    pub fn off_site(self) -> bool {
        self != BackupType::Snapshot
    }
}

/// Role of a permission (the names are oVirt's, they are not translated).
#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum PermRole {
    /// Everything, on the object and everything under it.
    SuperUser,
    /// Everything inside a data center.
    DataCenterAdmin,
    /// Hosts, VMs and the cluster itself.
    ClusterAdmin,
    /// A host and its VMs.
    HostAdmin,
    /// Look and run.
    UserRole,
}

impl PermRole {
    /// All roles.
    pub const ALL: [PermRole; 5] =
        [PermRole::SuperUser, PermRole::DataCenterAdmin, PermRole::ClusterAdmin, PermRole::HostAdmin, PermRole::UserRole];

    /// Name in data files (the same as the oVirt name).
    pub fn as_str(self) -> &'static str {
        match self {
            PermRole::SuperUser => "SuperUser",
            PermRole::DataCenterAdmin => "DataCenterAdmin",
            PermRole::ClusterAdmin => "ClusterAdmin",
            PermRole::HostAdmin => "HostAdmin",
            PermRole::UserRole => "UserRole",
        }
    }

    /// Parse the name from a data file.
    pub fn parse(s: &str) -> Option<PermRole> {
        PermRole::ALL.into_iter().find(|r| r.as_str() == s)
    }
}

/// Polarity of an affinity group.
#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Polarity {
    /// The members run on one host.
    Positive,
    /// The members run on different hosts.
    Negative,
}

impl Polarity {
    /// Name in data files.
    pub fn as_str(self) -> &'static str {
        match self {
            Polarity::Positive => "positive",
            Polarity::Negative => "negative",
        }
    }
}
