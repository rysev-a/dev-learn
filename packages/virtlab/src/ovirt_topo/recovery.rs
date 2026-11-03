//! What the environment does when something goes away (chapters 19, 22, 24): HA restarts after the loss of a host, evacuation of a host,
//! backups after the loss of a domain, replicas after the loss of a data center. The functions answer one yes/no question each; the goals
//! ([`TopoGoal`](super::TopoGoal)) call them.

use super::{evaluate, fence_agent, fence_proxy, Edge, Kind, Node, Param, Rel, Topology, VmStatus};

/// The first other host of the cluster (link order) where the VM would run if it were put there. `t` is the board in which the VM has no
/// host; `exclude` is the host the VM comes from.
pub fn restart_target(t: &Topology, vm: &str, cluster: &str, exclude: &str) -> Option<String> {
    t.targets(cluster, Rel::Member).filter(|h| h.id != exclude).find_map(|h| {
        let mut next = t.clone();
        next.edges.push(Edge::new(&h.id, vm));
        let runs = evaluate(&next).vm(vm).is_some_and(|v| v.status == VmStatus::Running);
        runs.then(|| h.id.clone())
    })
}

/// VMs placed on a host, in link order.
fn vms_on(t: &Topology, host: &str) -> Vec<String> {
    t.targets(host, Rel::Runs).map(|v| v.id.clone()).collect()
}

/// Every host that runs an HA VM has a fence agent and a fence proxy, and after its loss each HA VM of it restarts on another host of the
/// cluster (one after the other, so they share the memory). There must be at least one placed HA VM. The non-HA VMs of the lost host stay down.
pub fn ha_restart_ok(t: &Topology) -> bool {
    let hosts: Vec<&Node> = t.of_kind(Kind::Host).filter(|h| t.targets(&h.id, Rel::Runs).any(Node::ha)).collect();
    !hosts.is_empty()
        && hosts.iter().all(|host| {
            if fence_agent(t, &host.id).is_none() {
                return false;
            }
            let mut after = t.without(&host.id);
            if fence_proxy(t, &evaluate(&after), &host.id).is_none() {
                return false;
            }
            let Some(cluster) = t.cluster_of_host(&host.id) else { return false };
            t.targets(&host.id, Rel::Runs).filter(|v| v.ha()).all(|vm| match restart_target(&after, &vm.id, &cluster.id, &host.id) {
                Some(target) => {
                    after.edges.push(Edge::new(&target, &vm.id));
                    true
                }
                None => false,
            })
        })
}

/// Every host that runs VMs can be put into maintenance: each of its VMs moves (one after the other) to another host of the cluster where
/// it would run. There must be at least one host that runs VMs.
pub fn evacuation_possible(t: &Topology) -> bool {
    let hosts: Vec<&Node> = t.of_kind(Kind::Host).filter(|h| t.targets(&h.id, Rel::Runs).next().is_some()).collect();
    !hosts.is_empty()
        && hosts.iter().all(|host| {
            let Some(cluster) = t.cluster_of_host(&host.id) else { return false };
            let mut cur = t.clone();
            if let Some(h) = cur.nodes.iter_mut().find(|n| n.id == host.id) {
                h.params.insert("maintenance".into(), Param::Bool(true));
            }
            cur.edges.retain(|e| !(e.from == host.id && vms_on(t, &host.id).contains(&e.to)));
            vms_on(t, &host.id).iter().all(|vm| match restart_target(&cur, vm, &cluster.id, &host.id) {
                Some(target) => {
                    cur.edges.push(Edge::new(&target, vm));
                    true
                }
                None => false,
            })
        })
}

/// After the loss of any storage domain that holds a VM disk, each VM that had a disk on it has an incremental or full backup (a snapshot
/// lives on the lost domain). There must be at least one such domain.
pub fn restorable_after_domain_loss(t: &Topology) -> bool {
    let domains: Vec<&Node> = t.of_kind(Kind::StorageDomain).filter(|d| t.targets(&d.id, Rel::Disk).next().is_some()).collect();
    !domains.is_empty()
        && domains.iter().all(|d| {
            t.targets(&d.id, Rel::Disk).all(|vm| t.targets(&vm.id, Rel::BackupOf).any(|b| b.backup_type().off_site()))
        })
}

/// After the loss of any data center that hosts VMs (with everything under it), every VM that was on it is recoverable: each of its disks
/// is on a domain that is gone and has a replica on an Active domain of another data center that is Up (or is on a domain that survives). A VM
/// without a disk is not recoverable. There must be at least two data centers and one data center that hosts VMs.
pub fn survives_site_loss(t: &Topology) -> bool {
    if t.of_kind(Kind::DataCenter).count() < 2 {
        return false;
    }
    let sites: Vec<&Node> = t
        .of_kind(Kind::DataCenter)
        .filter(|dc| t.hosts_of_dc(&dc.id).any(|h| t.targets(&h.id, Rel::Runs).next().is_some()))
        .collect();
    !sites.is_empty()
        && sites.iter().all(|dc| {
            let after = t.without_dc(&dc.id);
            let ev = evaluate(&after);
            t.hosts_of_dc(&dc.id).flat_map(|h| t.targets(&h.id, Rel::Runs)).all(|vm| {
                let disks: Vec<&Node> = t.sources(&vm.id, Rel::Disk).collect();
                !disks.is_empty()
                    && disks.iter().all(|d| {
                        after.node(&d.id).is_some()
                            || t.targets(&d.id, Rel::Replica).any(|r| {
                                ev.domain(&r.id).is_some_and(|e| e.status == super::DomainStatus::Active)
                                    && t.sources(&r.id, Rel::Domain).next().is_some_and(|other| {
                                        ev.dc(&other.id).is_some_and(|e| e.status == super::DcStatus::Up)
                                    })
                            })
                    })
            })
        })
}
