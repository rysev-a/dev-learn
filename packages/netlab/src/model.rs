//! Операции над состоянием сети: кабели, поиск портов, копия без кэшей, проверка целостности.

use crate::ip::mac_str;
use crate::types::*;

/// Генератор MAC-адресов для построения сетей кодом: 28:28:00:00:00:01, 02, …
#[derive(Clone, Debug)]
pub struct MacGen(u32);

impl Default for MacGen {
    fn default() -> Self {
        MacGen(1)
    }
}

impl MacGen {
    pub fn new() -> MacGen {
        MacGen::default()
    }
    /// Интерфейс с новым MAC и без адреса.
    pub fn iface(&mut self, name: &str) -> Iface {
        let n = self.0;
        self.0 += 1;
        Iface::new(name, &mac_str(n))
    }
}

/// «pc1:eth0» → («pc1», «eth0»).
pub fn split_ref(s: &str) -> (&str, &str) {
    match s.split_once(':') {
        Some((d, p)) => (d, p),
        None => (s, ""),
    }
}

/// Сосед по кабелю: устройство, порт и индекс кабеля.
#[derive(Clone, Debug, PartialEq)]
pub struct Peer {
    pub dev: String,
    pub port: String,
    pub link: usize,
}

impl NetState {
    /// Устройство по id.
    pub fn device(&self, id: &str) -> Option<&Device> {
        self.devices.get(id)
    }

    /// Индекс кабеля, подключённого к порту.
    pub fn link_of(&self, dev: &str, port: &str) -> Option<usize> {
        let key = port_ref(dev, port);
        self.links.iter().position(|l| l.a == key || l.b == key)
    }

    /// По другую сторону кабеля от (dev, port).
    pub fn peer_of(&self, dev: &str, port: &str) -> Option<Peer> {
        let i = self.link_of(dev, port)?;
        let l = &self.links[i];
        let key = port_ref(dev, port);
        let other = if l.a == key { &l.b } else { &l.a };
        let (d, p) = split_ref(other);
        Some(Peer { dev: d.to_string(), port: p.to_string(), link: i })
    }

    /// Первый порт устройства без кабеля.
    pub fn free_port(&self, dev: &str) -> Option<&Iface> {
        let d = self.devices.get(dev)?;
        d.ifaces.iter().find(|i| self.link_of(dev, &i.name).is_none())
    }

    /// Проложить кабель между первыми свободными портами. Ошибка — текст для ученика.
    pub fn connect(&mut self, a: &str, b: &str, extra: Option<&LinkExtra>) -> Result<(), String> {
        if a == b {
            return Err("Нельзя соединить устройство с самим собой".into());
        }
        let name_of = |s: &NetState, id: &str| s.devices.get(id).map(|d| d.name.clone()).unwrap_or_else(|| id.to_string());
        if self.devices.get(a).is_none() {
            return Err(format!("нет устройства «{a}»"));
        }
        if self.devices.get(b).is_none() {
            return Err(format!("нет устройства «{b}»"));
        }
        let pa = self.free_port(a).map(|i| i.name.clone());
        let pb = self.free_port(b).map(|i| i.name.clone());
        let Some(pa) = pa else {
            return Err(format!("У «{}» нет свободных портов", name_of(self, a)));
        };
        let Some(pb) = pb else {
            return Err(format!("У «{}» нет свободных портов", name_of(self, b)));
        };
        let mut l = Link::new(&port_ref(a, &pa), &port_ref(b, &pb));
        if let Some(e) = extra {
            if let Some(km) = e.km {
                l.km = km;
            }
            if let Some(m) = e.mbps {
                l.mbps = m;
            }
            l.mtu = e.mtu;
            l.loss = e.loss;
        }
        self.links.push(l);
        Ok(())
    }

    /// Убрать кабель по индексу.
    pub fn disconnect(&mut self, idx: usize) {
        if idx < self.links.len() {
            self.links.remove(idx);
        }
    }

    /// Копия без служебных кэшей — для сохранения в кабинете и для проверки «с чистого листа».
    pub fn stripped(&self) -> NetState {
        NetState { devices: self.devices.clone(), links: self.links.clone(), pki: self.pki.clone(), rt: Runtime::default(), busy: false }
    }

    /// Сбросить кэши ARP, таблицы MAC и прочее.
    pub fn reset_runtime(&mut self) {
        self.rt = Runtime::default();
    }
}

/// Необязательные свойства кабеля при прокладке (шаг решения `cable`).
#[derive(Clone, Debug, Default, PartialEq, serde::Serialize, serde::Deserialize)]
pub struct LinkExtra {
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub km: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub mbps: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub mtu: Option<u32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub loss: Option<f64>,
}

/// Пределы размера присланного состояния: чтобы чужой JSON не превратился в бесконечную проверку.
pub const MAX_DEVICES: usize = 64;
pub const MAX_LINKS: usize = 256;
pub const MAX_ITEMS: usize = 1000;

impl NetState {
    /// Проверка целостности: кабели ведут к существующим портам, порт занят не более одним кабелем,
    /// размеры списков в пределах.
    pub fn validate(&self) -> Result<(), String> {
        if self.devices.len() > MAX_DEVICES {
            return Err(format!("слишком много устройств ({})", self.devices.len()));
        }
        if self.links.len() > MAX_LINKS {
            return Err(format!("слишком много кабелей ({})", self.links.len()));
        }
        for d in self.devices.iter() {
            let big = d.routes.len().max(d.nat.len()).max(d.fw.rules.len()).max(d.services.len()).max(d.ifaces.len());
            if big > MAX_ITEMS {
                return Err(format!("«{}»: слишком длинные списки настроек", d.name));
            }
            if let Some(h) = &d.dns {
                if h.records.len() > MAX_ITEMS || h.delegations.len() > MAX_ITEMS {
                    return Err(format!("«{}»: слишком много записей DNS", d.name));
                }
            }
            if let Some(h) = &d.http {
                if h.routes.len() > MAX_ITEMS {
                    return Err(format!("«{}»: слишком много маршрутов веб-сервера", d.name));
                }
            }
        }
        let mut used = std::collections::HashSet::new();
        for l in &self.links {
            for end in [&l.a, &l.b] {
                let (d, p) = split_ref(end);
                let ok = self.devices.get(d).map(|x| x.iface(p).is_some()).unwrap_or(false);
                if !ok {
                    return Err(format!("кабель ведёт к несуществующему порту «{end}»"));
                }
                if !used.insert(end.clone()) {
                    return Err(format!("к порту «{end}» подключено два кабеля"));
                }
            }
            if !(l.km.is_finite() && l.mbps.is_finite()) {
                return Err("у кабеля нечисловые параметры".into());
            }
        }
        Ok(())
    }
}

/// Разобрать состояние из JSON (каноническая запись или прежняя запись клиента) и проверить его.
pub fn state_from_json(s: &str) -> Result<NetState, String> {
    let st: NetState = serde_json::from_str(s).map_err(|e| format!("не удалось разобрать состояние сети: {e}"))?;
    st.validate()?;
    Ok(st)
}
