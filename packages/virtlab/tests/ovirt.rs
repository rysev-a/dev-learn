//! oVirt simulators (chapters 17, 19, 22): goals are reachable, the starting settings do not reach them, every setting matters,
//! and the server re-check accepts what the model accepts.

use serde_json::{json, Value};
use virtlab::ovirt_dc::{self, Action as A, Net, Refusal};
use virtlab::ovirt_fence::{self, FenceConfig, Outcome};
use virtlab::ovirt_sched::{self, Mistake, Policy};
use virtlab::{GoalStatus, Spec};

fn en() {
    locales::set_locale(i18n::Locale::En);
}

// ---------------------------------------------------------------- fencing

fn fence_scenario(id: &str) -> ovirt_fence::Scenario {
    en();
    ovirt_fence::default_scenarios().into_iter().find(|s| s.id == id).expect("scenario")
}

fn solution() -> FenceConfig {
    FenceConfig { soft: true, power: true, skip_lease: true, skip_connectivity: true, threshold: 50, vm_leases: true }
}

#[test]
fn fence_one_setting_set_reaches_every_scenario() {
    en();
    for sc in ovirt_fence::default_scenarios() {
        assert!(sc.reached(&solution()), "{}", sc.id);
        assert!(!sc.reached(&FenceConfig::default()), "{}: the starting settings must not reach the goal", sc.id);
    }
}

#[test]
fn fence_every_setting_is_needed_by_some_scenario() {
    en();
    let ok = solution();
    let breakers: [(&str, FenceConfig); 5] = [
        ("hung", FenceConfig { soft: false, ..ok }),
        ("dead", FenceConfig { power: false, ..ok }),
        ("mgmt", FenceConfig { skip_lease: false, ..ok }),
        ("switch", FenceConfig { skip_connectivity: false, ..ok }),
        ("bmc", FenceConfig { vm_leases: false, ..ok }),
    ];
    for (id, cfg) in breakers {
        assert!(!fence_scenario(id).reached(&cfg), "{id}");
    }
}

#[test]
fn fence_threshold_window() {
    en();
    // one host of four is 25%, three of four is 75%: the policy must skip at 75% and must not skip at 25%
    let at = |t: u32| FenceConfig { threshold: t, ..solution() };
    for t in [26, 50, 75] {
        assert!(fence_scenario("dead").reached(&at(t)) && fence_scenario("switch").reached(&at(t)), "{t}");
    }
    assert!(!fence_scenario("dead").reached(&at(25)), "25% skips the single dead host");
    assert!(!fence_scenario("dead").reached(&at(10)));
    assert!(!fence_scenario("switch").reached(&at(76)), "76% does not skip a 75% outage");
    assert!(!fence_scenario("switch").reached(&at(100)));
}

#[test]
fn fence_details() {
    en();
    // a live host rebooted through power management loses its VMs
    let s = ovirt_fence::simulate(
        &FenceConfig { power: true, ..FenceConfig::default() },
        &fence_scenario("mgmt").situation,
    );
    assert_eq!(s.outcome, Outcome::Fenced);
    assert!(s.vms_killed && s.ha_restarted);
    // a broken controller: fencing failed, HA only through the lease
    let sit = fence_scenario("bmc").situation;
    let s = ovirt_fence::simulate(&FenceConfig { power: true, ..FenceConfig::default() }, &sit);
    assert_eq!((s.outcome, s.ha_restarted), (Outcome::FenceFailed, false));
    let s = ovirt_fence::simulate(&FenceConfig { power: true, vm_leases: true, ..FenceConfig::default() }, &sit);
    assert_eq!((s.outcome, s.ha_restarted), (Outcome::FenceFailed, true));
    // without power management the administrator confirms the reboot
    let s = ovirt_fence::simulate(&FenceConfig::default(), &sit);
    assert_eq!(s.outcome, Outcome::Manual);
    // every step has a text
    for st in &s.steps {
        assert!(!ovirt_fence::step_text(st).is_empty());
    }
}

// ---------------------------------------------------------------- scheduler

fn sched_scenario(id: &str) -> ovirt_sched::Scenario {
    en();
    ovirt_sched::default_scenarios().into_iter().find(|s| s.id == id).expect("scenario")
}

#[test]
fn sched_starting_policy_reaches_no_goal() {
    en();
    for sc in ovirt_sched::default_scenarios() {
        assert!(!sc.reached(&Policy::default()), "{}", sc.id);
    }
}

#[test]
fn sched_each_scenario_has_a_solution() {
    en();
    let even = Policy { even: 1, ..Policy::default() };
    assert!(sched_scenario("even").reached(&even));
    assert!(sched_scenario("even").reached(&Policy { free_mem: 1, ..Policy::default() }));
    assert!(sched_scenario("nets").reached(&Policy { network: true, ..even }));
    assert!(sched_scenario("anti").reached(&Policy { affinity: true, ..even }));
    assert!(sched_scenario("pack").reached(&Policy { memory: true, ..Policy::default() }));
    assert!(sched_scenario("pack").reached(&Policy { memory: true, pack: 1, ..Policy::default() }));
}

#[test]
fn sched_every_filter_and_weight_matters() {
    en();
    let even = Policy { even: 1, ..Policy::default() };
    // the network filter: without it the VM goes to a host without its VLAN
    let p = sched_scenario("nets").run(&even);
    assert!(p.placements.iter().any(|p| p.mistakes == [Mistake::Network]));
    // spreading is required in the network scenario: the filter alone does not reach the goal
    assert!(!sched_scenario("nets").reached(&Policy { network: true, ..Policy::default() }));
    // the affinity filter: the emptiest host takes both replicas
    let p = sched_scenario("anti").run(&even);
    assert!(p.placements.iter().any(|p| p.mistakes == [Mistake::Affinity]));
    // power saving: without the memory filter the first host is overfilled, an even load uses all hosts
    let p = sched_scenario("pack").run(&Policy::default());
    assert!(p.placements.iter().any(|p| p.mistakes == [Mistake::Memory]));
    assert!(!sched_scenario("pack").reached(&Policy { memory: true, even: 1, ..Policy::default() }));
}

#[test]
fn sched_rank_sum_and_ties() {
    en();
    let sc = sched_scenario("anti");
    // a heavier weight of the second module overrides the first
    let a = Policy { affinity: true, even: 1, free_mem: 0, ..Policy::default() };
    let p = sc.run(&a);
    assert_eq!(p.placements[0].host.as_deref(), Some("host1"));
    assert_eq!(p.placements[1].host.as_deref(), Some("host2"), "the tie goes to the first name");
    assert_eq!(p.unplaced(), 0);
    // a VM that fits nowhere is unplaced and is not a mistake of a host
    let mut sc = sched_scenario("pack");
    sc.vms[0].mem = 64;
    let p = sc.run(&Policy { memory: true, ..Policy::default() });
    assert_eq!(p.unplaced(), 1);
    assert!(!sc.reached(&Policy { memory: true, ..Policy::default() }));
}

// ---------------------------------------------------------------- data center

const FULL: [A; 10] = [
    A::AddCluster,
    A::AddHost { host: 1 },
    A::AddHost { host: 2 },
    A::CreateNetwork,
    A::AssignNetwork { host: 1 },
    A::AssignNetwork { host: 2 },
    A::CreateDomain,
    A::AttachDomain,
    A::ActivateDomain,
    A::CreateVm { net: Net::VmNet },
];

fn session() -> ovirt_dc::Session {
    en();
    ovirt_dc::Session::new(&ovirt_dc::default_goals())
}

#[test]
fn dc_full_walkthrough_reaches_all_goals() {
    let mut s = session();
    for a in FULL {
        s.act(a).unwrap_or_else(|e| panic!("{a:?}: {e:?}"));
    }
    assert_eq!(s.state().dc_status(), ovirt_dc::DcStatus::Up);
    assert_eq!(s.done(), ["dc_up"]);
    s.act(A::RunVm).unwrap();
    assert_eq!(s.done(), ["dc_up", "vm_net"]);
    s.act(A::Maintenance { host: 1 }).unwrap();
    assert!(s.solved());
    assert_eq!(s.state().vm.and_then(|v| v.host), Some(2));
}

#[test]
fn dc_refusals_keep_state() {
    let mut s = session();
    let r = |s: &mut ovirt_dc::Session, a| s.act(a).unwrap_err();
    assert_eq!(r(&mut s, A::AddHost { host: 1 }), Refusal::NoCluster);
    assert_eq!(r(&mut s, A::CreateNetwork), Refusal::NoCluster);
    assert_eq!(r(&mut s, A::CreateDomain), Refusal::NoUpHost);
    assert_eq!(r(&mut s, A::AddHost { host: 3 }), Refusal::BadHost);
    s.act(A::AddCluster).unwrap();
    assert_eq!(r(&mut s, A::AddCluster), Refusal::ClusterExists);
    assert_eq!(r(&mut s, A::CreateDomain), Refusal::NoUpHost, "a host must be added first");
    s.act(A::AddHost { host: 1 }).unwrap();
    assert_eq!(r(&mut s, A::ActivateDomain), Refusal::DomainState);
    assert_eq!(r(&mut s, A::AttachDomain), Refusal::DomainState);
    s.act(A::CreateDomain).unwrap();
    assert_eq!(r(&mut s, A::ActivateDomain), Refusal::DomainState, "attach first");
    assert_eq!(r(&mut s, A::CreateVm { net: Net::Mgmt }), Refusal::NoActiveDomain);
    assert_eq!(r(&mut s, A::RunVm), Refusal::NoVm);
    assert_eq!(r(&mut s, A::AssignNetwork { host: 1 }), Refusal::NoNetwork);
    assert_eq!(r(&mut s, A::Maintenance { host: 2 }), Refusal::NoHost);
    s.act(A::AttachDomain).unwrap();
    s.act(A::ActivateDomain).unwrap();
    assert_eq!(r(&mut s, A::CreateVm { net: Net::VmNet }), Refusal::NoNetwork);
    s.act(A::CreateVm { net: Net::Mgmt }).unwrap();
    s.act(A::RunVm).unwrap();
    assert_eq!(r(&mut s, A::RunVm), Refusal::AlreadyRunning);
    assert_eq!(r(&mut s, A::ActivateHost { host: 1 }), Refusal::NotInMaintenance);
    for refusal in [Refusal::NoCluster, Refusal::DcNotUp, Refusal::NoSuitableHost, Refusal::Preparing] {
        assert!(!ovirt_dc::refusal_text(refusal).is_empty());
    }
}

#[test]
fn dc_required_network_breaks_hosts_until_assigned() {
    let mut s = session();
    s.act(A::AddCluster).unwrap();
    s.act(A::AddHost { host: 1 }).unwrap();
    s.act(A::AddHost { host: 2 }).unwrap();
    assert_eq!(s.act(A::CreateNetwork).unwrap(), ovirt_dc::Note::NetworkCreated(2));
    assert!(s.state().hosts.iter().flatten().all(|h| h.status == ovirt_dc::HostStatus::NonOperational));
    // with no Up host a domain cannot be created
    assert_eq!(s.act(A::CreateDomain).unwrap_err(), Refusal::NoUpHost);
    s.act(A::AssignNetwork { host: 2 }).unwrap();
    s.act(A::CreateDomain).unwrap();
    // a host added after the network is NonOperational right away
    let mut s = session();
    s.act(A::AddCluster).unwrap();
    s.act(A::CreateNetwork).unwrap();
    assert_eq!(s.act(A::AddHost { host: 1 }).unwrap(), ovirt_dc::Note::HostAdded(ovirt_dc::HostStatus::NonOperational));
}

#[test]
fn dc_preparing_maintenance_finishes_when_a_target_appears() {
    let mut s = session();
    for a in &FULL[..5] {
        s.act(*a).unwrap(); // host 2 has no vm-net
    }
    for a in [A::CreateDomain, A::AttachDomain, A::ActivateDomain, A::CreateVm { net: Net::VmNet }, A::RunVm] {
        s.act(a).unwrap();
    }
    assert_eq!(s.state().vm.and_then(|v| v.host), Some(1));
    // host 2 is NonOperational, so the VM has nowhere to go
    assert_eq!(s.act(A::Maintenance { host: 1 }).unwrap(), ovirt_dc::Note::HostPreparing);
    assert_eq!(s.act(A::Maintenance { host: 1 }).unwrap_err(), Refusal::Preparing);
    assert_eq!(s.act(A::ActivateHost { host: 1 }).unwrap_err(), Refusal::Preparing);
    assert!(!s.done().contains(&"migrate".to_string()));
    // assigning the network to host 2 makes the migration possible: the maintenance finishes by itself
    s.act(A::AssignNetwork { host: 2 }).unwrap();
    assert_eq!(s.state().hosts[0].map(|h| h.status), Some(ovirt_dc::HostStatus::Maintenance));
    assert_eq!(s.state().vm.and_then(|v| v.host), Some(2));
    assert!(s.solved());
}

#[test]
fn dc_maintenance_without_vm_does_not_reach_migration_goal() {
    let mut s = session();
    for a in FULL {
        s.act(a).unwrap();
    }
    s.act(A::RunVm).unwrap(); // host 1
    s.act(A::Maintenance { host: 2 }).unwrap();
    assert!(!s.done().contains(&"migrate".to_string()), "the empty host went to maintenance, nothing migrated");
    s.act(A::ActivateHost { host: 2 }).unwrap();
    s.act(A::Maintenance { host: 1 }).unwrap();
    assert!(s.done().contains(&"migrate".to_string()));
}

#[test]
fn dc_status_rules() {
    let mut s = session();
    for a in &FULL[..9] {
        s.act(*a).unwrap();
    }
    assert_eq!(s.state().dc_status(), ovirt_dc::DcStatus::Up);
    s.act(A::Maintenance { host: 1 }).unwrap();
    s.act(A::Maintenance { host: 2 }).unwrap();
    assert_eq!(s.state().dc_status(), ovirt_dc::DcStatus::NonResponsive);
    s.act(A::ActivateHost { host: 1 }).unwrap();
    assert_eq!(s.state().dc_status(), ovirt_dc::DcStatus::Up);
}

// ---------------------------------------------------------------- server re-check

fn spec(id: &str) -> Spec {
    en();
    virtlab::builtin(id).expect("builtin")
}

fn verdict(spec: &Spec, goal: &str, data: Value) -> GoalStatus {
    let mut m = serde_json::Map::new();
    m.insert(goal.to_string(), data);
    virtlab::verify(spec, &Value::Object(m)).goals.into_iter().find(|g| g.id == goal).expect("goal").status
}

#[test]
fn verify_fence_recomputes_from_settings() {
    let spec = spec("virt-sim-ovirt-fence");
    let ok = serde_json::to_value(solution()).unwrap();
    for sc in ["hung", "dead", "mgmt", "switch", "bmc"] {
        assert_eq!(verdict(&spec, sc, ok.clone()), GoalStatus::Verified, "{sc}");
    }
    let mut bad = ok.clone();
    bad["soft"] = json!(false);
    assert!(matches!(verdict(&spec, "hung", bad), GoalStatus::Rejected { .. }));
    let mut bad = ok.clone();
    bad["threshold"] = json!(0);
    assert!(matches!(verdict(&spec, "dead", bad), GoalStatus::Rejected { .. }));
    assert!(matches!(verdict(&spec, "dead", json!({"soft": true})), GoalStatus::Rejected { .. }), "missing fields");
    // the full solution is accepted in strict mode too
    let mut all = serde_json::Map::new();
    for sc in ["hung", "dead", "mgmt", "switch", "bmc"] {
        all.insert(sc.into(), ok.clone());
    }
    assert!(virtlab::verify_with(&spec, &Value::Object(all), virtlab::Strictness::Strict).solved);
}

#[test]
fn verify_sched_recomputes_from_policy() {
    let spec = spec("virt-sim-ovirt-sched");
    let p = |v: Value| v;
    assert_eq!(
        verdict(
            &spec,
            "even",
            p(json!({"memory": false, "network": false, "affinity": false, "even": 1, "free_mem": 0, "pack": 0}))
        ),
        GoalStatus::Verified
    );
    assert_eq!(
        verdict(
            &spec,
            "pack",
            p(json!({"memory": true, "network": false, "affinity": false, "even": 0, "free_mem": 0, "pack": 2}))
        ),
        GoalStatus::Verified
    );
    assert!(matches!(
        verdict(
            &spec,
            "pack",
            p(json!({"memory": false, "network": false, "affinity": false, "even": 0, "free_mem": 0, "pack": 2}))
        ),
        GoalStatus::Rejected { .. }
    ));
    assert!(matches!(
        verdict(
            &spec,
            "even",
            p(json!({"memory": false, "network": false, "affinity": false, "even": 11, "free_mem": 0, "pack": 0}))
        ),
        GoalStatus::Rejected { .. }
    ));
}

#[test]
fn verify_dc_replays_the_trace() {
    let spec = spec("virt-sim-ovirt-dc");
    let mut trace: Vec<A> = FULL.to_vec();
    trace.push(A::RunVm);
    assert_eq!(verdict(&spec, "dc_up", json!({"trace": trace})), GoalStatus::Verified);
    assert_eq!(verdict(&spec, "vm_net", json!({"trace": trace})), GoalStatus::Verified);
    assert!(matches!(verdict(&spec, "migrate", json!({"trace": trace})), GoalStatus::Rejected { .. }));
    trace.push(A::Maintenance { host: 1 });
    assert_eq!(verdict(&spec, "migrate", json!({"trace": trace})), GoalStatus::Verified);
    // a refused action in the trace is skipped, as in the interface
    let mut with_refused = vec![A::RunVm];
    with_refused.extend(trace.clone());
    assert_eq!(verdict(&spec, "migrate", json!({"trace": with_refused})), GoalStatus::Verified);
    // a forged trace that does not reach the goal
    assert!(matches!(verdict(&spec, "dc_up", json!({"trace": [A::AddCluster]})), GoalStatus::Rejected { .. }));
    // no trace — cannot be verified
    assert_eq!(verdict(&spec, "dc_up", json!(true)), GoalStatus::Unverified);
    let strict = virtlab::verify_with(
        &spec,
        &json!({"dc_up": true, "vm_net": true, "migrate": true}),
        virtlab::Strictness::Strict,
    );
    assert!(!strict.solved);
}

#[test]
fn texts_exist_for_every_note() {
    en();
    let mut s = session();
    for a in FULL {
        let n = s.act(a).unwrap();
        assert!(!ovirt_dc::note_text(&n).is_empty());
    }
    for mistake in [Mistake::Memory, Mistake::Network, Mistake::Affinity] {
        assert!(!ovirt_sched::mistake_text(mistake).is_empty());
    }
}
