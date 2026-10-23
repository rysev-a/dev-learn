//! Атаки на фоне: подмена ARP (MITM), SYN-флуд, сканирование портов. Нарушитель — обычное устройство с полем
//! `attack`; перед каждой пробой атаки «проверяются на достижимость» настоящими пакетами, поэтому файрвол
//! и коммутация влияют на результат так же, как в жизни.

use crate::ip::*;
use crate::sim::{lookup, tcp1};
use crate::types::*;

fn first_ip(d: &Device) -> Option<&Iface> {
    d.ifaces.iter().find(|i| i.ip.is_some())
}

/// Подготовить побочные эффекты атак перед пробой (подмена ARP-кэша жертвы, перегруженные очереди SYN).
pub fn attacks_before(state: &mut NetState) {
    if state.busy {
        return;
    }
    state.busy = true;
    state.rt.synflood.clear();
    let ids: Vec<String> = state.devices.iter().map(|d| d.id.clone()).collect();
    for id in ids {
        let Some(dev) = state.devices.get(&id).cloned() else { continue };
        let Some(a) = dev.attack.clone() else { continue };
        match a.typ {
            AttackKind::Arpspoof => {
                let (Some(victim_id), Some(gw)) =
                    (a.victim.as_deref().filter(|s| !s.is_empty()), a.gateway_ip.as_deref().filter(|s| !s.is_empty()))
                else {
                    continue;
                };
                let Some(victim) = state.devices.get(victim_id) else { continue };
                let Some(gw_ip) = parse_ip(gw) else { continue };
                if victim.arp_static.get(gw).map(|m| !m.is_empty()).unwrap_or(false) {
                    continue;
                }
                let (Some(own), Some(vif)) = (first_ip(&dev), first_ip(victim)) else { continue };
                if !in_net(
                    parse_ip_opt(vif.ip.as_deref()),
                    Some(network_of(parse_ip_opt(own.ip.as_deref()), own.prefix as u32)),
                    own.prefix as u32,
                ) {
                    continue;
                }
                let (mac, vid) = (own.mac.clone(), victim.id.clone());
                state.rt.arp.entry(vid).or_default().insert(gw_ip, ArpEntry { mac, at: 0.0, sim: -1 });
            }
            AttackKind::Synflood => {
                let (Some(target), Some(port)) = (a.target.as_deref().filter(|s| !s.is_empty()), a.port) else { continue };
                let Some(tgt) = state.devices.get(target) else { continue };
                let Some(tip) = parse_ip_opt(first_ip(tgt).and_then(|i| i.ip.as_deref())) else { continue };
                if lookup(&dev, Some(tip), false).is_none() {
                    continue;
                }
                let r = tcp1(state, &dev.id, tip, port, 60000, false);
                if r.status == ProbeStatus::Connected || r.status == ProbeStatus::Refused {
                    state.rt.synflood.insert(format!("{target}:{port}"));
                }
            }
            AttackKind::Scan => {}
        }
    }
    state.busy = false;
}

/// Фоновый трафик для перехвата: сканер обходит порты цели.
pub fn background_traffic(state: &mut NetState) {
    if state.busy {
        return;
    }
    state.busy = true;
    let ids: Vec<String> = state.devices.iter().map(|d| d.id.clone()).collect();
    for id in ids {
        let Some(dev) = state.devices.get(&id).cloned() else { continue };
        let Some(a) = dev.attack.clone() else { continue };
        if a.typ != AttackKind::Scan {
            continue;
        }
        let Some(target) = a.target.as_deref().filter(|s| !s.is_empty()) else { continue };
        let Some(tgt) = state.devices.get(target) else { continue };
        let Some(tip) = parse_ip_opt(first_ip(tgt).and_then(|i| i.ip.as_deref())) else { continue };
        if lookup(&dev, Some(tip), false).is_none() {
            continue;
        }
        for p in &a.ports {
            tcp1(state, &dev.id, tip, *p, 61000 + *p, false);
        }
    }
    state.busy = false;
}
