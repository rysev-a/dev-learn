//! Parameters of the objects of the board: the table of what an object of a kind may be told ([`param_specs`]). The UI draws the inspector from
//! the table, [`param_error`] validates the values (the server rejects what the table does not allow), and
//! [`Node::param_text`](super::Node::param_text) reads a value with the default when it is unset.
//!
//! The value sets are small and fixed on purpose: three networks `a`, `b`, `c` ([`net_label`]), the VLAN tags 10, 20, 30 (0: untagged).

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
const NETS: &[&str] = &["none", "a", "b", "c"];
const NETS_OUT: &[&str] = &["a", "b", "c"];
const TAGS: &[&str] = &["0", "10", "20", "30"];
const IDS: &[&str] = &["10", "20", "30"];
const MODES: &[&str] = &["active-backup", "802.3ad"];
const NAT_KINDS: &[&str] = &["masquerade", "dnat"];

pub(crate) fn raw_specs(kind: Kind) -> &'static [Raw] {
    match kind {
        Kind::Netns => &[Raw { key: "forward", options: SWITCH, default: "false" }],
        Kind::Eth | Kind::Veth | Kind::Bridge | Kind::Vm => &[
            Raw { key: "net", options: NETS, default: "none" },
            Raw { key: "up", options: SWITCH, default: "true" },
            Raw { key: "access_vlan", options: TAGS, default: "0" },
            Raw { key: "default_route", options: SWITCH, default: "false" },
        ],
        Kind::Bond => &[
            Raw { key: "mode", options: MODES, default: "active-backup" },
            Raw { key: "net", options: NETS, default: "none" },
            Raw { key: "up", options: SWITCH, default: "true" },
            Raw { key: "access_vlan", options: TAGS, default: "0" },
            Raw { key: "default_route", options: SWITCH, default: "false" },
        ],
        Kind::Vlan => &[
            Raw { key: "id", options: IDS, default: "10" },
            Raw { key: "net", options: NETS, default: "none" },
            Raw { key: "up", options: SWITCH, default: "true" },
            Raw { key: "access_vlan", options: TAGS, default: "0" },
            Raw { key: "default_route", options: SWITCH, default: "false" },
        ],
        Kind::External => &[
            Raw { key: "net", options: NETS_OUT, default: "a" },
            Raw { key: "tagged", options: TAGS, default: "0" },
        ],
        Kind::Nat => &[Raw { key: "kind", options: NAT_KINDS, default: "masquerade" }],
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

/// The network of a `net` value for the student: `none`, or the subnet.
pub fn net_label(value: &str) -> &'static str {
    match value {
        "a" => "10.0.1.0/24",
        "b" => "10.0.2.0/24",
        "c" => "10.0.3.0/24",
        _ => i18n::tr("no address"),
    }
}

fn net_spec(with_none: bool) -> ParamSpec {
    if with_none {
        ParamSpec::select(
            "net",
            i18n::tr("Address"),
            "none",
            &[("none", i18n::tr("no address")), ("a", "10.0.1.0/24"), ("b", "10.0.2.0/24"), ("c", "10.0.3.0/24")],
        )
    } else {
        ParamSpec::select("net", i18n::tr("Network"), "a", &[("a", "10.0.1.0/24"), ("b", "10.0.2.0/24"), ("c", "10.0.3.0/24")])
    }
}

fn tag_spec(key: &'static str, label: &'static str) -> ParamSpec {
    ParamSpec::select(
        key,
        label,
        "0",
        &[("0", i18n::tr("0: untagged")), ("10", "10"), ("20", "20"), ("30", "30")],
    )
}

fn iface_specs(first: Vec<ParamSpec>) -> Vec<ParamSpec> {
    let mut v = first;
    v.push(net_spec(true));
    v.push(ParamSpec::flag("up", i18n::tr("Up"), true));
    v.push(tag_spec("access_vlan", i18n::tr("VLAN tag of the port in a bridge")));
    v.push(ParamSpec::flag("default_route", i18n::tr("Default route goes out here"), false));
    v
}

/// The parameters an object of the kind has, in the order the inspector shows them.
pub fn param_specs(kind: Kind) -> Vec<ParamSpec> {
    match kind {
        Kind::Netns => vec![ParamSpec::flag("forward", i18n::tr("Forwarding between interfaces (ip_forward)"), false)],
        Kind::Eth | Kind::Veth | Kind::Bridge | Kind::Vm => iface_specs(vec![]),
        Kind::Bond => iface_specs(vec![ParamSpec::select(
            "mode",
            i18n::tr("Mode"),
            "active-backup",
            &[("active-backup", "active-backup"), ("802.3ad", i18n::tr("802.3ad (LACP): all slaves on one switch"))],
        )]),
        Kind::Vlan => iface_specs(vec![ParamSpec::select("id", i18n::tr("VLAN id"), "10", &[("10", "10"), ("20", "20"), ("30", "30")])]),
        Kind::External => vec![net_spec(false), tag_spec("tagged", i18n::tr("VLAN the outside network speaks"))],
        Kind::Nat => vec![ParamSpec::select(
            "kind",
            i18n::tr("Rule"),
            "masquerade",
            &[("masquerade", i18n::tr("masquerade: outgoing traffic gets the address of the router")), ("dnat", i18n::tr("DNAT: a published port goes to a host inside"))],
        )],
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
