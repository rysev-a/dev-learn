//! Permissions (chapter 18): who may do what on which object. A user is granted permissions (`user → permission`), a permission is a role
//! on one object (`permission → object`) and applies to that object **and everything under it**:
//!
//! | object | what is under it |
//! |---|---|
//! | data center | its clusters, logical networks and storage domains, and everything under the clusters |
//! | cluster | its hosts |
//! | host | the VMs placed on it |
//! | VM, network, storage domain | nothing |
//!
//! A permission on an object never reaches up or sideways. The roles allow (inside the subtree of the object the permission is on):
//!
//! | role | view | run VM | edit VM | manage host | manage cluster | manage storage | manage network | manage data center |
//! |---|---|---|---|---|---|---|---|---|
//! | `SuperUser` | yes | yes | yes | yes | yes | yes | yes | yes |
//! | `DataCenterAdmin` | yes | yes | yes | yes | yes | yes | yes | yes |
//! | `ClusterAdmin` | yes | yes | yes | yes | yes | no | no | no |
//! | `HostAdmin` | yes | yes | yes | yes | no | no | no | no |
//! | `UserRole` | yes | yes | no | no | no | no | no | no |
//!
//! `SuperUser` is not global in the lab: like the other roles it works in the subtree of its object (put it on the data center to cover the
//! data center), and `DataCenterAdmin` differs from it by name only — an administrator of a data center cannot manage another one because the
//! other one is outside the subtree.

use serde::{Deserialize, Serialize};

use super::{Kind, PermRole, Rel, Topology};

/// What a user does with an object.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Action {
    /// Look at the object.
    View,
    /// Start and stop a VM.
    RunVm,
    /// Change the configuration of a VM.
    EditVm,
    /// Manage a host (maintenance, activation, power management).
    ManageHost,
    /// Manage a cluster.
    ManageCluster,
    /// Manage a data center.
    ManageDataCenter,
    /// Manage storage domains.
    ManageStorage,
    /// Manage logical networks.
    ManageNetwork,
}

impl Action {
    /// All actions.
    pub const ALL: [Action; 8] = [
        Action::View,
        Action::RunVm,
        Action::EditVm,
        Action::ManageHost,
        Action::ManageCluster,
        Action::ManageDataCenter,
        Action::ManageStorage,
        Action::ManageNetwork,
    ];

    /// Name for the student, as a verb phrase ("can {label} on …").
    pub fn label(self) -> &'static str {
        match self {
            Action::View => i18n::tr("view"),
            Action::RunVm => i18n::tr("run VMs"),
            Action::EditVm => i18n::tr("edit VMs"),
            Action::ManageHost => i18n::tr("manage hosts"),
            Action::ManageCluster => i18n::tr("manage clusters"),
            Action::ManageDataCenter => i18n::tr("manage data centers"),
            Action::ManageStorage => i18n::tr("manage storage"),
            Action::ManageNetwork => i18n::tr("manage networks"),
        }
    }
}

impl PermRole {
    /// The role allows the action (on the objects the permission covers).
    pub fn allows(self, a: Action) -> bool {
        match self {
            PermRole::SuperUser | PermRole::DataCenterAdmin => true,
            PermRole::ClusterAdmin => {
                matches!(a, Action::View | Action::RunVm | Action::EditVm | Action::ManageHost | Action::ManageCluster)
            }
            PermRole::HostAdmin => matches!(a, Action::View | Action::RunVm | Action::EditVm | Action::ManageHost),
            PermRole::UserRole => matches!(a, Action::View | Action::RunVm),
        }
    }
}

/// The object and the objects above it up to the data center: a VM, the host it is placed on, the cluster, the data center; a network or a
/// storage domain and its data center. Unknown identifiers give an empty list.
pub fn ancestors(t: &Topology, id: &str) -> Vec<String> {
    let mut out = vec![];
    let mut cur = t.node(id);
    while let Some(n) = cur {
        out.push(n.id.clone());
        let parent = match n.kind {
            Kind::Vm => t.sources(&n.id, Rel::Runs).next(),
            Kind::Host => t.sources(&n.id, Rel::Member).next(),
            Kind::Cluster => t.sources(&n.id, Rel::Contains).next(),
            Kind::Network => t.sources(&n.id, Rel::Defined).next(),
            Kind::StorageDomain => t.sources(&n.id, Rel::Domain).next(),
            _ => None,
        };
        cur = parent.filter(|p| !out.contains(&p.id));
    }
    out
}

/// The user may do the action on the object: one of their permissions is on the object or above it, and its role allows the action.
/// Unknown users and objects may do nothing.
pub fn user_can(t: &Topology, user: &str, action: Action, object: &str) -> bool {
    if t.node(user).is_none_or(|u| u.kind != Kind::User) {
        return false;
    }
    let above = ancestors(t, object);
    t.targets(user, Rel::Grants).any(|perm| {
        perm.perm_role().allows(action) && t.targets(&perm.id, Rel::OnObject).any(|on| above.contains(&on.id))
    })
}
