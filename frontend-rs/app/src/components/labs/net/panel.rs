//! Карточка устройства: вкладки «Настройки» (формы по виду устройства и флагам `tools` упражнения) и «Терминал».

use leptos::prelude::*;
use netlab::types::DeviceKind;
use netlab::Tools;

use super::forms::{Firewall, Forwarding, Gateway, Interfaces, MacTable, Nat, Routes, Services, SwitchPorts};
use super::lab::Lab;
use super::logic;
use super::services::{DnsServer, LbBox, ProxyBox, Resolver, RproxyBox, SshBox, TcpTune, TlsServer, TrustStore, VpnBox, WebServer};
use super::terminal::Terminal;
use super::forms::Ctx;

#[derive(Clone, Copy, PartialEq)]
enum Tab {
    Config,
    Term,
}

/// Карточка выбранного устройства; при смене выбора пересоздаётся (поля форм начинают с чистого листа).
#[component]
pub fn DevicePanel(lab: Lab) -> impl IntoView {
    move || {
        let id = lab.sel.get();
        view! { <PanelFor lab=lab id=id /> }
    }
}

#[component]
fn PanelFor(lab: Lab, id: String) -> impl IntoView {
    let Some(dev) = lab.device(&id) else { return ().into_any() };
    let tab = RwSignal::new(Tab::Config);
    let ctx = Ctx::new(lab, &id);
    let tools = lab.tools();
    let (name, kind, locked) = (dev.name.clone(), dev.kind, dev.locked);
    let tab_btn = move |t: Tab, label: &'static str| view! { <button type="button" class:on=move || tab.get() == t on:click=move |_| tab.set(t)>{label}</button> };
    view! {
        <div class="nl-panel">
            <div class="nl-panel-head">
                <h4>{name}</h4>
                <span class="nl-kind">{logic::kind_title(kind)}</span>
                {locked.then(|| view! { <span class="nl-lock">"только чтение"</span> })}
            </div>
            <div class="nl-tabs">{tab_btn(Tab::Config, "Настройки")}{tab_btn(Tab::Term, "Терминал")}</div>
            {move || match tab.get() {
                Tab::Config => view! { <Config ctx=ctx kind=kind tools=tools.clone() /> }.into_any(),
                Tab::Term => view! { <Terminal lab=lab id=ctx.id() /> }.into_any(),
            }}
        </div>
    }
    .into_any()
}

/// Какие формы показывать устройству: вид устройства и инструменты упражнения (чистая функция).
#[derive(Clone, Debug, Default, PartialEq)]
pub struct Sections {
    pub interfaces: bool,
    pub gateway: bool,
    pub tcp: bool,
    pub resolver: bool,
    pub trust: bool,
    pub ssh: bool,
    pub vpn: bool,
    pub forwarding: bool,
    pub routes: bool,
    pub nat: bool,
    pub fw: bool,
    pub services: bool,
    pub switch: bool,
}

impl Sections {
    pub fn of(kind: DeviceKind, tools: &Tools, has_ssh_server: bool) -> Sections {
        let host = matches!(kind, DeviceKind::Host | DeviceKind::Server);
        let router = matches!(kind, DeviceKind::Router | DeviceKind::Internet);
        let switch = kind == DeviceKind::Switch;
        // таблица маршрутов у компьютеров открывалась флагом `routes`, но ни одно упражнение его не включает —
        // в `Tools` флага нет, а маршрутизаторам таблица показывается всегда
        Sections {
            interfaces: !switch,
            gateway: host,
            tcp: host && tools.tcp,
            resolver: host && tools.dns,
            trust: host && tools.tls,
            ssh: tools.ssh && !switch && (has_ssh_server || host),
            vpn: tools.vpn && (router || host),
            forwarding: router,
            routes: router,
            nat: router && tools.nat,
            fw: router && tools.fw,
            services: kind == DeviceKind::Server,
            switch,
        }
    }
}

#[component]
fn Config(ctx: Ctx, kind: DeviceKind, tools: Tools) -> impl IntoView {
    let has_ssh_server = ctx.read(|d| d.ssh.is_some()).unwrap_or(false);
    let s = Sections::of(kind, &tools, has_ssh_server);
    // службы показываются, пока они есть на устройстве (команда терминала может их создать)
    let has = move |f: fn(&netlab::types::Device) -> bool| move || ctx.read(f).unwrap_or(false);
    let t = tools;
    view! {
        <div class="nl-cfg">
            {s.interfaces.then(|| view! { <Interfaces ctx=ctx queue=t.queue /> })}
            {s.gateway.then(|| view! { <Gateway ctx=ctx /> })}
            {s.tcp.then(|| view! { <TcpTune ctx=ctx /> })}
            {s.resolver.then(|| view! { <Resolver ctx=ctx /> })}
            <Show when=move || t.tls && has(|d| d.tls.is_some())()><TlsServer ctx=ctx /></Show>
            {s.trust.then(|| view! { <TrustStore ctx=ctx /> })}
            {s.ssh.then(|| view! { <SshBox ctx=ctx /> })}
            {s.vpn.then(|| view! { <VpnBox ctx=ctx /> })}
            <Show when=move || t.lb && has(|d| d.lb.is_some())()><LbBox ctx=ctx /></Show>
            <Show when=move || t.rproxy && has(|d| d.rproxy.is_some())()><RproxyBox ctx=ctx /></Show>
            <Show when=move || t.proxy && has(|d| d.proxy.is_some())()><ProxyBox ctx=ctx /></Show>
            <Show when=move || t.http && has(|d| d.http.is_some())()><WebServer ctx=ctx /></Show>
            <Show when=move || t.dns && has(|d| d.dns.is_some())()><DnsServer ctx=ctx /></Show>
            {s.forwarding.then(|| view! { <Forwarding ctx=ctx /> })}
            {s.routes.then(|| view! { <Routes ctx=ctx /> })}
            {s.nat.then(|| view! { <Nat ctx=ctx /> })}
            {s.fw.then(|| view! { <Firewall ctx=ctx /> })}
            {s.services.then(|| view! { <Services ctx=ctx /> })}
            {s.switch.then(|| view! { <SwitchPorts ctx=ctx /> <MacTable ctx=ctx /> })}
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn tools(f: impl FnOnce(&mut Tools)) -> Tools {
        let mut t = Tools::default();
        f(&mut t);
        t
    }

    #[test]
    fn host_gets_gateway_but_no_router_forms() {
        let s = Sections::of(DeviceKind::Host, &tools(|t| t.nat = true), false);
        assert!(s.interfaces && s.gateway && !s.routes && !s.nat && !s.forwarding && !s.services);
    }

    #[test]
    fn router_forms_follow_tools() {
        let s = Sections::of(DeviceKind::Router, &tools(|t| t.nat = true), false);
        assert!(s.routes && s.forwarding && s.nat && !s.fw && !s.gateway);
        let s = Sections::of(DeviceKind::Internet, &tools(|t| t.fw = true), false);
        assert!(s.fw && s.routes);
    }

    #[test]
    fn switch_has_ports_and_no_interfaces() {
        let s = Sections::of(DeviceKind::Switch, &tools(|t| t.ssh = true), true);
        assert!(s.switch && !s.interfaces && !s.ssh && !s.gateway);
    }

    #[test]
    fn server_lists_listening_ports_and_ssh_when_open() {
        let s = Sections::of(DeviceKind::Server, &tools(|t| t.ssh = true), false);
        assert!(s.services && s.ssh);
        assert!(!Sections::of(DeviceKind::Router, &tools(|t| t.ssh = true), false).ssh, "роутер без SSH-сервера и не компьютер");
        assert!(Sections::of(DeviceKind::Router, &tools(|t| t.ssh = true), true).ssh);
    }

    #[test]
    fn tcp_dns_tls_forms_are_for_hosts_only() {
        let all = tools(|t| {
            t.tcp = true;
            t.dns = true;
            t.tls = true;
        });
        let h = Sections::of(DeviceKind::Host, &all, false);
        assert!(h.tcp && h.resolver && h.trust);
        let r = Sections::of(DeviceKind::Router, &all, false);
        assert!(!r.tcp && !r.resolver && !r.trust);
    }
}
