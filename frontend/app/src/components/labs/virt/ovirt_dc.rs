//! oVirt data center simulator (chapter 17): the student performs the Administration Portal operations — cluster, hosts, network, storage domain, VM —
//! and watches the states of the objects. Solved when all goals are met. The goal data is `{trace}`: the recorded accepted actions, from which the
//! server replays the session.

use leptos::prelude::*;
use serde_json::Value;
use virtlab::ovirt_dc::{
    note_text, refusal_text, Action, DcGoal, DcStatus, Domain, HostStatus, Net, Session, State, HOSTS,
};

use super::common::{trace_data, GoalItem, GoalList, Goals};

/// Exercise progress: model session, record of accepted actions and the caption.
#[derive(Clone)]
pub struct DcRun {
    goals: Vec<DcGoal>,
    session: Session,
    trace: Vec<Action>,
    msg: String,
    refused: bool,
    seen: usize,
}

impl DcRun {
    pub fn new(goals: &[DcGoal]) -> Self {
        Self {
            goals: goals.to_vec(),
            session: Session::new(goals),
            trace: vec![],
            msg: i18n::tr("An empty environment: there is a data center, nothing else yet.").to_string(),
            refused: false,
            seen: 0,
        }
    }

    pub fn state(&self) -> &State {
        self.session.state()
    }

    pub fn msg(&self) -> &str {
        &self.msg
    }

    pub fn refused(&self) -> bool {
        self.refused
    }

    /// Start over: an empty environment, the record is cleared (goals reached earlier stay reached).
    pub fn reset(&mut self) {
        *self = Self::new(&self.goals.clone());
    }

    /// Perform an action. Returns the goals just reached, with data for the server (the record up to this moment).
    /// A refused action changes nothing and is not recorded.
    pub fn act(&mut self, a: Action) -> Vec<(String, Value)> {
        match self.session.act(a) {
            Ok(note) => {
                self.trace.push(a);
                self.msg = note_text(&note);
                self.refused = false;
            }
            Err(r) => {
                self.msg = refusal_text(r).to_string();
                self.refused = true;
                return vec![];
            }
        }
        let fresh: Vec<(String, Value)> =
            self.session.done()[self.seen..].iter().map(|id| (id.clone(), trace_data(&self.trace))).collect();
        self.seen = self.session.done().len();
        fresh
    }
}

/// Class of a status chip.
pub fn host_class(s: HostStatus) -> &'static str {
    match s {
        HostStatus::Up => "ok",
        HostStatus::NonOperational => "bad",
        HostStatus::Preparing | HostStatus::Maintenance => "warn",
    }
}

/// Name of a host status as oVirt shows it.
pub fn host_name(s: HostStatus) -> &'static str {
    match s {
        HostStatus::Up => "Up",
        HostStatus::NonOperational => "NonOperational",
        HostStatus::Preparing => "Preparing for Maintenance",
        HostStatus::Maintenance => "Maintenance",
    }
}

/// Class and name of the data center status.
pub fn dc_chip(s: DcStatus) -> (&'static str, &'static str) {
    match s {
        DcStatus::Up => ("ok", "Up"),
        DcStatus::Uninitialized => ("warn", "Uninitialized"),
        DcStatus::NonResponsive => ("bad", "Non Responsive"),
    }
}

/// Class and name of the storage domain state.
pub fn domain_chip(d: Domain) -> Option<(&'static str, &'static str)> {
    match d {
        Domain::Absent => None,
        Domain::Unattached => Some(("warn", "Unattached")),
        Domain::Maintenance => Some(("warn", "Maintenance")),
        Domain::Active => Some(("ok", "Active (master)")),
    }
}

#[component]
pub fn OvirtDcLab(targets: Vec<DcGoal>, goals: Goals) -> impl IntoView {
    let items: Vec<GoalItem> = targets.iter().map(|g| GoalItem::new(g.id.clone(), g.text.clone())).collect();
    let run = RwSignal::new(DcRun::new(&targets));
    let nic = RwSignal::new(Net::VmNet);
    let act = Callback::new(move |a: Action| {
        for (id, info) in run.try_update(|r| r.act(a)).unwrap_or_default() {
            goals.mark(&id, info);
        }
    });
    let reset = move |_| run.update(DcRun::reset);
    let hosts = |label: &'static str, make: fn(u8) -> Action| {
        (1..=HOSTS)
            .map(|n| view! { <button class="quiz-btn ghost" on:click=move |_| act.run(make(n))>{format!("{label} {n}")}</button> })
            .collect_view()
    };
    view! {
        <div class="vl">
            <div class="vl-grid">
                <div class="vl-card">
                    <span class="s-label">{i18n::tr("infrastructure")}</span>
                    <div class="vl-actions wrap">
                        <button class="quiz-btn" on:click=move |_| act.run(Action::AddCluster)>{i18n::tr("Create cluster")}</button>
                        {hosts(i18n::tr("Add host"), |host| Action::AddHost { host })}
                    </div>
                    <span class="s-label">{i18n::tr("networks")}</span>
                    <div class="vl-actions wrap">
                        <button class="quiz-btn" on:click=move |_| act.run(Action::CreateNetwork)>
                            {i18n::tr("Create network vm-net (required)")}
                        </button>
                        {hosts(i18n::tr("Assign vm-net to host"), |host| Action::AssignNetwork { host })}
                    </div>
                    <span class="s-label">{i18n::tr("storage")}</span>
                    <div class="vl-actions wrap">
                        <button class="quiz-btn" on:click=move |_| act.run(Action::CreateDomain)>{i18n::tr("Create NFS domain")}</button>
                        <button class="quiz-btn ghost" on:click=move |_| act.run(Action::AttachDomain)>{i18n::tr("Attach to data center")}</button>
                        <button class="quiz-btn ghost" on:click=move |_| act.run(Action::ActivateDomain)>{i18n::tr("Activate domain")}</button>
                    </div>
                    <span class="s-label">{i18n::tr("virtual machine")}</span>
                    <div class="vl-field">
                        <span>{i18n::tr("network of the NIC")}</span>
                        <div class="vl-seg">
                            <button class="vl-segbtn" class:on=move || nic.get() == Net::Mgmt on:click=move |_| nic.set(Net::Mgmt)>
                                "ovirtmgmt"
                            </button>
                            <button class="vl-segbtn" class:on=move || nic.get() == Net::VmNet on:click=move |_| nic.set(Net::VmNet)>
                                "vm-net"
                            </button>
                        </div>
                    </div>
                    <div class="vl-actions wrap">
                        <button class="quiz-btn" on:click=move |_| act.run(Action::CreateVm { net: nic.get_untracked() })>
                            {i18n::tr("Create VM")}
                        </button>
                        <button class="quiz-btn" on:click=move |_| act.run(Action::RunVm)>{i18n::tr("Run VM")}</button>
                    </div>
                    <span class="s-label">{i18n::tr("hosts in operation")}</span>
                    <div class="vl-actions wrap">
                        {hosts(i18n::tr("Maintenance, host"), |host| Action::Maintenance { host })}
                        {hosts(i18n::tr("Activate host"), |host| Action::ActivateHost { host })}
                    </div>
                    <GoalList goals=goals items=items />
                </div>

                <div class="vl-card">
                    <div class="pr-res-head">
                        <span class="s-label">{i18n::tr("environment")}</span>
                        <button class="quiz-btn ghost" on:click=reset>{i18n::tr("Start over")}</button>
                    </div>
                    {move || run.with(|r| env_view(r.state()))}
                    <p class="vl-final" class:vl-no=move || run.with(DcRun::refused)>{move || run.with(|r| r.msg().to_string())}</p>
                </div>
            </div>
        </div>
    }
}

fn chip(class: &'static str, text: &'static str) -> impl IntoView {
    view! { <span class=format!("vl-chip {class}")>{text}</span> }
}

/// The environment tree: data center, cluster, hosts, network, domain, VM.
fn env_view(st: &State) -> impl IntoView {
    let (dc_class, dc_name) = dc_chip(st.dc_status());
    let hosts = st
        .hosts
        .iter()
        .enumerate()
        .map(|(i, h)| {
            let body = match h {
                None => view! { <span class="vl-muted">{i18n::tr("not added")}</span> }.into_any(),
                Some(h) => view! {
                    {chip(host_class(h.status), host_name(h.status))}
                    <span class="vl-muted">{if h.vm_net { i18n::tr("vm-net on the NIC") } else { i18n::tr("no vm-net") }}</span>
                }
                .into_any(),
            };
            let running = st.vm.is_some_and(|v| v.host == Some(i as u8 + 1));
            view! {
                <li class="vl-env-host">
                    <span class="vl-env-k">{i18n::trf!("host {0}", i + 1)}</span>
                    {body}
                    {running.then(|| view! { <span class="vl-vm">"VM"</span> })}
                </li>
            }
        })
        .collect_view();
    let domain = match domain_chip(st.domain) {
        None => view! { <span class="vl-muted">{i18n::tr("not created")}</span> }.into_any(),
        Some((class, name)) => chip(class, name).into_any(),
    };
    let net = if st.net { i18n::tr("created, required in the cluster") } else { i18n::tr("not created") };
    let vm = match st.vm {
        None => view! { <span class="vl-muted">{i18n::tr("not created")}</span> }.into_any(),
        Some(v) => {
            let nic = if v.net == Net::VmNet { "vm-net" } else { "ovirtmgmt" };
            let state = match v.host {
                Some(h) => view! {
                    {chip("ok", "Up")}
                    <span class="vl-muted">{i18n::trf!("on host {0}", h)}</span>
                }
                .into_any(),
                None => chip("warn", "Down").into_any(),
            };
            view! { <span class="vl-muted">{i18n::trf!("NIC on {0}", nic)}</span> {state} }.into_any()
        }
    };
    view! {
        <ul class="vl-env">
            <li>
                <span class="vl-env-k">{i18n::tr("data center")}</span>
                {chip(dc_class, dc_name)}
            </li>
            <li>
                <span class="vl-env-k">{i18n::tr("cluster")}</span>
                <span class="vl-muted">{if st.cluster { i18n::tr("created") } else { i18n::tr("not created") }}</span>
            </li>
            <li class="vl-env-sub"><ul>{hosts}</ul></li>
            <li>
                <span class="vl-env-k">"vm-net"</span>
                <span class="vl-muted">{net}</span>
            </li>
            <li>
                <span class="vl-env-k">{i18n::tr("storage domain")}</span>
                {domain}
            </li>
            <li>
                <span class="vl-env-k">"VM"</span>
                {vm}
            </li>
        </ul>
    }
}

#[cfg(test)]
mod tests {
    use virtlab::ovirt_dc::default_goals;

    use super::*;

    fn run() -> DcRun {
        DcRun::new(&default_goals())
    }

    fn ids(v: Vec<(String, Value)>) -> Vec<String> {
        v.into_iter().map(|(id, _)| id).collect()
    }

    fn build(r: &mut DcRun) {
        for a in [
            Action::AddCluster,
            Action::AddHost { host: 1 },
            Action::AddHost { host: 2 },
            Action::CreateNetwork,
            Action::AssignNetwork { host: 1 },
            Action::AssignNetwork { host: 2 },
            Action::CreateDomain,
            Action::AttachDomain,
        ] {
            assert!(ids(r.act(a)).is_empty());
        }
    }

    #[test]
    fn walkthrough_reaches_goals_and_trace_replays_on_server() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mut r = run();
        build(&mut r);
        assert_eq!(ids(r.act(Action::ActivateDomain)), ["dc_up"]);
        assert_eq!(r.msg(), "Домен активен — он стал главным. Дата-центр в статусе Up.");
        r.act(Action::CreateVm { net: Net::VmNet });
        let got = r.act(Action::RunVm);
        assert_eq!(ids(got.clone()), ["vm_net"]);
        let (_, info) = got.into_iter().next().expect("goal");
        assert_eq!(info["trace"].as_array().map(Vec::len), Some(11));
        let spec = virtlab::Spec::OvirtDc { goals: default_goals() };
        let mut solution = serde_json::Map::new();
        solution.insert("vm_net".into(), info);
        let v = virtlab::verify(&spec, &Value::Object(solution));
        assert_eq!(v.goals.iter().find(|g| g.id == "vm_net").map(|g| g.status.clone()), Some(virtlab::GoalStatus::Verified));
        assert_eq!(ids(r.act(Action::Maintenance { host: 1 })), ["migrate"]);
    }

    #[test]
    fn refused_actions_are_not_traced() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mut r = run();
        assert!(r.act(Action::AddHost { host: 1 }).is_empty());
        assert!(r.refused());
        assert_eq!(r.msg(), "Кластера ещё нет.");
        assert!(r.trace.is_empty());
        r.act(Action::AddCluster);
        assert!(!r.refused());
        assert_eq!(r.trace.len(), 1);
    }

    #[test]
    fn reset_clears_state_and_record_but_keeps_nothing_stale() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mut r = run();
        build(&mut r);
        r.act(Action::ActivateDomain);
        r.reset();
        assert!(!r.state().cluster && r.trace.is_empty());
        build(&mut r);
        // goals are reported again after a reset with a record of the new run
        assert_eq!(ids(r.act(Action::ActivateDomain)), ["dc_up"]);
    }

    #[test]
    fn chips() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(host_class(HostStatus::NonOperational), "bad");
        assert_eq!(host_class(HostStatus::Preparing), "warn");
        assert_eq!(dc_chip(DcStatus::Up), ("ok", "Up"));
        assert_eq!(domain_chip(Domain::Absent), None);
        assert_eq!(host_name(HostStatus::Preparing), "Preparing for Maintenance");
    }
}
