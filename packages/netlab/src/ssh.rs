//! SSH в симуляторе: ключ хоста, known_hosts, вход по ключу или паролю, прыжок через бастион (-J).
//! Сеть — настоящая (TCP-проба на порт 22), а проверки ключей и паролей — здесь.

use crate::ip::*;
use crate::sim::{delivered_to, fmt_ms, tcp1};
use crate::types::*;

/// Конфигурация SSH-сервера по умолчанию.
pub fn new_ssh() -> SshConfig {
    SshConfig { host_key: "SHA256:hostKeyA1".into(), rot: None, password_auth: true, users: Default::default() }
}

/// Ключ клиента (отпечаток).
pub fn key_of(d: &Device) -> Option<&str> {
    d.ssh_key.as_deref()
}

/// Новый отпечаток ключа устройства.
pub fn make_key(d: &Device) -> String {
    format!("SHA256:{}Key{}", d.id, (crate::util::utf16_len(&d.name) * 7) % 97)
}

/// Способ входа.
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

/// Итог подключения.
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

/// Одно подключение клиента к серверу: порт 22, ключ хоста, пользователь, ключ или пароль.
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
        return fail("ssh_exchange_identification: на порту нет SSH-сервера".into(), Some(run), None);
    };
    let Some(sshd) = srv.ssh.clone() else { return SshResult::default() };
    let mut lines = Vec::new();
    let k = ip_str(ip);
    let Some(client) = state.devices.get_mut(client_id) else { return SshResult::default() };
    let known = client.known_hosts.get(&k).cloned().filter(|s| !s.is_empty());
    match known {
        None => {
            client.known_hosts.insert(k.clone(), sshd.host_key.clone());
            lines.push(format!("Warning: Permanently added '{k}' (ключ хоста {}) to known_hosts.", sshd.host_key));
        }
        Some(old) if old != sshd.host_key => {
            let msg = [
                "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@".to_string(),
                "@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @".to_string(),
                "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@".to_string(),
                format!(
                    "Ключ хоста {k} изменился: был {old}, сейчас {}. Это либо плановая смена ключа, либо подмена сервера (MITM).",
                    sshd.host_key
                ),
                format!("Если смена законная: ssh-keygen -R {k}"),
            ]
            .join("\n");
            return fail(msg, Some(run), None);
        }
        Some(_) => {}
    }
    let client_key = client.ssh_key.clone();
    let Some(u) = sshd.users.get(user) else {
        return fail(format!("{user}@{k}: Permission denied ({}) — пользователя нет", perm(sshd.password_auth)), Some(run), Some(srv));
    };
    let key = if no_key { None } else { client_key };
    if let Some(key) = key {
        if u.keys.contains(&key) {
            lines.push(format!("Вход по ключу {key} выполнен{label}"));
            return SshResult { ok: true, error: None, run: Some(run), srv: Some(srv), auth: Some(Auth::Key), lines };
        }
    }
    if sshd.password_auth && pass.is_some() && pass == u.password.as_deref() {
        lines.push(format!("Вход по паролю выполнен{label}"));
        return SshResult { ok: true, error: None, run: Some(run), srv: Some(srv), auth: Some(Auth::Password), lines };
    }
    let why = if !sshd.password_auth {
        "парольный вход выключен, а ваш ключ на сервере не разрешён"
    } else if pass.is_none() {
        "нужен ключ или пароль"
    } else {
        "неверный пароль"
    };
    fail(format!("{user}@{k}: Permission denied ({}) — {why}", perm(sshd.password_auth)), Some(run), Some(srv))
}

/// `ssh [-J jump] user@host`: через бастион клиент сначала входит на него, затем TCP до цели идёт с бастиона.
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
    let a = ssh_hop(state, client_id, user, jump_ip, pass, no_key, " (бастион)");
    let Some(jd) = a.srv.clone().filter(|_| a.ok) else {
        let e = a.error.clone().unwrap_or_else(|| "undefined".into());
        return SshResult { ok: false, error: Some(format!("бастион: {e}")), ..a };
    };
    // дальше TCP идёт с бастиона: клиент проходит аутентификацию на цели своим ключом
    let probe = tcp1(state, &jd.id, ip, 22, 50000, false);
    if probe.status != ProbeStatus::Connected {
        let why = if probe.status == ProbeStatus::Refused { "порт закрыт" } else { "нет ответа" };
        return fail(format!("ssh: бастион не достаёт до {}:22 ({why})", ip_str(ip)), a.run, None);
    }
    let srv = delivered_to(state, &probe, Some(ip));
    let Some(srv) = srv.filter(|s| s.ssh.is_some()) else {
        return fail("на цели нет SSH-сервера".into(), a.run, None);
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
    lines.push(format!("прыжок {} → {}: {}", jd.name, srv.name, fmt_ms(probe.rtt_us)));
    if let (Some(u), Some(key)) = (u, key.as_ref()) {
        if u.keys.contains(key) {
            lines.push(format!("Вход по ключу {key} выполнен на {}", srv.name));
            return SshResult { ok: true, error: None, run: a.run, srv: Some(srv), auth: Some(Auth::Key), lines };
        }
    }
    if let Some(u) = u {
        if sshd.password_auth && pass.is_some() && pass == u.password.as_deref() {
            lines.push("Вход по паролю выполнен".into());
            return SshResult { ok: true, error: None, run: a.run, srv: Some(srv), auth: Some(Auth::Password), lines };
        }
    }
    fail(format!("{user}@{k}: Permission denied ({})", perm(sshd.password_auth)), a.run, Some(srv))
}
