//! SSH in the simulator: host key, known_hosts, login by key or password, jump through a bastion (-J).
//! The network is real (TCP probe to port 22), while key and password checks are here.

use crate::ip::*;
use crate::sim::{delivered_to, fmt_ms, tcp1};
use crate::types::*;

/// Default SSH server configuration.
pub fn new_ssh() -> SshConfig {
    SshConfig { host_key: "SHA256:hostKeyA1".into(), rot: None, password_auth: true, users: Default::default() }
}

/// Client key (fingerprint).
pub fn key_of(d: &Device) -> Option<&str> {
    d.ssh_key.as_deref()
}

/// New key fingerprint for a device.
pub fn make_key(d: &Device) -> String {
    format!("SHA256:{}Key{}", d.id, (crate::util::utf16_len(&d.name) * 7) % 97)
}

/// Login method.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Auth {
    Key,
    Password,
}

impl Auth {
    pub fn as_str(self) -> &'static str {
        match self {
            Auth::Key => "key",
            Auth::Password => "password",
        }
    }
}

/// Connection outcome.
#[derive(Clone, Debug, Default)]
pub struct SshResult {
    pub ok: bool,
    pub error: Option<String>,
    pub run: Option<ProbeRun>,
    pub srv: Option<Device>,
    pub auth: Option<Auth>,
    pub lines: Vec<String>,
}

fn fail(error: String, run: Option<ProbeRun>, srv: Option<Device>) -> SshResult {
    SshResult { ok: false, error: Some(error), run, srv, auth: None, lines: vec![] }
}

fn perm(pw: bool) -> String {
    format!("publickey{}", if pw { ",password" } else { "" })
}

/// One client connection to a server: port 22, host key, user, key or password.
pub fn ssh_hop(state: &mut NetState, client_id: &str, user: &str, ip: u32, pass: Option<&str>, no_key: bool, label: &str) -> SshResult {
    let run = tcp1(state, client_id, ip, 22, 50000, false);
    if run.status == ProbeStatus::Refused {
        return fail(format!("ssh: connect to host {} port 22: Connection refused", ip_str(ip)), Some(run), None);
    }
    if run.status != ProbeStatus::Connected {
        return fail(format!("ssh: connect to host {} port 22: Connection timed out", ip_str(ip)), Some(run), None);
    }
    let srv = delivered_to(state, &run, Some(ip));
    let Some(srv) = srv.filter(|s| s.ssh.is_some()) else {
        return fail(i18n::tr("ssh_exchange_identification: no SSH server on the port").into(), Some(run), None);
    };
    let Some(sshd) = srv.ssh.clone() else { return SshResult::default() };
    let mut lines = Vec::new();
    let k = ip_str(ip);
    let Some(client) = state.devices.get_mut(client_id) else { return SshResult::default() };
    let known = client.known_hosts.get(&k).cloned().filter(|s| !s.is_empty());
    match known {
        None => {
            client.known_hosts.insert(k.clone(), sshd.host_key.clone());
            lines.push(i18n::trf!("Warning: Permanently added '{0}' (host key {1}) to known_hosts.", k, sshd.host_key));
        }
        Some(old) if old != sshd.host_key => {
            let msg = [
                "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@".to_string(),
                "@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @".to_string(),
                "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@".to_string(),
                i18n::trf!("Host key of {0} changed: was {1}, now {2}. Either a planned key rotation or a server impersonation (MITM).", k, old, sshd.host_key),
                i18n::trf!("If the change is legitimate: ssh-keygen -R {0}", k),
            ]
            .join("\n");
            return fail(msg, Some(run), None);
        }
        Some(_) => {}
    }
    let client_key = client.ssh_key.clone();
    let Some(u) = sshd.users.get(user) else {
        return fail(i18n::trf!("{0}@{1}: Permission denied ({2}) — no such user", user, k, perm(sshd.password_auth)), Some(run), Some(srv));
    };
    let key = if no_key { None } else { client_key };
    if let Some(key) = key {
        if u.keys.contains(&key) {
            lines.push(i18n::trf!("Key login {0} succeeded{1}", key, label));
            return SshResult { ok: true, error: None, run: Some(run), srv: Some(srv), auth: Some(Auth::Key), lines };
        }
    }
    if sshd.password_auth && pass.is_some() && pass == u.password.as_deref() {
        lines.push(i18n::trf!("Password login succeeded{0}", label));
        return SshResult { ok: true, error: None, run: Some(run), srv: Some(srv), auth: Some(Auth::Password), lines };
    }
    let why = if !sshd.password_auth {
        i18n::tr("password login is disabled, and your key is not authorized on the server")
    } else if pass.is_none() {
        i18n::tr("a key or a password is required")
    } else {
        i18n::tr("wrong password")
    };
    fail(format!("{user}@{k}: Permission denied ({}) — {why}", perm(sshd.password_auth)), Some(run), Some(srv))
}

/// `ssh [-J jump] user@host`: via a bastion the client first logs in there, then TCP to the target goes from the bastion.
pub fn ssh_connect(
    state: &mut NetState,
    client_id: &str,
    user: &str,
    ip: u32,
    jump: Option<u32>,
    pass: Option<&str>,
    no_key: bool,
) -> SshResult {
    let Some(jump_ip) = jump else {
        return ssh_hop(state, client_id, user, ip, pass, no_key, "");
    };
    let a = ssh_hop(state, client_id, user, jump_ip, pass, no_key, i18n::tr(" (bastion)"));
    let Some(jd) = a.srv.clone().filter(|_| a.ok) else {
        let e = a.error.clone().unwrap_or_else(|| "undefined".into());
        return SshResult { ok: false, error: Some(i18n::trf!("bastion: {0}", e)), ..a };
    };
    // from here TCP goes from the bastion: the client authenticates on the target with its own key
    let probe = tcp1(state, &jd.id, ip, 22, 50000, false);
    if probe.status != ProbeStatus::Connected {
        let why = if probe.status == ProbeStatus::Refused { i18n::tr("port closed") } else { i18n::tr("no reply") };
        return fail(i18n::trf!("ssh: the bastion cannot reach {0}:22 ({1})", ip_str(ip), why), a.run, None);
    }
    let srv = delivered_to(state, &probe, Some(ip));
    let Some(srv) = srv.filter(|s| s.ssh.is_some()) else {
        return fail(i18n::tr("the target has no SSH server").into(), a.run, None);
    };
    let Some(sshd) = srv.ssh.clone() else { return SshResult::default() };
    let k = ip_str(ip);
    let Some(client) = state.devices.get_mut(client_id) else { return SshResult::default() };
    let known = client.known_hosts.get(&k).cloned().filter(|s| !s.is_empty());
    if let Some(old) = &known {
        if *old != sshd.host_key {
            return fail(format!("WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! ({k}) — ssh-keygen -R {k}"), a.run, None);
        }
    }
    if known.is_none() {
        client.known_hosts.insert(k.clone(), sshd.host_key.clone());
    }
    let u = sshd.users.get(user);
    let key = if no_key { None } else { client.ssh_key.clone() };
    let mut lines = a.lines.clone();
    lines.push(i18n::trf!("hop {0} → {1}: {2}", jd.name, srv.name, fmt_ms(probe.rtt_us)));
    if let (Some(u), Some(key)) = (u, key.as_ref()) {
        if u.keys.contains(key) {
            lines.push(i18n::trf!("Key login {0} succeeded on {1}", key, srv.name));
            return SshResult { ok: true, error: None, run: a.run, srv: Some(srv), auth: Some(Auth::Key), lines };
        }
    }
    if let Some(u) = u {
        if sshd.password_auth && pass.is_some() && pass == u.password.as_deref() {
            lines.push(i18n::tr("Password login succeeded").into());
            return SshResult { ok: true, error: None, run: a.run, srv: Some(srv), auth: Some(Auth::Password), lines };
        }
    }
    fail(format!("{user}@{k}: Permission denied ({})", perm(sshd.password_auth)), a.run, Some(srv))
}
